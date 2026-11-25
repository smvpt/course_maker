"""md главы → единицы (Unit). Чистые функции, без LLM и сети.

Порядок: страницы по меткам <!-- page N --> → опечатки → колонтитулы → блоки → границы главы
→ классификация → склейка абзацев через страницу → описания рисунков конвертера к подписям.
Текст единицы — дословно из md (после листа опечаток); всё, что написала модель, — в ext["core"] с пометкой.
"""
from __future__ import annotations

import csv
import io
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Optional

from contracts.models import ChapterUnits, Unit

PAGE_RE = re.compile(r"<!--\s*page\s+(\d+)\s*-->")
CAPTION_FIG = re.compile(r"^(?:\*\*)?(Рис\.|Рисунок|Fig\.|Figure)\s*(\d+(?:[.\-]\d+)*[а-яa-z]?)", re.I)
CAPTION_TAB = re.compile(r"^(?:\*\*)?(Таблица|Табл\.|Table)\s*(\d+(?:[.\-]\d+)*)", re.I)
TASK_HEAD = re.compile(r"^(Задач[аи]|Упражнени[яе]|Вопросы|Problems?|Exercises?|Questions)\b\.?\s*$", re.I)
TASK_ITEM = re.compile(r"^\s*(\d+)\.\s+\S")
TASK_ONE = re.compile(r"^(Задача|Problem|Exercise)\s*\d+", re.I)
EXAMPLE = re.compile(r"^(?:\*\*)?(Пример|Example)\s*\d*\s*\.?\s*(?:\*\*)?\s*[.:]", re.I)
FOOTNOTE = re.compile(r"^(\$\^\{?\d+\}?\$|[¹²³⁴⁵⁶⁷⁸⁹]|\*\s)")
DESC_HEAD = re.compile(r"^━━━.*━━━$")
FENCE = "----"
EQ_NUM = re.compile(r"\(\s*[IVXLC]*\.?\s*\d+(?:[.,]\d+)*[а-яa-z]?\s*\)")   # номер уравнения: (1.2), (I.7)
END_PUNCT = tuple(".!?:;…»\")]")


# ---------------------------------------------------------------- страницы и колонтитулы

def split_pages(md: str) -> list[tuple[int, str]]:
    parts = PAGE_RE.split(md)
    if len(parts) < 3:
        raise ValueError("в md нет меток <!-- page N --> — номера страниц PDF взять неоткуда")
    pages = [(int(parts[i]), parts[i + 1]) for i in range(1, len(parts), 2)]
    nums = [p for p, _ in pages]
    if len(set(nums)) != len(nums):
        dup = sorted(p for p, c in Counter(nums).items() if c > 1)
        raise ValueError(f"метки страниц повторяются: {dup}")
    return pages


def _edge_lines(text: str, k: int = 3) -> list[str]:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines[:k] + lines[-k:] if len(lines) > 2 * k else lines


def _header_candidate(line: str) -> bool:
    return (len(line) >= 6 and len(line) <= 120 and re.search(r"[A-Za-zА-Яа-яЁё]", line) is not None
            and not line.startswith(("#", "$", "|", "!", "\\", "-", "*", "━"))
            and not CAPTION_FIG.match(line) and not CAPTION_TAB.match(line))


def find_running_headers(pages: list[tuple[int, str]], min_pages: int = 3) -> set[str]:
    """Строки, стоящие у края (3 первых/последних строки) на ≥ min_pages страницах: колонтитулы."""
    c = Counter()
    for _, text in pages:
        c.update({l for l in _edge_lines(text) if _header_candidate(l)})
    return {l for l, n in c.items() if n >= min_pages}


