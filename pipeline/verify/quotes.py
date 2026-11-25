"""Сверка цитаты со страницей md главы: found | other_page(N) | not_found."""
import json
from pathlib import Path
from typing import NamedTuple, Optional

from rapidfuzz import fuzz

from pipeline.verify.pages import load_norm_pages, normalize, out_root

ROOT = Path(__file__).resolve().parents[2]

# partial_ratio нормализованных строк. Калибровка на контрольном пакете (60 утверждений):
# все цитаты — 100; формулировки модели вместо цитат — ≤ 87, кроме почти дословных (≥ 90).
THRESHOLD = 88.0


class QuoteResult(NamedTuple):
    status: str            # "found" | "other_page" | "not_found"
    page: Optional[int]    # где найдена (None для not_found)
    score: float           # лучшее сходство 0–100


def _score(q, pages, n):
    """Сходство цитаты со страницей n. Окно — страница + начало следующей (цитата может
    переходить через границу), но совпадение обязано начинаться на странице n."""
    if n not in pages:
        return 0.0
    body = pages[n]
    window = body + " " + pages.get(n + 1, "")[: len(q) + 40]
    al = fuzz.partial_ratio_alignment(q, window)
    if al is None or al.dest_start >= len(body):
        return 0.0
    return al.score


def check_quote_md(md_path, page, quote):
    pages = load_norm_pages(md_path)
    q = normalize(quote)
    if not q:
        raise ValueError(f"пустая цитата после нормализации: {quote!r}")
    s = _score(q, pages, page)
    if s >= THRESHOLD:
        return QuoteResult("found", page, s)
    # ищем по всей главе, при равенстве — ближайшая к заявленной странице
    best_n, best_s = None, s
    for n in sorted(pages, key=lambda x: (abs(x - page), x)):
        if n == page:
            continue
        sn = _score(q, pages, n)
        if sn > best_s:
            best_n, best_s = n, sn
    if best_n is not None and best_s >= THRESHOLD:
        return QuoteResult("other_page", best_n, best_s)
    return QuoteResult("not_found", None, best_s)


def chapter_md(chapter_id):
    """Путь к md главы — из out/<ch>/units.json (поле source, пишет ingest П1)."""
    return md_from_units(out_root() / chapter_id / "units.json")


def md_from_units(units):
    if not units.exists():
        raise FileNotFoundError(f"{units} не найден: сначала ingest этой главы")
    src = Path(json.loads(units.read_text(encoding="utf-8"))["source"])
    if not src.is_absolute():
        src = ROOT / src
    if not src.exists():
        raise FileNotFoundError(f"md главы из {units} не найден: {src}")
    return src


def check_quote(chapter_id, page, quote):
    """Интерфейс для П1: цитата на странице page_pdf главы chapter_id."""
    return check_quote_md(chapter_md(chapter_id), page, quote)
