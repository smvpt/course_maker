"""Сборка демо-курса: out/<ch>/layer.json → out/<ch>/course/ (статический сайт, открывается из файла).

python -m pipeline.course.build --ch <id> [--node <node_id>]

Обязательный вход: layer.json. Необязательные (нет файла — блок не показывается):
routing.json, verify/report.json, illus/illustrations.json, videos/<node_id>/, data/pages/<ch>/p<N>.png.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markupsafe import Markup
from PIL import Image

from contracts.models import Field_, Illustrations, Layer, Node, ReviewOutput, Routing
from pipeline.course.order import group_parts, order_nodes

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
STYLEGUIDE = ROOT / "data/organizers/03_стайлгайд/styleguide.json"
VIDEO_FORMATS = {"шортс", "длинное видео"}
WORDS_PER_MIN = 120          # медленное чтение плотного текста новичком
SCAN_MAX_BYTES = 110_000     # «ужать до ~100 КБ»
SCAN_MAX_WIDTH = 1100


# ---------------------------------------------------------------- входы

def _read(path: Path, model):
    return model.model_validate_json(path.read_text(encoding="utf-8"))


def load_inputs(ch_dir: Path) -> dict:
    layer_path = ch_dir / "layer.json"
    if not layer_path.exists():
        raise FileNotFoundError(f"нет {layer_path}: сначала make structure (П1)")
    inp = {"layer": _read(layer_path, Layer), "routes": {}, "remarks": None, "illus": {}}
    if (ch_dir / "routing.json").exists():
        inp["routes"] = {r.node_id: r for r in _read(ch_dir / "routing.json", Routing).routes}
    if (ch_dir / "verify/report.json").exists():
        remarks: dict[str, object] = {}
        for r in _read(ch_dir / "verify/report.json", ReviewOutput).remarks:
            remarks[r.target] = r
        inp["remarks"] = remarks
    if (ch_dir / "illus/illustrations.json").exists():
        for il in _read(ch_dir / "illus/illustrations.json", Illustrations).illustrations:
            inp["illus"].setdefault(il.step_id, []).append(il)
    return inp


# ---------------------------------------------------------------- вид шага

def by_of(f) -> str:
    """author | model | hypothesis. Где в схеме нет by_model (примеры, задачи, решение на данных),
    берём ext["by_model"]; если и его нет — «модель»: приписать модели безопаснее, чем автору."""
    if getattr(f, "hypothesis", None):
        return "hypothesis"
    flag = getattr(f, "by_model", None)
    if flag is None:
        flag = f.ext.get("by_model", True)
    return "model" if flag else "author"


def has_text(f) -> bool:
    return f is not None and bool(f.text.strip())


def verify_status(claim_id: str, remarks) -> dict:
    if remarks is None:
        return {"status": "not_checked"}
    r = remarks.get(claim_id)
    if r is None:
        return {"status": "ok"}
    return {"status": "remark", "severity": r.severity, "problem": r.problem}


def parse_md_table(text: str) -> list[list[str]] | None:
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    if len(lines) < 2 or not all(l.startswith("|") for l in lines):
        return None
    rows = []
    for l in lines:
        cells = [c.strip() for c in l.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        rows.append(cells)
    return rows


def ocr_fixes(node: Node) -> list[dict]:
    """node.ext["core"]["ocr_fixes"] = [{page_pdf, was, now, where?}] — формат П3, пока П1 не поднял в контракт."""
    fixes = list(node.ext.get("core", {}).get("ocr_fixes", []))
    for f in fixes:
        missing = {"page_pdf", "was", "now"} - set(f)
        if missing:
            raise ValueError(f"{node.id}: в ext.core.ocr_fixes нет полей {sorted(missing)}: {f}")
    return fixes


def mark_fixes(cell: str, fixes: list[dict]) -> Markup:
    out = Markup.escape(cell)
    for f in fixes:
        now = str(f["now"])
        if now and now in cell:
            tip = f"исправлено распознавание: было «{f['was']}»"
            out = Markup(str(out).replace(str(Markup.escape(now)),
                         f'<mark class="ocr-fix" tabindex="0" title="{Markup.escape(tip)}">{Markup.escape(now)}</mark>'))
    return out


def node_words(node: Node) -> int:
    parts = [node.layers.main.text, node.layers.mechanism.text, node.layers.practice.text,
             node.layers.nuances.text, node.data_meaning.from_chapter.text, node.data_meaning.breaks.text,
             node.it_analogy.text, node.it_analogy.breaks_where]
    parts += [c.text + " " + c.quote for c in node.claims]
    parts += [d.text for d in node.layers.deeper] + [h.text for h in node.data_meaning.hypotheses]
    for w in node.worked_examples:
        parts += [w.condition, w.result, *w.steps]
    parts += [t.text for t in node.book_tasks]
    if node.misconception:
        parts.append(node.misconception.text)
    return sum(len(p.split()) for p in parts)


def minutes(node: Node) -> int:
    return max(1, math.ceil(node_words(node) / WORDS_PER_MIN))


def compress_scan(src: Path, dst: Path) -> None:
    img = Image.open(src).convert("RGB")
    if img.width > SCAN_MAX_WIDTH:
        img = img.resize((SCAN_MAX_WIDTH, round(img.height * SCAN_MAX_WIDTH / img.width)), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    for q in (70, 60, 50, 40, 30):
        img.save(dst, "JPEG", quality=q, optimize=True)
        if dst.stat().st_size <= SCAN_MAX_BYTES:
            return
    while dst.stat().st_size > SCAN_MAX_BYTES:
        img = img.resize((img.width * 4 // 5, img.height * 4 // 5), Image.LANCZOS)
        img.save(dst, "JPEG", quality=30, optimize=True)


def node_pages(node: Node) -> list[int]:
    pages = set(node.pages) | {c.page_pdf for c in node.claims}
    pages |= {w.page_pdf for w in node.worked_examples} | {t.page_pdf for t in node.book_tasks}
    return sorted(pages)


def step_view(node: Node, inp: dict, course: Path, pages_src: Path, ch_dir: Path) -> dict:
    fixes = ocr_fixes(node)
    text_claims = [c for c in node.claims if c.source_kind not in ("formula", "table")]
    formulas = [c for c in node.claims if c.source_kind == "formula"]
    tables = []
    for c in node.claims:
        if c.source_kind != "table":
            continue
        rows = parse_md_table(c.quote)
        page_fixes = [f for f in fixes if f.get("page_pdf") == c.page_pdf]
        tables.append({"claim": c, "rows": [[mark_fixes(x, page_fixes) for x in r] for r in rows] if rows else None})

    scans = {}
    for p in node_pages(node):
        src = pages_src / f"p{p}.png"
        rel = f"assets/pages/p{p}.jpg"
        if src.exists():
            if not (course / rel).exists():
                compress_scan(src, course / rel)
            scans[str(p)] = {"scan": rel, "claim_ids": [c.id for c in node.claims if c.page_pdf == p]}
        else:
            scans[str(p)] = {"scan": None, "claim_ids": [c.id for c in node.claims if c.page_pdf == p]}

    data = {
        "node_id": node.id,
        "claims": {c.id: {"quote": c.quote, "page": c.page_pdf, "page_print": c.page_print,
                          "text": c.text, "kind": c.kind, "source_kind": c.source_kind,
                          "by": "model" if c.by_model else "author",
                          "verify": verify_status(c.id, inp["remarks"])} for c in node.claims},
        "pages": scans,
    }

    media = video_view(node, inp, course, ch_dir)
    illus = []
    for il in inp["illus"].get(node.id, []):
        src = ch_dir / "illus" / il.file
        if not src.exists():
            raise FileNotFoundError(f"illustrations.json ссылается на несуществующий файл {src}")
        dst = course / "assets/illus" / il.file
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        illus.append({"il": il, "src": f"assets/illus/{il.file}"})

    lay = node.layers
    show_data = (has_text(node.data_meaning.from_chapter) or has_text(node.data_meaning.breaks)
                 or any(has_text(h) for h in node.data_meaning.hypotheses))
    # (id, заголовок, показывать ли) — порядок блоков на странице и в её оглавлении
    blocks = [
        ("b-main", "Суть", has_text(lay.main)),
        ("b-why", "Зачем этот шаг", has_text(node.why_here)),
        ("b-how", "Как это работает", has_text(lay.mechanism) or bool(text_claims)),
        ("b-formulas", "Формулы", bool(formulas)),
        ("b-tables", "Таблицы книги", bool(tables)),
        ("b-examples", "Разбор примеров из главы", bool(node.worked_examples)),
        ("b-practice", "Как делает специалист", has_text(lay.practice) or has_text(node.now_practice)),
        ("b-nuances", "Нюансы", has_text(lay.nuances)),
        ("b-misconception", "Частая ошибка", node.misconception is not None and has_text(node.misconception)),
        ("b-decision", "Решение на данных", node.decision_on_data is not None),
        ("b-data", "Что это значит для данных", show_data),
        ("b-analogy", "Аналогия", has_text(node.it_analogy)),
        ("b-terms", "Новые понятия", bool(node.terms_introduced or node.terms_used)),
        ("b-deeper", "Глубже", any(has_text(d) for d in lay.deeper)),
        ("b-tasks", "Задачи из книги", bool(node.book_tasks)),
        ("b-illus", "Иллюстрации", bool(illus)),
        ("b-media", "Ролик", media is not None),
        ("b-source", "Источник", True),
    ]
    return {
        "show": {b: on for b, _, on in blocks},
        "toc": [(b, t) for b, t, on in blocks if on],
        "node": node,
        "title": node.title_novice or node.title,
        "minutes": minutes(node),
        "text_claims": text_claims,
        "formulas": formulas,
        "tables": tables,
        "deeper": [d for d in lay.deeper if has_text(d)],
        "hypotheses": [h for h in node.data_meaning.hypotheses if has_text(h)],
        "prereqs": [l.target for l in node.links if l.type == "prerequisite"],
        "illus": illus,
        "media": media,
        "route": inp["routes"].get(node.id),
        "pages": node_pages(node),
        "data_json": Markup(json.dumps(data, ensure_ascii=False).replace("</", "<\\/")),
    }


def video_view(node: Node, inp: dict, course: Path, ch_dir: Path) -> dict | None:
    route = inp["routes"].get(node.id)
    vdir = ch_dir / "videos" / node.id
    mp4s = sorted(vdir.glob("*.mp4")) if vdir.exists() else []
    if mp4s:
        dst = course / "media" / node.id
        dst.mkdir(parents=True, exist_ok=True)
        files = []
        for f in mp4s + sorted(vdir.glob("*.vtt")):
            shutil.copy2(f, dst / f.name)
            files.append(f.name)
        mp4 = mp4s[0].name
        vtt = next((f for f in files if f.endswith(".vtt")), None)
        return {"kind": "video", "src": f"media/{node.id}/{mp4}",
                "vtt": f"media/{node.id}/{vtt}" if vtt else None}
    wants_video = route is not None and (route.format in VIDEO_FORMATS or route.secondary_format in VIDEO_FORMATS)
    if not wants_video:
        return None
    passport = vdir / "passport.json"
    if passport.exists():
        dst = course / "media" / node.id / "passport.json"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(passport, dst)
        return {"kind": "pending", "passport": f"media/{node.id}/passport.json"}
    return {"kind": "pending", "passport": None}


# ---------------------------------------------------------------- карта связей

def map_view(ordered: list[Node]) -> dict:
    ids = {n.id for n in ordered}
    depth: dict[str, int] = {}
    for n in ordered:  # порядок топологический → предпосылки уже посчитаны
        pre = [l.target for l in n.links if l.type == "prerequisite" and l.target in ids and l.target != n.id]
        depth[n.id] = 1 + max((depth[p] for p in pre), default=-1)
    row_h, box_h, indent, width = 56, 40, 22, 360
    boxes, pos = [], {}
    for i, n in enumerate(ordered):
        x = 8 + depth[n.id] * indent
        y = 8 + i * row_h
        pos[n.id] = (x, y)
        title = n.title_novice or n.title
        short = title if len(title) <= 30 else title[:29] + "…"
        boxes.append({"id": n.id, "x": x, "y": y, "w": width - x - 8, "h": box_h, "num": i + 1,
                      "label": short, "full": title})
    edges = []
    for n in ordered:
        for l in n.links:
            if l.type == "prerequisite" and l.target in pos and l.target != n.id:
                (x1, y1), (x2, y2) = pos[l.target], pos[n.id]
                sx, sy, ex, ey = x1 + 4, y1 + box_h, x2 + 4, y2 + box_h / 2
                edges.append(f"M{sx},{sy} C{sx},{ey} {sx},{ey} {ex - 2},{ey}")
    return {"boxes": boxes, "edges": edges, "w": width, "h": 16 + len(ordered) * row_h}


# ---------------------------------------------------------------- стили

def tokens_css(style: dict) -> str:
    legend = []
    for k, v in style["lithology"].items():
        legend.append(f"  --lith-{k}: {v['color']};")
    for k, v in style["fluids"].items():
        legend.append(f"  --fluid-{k}: {v['color']};")
    for k, v in style["curves"].items():
        legend.append(f"  --curve-{k.lower()}: {v['color']};")
    legend.append(f"  --measurement: {style['measurement']['color']};")
    legend.append(f"  --uncertainty: {style['uncertainty']['color']};")
    for i, (k, v) in enumerate(style["provenance"].items()):
        legend.append(f"  --prov-{i}: {v}; /* {k} */")
    dark = (f"  --bg: {style['background']};\n  --panel: {style['panel']};\n"
            f"  --text: {style['text']};\n  --muted: {style['muted']};\n"
            "  --line: #2A3440;\n  --accent: #F1C40F;\n  --link: #7FB3D5;\n"
            "  --hl-author: rgba(241,196,15,.18);\n  --hl-model: rgba(127,179,213,.16);\n  color-scheme: dark;")
    light = ("  --bg: #FBFAF7;\n  --panel: #FFFFFF;\n  --text: #1B1F24;\n  --muted: #5B6672;\n"
             "  --line: #DDE1E6;\n  --accent: #9A6B00;\n  --link: #1F5F99;\n"
             "  --hl-author: rgba(241,196,15,.30);\n  --hl-model: rgba(41,128,185,.14);\n  color-scheme: light;")
    font = style["fonts"]["ui"]
    return ("/* Сгенерировано из styleguide.json организаторов. Не править руками. */\n"
            "/* legend: одинаковая в обеих темах */\n:root {\n" + "\n".join(legend) +
            f"\n  --font-ui: \"{font}\", system-ui, -apple-system, Roboto, sans-serif;\n}}\n"
            "/* theme */\n"
            f":root {{\n{light}\n}}\n"
            f"@media (prefers-color-scheme: dark) {{\n  :root:not([data-theme=\"light\"]) {{\n{dark}\n  }}\n}}\n"
            f":root[data-theme=\"dark\"] {{\n{dark}\n}}\n")


# ---------------------------------------------------------------- сборка

def make_env() -> Environment:
    env = Environment(loader=FileSystemLoader(HERE / "templates"), autoescape=select_autoescape(["html", "j2"]),
                      undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
    icons = {p.stem: p.read_text(encoding="utf-8") for p in (HERE / "assets/icons").glob("*.svg")}

    def icon(name: str) -> Markup:
        if name not in icons:
            raise KeyError(f"нет иконки {name}.svg в pipeline/course/assets/icons")
        svg = icons[name].replace("<svg ", '<svg class="ic" aria-hidden="true" focusable="false" ', 1)
        return Markup(svg)

    env.globals.update(icon=icon, by_of=by_of, has_text=has_text)
    return env


def chapter_title(layer: Layer) -> str:
    return layer.ext.get("core", {}).get("title") or Path(layer.source).stem


def build(ch: str, out_root: Path = ROOT / "out", node: str | None = None,
          pages_dir: Path = ROOT / "data/pages", styleguide: Path = STYLEGUIDE) -> Path:
    ch_dir = out_root / ch
    inp = load_inputs(ch_dir)
    layer: Layer = inp["layer"]
    if layer.chapter != ch:
        raise ValueError(f"{ch_dir / 'layer.json'}: chapter={layer.chapter!r}, а запрошена глава {ch!r}")
    ordered = order_nodes(layer.nodes)
    if node is not None and node not in {n.id for n in ordered}:
        raise ValueError(f"узла {node!r} нет в {ch_dir / 'layer.json'}")

    course = ch_dir / "course"
    (course / "assets").mkdir(parents=True, exist_ok=True)
    for f in ("course.css", "course.js"):
        shutil.copy2(HERE / "assets" / f, course / "assets" / f)
    style = json.loads(styleguide.read_text(encoding="utf-8"))
    (course / "assets/tokens.css").write_text(tokens_css(style), encoding="utf-8")

    env = make_env()
    errata = [{"node": n, **f} for n in ordered for f in ocr_fixes(n)]
    common = {
        "ch": ch, "chapter_title": chapter_title(layer), "has_errata": bool(errata),
        "steps": [{"id": n.id, "title": n.title_novice or n.title, "minutes": minutes(n)} for n in ordered],
    }
    common["total_minutes"] = sum(s["minutes"] for s in common["steps"])
    titles = {n.id: n.title_novice or n.title for n in ordered}

    def render(name: str, tpl: str, **ctx) -> None:
        html = env.get_template(tpl).render(**common, **ctx)
        (course / name).write_text(html, encoding="utf-8")

    pages_src = pages_dir / ch
    for i, n in enumerate(ordered):
        if node is not None and n.id != node:
            continue
        render(f"step-{n.id}.html", "step.html.j2", v=step_view(n, inp, course, pages_src, ch_dir),
               idx=i, prev=ordered[i - 1] if i > 0 else None,
               next=ordered[i + 1] if i + 1 < len(ordered) else None, titles=titles, page="step")

    render("index.html", "index.html.j2", parts=group_parts(ordered), page="index")
    render("cards.html", "cards.html.j2", nodes=ordered, page="cards")
    render("summary.html", "summary.html.j2", nodes=ordered, page="summary")
    render("map.html", "map.html.j2", m=map_view(ordered), nodes=ordered, titles=titles, page="map")
    if errata:
        render("errata.html", "errata.html.j2", errata=errata, page="errata")
    elif (course / "errata.html").exists():
        (course / "errata.html").unlink()
    return course


def main() -> None:
    ap = argparse.ArgumentParser(description="layer.json → out/<ch>/course/")
    ap.add_argument("--ch", required=True)
    ap.add_argument("--node")
    ap.add_argument("--out", type=Path, default=ROOT / "out", help="корень out/ (по умолчанию out/)")
    ap.add_argument("--pages", type=Path, default=ROOT / "data/pages", help="корень сканов страниц")
    a = ap.parse_args()
    course = build(a.ch, out_root=a.out, node=a.node, pages_dir=a.pages)
    print(f"курс: {course / 'index.html'}")


if __name__ == "__main__":
    main()