def clean_page(text: str, headers: set[str]) -> tuple[str, Optional[int], list[str]]:
    """Убирает колонтитулы и печатный номер у краёв страницы. Возвращает (текст, печатный номер, убранное)."""
    lines = text.splitlines()
    idx = [i for i, l in enumerate(lines) if l.strip()]
    edge = set(idx[:3] + idx[-3:])
    printed, dropped, keep = None, [], []
    for i, l in enumerate(lines):
        s = l.strip()
        if i in edge and re.fullmatch(r"\d{1,4}", s):
            printed = printed or int(s)
            dropped.append(s)
            continue
        if i in edge and s in headers:
            dropped.append(s)
            continue
        keep.append(l)
    return "\n".join(keep), printed, dropped


# ---------------------------------------------------------------- опечатки

ERRATA_COLS = {
    "page": ("стр", "стр.", "страница", "page", "p", "page_pdf"),
    "wrong": ("было", "неверно", "ошибка", "распознано", "wrong", "was", "error", "ocr"),
    "right": ("стало", "верно", "исправление", "правильно", "right", "correct", "fix", "should_be"),
}


def _col(name: str) -> Optional[str]:
    n = name.strip().strip("*").lower()
    for key, names in ERRATA_COLS.items():
        if n in names:
            return key
    return None


def load_errata(path: Path) -> list[dict]:
    """Лист опечаток: markdown-таблица или CSV/TSV с колонками (стр.|page, было|wrong, стало|right),
    либо строки «[стр. N:] было → стало». Формат не распознан — ошибка."""
    text = Path(path).read_text(encoding="utf-8-sig")
    rows: list[list[str]] = []
    if re.search(r"^\s*\|", text, re.M):
        for l in text.splitlines():
            if l.strip().startswith("|") and not re.fullmatch(r"[\s|:\-]+", l):
                rows.append([c.strip() for c in l.strip().strip("|").split("|")])
    elif re.search(r"(->|→)", text):
        out = []
        for l in text.splitlines():
            m = re.match(r"\s*(?:(?:стр\.?|page|p\.?)\s*(\d+)\s*[:.]\s*)?(.+?)\s*(?:->|→)\s*(.+?)\s*$", l, re.I)
            if m:
                out.append({"page": int(m.group(1)) if m.group(1) else None, "wrong": m.group(2), "right": m.group(3)})
        if not out:
            raise ValueError(f"лист опечаток {path}: нет строк «было → стало»")
        return out
    else:
        dialect = "excel-tab" if "\t" in text.splitlines()[0] else "excel"
        rows = [r for r in csv.reader(io.StringIO(text), dialect=dialect) if any(c.strip() for c in r)]
    if not rows:
        raise ValueError(f"лист опечаток {path} пуст")
    cols = [_col(h) for h in rows[0]]
    if "wrong" not in cols or "right" not in cols:
        raise ValueError(f"лист опечаток {path}: не нашёл колонки «было» и «стало» в заголовке {rows[0]}")
    out = []
    for r in rows[1:]:
        rec = {k: r[i].strip() for i, k in enumerate(cols) if k and i < len(r)}
        if not rec.get("wrong"):
            continue
        page = re.search(r"\d+", rec.get("page") or "")
        out.append({"page": int(page.group()) if page else None, "wrong": rec["wrong"], "right": rec.get("right", "")})
    return out


def apply_errata(pages: list[tuple[int, str]], errata: list[dict]):
    """Возвращает (страницы, применённые по странице, неприменённые)."""
    applied: dict[int, list[dict]] = {}
    unapplied = []
    pages = list(pages)
    for e in errata:
        hit = False
        for i, (p, text) in enumerate(pages):
            if e["page"] is not None and p != e["page"]:
                continue
            if e["wrong"] in text:
                pages[i] = (p, text.replace(e["wrong"], e["right"]))
                applied.setdefault(p, []).append(e)
                hit = True
        if not hit:
            unapplied.append(e)
    for e in unapplied:
        print(f"[ingest] ВНИМАНИЕ: опечатка не найдена в тексте (стр. {e['page']}): «{e['wrong']}»", file=sys.stderr)
    return pages, applied, unapplied


# ---------------------------------------------------------------- блоки

