"""Отчёт покрытия видеоузлов шаблонами (без LLM и без рендера).

    python -m pipeline.video.coverage --ch <id> [--layer <layer.json>] [--routing <routing.json>] [--domain geology]

Видеоузел — узел, у маршрута которого «шортс» или «длинное видео» в format или secondary_format.
Для каждого: шаблон и формат из маршрута, модель состояния и ограничения из domain/<домен>/templates/<T>.json,
реализован ли шаблон (есть ли рендер), поддерживается ли формат, есть ли готовая пара script.json/scene_spec.json
в каталоге video.spec и проходит ли она те же проверки, что video.build перед повторным использованием.
Статусы (по приоритету): «ошибка маршрута», «нужен новый шаблон», «формат не поддерживается»,
«спецификация ещё не создана», «спецификация не прошла проверку», «поддерживается».
Физическая применимость модели шаблона к узлу маршрутом не подтверждается — у каждого узла «не проверено».
Выход — out/<ch>/videos/coverage.json (out/<ch>/coverage.json — выход ядра, не трогается) и сводка в консоли.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from contracts.models import Layer, Routing
from pipeline.video import spec as vspec
from pipeline.video.inputs import ID_RE, VideoInputError
from pipeline.video.templates import TEMPLATE_FORMATS, TEMPLATE_INFO, VIDEO_FORMATS, format_problem, load_template_config

ROOT = Path(__file__).resolve().parents[2]
STATUSES = ["поддерживается", "нужен новый шаблон", "формат не поддерживается", "спецификация ещё не создана",
            "спецификация не прошла проверку", "ошибка маршрута"]
APPLICABILITY = {"status": "не проверено",
                 "reason": "шаблон назначен маршрутизацией; соответствие физики узла модели шаблона не подтверждено — "
                           "его проверяют спецификация (источники параметров из узла) и ментор"}


def _video_format(route) -> tuple[str | None, str | None, str | None]:
    if route.format in VIDEO_FORMATS:
        return VIDEO_FORMATS[route.format], route.format, "format"
    if route.secondary_format in VIDEO_FORMATS:
        return VIDEO_FORMATS[route.secondary_format], route.secondary_format, "secondary_format"
    return None, None, None


def _pair_state(out_root: Path, ch: str, node, route, fmt: str, domain: str) -> tuple[dict, list[str]]:
    from pipeline.video.build import _check_ready_pair            # та же проверка, что перед повторным использованием
    d = vspec.output_dir(out_root, ch, node.id, fmt)
    sp, cp = d / "script.json", d / "scene_spec.json"
    pair = {"script": sp.is_file(), "scene_spec": cp.is_file()}
    if not pair["script"] and not pair["scene_spec"]:
        return {**pair, "checks": "нет пары"}, [f"нет {d.relative_to(out_root).as_posix()}/script.json и scene_spec.json "
                                               f"— запустите video.spec или video.build без явной пары"]
    if pair["script"] != pair["scene_spec"]:
        return {**pair, "checks": "не пройдены"}, ["пара неполная: в каталоге только один из файлов "
                                                   "script.json/scene_spec.json"]
    try:
        _check_ready_pair(sp, cp, node, route, fmt, None, domain)
    except VideoInputError as e:
        return {**pair, "checks": "не пройдены"}, [str(e)]
    except Exception as e:   # проверка этого узла упала — не скрываем и продолжаем отчёт по остальным узлам
        return {**pair, "checks": "не пройдены"}, [f"проверка упала: {type(e).__name__}: {e}"]
    return {**pair, "checks": "пройдены"}, []


def build_report(ch: str, layer: Layer, routing: Routing, out_root: Path, domain: str) -> dict:
    if layer.chapter != ch:
        raise VideoInputError(f"layer.json относится к главе «{layer.chapter}», а запрошена --ch {ch}")
    if routing.chapter != ch:
        raise VideoInputError(f"routing.json относится к главе «{routing.chapter}», а запрошена --ch {ch}")
    templates_dir = ROOT / "domain" / domain / "templates"
    nodes = {n.id: n for n in layer.nodes}
    count = Counter(r.node_id for r in routing.routes)
    rows, seen = [], set()
    for route in routing.routes:
        fmt, fmt_ru, fmt_src = _video_format(route)
        if fmt is None or route.node_id in seen:
            continue
        seen.add(route.node_id)
        node = nodes.get(route.node_id)
        row = {"node_id": route.node_id, "title": node.title if node else None,
               "title_novice": node.title_novice if node else None, "format_ru": fmt_ru, "format_source": fmt_src,
               "format": fmt, "template": route.template, "route_why": route.why,
               "template_implemented": route.template in TEMPLATE_FORMATS,
               "format_supported": route.template in TEMPLATE_FORMATS and not format_problem(route.template, fmt),
               "model": None, "state_variable": None, "limitations": None, "assumptions": [],
               "pair": None, "physical_applicability": APPLICABILITY, "reasons": []}
        reasons = row["reasons"]
        if count[route.node_id] > 1:
            reasons.append(f"у узла {count[route.node_id]} маршрута в routing.json — нужен ровно один")
        if node is None:
            reasons.append(f"узла {route.node_id} нет в layer.json главы {ch}")
        if reasons:
            row["status"] = "ошибка маршрута"
            rows.append(row)
            continue
        cfg = load_template_config(templates_dir, route.template) if route.template in TEMPLATE_INFO else None
        if cfg is not None:
            row.update(model=cfg.get("model"), state_variable=cfg.get("state_variable"),
                       limitations=cfg.get("limitations"), assumptions=cfg.get("assumptions", []))
        if not route.template:
            reasons.append("в маршруте не указан шаблон сцены")
        elif route.template not in TEMPLATE_INFO:
            reasons.append(f"шаблон {route.template} неизвестен видео-модулю; есть {sorted(TEMPLATE_INFO)}")
        elif cfg is None:
            reasons.append(f"в доменном пакете нет описания шаблона: {templates_dir / f'{route.template}.json'}")
        elif route.template not in TEMPLATE_FORMATS:
            reasons.append(f"для шаблона {route.template} нет рендера")
        if reasons:
            row["status"] = "нужен новый шаблон"
        elif format_problem(route.template, fmt):
            row["status"] = "формат не поддерживается"
            reasons.append(format_problem(route.template, fmt))
        else:
            row["pair"], pair_reasons = _pair_state(out_root, ch, node, route, fmt, domain)
            reasons += pair_reasons
            row["status"] = {"нет пары": "спецификация ещё не создана", "не пройдены": "спецификация не прошла проверку",
                             "пройдены": "поддерживается"}[row["pair"]["checks"]]
        rows.append(row)
    summary = {s: sum(r["status"] == s for r in rows) for s in STATUSES}
    return {"chapter": ch, "domain": domain, "video_nodes": len(rows), "summary": summary, "nodes": rows,
            "note": "отчёт не генерирует сценарии и не рендерит; физическая применимость шаблонов не подтверждается"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.video.coverage", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ch", required=True, help="id главы")
    ap.add_argument("--layer", type=Path, help="layer.json (по умолчанию out/<ch>/layer.json)")
    ap.add_argument("--routing", type=Path, help="routing.json (по умолчанию out/<ch>/routing.json)")
    ap.add_argument("--domain", default="geology", help="доменный пакет: описания шаблонов в domain/<домен>/templates/")
    ap.add_argument("--out-root", type=Path, default=ROOT / "out")
    a = ap.parse_args(argv)
    try:
        if not ID_RE.match(a.ch) or not ID_RE.match(a.domain):
            raise VideoInputError("--ch и --domain — только [a-z0-9_.-]")
        layer_path, routing_path = vspec.default_paths(a.ch, a.out_root, a.layer, a.routing)
        try:
            layer = vspec._load(layer_path, Layer, "учебный слой; путь можно задать --layer")
            routing = vspec._load(routing_path, Routing, "маршрутизация; путь можно задать --routing")
        except vspec.SpecError as e:
            raise VideoInputError(str(e)) from e
        report = build_report(a.ch, layer, routing, a.out_root, a.domain)
    except VideoInputError as e:
        print(f"ОШИБКА video.coverage: {e}", file=sys.stderr)
        return 2
    report["inputs"] = {"layer": str(layer_path), "routing": str(routing_path)}
    out = a.out_root / a.ch / "videos" / "coverage.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"видеоузлов: {report['video_nodes']} — " + ", ".join(f"{k}: {v}" for k, v in report["summary"].items() if v))
    for r in report["nodes"]:
        why = f" — {r['reasons'][0].splitlines()[0]}" if r["reasons"] else ""
        print(f"  {r['node_id']} [{r['format_ru']}, {r['template'] or 'без шаблона'}]: {r['status']}{why}")
    print(f"отчёт: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
