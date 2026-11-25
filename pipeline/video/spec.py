"""Сценарий и спецификация сцены из учебного слоя (без озвучки и рендера).

    python -m pipeline.video.spec --ch <id> --node <node_id> [--layer PATH] [--routing PATH]

Вход: out/<ch>/layer.json и out/<ch>/routing.json (или явные пути).
Выход: out/<ch>/videos/<video_id>/script.json и scene_spec.json, video_id = <node_id>.<short|long>.
LLM — только pipeline.llm.complete_json; промпты — prompts/video/. Ответ модели проверяется
кодом (spec_check); при замечаниях одна повторная попытка с их текстом, затем ошибка.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from pydantic import BaseModel, ValidationError

from contracts.models import Layer, Node, Phrase, Route, Routing, SceneSpec, Script, Shot
from pipeline.video.inputs import ID_RE
from pipeline.video.spec_check import (ESTIMATE_WPM, DURATION_S, check_scene, check_script, count_words,
                                       estimate_duration, param_source_problems, source_language, sources_table)
from pipeline.video.templates import (ASPECT, TEMPLATE_INFO, VIDEO_FORMATS, format_problem, load_template_config,
                                      template_contract)

ROOT = Path(__file__).resolve().parents[2]
ATTEMPTS = 2
TIER_SCRIPT, TIER_SCENE = "strong", "default"
LANG_RU = {"ru": "русский (ru)", "en": "английский (en)"}
NO_FEEDBACK = "Нет — это первая попытка."


class SpecError(ValueError):
    pass


# Схемы ответа модели: поля Script/SceneSpec, которые пишет модель. id, узел, формат и шаблон ставит код.
class ScriptDraft(BaseModel):
    phrases: list[Phrase]
    prediction_question: str
    transfer_question: str
    data_it_bridge: str


class ParamSource(BaseModel):
    claim_ids: list[str]
    numbers: list[str]
    derivation: str


class SceneDraft(BaseModel):
    params: dict
    objects: list[str]
    invariants: list[str]
    assumptions: list[str]
    exaggerations: list[str]
    shots: list[Shot]
    true_scale_shot_id: str | None = None
    convention: str = "русская школа ГИС"
    data_sources: list[str] = []
    references: list[str] = []
    historical_objects: list[str] = []
    param_sources: dict[str, ParamSource] = {}   # источники физических параметров шаблона
    missing_params: list[str] = []               # физические параметры, которых в узле нет


def _load(path: Path, model: type[BaseModel], hint: str) -> BaseModel:
    if not path.is_file():
        raise SpecError(f"нет файла {path} ({hint})")
    try:
        return model.model_validate_json(path.read_text(encoding="utf-8"))
    except ValidationError as e:
        raise SpecError(f"{path} не проходит контракт {model.__name__}:\n{e}") from e


def select(layer: Layer, routing: Routing, ch: str, node_id: str) -> tuple[Node, Route, str]:
    """Узел, его маршрут и формат ролика (short|long); любое несоответствие — ошибка."""
    if layer.chapter != ch:
        raise SpecError(f"layer.json относится к главе «{layer.chapter}», а запрошена --ch {ch}")
    if routing.chapter != ch:
        raise SpecError(f"routing.json относится к главе «{routing.chapter}», а запрошена --ch {ch}")
    nodes = {n.id: n for n in layer.nodes}
    if node_id not in nodes:
        raise SpecError(f"узел {node_id} не найден в layer.json главы {ch}; есть: {', '.join(list(nodes)[:15])}")
    routes = [r for r in routing.routes if r.node_id == node_id]
    if len(routes) != 1:
        raise SpecError(f"для узла {node_id} в routing.json {len(routes)} маршрутов, нужен ровно один")
    route = routes[0]
    fmt = VIDEO_FORMATS.get(route.format) or VIDEO_FORMATS.get(route.secondary_format or "")
    if fmt is None:
        raise SpecError(f"маршрут узла {node_id} не видео: format «{route.format}», "
                        f"secondary_format «{route.secondary_format}»")
    if not route.template:
        raise SpecError(f"в маршруте узла {node_id} не задан шаблон сцены (template)")
    if route.template not in TEMPLATE_INFO:
        raise SpecError(f"шаблон {route.template} из routing.json неизвестен; есть {sorted(TEMPLATE_INFO)}")
    if format_problem(route.template, fmt):                 # до вызова LLM: та же таблица, что у video.build
        raise SpecError(f"узел {node_id}: {format_problem(route.template, fmt)}")
    return nodes[node_id], route, fmt


def _complete_json(prompt: str, vars: dict, schema: type[BaseModel], tier: str) -> BaseModel:
    try:
        from pipeline.llm import complete_json
    except ModuleNotFoundError as e:
        if e.name in ("pipeline.llm", "pipeline"):
            raise SpecError("модуль pipeline.llm (ядро П1) отсутствует: без LLM сценарий не генерируется. "
                            "Нужна ветка с ядром П1 (после мёржа в main).") from e
        raise SpecError(f"pipeline.llm не импортируется: не установлена зависимость «{e.name}» "
                        f"(requirements/core.txt)") from e
    try:
        return complete_json(prompt=prompt, vars=vars, schema=schema, tier=tier)
    except Exception as e:   # ошибки ключа, сети, кэша и JSON ядра — с именем промпта
        raise SpecError(f"LLM-вызов {prompt} не удался: {type(e).__name__}: {e}") from e


def _feedback(problems: list[str]) -> str:
    return ("Предыдущий ответ отклонён автоматической проверкой. Исправь всё перечисленное, "
            "остальное сохрани:\n- " + "\n- ".join(problems))


def _generate(prompt: str, vars: dict, schema: type[BaseModel], tier: str, build, check) -> BaseModel:
    feedback = NO_FEEDBACK
    for _ in range(ATTEMPTS):
        draft = _complete_json(prompt, {**vars, "feedback": feedback}, schema, tier)
        obj = build(draft)
        problems = check(obj)
        if not problems:
            return obj
        feedback = _feedback(problems)
    raise SpecError(f"{prompt}: ответ модели не прошёл проверку после {ATTEMPTS} попыток:\n- "
                    + "\n- ".join(problems))


def _template_problems(scene: SceneSpec, script: Script, node: Node, cfg: dict | None) -> list[str]:
    """Требования конкретного шаблона (из его конфигурации) — до сохранения спецификации."""
    if cfg is None:
        return []
    problems = param_source_problems(scene, node, cfg)
    if scene.template == "T1":
        from pipeline.video import t1_template
        problems += t1_template.check(scene, script, cfg)
    if scene.template == "T2":
        from pipeline.video import t2_template
        problems += t2_template.check(scene, script, cfg)
    if scene.template == "T3":
        from pipeline.video import t3_template
        problems += t3_template.check(scene, script, cfg)
    return problems


def scene_problems(scene: SceneSpec, script: Script, node: Node, cfg: dict | None, real_data_ok: bool) -> list[str]:
    """Все проверки спецификации сцены относительно сценария и узла — одни для генерации и готовой пары."""
    return check_scene(scene, script, real_data_ok=real_data_ok) + _template_problems(scene, script, node, cfg)


def pair_problems(script: Script, scene: SceneSpec, node: Node, fmt: str, templates_dir: Path) -> list[str]:
    """Готовая пара против текущего узла — те же проверки, что при генерации (без LLM): claim_id узла,
    правила сценария, связи кадров, источники параметров, требования шаблона и набора данных."""
    cfg = load_template_config(templates_dir, scene.template)
    real_ok = False
    if cfg is not None and cfg.get("requires_dataset") and isinstance(scene.params.get("dataset"), str):
        from pipeline.video.inputs import VideoInputError
        from pipeline.video.las_data import load_dataset
        from pipeline.video.t2_template import resolve_dataset_path
        try:
            real_ok = load_dataset(resolve_dataset_path(scene.params["dataset"]), cfg).real_verified
        except VideoInputError:
            pass                                  # сам набор данных проверит и отклонит t2_template.check
    return check_script(script, node, fmt) + scene_problems(scene, script, node, cfg, real_ok)


def _dataset_for(template: str, cfg: dict | None, dataset_path: Path | None):
    """Набор данных для шаблона, которому он нужен: (Dataset, параметры, которые подставляет код, сводка)."""
    if cfg is None or not cfg.get("requires_dataset"):
        if dataset_path is not None:
            raise SpecError(f"--dataset задан, а шаблону {template} набор данных не нужен")
        return None, {}, ""
    if dataset_path is None:
        raise SpecError(f"шаблону {template} нужен набор данных: --dataset <описание dataset.json с LAS>")
    from pipeline.video.inputs import VideoInputError
    from pipeline.video.las_data import load_dataset
    try:
        ds = load_dataset(dataset_path, cfg)
    except VideoInputError as e:
        raise SpecError(str(e)) from e
    if ds.borehole_diameter_m is None and "borehole_diameter_m" in cfg["params"]:
        raise SpecError(f"в описании набора данных {dataset_path} нет borehole_diameter_m — "
                        f"значение не выдумывается, добавьте его с источником в описание")
    path = Path(dataset_path).resolve()
    try:
        ref = path.relative_to(ROOT).as_posix()
    except ValueError:
        ref = str(path)
    injected = {"dataset": ref, "borehole_diameter_m": ds.borehole_diameter_m}
    injected = {k: v for k, v in injected.items() if k in cfg["params"]}
    lo, hi = ds.interval
    summary = "\n".join([
        "", "Набор данных (подставлен кодом; dataset и borehole_diameter_m в params не задавай):",
        f"- происхождение: {ds.kind}; метка кадров с этими данными — «{ds.label}»",
        f"- источник: {ds.provenance['source']}; файл {ds.provenance['file']}; скважина {ds.well}",
        f"- интервал набора: {lo:g}–{hi:g} м; шаг глубины {float(ds.depth[1] - ds.depth[0]):g} м",
        "- кривые (мнемоника и единица точно как в LAS): "
        + ", ".join(f"{m} [{u}]" for m, u in ds.units.items()),
        f"- диаметр ствола: {ds.borehole_diameter_m:g} м ({ds.provenance.get('borehole_diameter_source') or 'из описания'})",
    ])
    return ds, injected, summary


def generate(node: Node, route: Route, fmt: str, templates_dir: Path,
             dataset_path: Path | None = None) -> tuple[Script, SceneSpec]:
    video_id = f"{node.id}.{fmt}"
    lo, hi = DURATION_S[fmt]
    lang = source_language(node)
    claims = [{"id": c.id, "kind": c.kind, "text": c.text, "quote": c.quote} for c in node.claims]
    base = {"format_ru": route.format if route.format in VIDEO_FORMATS else route.secondary_format,
            "aspect": ASPECT[fmt], "template": route.template, "template_about": TEMPLATE_INFO[route.template],
            "node": node.model_dump(by_alias=True, exclude={"ext"})}
    cfg = load_template_config(templates_dir, route.template)
    ds, injected, ds_summary = _dataset_for(route.template, cfg, dataset_path)   # до вызова модели

    script = _generate(
        "video/script",
        {**base, "duration_range": f"{lo}–{hi} с",
         "word_budget": f"{lo * ESTIMATE_WPM // 60}–{hi * ESTIMATE_WPM // 60}",
         "source_language": LANG_RU[lang], "claims": claims},
        ScriptDraft, TIER_SCRIPT,
        lambda d: Script(video_id=video_id, node_id=node.id, format=fmt, **d.model_dump()),
        lambda s: check_script(s, node, fmt))

    phrases = [{"id": p.id, "beat": p.beat, "text": p.text, "on_screen": p.on_screen, "claim_id": p.claim_id}
               for p in script.phrases]
    def scene_from(d: SceneDraft) -> SceneSpec:
        if d.missing_params:   # данных в узле нет — повтор не поможет, выдумывать нельзя
            raise SpecError(f"в узле {node.id} нет данных для параметров шаблона {route.template}: "
                            f"{sorted(d.missing_params)}. Физические параметры не выдумываются: добавьте их "
                            f"в утверждения узла или выберите другой шаблон в маршрутизации")
        data = d.model_dump(exclude={"param_sources", "missing_params"})
        data["params"] = {**data["params"], **injected}          # значения из набора данных — от кода
        scene = SceneSpec(video_id=video_id, node_id=node.id, template=route.template, **data)
        scene.ext["video"] = {"param_sources": {k: v.model_dump() for k, v in d.param_sources.items()}}
        if ds is not None:
            scene.ext["video"]["dataset_provenance"] = ds.provenance
        return scene

    scene = _generate(
        "video/scene_spec",
        {**base, "phrases": phrases, "template_contract": template_contract(route.template, cfg) + ds_summary},
        SceneDraft, TIER_SCENE, scene_from,
        lambda s: scene_problems(s, script, node, cfg, real_data_ok=bool(ds and ds.real_verified)))

    est = estimate_duration(script)
    words = sum(count_words(p.text) for p in script.phrases)
    route_info = {"format": route.format, "secondary_format": route.secondary_format, "template": route.template,
                  "hook_short": route.hook_short, "why": route.why}
    script.ext["video"] = {
        "duration_estimate": {"seconds": est, "words": words,
                              "method": f"оценка до синтеза: {words} слов при {ESTIMATE_WPM} слов/мин + паузы; "
                                        f"не замер, фактическая длительность — после озвучки"},
        "source_language": lang, "route": route_info}
    scene.ext["video"].update({"sources": sources_table(script, node), "route": route_info,
                               "template_config": str(Path(templates_dir) / f"{route.template}.json") if cfg else None})
    return script, scene


def default_paths(ch: str, out_root: Path, layer_path: Path | None, routing_path: Path | None) -> tuple[Path, Path]:
    return layer_path or out_root / ch / "layer.json", routing_path or out_root / ch / "routing.json"


def output_dir(out_root: Path, ch: str, node_id: str, fmt: str) -> Path:
    """Стандартный каталог пары script.json + scene_spec.json (video_id = <node_id>.<fmt>)."""
    return out_root / ch / "videos" / f"{node_id}.{fmt}"


def load_route(ch: str, node_id: str, layer_path: Path | None, routing_path: Path | None,
               out_root: Path) -> tuple[Node, Route, str]:
    """Узел, маршрут и формат из layer.json и routing.json — общая точка для video.spec и video.build."""
    if not ID_RE.match(ch):
        raise SpecError(f"--ch «{ch}» — допустимы только [a-z0-9_.-]")
    layer_path, routing_path = default_paths(ch, out_root, layer_path, routing_path)
    layer = _load(layer_path, Layer, "учебный слой; путь можно задать --layer")
    routing = _load(routing_path, Routing, "маршрутизация; путь можно задать --routing")
    return select(layer, routing, ch, node_id)


def run(ch: str, node_id: str, layer_path: Path | None, routing_path: Path | None, out_root: Path,
        domain: str = "geology", dataset: Path | None = None) -> Path:
    if not ID_RE.match(domain):
        raise SpecError(f"--domain «{domain}» — допустимы только [a-z0-9_.-]")
    node, route, fmt = load_route(ch, node_id, layer_path, routing_path, out_root)
    script, scene = generate(node, route, fmt, ROOT / "domain" / domain / "templates", dataset)
    out = output_dir(out_root, ch, node.id, fmt)
    out.mkdir(parents=True, exist_ok=True)
    (out / "script.json").write_text(script.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    (out / "scene_spec.json").write_text(scene.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.video.spec", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ch", required=True, help="id главы")
    ap.add_argument("--node", required=True, help="id узла учебного слоя")
    ap.add_argument("--layer", type=Path, help="layer.json (по умолчанию out/<ch>/layer.json)")
    ap.add_argument("--routing", type=Path, help="routing.json (по умолчанию out/<ch>/routing.json)")
    ap.add_argument("--out-root", type=Path, default=ROOT / "out")
    ap.add_argument("--domain", default="geology", help="доменный пакет: конфигурации шаблонов в domain/<домен>/templates/")
    ap.add_argument("--dataset", type=Path, help="описание набора данных (dataset.json + LAS) для шаблонов с данными (T2)")
    a = ap.parse_args(argv)
    os.environ.setdefault("CH", a.ch)   # pipeline.llm пишет главу в журнал вызовов
    try:
        out = run(a.ch, a.node, a.layer, a.routing, a.out_root, a.domain, a.dataset)
    except SpecError as e:
        print(f"ОШИБКА video.spec: {e}", file=sys.stderr)
        return 2
    script = json.loads((out / "script.json").read_text(encoding="utf-8"))
    est = script["ext"]["video"]["duration_estimate"]
    print(f"script.json, scene_spec.json: {out}\n"
          f"фраз: {len(script['phrases'])}, длительность — оценка {est['seconds']} с ({est['method']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
