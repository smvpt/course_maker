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

from typing import get_args

from contracts.models import FormatRu, Illustrations, Layer, Node, ReviewOutput, Route, Task, Tasks
from pipeline.course import guess as guess_mod, interactive as inter_mod
from pipeline.course.order import break_cycles, group_parts, order_nodes, part_of
from pipeline.course.pernode import read_store
from pipeline.course.steptext import Para, node_hash, norm, normalize_terms, read_step_text
from pipeline.course.tasks import MISMATCH
from pipeline.illus import gen as illus_gen

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


KNOWN_FORMATS = set(get_args(FormatRu))
KNOWN_TEMPLATES = {"T1", "T2", "T3", "T4"}


def load_routes(path: Path) -> tuple[dict[str, Route], list[dict], bool]:
    """Маршруты из routing.json, терпимо к ошибкам: (маршруты по id узла, замечания, файл пригоден).

    Неизвестный шаблон (не T1–T4) отбрасывается, маршрут остаётся: интерактив выберет шаблон по типу трудности узла.
    Неизвестный формат или маршрут без обязательных полей пропускается. Нечитаемый файл считается отсутствующим.
    Каждое замечание попадёт в stderr и build_report.json."""
    problems: list[dict] = []

    def bad(code: str, message: str, node: str | None = None) -> None:
        problems.append({"code": code, "message": message, **({"node": node} if node else {})})

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        items = raw["routes"]
        if not isinstance(items, list):
            raise TypeError(f"routes должен быть списком, а не {type(items).__name__}")
    except (ValueError, KeyError, TypeError) as e:       # JSONDecodeError — ValueError; запись о причине остаётся в замечаниях
        bad("routing_unreadable", f"routing.json нельзя прочитать ({type(e).__name__}: {e}): маршрутизация не учитывается")
        return {}, problems, False
    routes: dict[str, Route] = {}
    for item in items:
        nid = item.get("node_id") if isinstance(item, dict) else None
        if not isinstance(item, dict) or not nid:
            bad("routing_invalid_route", f"в routing.json запись без node_id пропущена: {str(item)[:80]}")
            continue
        item = dict(item)
        if item.get("format") not in KNOWN_FORMATS:
            bad("routing_unknown_format", f"маршрут шага {nid}: неизвестный формат {item.get('format')!r}, маршрут пропущен", nid)
            continue
        if item.get("secondary_format") is not None and item["secondary_format"] not in KNOWN_FORMATS:
            bad("routing_unknown_format", f"маршрут шага {nid}: неизвестный дополнительный формат {item['secondary_format']!r}, он не учитывается", nid)
            item["secondary_format"] = None
        if item.get("template") is not None and item["template"] not in KNOWN_TEMPLATES:
            bad("routing_unknown_template", f"маршрут шага {nid}: шаблон {item['template']!r} не из T1–T4, шаблон выбран по типу трудности узла", nid)
            item["template"] = None
        try:
            routes[nid] = Route.model_validate(item)
        except ValueError as e:                            # pydantic.ValidationError
            bad("routing_invalid_route", f"маршрут шага {nid} не соответствует схеме, пропущен: {str(e).splitlines()[0]}", nid)
    return routes, problems, True


def load_inputs(ch_dir: Path) -> dict:
    layer_path = ch_dir / "layer.json"
    if not layer_path.exists():
        raise FileNotFoundError(f"нет {layer_path}: сначала make structure (П1)")
    inp = {"layer": _read(layer_path, Layer), "routes": {}, "remarks": None, "illus": {}, "illus_warnings": []}
    inp["has_routing"] = False
    inp["routing_problems"] = []
    if (ch_dir / "routing.json").exists():
        inp["routes"], inp["routing_problems"], inp["has_routing"] = load_routes(ch_dir / "routing.json")
    if (ch_dir / "verify/report.json").exists():
        remarks: dict[str, object] = {}
        for r in _read(ch_dir / "verify/report.json", ReviewOutput).remarks:
            remarks[r.target] = r
        inp["remarks"] = remarks
    if (ch_dir / "illus/illustrations.json").exists():
        illus = _read(ch_dir / "illus/illustrations.json", Illustrations)
        for il in illus.illustrations:
            inp["illus"].setdefault(il.step_id, []).append(il)
        inp["illus_warnings"] = illus.ext.get("illus", {}).get("warnings", [])
    return inp


# ---------------------------------------------------------------- задания (tasks.json делает задача 3 этого же модуля)