def split_blocks(text: str) -> list[str]:
    """Блоки через пустую строку; $$…$$, \\[…\\], описания рисунков в ----…---- и заголовки — целиком/отдельно."""
    lines = text.splitlines()
    out, cur, i = [], [], 0

    def flush():
        if cur and "\n".join(cur).strip():
            out.append("\n".join(cur).strip())
        cur.clear()

    while i < len(lines):
        l = lines[i]
        s = l.strip()
        nxt = next((x.strip() for x in lines[i + 1:] if x.strip()), "")
        if s == FENCE and DESC_HEAD.match(nxt):
            # описание рисунка от конвертера; закрывающей ---- бывает нет — тогда конец на KEYWORDS,
            # новом описании, заголовке или подписи
            flush()
            j = i + 1
            while lines[j].strip() != nxt:
                j += 1
            j += 1
            end = None
            while j < len(lines):
                t = lines[j].strip()
                if t == FENCE or t.startswith("KEYWORDS"):
                    end = j + 1
                    break
                if DESC_HEAD.match(t) or t.startswith("#") or CAPTION_FIG.match(t) or CAPTION_TAB.match(t):
                    end = j
                    break
                j += 1
            end = len(lines) if end is None else end
            out.append("\n".join(lines[i:end]).strip())
            i = end
            continue
        if s.startswith("$$") and (s.count("$$") % 2 == 1):
            flush()
            j = i + 1
            while j < len(lines) and "$$" not in lines[j]:
                j += 1
            out.append("\n".join(lines[i:j + 1]).strip())
            i = j + 1
            continue
        if s == "\\[":
            flush()
            j = i + 1
            while j < len(lines) and lines[j].strip() != "\\]":
                j += 1
            out.append("\n".join(lines[i:j + 1]).strip())
            i = j + 1
            continue
        if s.startswith("#"):
            flush()
            out.append(s)
            i += 1
            continue
        if not s:
            flush()
        else:
            cur.append(l.rstrip())
        i += 1
    flush()
    return [b for b in out if b.strip() != FENCE]


# ---------------------------------------------------------------- язык

def detect_language(text: str) -> str:
    plain = re.sub(r"\$\$.*?\$\$|\$[^$]*\$|\\\[.*?\\\]", " ", text, flags=re.S)
    cyr = len(re.findall(r"[А-Яа-яЁё]", plain))
    lat = len(re.findall(r"[A-Za-z]", plain))
    if cyr + lat == 0:
        raise ValueError("не удалось определить язык: в тексте нет букв")
    return "ru" if cyr >= lat else "en"


# ---------------------------------------------------------------- сборка

def _strip_heading(b: str) -> str:
    return b.lstrip("#").strip()


def _words(b: str) -> int:
    return len(b.split())


