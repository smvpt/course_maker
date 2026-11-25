"""Сборка демо-курса: out/<ch>/layer.json → out/<ch>/course/ (статический сайт, открывается из файла).

python -m pipeline.course.build --ch <id> [--node <node_id>]

Обязательный вход: layer.json. Необязательные (нет файла — блок не показывается):
routing.json, verify/report.json, illus/illustrations.json, videos/<node_id>/, data/pages/<ch>/p<N>.png.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markupsafe import Markup
from PIL import Image

from contracts.models import Illustrations, Layer, Node, ReviewOutput, Routing, Task, Tasks
from pipeline.course.order import break_cycles, group_parts, order_nodes, part_of
from pipeline.course.steptext import Para, load_step_text, node_hash

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


# ---------------------------------------------------------------- задания (tasks.json делает задача 3 этого же модуля)

def load_tasks(ch: str, course_dir: Path, layer: Layer) -> list[Task]:
    path = course_dir / "tasks.json"
    if not path.exists():
        return []
    tasks = _read(path, Tasks)
    if tasks.chapter != ch:
        raise ValueError(f"{path}: chapter={tasks.chapter!r}, а запрошена глава {ch!r}")
    claims = {n.id: {c.id for c in n.claims} for n in layer.nodes}
    for t in tasks.tasks:
        if t.step_id not in claims:
            raise ValueError(f"{path}: задание {t.id}: нет шага {t.step_id!r} в layer.json")
        missing = [c for c in t.claim_ids if c not in claims[t.step_id]]
        if missing:
            raise ValueError(f"{path}: задание {t.id}: нет утверждений {missing} в шаге {t.step_id}")
    return tasks.tasks


def answer_text(t: Task) -> str:
    opts = {o.id: o.text for o in t.options}

    def opt(i) -> str:
        if i not in opts:
            raise ValueError(f"задание {t.id}: в answer указан вариант {i!r}, которого нет в options")
        return opts[i]

    if t.type == "single":
        return opt(t.answer)
    if t.type == "multiple":
        return "; ".join(opt(i) for i in t.answer)
    if t.type == "order":
        return " → ".join(opt(i) for i in t.answer)
    if t.type == "gap":
        return ", ".join(str(w) for w in t.answer)
    num = str(t.answer).replace(".", ",")
    tol = f" (±{str(t.tolerance).replace('.', ',')})" if t.tolerance else ""
    return f"{num}{(' ' + t.unit) if t.unit else ''}{tol}"


def gap_parts(prompt: str) -> list[tuple[str, str | int]]:
    """Текст с пропусками {{1}} → [("text", ...), ("gap", 1), ...]."""
    out: list[tuple[str, str | int]] = []
    pos = 0
    for m in re.finditer(r"\{\{(\d+)\}\}", prompt):
        out.append(("text", prompt[pos:m.start()]))
        out.append(("gap", int(m.group(1))))
        pos = m.end()
    out.append(("text", prompt[pos:]))
    return out


def mask_gaps(prompt: str) -> str:
    return re.sub(r"\{\{\d+\}\}", "…", prompt)


def task_view(t: Task, i: int) -> dict:
    short = mask_gaps(t.prompt)
    return {"t": t, "i": i, "answer": answer_text(t),
            "parts": gap_parts(t.prompt) if t.type == "gap" else None,
            "short": short if len(short) <= 140 else short[:139] + "…"}


# ---------------------------------------------------------------- текст шага (step_text.json, задача 2)

def paras_view(node: Node, paras: list[Para]) -> dict[str, list[dict]]:
    """Абзацы по блокам. «стр. N» — страницы именно тех утверждений, на которые ссылается абзац."""
    page_of = {c.id: c.page_pdf for c in node.claims}
    out: dict[str, list[dict]] = {}
    for p in paras:
        for cid in p.claim_ids:
            if cid not in page_of:
                raise ValueError(f"step_text.json: шаг {node.id}: абзац ссылается на несуществующее утверждение {cid}")
        html = Markup(re.sub(r"\[\[(.+?)\]\]", r"<dfn>\1</dfn>", str(Markup.escape(p.text))))   # термин при первом упоминании
        out.setdefault(p.block, []).append({
            "html": html, "by": "hypothesis" if p.hypothesis else "model", "limit": p.limit,
            "pages": sorted({page_of[c] for c in p.claim_ids}), "claims": " ".join(p.claim_ids)})
    return out


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


def step_view(node: Node, inp: dict, course: Path, pages_src: Path, ch_dir: Path, tasks: list[Task],
              paras: list[Para] | None = None) -> dict:
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
    check_items = 1 + (1 if media is not None and media["kind"] == "video" else 0) + (1 if tasks else 0)
    show_data = (has_text(node.data_meaning.from_chapter) or has_text(node.data_meaning.breaks)
                 or any(has_text(h) for h in node.data_meaning.hypotheses))
    # (id, заголовок, показывать ли) — порядок блоков на странице и в её оглавлении
    blocks = [
        ("b-main", "Суть", has_text(lay.main)),
        ("b-why", "Зачем этот шаг", has_text(node.why_here)),
        ("b-how", "Как это работает", has_text(lay.mechanism) or bool(text_claims)),
        ("b-quotes", "Цитаты автора", paras is not None and bool(text_claims)),
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
        ("b-quiz", "Задания", bool(tasks)),
        ("b-source", "Источник", True),
        ("b-check", "Чек-лист шага", True),
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
        "tasks": [task_view(t, i + 1) for i, t in enumerate(tasks)],
        "tasks_json": Markup(json.dumps({t.id: {"type": t.type, "answer": t.answer, "tolerance": t.tolerance} for t in tasks},
                                        ensure_ascii=False).replace("</", "<\\/")),
        "paras": paras_view(node, paras) if paras is not None else None,
        "check_items": check_items,
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


# ---------------------------------------------------------------- «Где здесь ИТ-задачи»

def it_items(ordered: list[Node]) -> list[dict]:
    """По шагам: линза неэффективности, что значит для данных (гипотезы помечены), аналогия с границей."""
    items = []
    for i, n in enumerate(ordered):
        sections: list[tuple[str, str, str]] = []
        lens = n.inefficiency_lens
        if lens is not None:
            by = "model" if lens.by_model else "author"
            for label, text in (("Входные данные", lens.inputs), ("Ручные шаги", lens.manual_steps),
                                ("Точки суждения", lens.judgment_points), ("Время", lens.time),
                                ("Типичные ошибки", lens.typical_errors)):
                if text.strip():
                    sections.append((label, text, by))
        dm = n.data_meaning
        if has_text(dm.from_chapter):
            sections.append(("Что это значит для данных", dm.from_chapter.text, by_of(dm.from_chapter)))
        if has_text(dm.breaks):
            sections.append(("Где ломается в данных", dm.breaks.text, by_of(dm.breaks)))
        for h in dm.hypotheses:
            if has_text(h):
                sections.append(("Гипотеза", h.text, by_of(h)))
        if n.it_analogy.text.strip():
            by = "model" if n.it_analogy.by_model else "author"
            sections.append(("Аналогия", n.it_analogy.text, by))
            if n.it_analogy.breaks_where.strip():
                sections.append(("Где аналогия перестаёт работать", n.it_analogy.breaks_where, by))
        if sections:
            items.append({"id": n.id, "index": i + 1, "title": n.title_novice or n.title, "sections": sections})
    return items


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
    # UI-палитра (синий акцент и статусы) — только для интерфейса, никогда для контента и картинок:
    # в контенте эти оттенки заняты легендой (вода, газ, нефть, кривые ГИС).
    dark = (f"  --bg: {style['background']};\n  --panel: {style['panel']};\n"
            f"  --text: {style['text']};\n  --muted: {style['muted']};\n"
            "  --border: rgba(255, 255, 255, .08);\n"
            "  --ui-accent: #2F6BDB;\n  --ui-on-accent: #FFFFFF;\n  --ui-link: #7FA8FF;\n"
            "  --ui-ok: #46C28A;\n  --ui-warn: #E3B341;\n  --ui-bad: #FF7B72;\n  color-scheme: dark;")
    light = ("  --bg: #FBFAF7;\n  --panel: #FFFFFF;\n  --text: #1B1F24;\n  --muted: #5B6672;\n"
             "  --border: rgba(0, 0, 0, .08);\n"
             "  --ui-accent: #1F5FD1;\n  --ui-on-accent: #FFFFFF;\n  --ui-link: #1F5FD1;\n"
             "  --ui-ok: #1E7F52;\n  --ui-warn: #8A6100;\n  --ui-bad: #C0392B;\n  color-scheme: light;")
    return ("/* Сгенерировано из styleguide.json организаторов. Не править руками. */\n"
            "/* legend: одинаковая в обеих темах */\n:root {\n" + "\n".join(legend) + "\n}\n"
            "/* theme */\n"
            ":root {\n  --radius: 12px;\n  --font-ui: system-ui, \"Segoe UI\", sans-serif;\n}\n"
            f":root {{\n{light}\n}}\n"
            f"@media (prefers-color-scheme: dark) {{\n  :root:not([data-theme=\"light\"]) {{\n{dark}\n  }}\n}}\n"
            f":root[data-theme=\"dark\"] {{\n{dark}\n}}\n")


# ---------------------------------------------------------------- сборка

def plural(n: int, one: str, few: str, many: str) -> str:
    n10, n100 = n % 10, n % 100
    if n10 == 1 and n100 != 11:
        return one
    if 2 <= n10 <= 4 and not 12 <= n100 <= 14:
        return few
    return many


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
    env.filters["plural"] = plural
    return env


def chapter_title(layer: Layer) -> str:
    """Человеческое название — layer.ext["core"]["title"] (поле поставляет П1); id главы — только запасной вариант."""
    return layer.ext.get("core", {}).get("title") or layer.chapter


def _has_video(ch_dir: Path, node_id: str) -> bool:
    vdir = ch_dir / "videos" / node_id
    return vdir.exists() and any(vdir.glob("*.mp4"))


def build(ch: str, out_root: Path = ROOT / "out", node: str | None = None,
          pages_dir: Path = ROOT / "data/pages", styleguide: Path = STYLEGUIDE,
          generate: bool = False, domain: str | None = None) -> Path:
    ch_dir = out_root / ch
    inp = load_inputs(ch_dir)
    layer: Layer = inp["layer"]
    if layer.chapter != ch:
        raise ValueError(f"{ch_dir / 'layer.json'}: chapter={layer.chapter!r}, а запрошена глава {ch!r}")

    warnings: list[dict] = []

    def warn(code: str, message: str, **extra) -> None:
        print(f"WARNING: {message}", file=sys.stderr)
        warnings.append({"code": code, "message": message, **extra})

    nodes, cycles = break_cycles(layer.nodes)          # повтор id → ValueError
    for c in cycles:
        loop = " → ".join(c["cycle"] + [c["cycle"][0]])
        warn("prerequisite_cycle",
             f"цикл в links.prerequisite (стрелка = «опирается на»): {loop}; "
             f"отброшена опора {c['dropped'][0]} → {c['dropped'][1]}",
             nodes=c["cycle"], dropped=c["dropped"])
    ordered = order_nodes(nodes)
    if node is not None and node not in {n.id for n in ordered}:
        raise ValueError(f"узла {node!r} нет в {ch_dir / 'layer.json'}")

    no_part = [n.id for n in layer.nodes if not n.ext.get("core", {}).get("part")]
    if len(no_part) == len(layer.nodes):
        warn("no_parts", 'ни у одного узла нет ext["core"]["part"]: вся глава собрана одной частью «Глава»')
    elif no_part:
        warn("partial_parts", f'у узлов нет ext["core"]["part"], они попали в часть «Глава»: {", ".join(no_part)}',
             nodes=no_part)

    if not layer.ext.get("core", {}).get("title"):
        warn("no_title", 'нет layer.ext["core"]["title"]: в заголовке курса показан id главы')

    course = ch_dir / "course"
    (course / "assets").mkdir(parents=True, exist_ok=True)
    for f in ("course.css", "course.js"):
        shutil.copy2(HERE / "assets" / f, course / "assets" / f)
    shutil.copytree(HERE / "assets/katex", course / "assets/katex", dirs_exist_ok=True)   # формулы без CDN
    style = json.loads(styleguide.read_text(encoding="utf-8"))
    (course / "assets/tokens.css").write_text(tokens_css(style), encoding="utf-8")

    if generate:                                   # текст шагов и задания: модель только через pipeline.llm
        from pipeline.course import generate as gen
        gen.run(layer, ch_dir, course, node, domain)
    step_text = load_step_text(course / "step_text.json", ch)
    orig = {n.id: n for n in layer.nodes}
    fresh = {nid: st.paragraphs for nid, st in step_text.items() if nid in orig and st.hash == node_hash(orig[nid])}
    stale = [nid for nid in step_text if nid in orig and nid not in fresh]
    if stale:
        warn("stale_step_text", f"step_text.json устарел для шагов {', '.join(stale)} (узел изменился после генерации): "
             "они собраны из полей слоя, запусти сборку без --no-llm", nodes=stale)
    tasks = load_tasks(ch, course, layer)
    tasks_by_step: dict[str, list[Task]] = {}
    for t in tasks:
        tasks_by_step.setdefault(t.step_id, []).append(t)

    env = make_env()
    errata = [{"node": n, **f} for n in ordered for f in ocr_fixes(n)]
    steps = [{"id": n.id, "title": n.title_novice or n.title, "minutes": minutes(n), "part": part_of(n),
              "video": _has_video(ch_dir, n.id), "illus": len(inp["illus"].get(n.id, [])),
              "tasks": len(tasks_by_step.get(n.id, []))} for n in ordered]
    meta = {"ch": ch, "steps": steps,
            "tasks": [{"id": t.id, "step_id": t.step_id, "claim_ids": t.claim_ids, "type": t.type, "kind": t.kind,
                       "prompt": mask_gaps(t.prompt), "explanation": t.explanation} for t in tasks]}
    common = {"ch": ch, "chapter_title": chapter_title(layer), "has_errata": bool(errata), "steps": steps,
              "n_tasks": len(tasks), "meta": meta, "total_minutes": sum(s["minutes"] for s in steps)}
    titles = {n.id: n.title_novice or n.title for n in ordered}

    def render(name: str, tpl: str, **ctx) -> None:
        html = env.get_template(tpl).render(**common, **ctx)
        (course / name).write_text(html, encoding="utf-8")

    pages_src = pages_dir / ch
    for i, n in enumerate(ordered):
        if node is not None and n.id != node:
            continue
        render(f"step-{n.id}.html", "step.html.j2",
               v=step_view(n, inp, course, pages_src, ch_dir, tasks_by_step.get(n.id, []), fresh.get(n.id)),
               idx=i, prev=ordered[i - 1] if i > 0 else None,
               next=ordered[i + 1] if i + 1 < len(ordered) else None, titles=titles, page="step")

    groups = [(s, [task_view(t, i + 1) for i, t in enumerate(tasks_by_step[s["id"]])])
              for s in steps if s["id"] in tasks_by_step]
    render("index.html", "index.html.j2", parts=group_parts(ordered), page="index")
    render("tasks.html", "tasks.html.j2", groups=groups, page="tasks")
    render("progress.html", "progress.html.j2", page="progress")
    render("mistakes.html", "mistakes.html.j2", page="mistakes")
    render("cards.html", "cards.html.j2", nodes=ordered, page="cards")
    render("summary.html", "summary.html.j2", nodes=ordered, page="summary")
    render("it.html", "it.html.j2", items=it_items(ordered), page="it")
    render("map.html", "map.html.j2", m=map_view(ordered), nodes=ordered, titles=titles, page="map")
    if errata:
        render("errata.html", "errata.html.j2", errata=errata, page="errata")
    elif (course / "errata.html").exists():
        (course / "errata.html").unlink()

    all_pages = sorted({p for n in ordered for p in node_pages(n)})
    report = {"chapter": ch, "nodes": len(ordered), "tasks": len(tasks), "step_text_nodes": len(fresh), "warnings": warnings,
              "missing_scans": [p for p in all_pages if not (pages_src / f"p{p}.png").exists()]}
    (course / "build_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return course


def main() -> None:
    ap = argparse.ArgumentParser(description="layer.json → out/<ch>/course/ (с текстом шагов и заданиями через LLM)")
    ap.add_argument("--ch", required=True)
    ap.add_argument("--node", help="пересобрать один шаг (его текст и задания генерируются заново, если узел изменился)")
    ap.add_argument("--no-llm", action="store_true", help="не звать модель: использовать step_text.json и tasks.json как есть")
    ap.add_argument("--domain", help="доменный пакет (по умолчанию — из out/<ch>/units.json)")
    ap.add_argument("--out", type=Path, default=Path(os.environ.get("OUT_DIR") or ROOT / "out"), help="корень out/")
    ap.add_argument("--pages", type=Path, default=ROOT / "data/pages", help="корень сканов страниц")
    a = ap.parse_args()
    course = build(a.ch, out_root=a.out, node=a.node, pages_dir=a.pages, generate=not a.no_llm, domain=a.domain)
    print(f"курс: {course / 'index.html'}")


if __name__ == "__main__":
    main()