def task_problems(t: Task, claims: dict[str, set[str]]) -> list[str]:
    """Что не так с заданием относительно текущего слоя (узел или утверждение удалили, ответ ссылается на несуществующий вариант)."""
    if t.step_id not in claims:
        return [f"нет шага {t.step_id!r} в layer.json"]
    problems = []
    missing = [c for c in t.claim_ids if c not in claims[t.step_id]]
    if missing:
        problems.append(f"нет утверждений {missing} в шаге {t.step_id}")
    if t.type in ("single", "multiple", "order"):
        given = [t.answer] if isinstance(t.answer, str) else list(t.answer)
        absent = [a for a in given if a not in {o.id for o in t.options}]
        if absent:
            problems.append(f"в answer указаны варианты {absent}, которых нет в options")
    return problems


def load_tasks(ch: str, course_dir: Path, layer: Layer) -> tuple[list[Task], dict, list[dict]]:
    """Задания, служебные данные генерации (ext.course) и устаревшие задания, которые курс не показывает.

    Устаревшее задание (слой правили после генерации) выбрасывается с записью: живая пересборка не должна падать.
    Файл tasks.json при этом не меняется, его перезапишет следующая генерация."""
    path = course_dir / "tasks.json"
    if not path.exists():
        return [], {}, []
    tasks = _read(path, Tasks)
    if tasks.chapter != ch:
        raise ValueError(f"{path}: chapter={tasks.chapter!r}, а запрошена глава {ch!r}")
    claims = {n.id: {c.id for c in n.claims} for n in layer.nodes}
    good, stale = [], []
    for t in tasks.tasks:
        problems = task_problems(t, claims)
        if problems:
            stale.append({"task": t.id, "node": t.step_id, "errors": problems})
        else:
            good.append(t)
    return good, tasks.ext.get("course", {}), stale


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
            "id": f"p-{p.block}-{len(out.get(p.block, [])) + 1}",                       # якорь: поиск, словарь, «Перечитать»
            "html": html, "by": "hypothesis" if p.hypothesis else "model", "limit": p.limit,
            "pages": sorted({page_of[c] for c in p.claim_ids}), "claims": " ".join(p.claim_ids)})
    return out


# ---------------------------------------------------------------- словарь, поиск, подсказки терминов

MARK = re.compile(r"\[\[(.+?)\]\]")
BLOCK_TITLES = {"main": ("b-main", "Суть"), "why": ("b-why", "Зачем этот шаг"), "how": ("b-how", "Как это работает"),
                "practice": ("b-practice", "Как делает специалист"), "nuances": ("b-nuances", "Нюансы"),
                "misconception": ("b-misconception", "Частая ошибка"), "decision": ("b-decision", "Решение на данных"),
                "data": ("b-data", "Что это значит для данных"), "analogy": ("b-analogy", "Аналогия"), "deeper": ("b-deeper", "Глубже")}


def strip_marks(text: str) -> str:
    return MARK.sub(r"\1", text)


def term_definition(text: str, term: str) -> str:
    """Определение термина из текста шага: предложение, где он выделен, и следующее за ним (скобки [[ ]] сняты)."""
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    i = next((k for k, s in enumerate(sents) if term.casefold() in {m.casefold() for m in MARK.findall(s)}), 0)
    return strip_marks(" ".join(sents[i:i + 2]))


def build_glossary(ordered: list[Node], fresh: dict[str, list[Para]]) -> list[dict]:
    """Все термины, которые вводит глава, по алфавиту: определение, страница книги и шаг, где термин вводится.
    Определение — из текста шага (то, что модель объяснила по узлу); без текста модели — из утверждения узла."""
    items = []
    for n in ordered:
        paras = fresh.get(n.id)
        page_of = {c.id: c.page_pdf for c in n.claims}
        for t in n.terms_introduced:
            e = {"term": t, "key": norm(t), "node": n.id, "step_title": n.title_novice or n.title,
                 "definition": None, "page": None, "claim": None, "anchor": "b-main"}
            if paras:
                seen: dict[str, int] = {}
                for p in paras:
                    seen[p.block] = seen.get(p.block, 0) + 1
                    if t.casefold() in {m.casefold() for m in MARK.findall(p.text)}:
                        known = [c for c in p.claim_ids if c in page_of]     # неизвестное утверждение громко упадёт в paras_view
                        if not known:
                            continue
                        cid = min(known, key=lambda c: page_of[c])
                        e.update(definition=term_definition(p.text, t), page=page_of[cid], claim=cid, anchor=f"p-{p.block}-{seen[p.block]}")
                        break
            if e["definition"] is None:
                stem = norm(t)[:5]
                c = next((c for c in n.claims if c.source_kind not in ("formula", "table") and stem in norm(c.text)), None)
                if c is not None:
                    e.update(definition=c.text, page=c.page_pdf, claim=c.id)
            items.append(e)
    return sorted((e for e in items if e["definition"]), key=lambda e: e["key"])      # термин без определения в словарь не попадает: «см. шаг» — не определение