def build_units(md: str, chapter: str, source: str, pages: Optional[set[int]] = None,
                start_heading: Optional[str] = None, end_heading: Optional[str] = None,
                errata: Optional[list[dict]] = None, language: Optional[str] = None,
                domain: str = "geology") -> ChapterUnits:
    all_pages = split_pages(md)
    headers = find_running_headers(all_pages)          # по всей книге: так колонтитулы видны лучше
    sel = [(p, t) for p, t in all_pages if pages is None or p in pages]
    if not sel:
        raise ValueError(f"в md нет страниц из диапазона {sorted(pages)[:3]}…{sorted(pages)[-3:]}")
    sel, applied, unapplied = apply_errata(sel, errata or [])

    printed, dropped = {}, []
    seq: list[tuple[int, str]] = []                    # (страница, блок)
    for p, text in sel:
        clean, num, drop = clean_page(text, headers)
        if num is not None:
            printed[str(p)] = num
        dropped += [{"page": p, "text": d} for d in drop]
        seq += [(p, b) for b in split_blocks(clean)]

    before = after = []
    if start_heading:
        rx = re.compile(start_heading, re.M)
        k = next((i for i, (_, b) in enumerate(seq) if rx.search(b)), None)
        if k is None:
            raise ValueError(f"start_heading «{start_heading}» не найден на страницах главы")
        before, seq = seq[:k], seq[k:]
    if end_heading:
        rx = re.compile(end_heading, re.M)
        k = next((i for i, (_, b) in enumerate(seq) if i > 0 and rx.search(b)), None)
        if k is None:
            raise ValueError(f"end_heading «{end_heading}» не найден на страницах главы")
        seq, after = seq[:k], seq[k:]

    units: list[Unit] = []
    counter: Counter = Counter()
    task_ctx = False
    open_par: Optional[Unit] = None                    # абзац, который может продолжиться на следующей странице
    pending_desc: Optional[tuple[int, str, int]] = None  # (страница, текст, индекс блока)

    def add(p: int, kind: str, text: str, **ext) -> Unit:
        counter[p] += 1
        u = Unit(unit_id=f"p{p:03d}.{counter[p]:02d}", kind=kind, page_pdf=p, text=text)
        if ext:
            u.ext["core"] = ext
        units.append(u)
        return u

    def standalone_desc(dp: int, dtext: str) -> None:
        add(dp, "figure", dtext, figure_description=dtext, figure_description_by_model=True,
            note="описание рисунка, сделанное конвертером md (моделью), подписи рядом нет")

    def is_caption(block: str) -> bool:
        return bool(CAPTION_FIG.match(_strip_heading(block.splitlines()[0].strip())))

    def caption_ahead(idx: int, p: int) -> bool:
        """Подпись рисунка дальше на той же странице — сразу или через обрывки надписей (≤ 3 слов)."""
        for q, x in seq[idx + 1:idx + 7]:
            if q != p:
                return False
            if is_caption(x):
                return True
            if _words(x) > 3 or "\n" in x:
                return False
        return False

    for idx, (p, b) in enumerate(seq):
        first = b.splitlines()[0].strip()
        nxt = seq[idx + 1][1] if idx + 1 < len(seq) else ""

        # описание рисунка от конвертера: к подписи рядом (до или в 2 блоках после), иначе — отдельной единицей
        if first == FENCE and len(b.splitlines()) > 1 and DESC_HEAD.match(b.splitlines()[1].strip()):
            last = units[-1] if units else None
            if pending_desc:
                standalone_desc(*pending_desc[:2])
                pending_desc = None
            if (last and last.kind == "figure" and last.figure_ref and last.page_pdf == p
                    and "figure_description" not in last.ext.get("core", {})):
                last.ext.setdefault("core", {}).update(figure_description=b, figure_description_by_model=True)
            elif caption_ahead(idx, p):
                pending_desc = (p, b, idx)
            else:
                standalone_desc(p, b)
            continue

        # продолжение таблицы на следующей странице
        last = units[-1] if units else None
        if (last is not None and last.kind == "table" and last.page_pdf != p and first.startswith("|")
                and "|" in last.text.splitlines()[-1]):
            last.text = last.text + "\n" + b
            last.ext.setdefault("core", {})["pages"] = sorted({*last.ext.get("core", {}).get("pages", [last.page_pdf]), p})
            continue

        # продолжение абзаца, задачи или примера с прошлой страницы
        if (open_par is not None and p != open_par.page_pdf and re.match(r"^[a-zа-яё]", first)
                and not first.startswith(("$", "#", "|"))):
            if open_par.text.endswith("-") and re.search(r"[A-Za-zА-Яа-яЁё]-$", open_par.text):
                open_par.text = open_par.text[:-1] + b
            else:
                open_par.text = open_par.text + " " + b
            open_par.ext.setdefault("core", {})["pages"] = [open_par.page_pdf, p]
            open_par = None if b.rstrip().endswith(END_PUNCT) else open_par
            continue
        if open_par is not None and p != open_par.page_pdf:
            open_par = None

        if b.startswith("#"):
            h = _strip_heading(b)
            if CAPTION_FIG.match(h):
                m = CAPTION_FIG.match(h)
                u = add(p, "figure", b)
                u.figure_ref = f"{m.group(1)} {m.group(2)}"
                if pending_desc:
                    u.ext.setdefault("core", {}).update(figure_description=pending_desc[1], figure_description_by_model=True)
                    pending_desc = None
            elif CAPTION_TAB.match(h):
                add(p, "table", b)
            elif EXAMPLE.match(h):
                add(p, "worked_example", b)
            else:
                task_ctx = bool(TASK_HEAD.match(h))
                add(p, "heading", b)
            open_par = None
            continue

        if first.startswith("$$") or first.startswith("\\[") or first.startswith("\\begin{"):
            add(p, "formula", b)
            continue
        if first.startswith("|") or CAPTION_TAB.match(first):
            add(p, "table", b)
            continue
        m = CAPTION_FIG.match(first)
        if m or first.startswith("!["):
            u = add(p, "figure", b)
            if m:
                u.figure_ref = f"{m.group(1)} {m.group(2)}"
            if pending_desc:
                u.ext.setdefault("core", {}).update(figure_description=pending_desc[1], figure_description_by_model=True)
                pending_desc = None
            continue
        if TASK_HEAD.match(first) and len(b.splitlines()) == 1:
            task_ctx = True
            add(p, "heading", b)
            continue
        if TASK_ONE.match(first):
            u = add(p, "task", b)
            open_par = None if b.rstrip().endswith(END_PUNCT) else u
            continue
        if task_ctx and TASK_ITEM.match(first):
            items, cur = [], []
            for l in b.splitlines():
                if TASK_ITEM.match(l) and cur:
                    items.append("\n".join(cur))
                    cur = []
                cur.append(l)
            items.append("\n".join(cur))
            for it in items:
                u = add(p, "task", it.strip())
            open_par = None if b.rstrip().endswith(END_PUNCT) else u
            continue
        if EXAMPLE.match(first):
            u = add(p, "worked_example", b)
            open_par = None if b.rstrip().endswith(END_PUNCT) else u
            continue
        if FOOTNOTE.match(first):
            add(p, "paragraph", b, footnote=True)
            continue
        if EQ_NUM.fullmatch(b.strip()) or (_words(b) <= 4 and "=" in b):
            add(p, "formula", b)
            continue
        nxt_first = nxt.splitlines()[0].strip() if nxt else ""
        if (_words(b) <= 3 and not b.rstrip().endswith((":", ".")) and not nxt_first.startswith(("$$", "\\["))
                and "\n" not in b):
            add(p, "figure", b, fragment=True, note="обрывок надписи с рисунка (короткая строка без предложения)")
            continue
        u = add(p, "paragraph", b)
        open_par = None if b.rstrip().endswith(END_PUNCT) else u
    if pending_desc:
        standalone_desc(*pending_desc[:2])

    # пометки опечаток
    for u in units:
        for e in applied.get(u.page_pdf, []):
            if e["right"] and e["right"] in u.text:
                core = u.ext.setdefault("core", {})
                core.setdefault("errata", []).append(e)
                if u.kind == "table":
                    core["table_note"] = "; ".join(f"исправлено по листу опечаток: «{x['wrong']}» → «{x['right']}»"
                                                   for x in core["errata"])

    if not units:
        raise ValueError("в главе не получилось ни одной единицы")
    lang = language or detect_language("\n".join(u.text for u in units))
    cu = ChapterUnits(chapter=chapter, source=source, language=lang, domain=domain,
                      pdf_pages=sorted({p for p, _ in sel}), units=units)
    cu.ext["core"] = {
        "page_printed": printed,
        "dropped_colontitles": dropped,
        "outside_chapter": {"before": [{"page": p, "text": b[:80]} for p, b in before],
                            "after": [{"page": p, "text": b[:80]} for p, b in after]},
        "errata_unapplied": unapplied,
    }
    return cu