def search_index(ordered: list[Node], fresh: dict[str, list[Para]], glossary: list[dict]) -> list[dict]:
    """Индекс офлайн-поиска: названия шагов, термины, текст блоков. s — шаг, a — якорь абзаца, b — название блока, x — текст."""
    out: list[dict] = []
    for n in ordered:
        title = n.title_novice or n.title
        out.append({"k": "step", "s": n.id, "t": title, "b": "Шаг", "a": "", "x": " ".join(dict.fromkeys(x for x in (title, n.title, n.layers.topic.text if has_text(n.layers.topic) else "") if x))})   # без повторов
        paras = fresh.get(n.id)
        if paras:
            seen: dict[str, int] = {}
            for p in paras:
                seen[p.block] = seen.get(p.block, 0) + 1
                bid, btitle = BLOCK_TITLES[p.block]
                out.append({"k": "para", "s": n.id, "t": title, "b": btitle, "a": f"p-{p.block}-{seen[p.block]}", "x": strip_marks(p.text)})
        else:
            lay, dm = n.layers, n.data_meaning
            fields = [("main", lay.main), ("why", n.why_here), ("how", lay.mechanism), ("practice", lay.practice), ("nuances", lay.nuances),
                      ("data", dm.from_chapter), ("data", dm.breaks), ("misconception", n.misconception) if n.misconception else None]
            for item in fields:
                if item and has_text(item[1]):
                    out.append({"k": "para", "s": n.id, "t": title, "b": BLOCK_TITLES[item[0]][1], "a": BLOCK_TITLES[item[0]][0], "x": item[1].text})
            if n.it_analogy.text.strip():
                out.append({"k": "para", "s": n.id, "t": title, "b": "Аналогия", "a": "b-analogy", "x": n.it_analogy.text})
        d = n.decision_on_data
        if d:
            out.append({"k": "para", "s": n.id, "t": title, "b": "Решение на данных", "a": "b-decision", "x": " ".join([*d.features, d.rule, d.conclusion])})
    for g in glossary:
        if g["definition"]:
            out.append({"k": "term", "s": g["node"], "t": g["step_title"], "b": "Термин", "a": g["anchor"], "x": f"{g['term']}. {g['definition']}"})
    return out


def terms_view(glossary: list[dict], node_id: str) -> dict:
    """Подсказки терминов шага: ключ (термин без регистра, ё = е) → определение, страница, утверждение, ссылка на место, где вводится."""
    return {g["key"]: {"term": g["term"], "def": g["definition"], "page": g["page"], "claim": g["claim"],
                       "href": f"step-{g['node']}.html#{g['anchor']}", "step": g["step_title"]}
            for g in glossary if g["node"] == node_id and g["definition"]}


# ---------------------------------------------------------------- интерактив (interactive.json, задача 5)

def inter_view(data: dict, style_raw: dict) -> dict:
    """Данные интерактива + палитра из styleguide (цвета рисует JS из этих данных, а не из CSS)."""
    gs = illus_gen.Style(style_raw)
    if data["template"] == "scheme":
        parts = []
        for p in data["parts"]:
            color = style_raw["lithology"][p["rock"]]["color"] if p["rock"] else None
            parts.append({**p, "color": color, "on": gs.on(color) if color else None})
        return {"scheme": True, "data": data, "parts": parts, "json": Markup(json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))}
    badge = gs.prov("симуляция")
    palette = {"bg": gs.bg, "panel": gs.panel, "text": gs.text, "muted": gs.muted, "color": gs.curve(data["curve_key"]) or gs.measurement,
               "badge": badge, "badgeText": gs.on(badge)}
    head, rows = inter_mod.table_rows(data)
    return {"scheme": False, "data": data, "head": head, "rows": rows, "steps": len(data["slider"]["values"]),
            "json": Markup(json.dumps({**data, "palette": palette}, ensure_ascii=False).replace("</", "<\\/"))}


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


def page_range(node: Node) -> str:
    """«стр. 38» или «стр. 38–40» по страницам PDF утверждений узла."""
    pages = node_pages(node)
    if not pages:
        return ""
    return f"стр. {pages[0]}" if pages[0] == pages[-1] else f"стр. {pages[0]}–{pages[-1]}"


def step_view(node: Node, inp: dict, course: Path, pages_src: Path, ch_dir: Path, tasks: list[Task],
              paras: list[Para] | None = None, interactive: dict | None = None, guess: dict | None = None,
              style_raw: dict | None = None, terms: dict | None = None) -> dict:
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
    inter = inter_view(interactive, style_raw) if interactive else None
    if inter and media is not None and media["kind"] == "pending":
        media = None                                   # есть интерактив: ссылка на паспорт вместо ролика не нужна
    illus = []
    for il in inp["illus"].get(node.id, []):
        src = ch_dir / il.file                            # file — путь относительно out/<ch>/, напр. illus/<узел>.chain.svg
        if not src.exists():
            raise FileNotFoundError(f"illustrations.json ссылается на несуществующий файл {src}")
        dst = course / "assets/illus" / Path(il.file).name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        illus.append({"il": il, "src": f"assets/illus/{Path(il.file).name}"})

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
        ("b-interactive", "Интерактив", inter is not None),
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
        "pages_label": page_range(node),
        "text_claims": text_claims,
        "formulas": formulas,
        "tables": tables,
        "deeper": [d for d in lay.deeper if has_text(d)],
        "hypotheses": [h for h in node.data_meaning.hypotheses if has_text(h)],
        "prereqs": [l.target for l in node.links if l.type == "prerequisite"],
        "illus": illus,
        "media": media,
        "inter": inter,
        "guess": guess,
        "tasks": [task_view(t, i + 1) for i, t in enumerate(tasks)],
        "tasks_json": Markup(json.dumps({t.id: {"type": t.type, "answer": t.answer, "tolerance": t.tolerance} for t in tasks},
                                        ensure_ascii=False).replace("</", "<\\/")),
        "paras": paras_view(node, paras) if paras is not None else None,
        "check_items": check_items,
        "route": inp["routes"].get(node.id),
        "pages": node_pages(node),
        "data_json": Markup(json.dumps(data, ensure_ascii=False).replace("</", "<\\/")),
        "terms_json": Markup(json.dumps(terms or {}, ensure_ascii=False).replace("</", "<\\/")),
        "has_terms": bool(terms),
        "hint_page": (text_claims[0] if text_claims else node.claims[0]).page_pdf,
    }


def video_dirs(ch_dir: Path, node_id: str) -> list[tuple[str, str, Path]]:
    """[(формат, video_id, каталог)] роликов узла: videos/<узел>.short, videos/<узел>.long (так пишет П4),
    затем старый videos/<узел>/ как запасной."""
    found = []
    for fmt in ("short", "long"):
        d = ch_dir / "videos" / f"{node_id}.{fmt}"
        if d.is_dir():
            found.append((fmt, f"{node_id}.{fmt}", d))
    legacy = ch_dir / "videos" / node_id
    if legacy.is_dir():
        found.append(("legacy", node_id, legacy))
    return found


def _mp4(vid: str, d: Path) -> Path | None:
    exact = d / f"{vid}.mp4"
    if exact.exists():
        return exact
    others = sorted(d.glob("*.mp4"))
    return others[0] if others else None


def _has_video(ch_dir: Path, node_id: str) -> bool:
    return any(_mp4(vid, d) for _, vid, d in video_dirs(ch_dir, node_id))


_VTT_TIME = re.compile(r"(?:(\d+):)?(\d{1,2}):(\d{2})[.,](\d{1,3})")


def _vtt_seconds(t: str) -> float:
    m = _VTT_TIME.fullmatch(t.strip())
    if not m:
        raise ValueError(f"субтитры: не разобрать время {t!r}")
    h, mi, s, ms = m.groups()
    return int(h or 0) * 3600 + int(mi) * 60 + int(s) + int(ms.ljust(3, "0")) / 1000


def parse_vtt(text: str) -> list[dict]:
    """Реплики WebVTT → [{s, e, t}] (секунды). Субтитры встраиваются в страницу: Chromium не загружает <track src> с file://
    («'file:' URLs are treated as unique security origins»), а курс открывается двойным кликом."""
    cues = []
    for block in re.split(r"\r?\n\r?\n+", text.strip().lstrip(chr(0xFEFF))):
        lines = [l for l in block.splitlines() if l.strip()]
        i = next((k for k, l in enumerate(lines) if "-->" in l), None)
        if i is None:
            continue                                        # заголовок WEBVTT, NOTE, STYLE
        start, _, rest = lines[i].partition("-->")
        end = rest.strip().split()[0] if rest.strip() else ""
        body = " ".join(l.strip() for l in lines[i + 1:])
        if body:
            cues.append({"s": _vtt_seconds(start), "e": _vtt_seconds(end), "t": body})
    return cues


def _player(vid: str, d: Path, mp4: Path, course: Path) -> dict:
    dst = course / "media" / vid
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(mp4, dst / mp4.name)
    vtt = d / f"{vid}.vtt"
    if not vtt.exists():
        others = sorted(d.glob("*.vtt"))
        vtt = others[0] if others else None
    cues = None
    if vtt is not None:
        shutil.copy2(vtt, dst / vtt.name)                  # файл остаётся рядом (скачать), но плеер берёт реплики из страницы: см. parse_vtt
        cues = parse_vtt(vtt.read_text(encoding="utf-8"))
    return {"src": f"media/{vid}/{mp4.name}", "vtt": f"media/{vid}/{vtt.name}" if vtt else None,
            "cues": Markup(json.dumps(cues, ensure_ascii=False).replace("</", "<\\/")) if cues else None, "passport": _passport(vid, d, course)}


def _passport(vid: str, d: Path, course: Path) -> str | None:
    src = d / "passport.json"
    if not src.exists():
        return None
    dst = course / "media" / vid / "passport.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return f"media/{vid}/passport.json"


def video_view(node: Node, inp: dict, course: Path, ch_dir: Path) -> dict | None:
    """Ролик узла. short — основной плеер, long — второй плеер «подробнее»; только long — он основной.
    Каталог без mp4 (одна спецификация) — не ролик: ссылка на паспорт, если маршрутизация просила видео."""
    dirs = video_dirs(ch_dir, node.id)
    players = {}
    for fmt, vid, d in dirs:
        mp4 = _mp4(vid, d)
        if mp4:
            players[fmt] = _player(vid, d, mp4, course)
    if players:
        main_fmt = next(f for f in ("short", "long", "legacy") if f in players)
        main = players[main_fmt]
        more = players["long"] if main_fmt == "short" and "long" in players else None
        return {"kind": "video", **main, "more": more}
    route = inp["routes"].get(node.id)
    wants_video = route is not None and (route.format in VIDEO_FORMATS or route.secondary_format in VIDEO_FORMATS)
    if not wants_video:
        return None
    for _, vid, d in dirs:
        link = _passport(vid, d, course)
        if link:
            return {"kind": "pending", "passport": link}
    return None                                    # нет ни ролика, ни паспорта: блок не показываем


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

    used: list[str] = []                                  # иконки, показанные на странице: их спрайт ставится в конце body

    def icon(name: str) -> Markup:
        if name not in icons:
            raise KeyError(f"нет иконки {name}.svg в pipeline/course/assets/icons")
        used.append(name)
        return Markup(f'<svg class="ic" aria-hidden="true"><use href="#i-{name}"/></svg>')

    def sprite() -> Markup:
        """Один <symbol> на каждую иконку страницы (внешний файл через <use> на file:// не работает)."""
        symbols = []
        for name in sorted(set(used)):
            inner = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", icons[name].strip())
            symbols.append(f'<symbol id="i-{name}" viewBox="0 0 256 256" fill="currentColor">{inner}</symbol>')
        return Markup('<svg class="sprite" aria-hidden="true" width="0" height="0" style="position:absolute">' + "".join(symbols) + "</svg>")

    def brand(name: str) -> Markup:
        """Логотип KERN встроенным SVG: обводка и надпись берут цвет темы (--kern-ink), доступное имя — «KERN»."""
        svg = (HERE / "assets/brand" / f"{name}.svg").read_text(encoding="utf-8")
        return Markup(svg.replace("<svg ", '<svg class="brand-logo" ', 1).replace(' width="372" height="128"', "").replace(' width="164" height="128"', ""))

    env.globals.update(icon=icon, sprite=sprite, brand=brand, by_of=by_of, has_text=has_text)
    env.used_icons = used
    env.filters["plural"] = plural
    return env


def heading_title(ch_dir: Path | None) -> str | None:
    """Первый заголовок главы из units.json (как в книге, напр. «1.2 Дельты»): без #, без английского перевода в скобках."""
    units_path = ch_dir / "units.json" if ch_dir else None
    if units_path is None or not units_path.exists():
        return None
    for u in json.loads(units_path.read_text(encoding="utf-8")).get("units", []):
        if u.get("kind") == "heading":
            text = re.sub(r"\s*\[[^\]]*\]\s*$", "", u["text"].lstrip("#").strip()).strip()
            if text:
                return text
    return None


def book_parts(layer: Layer, ch_dir: Path | None = None) -> tuple[str | None, str | None]:
    """(автор, книга) для карточки курса на главной всех курсов. Поля поставляет П1: ext["core"]["author"] и ["book"] слоя (могут быть
    null) или те же поля в units.json (верхний уровень или ext.core). Нет значения — None; «автор — книга» хаб пишет, только если есть оба."""
    sources = [layer.ext.get("core", {})]
    units_path = ch_dir / "units.json" if ch_dir else None
    if units_path is not None and units_path.exists():
        u = json.loads(units_path.read_text(encoding="utf-8"))
        sources += [u, u.get("ext", {}).get("core", {})]

    def first(key: str) -> str | None:
        return next((s[key].strip() for s in sources if isinstance(s.get(key), str) and s[key].strip()), None)
    return first("author"), first("book")


def chapter_title(layer: Layer, ch_dir: Path | None = None) -> str:
    """Название главы: layer.ext["core"]["title"] (поставляет П1) → первый заголовок главы из units.json → id главы."""
    return layer.ext.get("core", {}).get("title") or heading_title(ch_dir) or layer.chapter


def build(ch: str, out_root: Path = ROOT / "out", node: str | None = None,
          pages_dir: Path = ROOT / "data/pages", styleguide: Path = STYLEGUIDE,
          generate: bool = False, domain: str | None = None, extras: bool = False, hub: bool = False) -> Path:
    """hub=True — рядом будет главная всех курсов (её собирает pipeline.course.hub): в шапке появятся «Курсы / название главы»."""
    ch_dir = out_root / ch
    inp = load_inputs(ch_dir)
    layer: Layer = inp["layer"]
    if layer.chapter != ch:
        raise ValueError(f"{ch_dir / 'layer.json'}: chapter={layer.chapter!r}, а запрошена глава {ch!r}")

    warnings: list[dict] = []

    def note(code: str, message: str, **extra) -> None:
        warnings.append({"code": code, "message": message, **extra})

    def warn(code: str, message: str, **extra) -> None:
        print(f"WARNING: {message}", file=sys.stderr)
        note(code, message, **extra)

    DOWN = "модель недоступна"            # такие записи собираем в одно предупреждение, а не по одному на узел/слот

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

    inter_plan, inter_no_data = inter_mod.plan(layer.nodes, inp["routes"], inp["has_routing"],
                                               lambda nid: _has_video(ch_dir, nid))
    scheme_ids = set(inter_no_data)                  # нужен интерактив, формулы нет: «схема-исследование» из утверждений узла
    inter_wanted = set(inter_plan) | scheme_ids
    for prob in inp["routing_problems"]:
        warn(prob["code"], prob["message"], **{k: v for k, v in prob.items() if k not in ("code", "message")})

    no_part = [n.id for n in layer.nodes if not n.ext.get("core", {}).get("part")]
    if len(no_part) == len(layer.nodes):
        warn("no_parts", 'ни у одного узла нет ext["core"]["part"]: вся глава собрана одной частью «Глава»')
    elif no_part:
        warn("partial_parts", f'у узлов нет ext["core"]["part"], они попали в часть «Глава»: {", ".join(no_part)}',
             nodes=no_part)

    if not layer.ext.get("core", {}).get("title"):
        shown = heading_title(ch_dir)
        warn("no_title", 'нет layer.ext["core"]["title"]: ' + (f"в заголовке курса первый заголовок главы из units.json: «{shown}»"
                                                              if shown else "в заголовке курса показан id главы"))

    course = ch_dir / "course"
    (course / "assets").mkdir(parents=True, exist_ok=True)
    for f in ("course.css", "course.js"):
        shutil.copy2(HERE / "assets" / f, course / "assets" / f)
    shutil.copytree(HERE / "assets/katex", course / "assets/katex", dirs_exist_ok=True)   # формулы без CDN
    shutil.copytree(HERE / "assets/brand", course / "assets/brand", dirs_exist_ok=True)   # логотип KERN и favicon
    style = json.loads(styleguide.read_text(encoding="utf-8"))
    (course / "assets/tokens.css").write_text(tokens_css(style), encoding="utf-8")

    state = None
    if generate:                                   # текст шагов и задания: модель только через pipeline.llm
        from pipeline.course import generate as gen
        state = gen.run(layer, ch_dir, course, node, domain, extras=extras, style=style, interactive_plan=inter_plan, scheme_plan=scheme_ids)
    stored = read_step_text(course / "step_text.json", ch)
    step_text = stored.nodes if stored else {}
    orig = {n.id: n for n in layer.nodes}
    down_steps: list[str] = []
    down_reason = ""
    for nid, f in (stored.failed if stored else {}).items():       # текст не удался: шаг собран из полей слоя
        if nid in orig and f.hash == node_hash(orig[nid]):
            msg = f"текст шага {nid} не прошёл проверки, шаг собран из полей слоя: {f.errors[0]}"
            if f.errors[0].startswith(DOWN):
                note("step_text_fallback", msg, node=nid, errors=f.errors)
                down_steps.append(nid)
                down_reason = down_reason or f.errors[0]
            else:
                warn("step_text_fallback", msg, node=nid, errors=f.errors)
    fresh = {nid: normalize_terms(orig[nid], st.paragraphs) for nid, st in step_text.items()
             if nid in orig and st.hash == node_hash(orig[nid])}     # и текст, созданный до правил терминов, приводится к ним
    for nid, st in step_text.items():
        if nid in fresh:
            for msg in st.warnings:
                warn("term_not_marked", f"шаг {nid}: {msg}", node=nid)
    stale = [nid for nid in step_text if nid in orig and nid not in fresh]
    if stale:
        warn("stale_step_text", f"step_text.json устарел для шагов {', '.join(stale)} (узел изменился после генерации): "
             "они собраны из полей слоя, запусти сборку без --no-llm", nodes=stale)
    tasks, tasks_ext, stale_tasks = load_tasks(ch, course, layer)
    for w in tasks_ext.get("warnings", []) + tasks_ext.get("node_warnings", []):
        warn(w["code"], w["message"], **{k: v for k, v in w.items() if k not in ("code", "message")})
    down_tasks = 0
    for d in tasks_ext.get("dropped", []):
        msg = f"задание {d['slot']} ({d['type']}) шага {d['node']} выброшено: {d['errors'][0]}"
        extra = dict(node=d["node"], slot=d["slot"], type=d["type"], errors=d["errors"])
        if d["errors"][0].startswith(DOWN):
            note("task_dropped", msg, **extra)
            down_tasks += 1
            down_reason = down_reason or d["errors"][0]
        elif any(e.startswith(MISMATCH) for e in d["errors"]):
            warn("task_answer_mismatch", f"задание {d['slot']} ({d['type']}) шага {d['node']} выброшено: помеченный ответ противоречит цитате книги "
                 f"(слепая проверка): {d['errors'][0]}", **extra)
        else:
            warn("task_dropped", msg, **extra)
    inter_store = read_store(course / "interactive.json", ch)
    guess_store = read_store(course / "guesses.json", ch)
    guess_ids = {n.id for n in layer.nodes if guess_mod.wanted(n)}
    down_other = 0
    for nid in inter_no_data:
        if inter_store and (nid in inter_store.nodes or nid in inter_store.failed):
            continue                                  # схему пробовали строить: итог (или причина отказа) ниже
        warn("interactive_no_data", f"шагу {nid} нужен интерактив (маршрутизация дала видео, ролика нет), но в нём нет формулы: интерактив не показан",
             node=nid)
    for store, wanted_ids, what, code in ((inter_store, inter_wanted, "интерактив", "interactive"),
                                          (guess_store, guess_ids, "вопрос «сначала угадай»", "guess")):
        for nid, f in (store.failed if store else {}).items():
            if nid not in wanted_ids or f.hash != node_hash(orig[nid]):
                continue
            msg = f"{what} шага {nid} не показан: {f.errors[0]}"
            if f.errors[0].startswith(DOWN):
                note(f"{code}_failed", msg, node=nid, errors=f.errors)
                down_other += 1
                down_reason = down_reason or f.errors[0]
            else:
                warn("interactive_no_data" if f.errors[0].startswith("модель ответила") else f"{code}_failed", msg, node=nid, errors=f.errors)
    fresh_inter = {nid: e.data["data"] for nid, e in (inter_store.nodes if inter_store else {}).items()
                   if nid in inter_wanted and e.hash == node_hash(orig[nid])}
    fresh_guess = {nid: e.data for nid, e in (guess_store.nodes if guess_store else {}).items()
                   if nid in guess_ids and e.hash == node_hash(orig[nid])}
    for w in inp["illus_warnings"]:                  # предупреждения генератора иллюстраций: в отчёт, в stderr их уже печатал он сам
        note(w["code"], w["message"], **{k: v for k, v in w.items() if k not in ("code", "message")})
    for rec in stale_tasks:
        warn("task_stale", f"задание {rec['task']} шага {rec['node']} выброшено: слой изменился после генерации ({rec['errors'][0]})",
             task=rec["task"], node=rec["node"], errors=rec["errors"])
    if down_steps or down_tasks or down_other:      # одно понятное предупреждение вместо десятков одинаковых
        warn("model_unavailable", f"{down_reason}: без текста модели {len(down_steps)} шагов, не создано {down_tasks} заданий"
             + (f", без интерактива и вопросов {down_other}" if down_other else "") + "; остальное собрано из слоя",
             steps=down_steps, tasks=down_tasks)
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
    glossary = build_glossary(ordered, fresh)
    search = search_index(ordered, fresh, glossary)
    it_list = it_items(ordered)
    # общие данные курса — один файл на курс (assets/course-data.js, подключается <script src>, на file:// работает без fetch),
    # а не копия в каждой странице: страница шага ≈ 60 КБ вместо ≈ 175 КБ
    (course / "assets/course-data.js").write_text("window.COURSE_DATA = " + json.dumps({"meta": meta, "search": search}, ensure_ascii=False) + ";\n", encoding="utf-8")
    minutes_total = sum(s["minutes"] for s in steps)
    author, book = book_parts(layer, ch_dir)
    (course / "course.json").write_text(json.dumps({                    # для главной всех курсов (pipeline.course.hub)
        "ch": ch, "title": chapter_title(layer, ch_dir), "author": author, "book": book, "minutes": minutes_total, "tasks": len(tasks),
        "steps": [{"id": s["id"], "title": s["title"], "minutes": s["minutes"], "tasks": s["tasks"]} for s in steps],
        "task_ids": [t.id for t in tasks], "search": search}, ensure_ascii=False), encoding="utf-8")
    common = {"ch": ch, "chapter_title": chapter_title(layer, ch_dir), "has_errata": bool(errata), "steps": steps,
              "n_tasks": len(tasks), "total_minutes": minutes_total, "hub": hub, "has_glossary": any(g["definition"] for g in glossary),
              "has_it": bool(it_list)}
    titles = {n.id: n.title_novice or n.title for n in ordered}

    def render(name: str, tpl: str, **ctx) -> None:
        env.used_icons.clear()
        html = env.get_template(tpl).render(**common, **ctx)
        (course / name).write_text(html, encoding="utf-8")

    pages_src = pages_dir / ch
    for i, n in enumerate(ordered):
        if node is not None and n.id != node:
            continue
        render(f"step-{n.id}.html", "step.html.j2",
               v=step_view(n, inp, course, pages_src, ch_dir, tasks_by_step.get(n.id, []), fresh.get(n.id),
                              fresh_inter.get(n.id), fresh_guess.get(n.id), style, terms_view(glossary, n.id)),
               idx=i, prev=ordered[i - 1] if i > 0 else None,
               next=ordered[i + 1] if i + 1 < len(ordered) else None, titles=titles, page="step")

    groups = [(s, [task_view(t, i + 1) for i, t in enumerate(tasks_by_step[s["id"]])])
              for s in steps if s["id"] in tasks_by_step]
    render("index.html", "index.html.j2", parts=group_parts(ordered), page="index")
    render("tasks.html", "tasks.html.j2", groups=groups, page="tasks")
    render("progress.html", "progress.html.j2", page="progress")
    render("mistakes.html", "mistakes.html.j2", page="mistakes")
    render("cards.html", "cards.html.j2", nodes=ordered, page="cards")
    sum_extras = {n.id: {"formulas": [c for c in n.claims if c.source_kind == "formula"],
                         "illus": [{"il": il, "src": f"assets/illus/{Path(il.file).name}"}
                               for il in inp["illus"].get(n.id, []) if il.ext.get("kind") != "chain"][:2]}
                  for n in ordered}                      # конспект: формулы и иллюстрации шага (файлы копирует страница шага)
    render("glossary.html", "glossary.html.j2", items=glossary, page="glossary")
    render("summary.html", "summary.html.j2", nodes=ordered, page="summary", extras=sum_extras,
           has_formulas=any(e["formulas"] for e in sum_extras.values()))
    render("it.html", "it.html.j2", items=it_list, page="it")
    render("map.html", "map.html.j2", m=map_view(ordered), nodes=ordered, titles=titles, page="map")
    if errata:
        render("errata.html", "errata.html.j2", errata=errata, page="errata")
    elif (course / "errata.html").exists():
        (course / "errata.html").unlink()

    all_pages = sorted({p for n in ordered for p in node_pages(n)})
    dropped_n = len(tasks_ext.get("dropped", []))
    if not generate:
        model = "не использовалась (--no-llm)"
    elif state.calls == 0:
        model = "не вызывалась (текст и задания взяты из step_text.json и tasks.json)"
    elif state.down:
        model = f"недоступна ({state.down})"
    else:
        model = "доступна"
    line = (f"ИТОГ СБОРКИ: текст модели: {len(fresh)} из {len(ordered)} шагов · заданий: {len(tasks)} (выброшено {dropped_n}) · "
            f"fallback: {len(ordered) - len(fresh)} · модель: {model}")
    print(line, file=sys.stderr)
    summary = {"text_model_steps": len(fresh), "steps": len(ordered), "tasks": len(tasks), "tasks_dropped": dropped_n,
               "fallback_steps": len(ordered) - len(fresh), "model": model, "line": line}
    report = {"chapter": ch, "nodes": len(ordered), "tasks": len(tasks), "step_text_nodes": len(fresh), "interactive_steps": len(fresh_inter),
              "guess_steps": len(fresh_guess), "summary": summary,
              "warnings": warnings, "missing_scans": [p for p in all_pages if not (pages_src / f"p{p}.png").exists()]}
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
    course = build(a.ch, out_root=a.out, node=a.node, pages_dir=a.pages, generate=not a.no_llm, domain=a.domain,
                   extras=not a.no_llm, hub=True)
    from pipeline.course import hub
    print(f"курс: {course / 'index.html'}")
    try:
        print(f"главная всех курсов: {hub.build_hub(a.out)}")        # обновляется в конце каждой сборки
    except FileNotFoundError as e:                                  # собран только тестовый курс: главной нечего показывать
        print(f"WARNING: главная всех курсов не обновлена: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
