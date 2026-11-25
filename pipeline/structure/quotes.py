"""Проверка «цитата дословно на странице» по правилу организаторов: без учёта пробелов, переносов и регистра.
Разметка md (*, _, `) — не текст: **термин** цитируют без звёздочек; «пере-» + новая строка + «нос» — перенос.
Цитата может переходить на следующую страницу, но начинаться обязана на найденной.
recover() достаёт из md дословный отрывок, который модель передала неточно (формула словами и т. п.).
"""
import re
from typing import Optional

from contracts.models import Unit

MARKUP = re.compile(r"[*_`]")
HYPHEN_BREAK = re.compile(r"(?<=\w)-[ \t]*\n\s*(?=\w)")


def norm(s: str) -> str:
    return re.sub(r"\s+", "", MARKUP.sub("", HYPHEN_BREAK.sub("", s))).lower()


def _norm_map(raw: str) -> tuple[str, list[int]]:
    """norm(raw) и для каждого его символа — индекс в raw."""
    keep = [True] * len(raw)
    for m in HYPHEN_BREAK.finditer(raw):
        for i in range(m.start(), m.end()):
            keep[i] = False
    out, idx = [], []
    for i, ch in enumerate(raw):
        if keep[i] and not ch.isspace() and ch not in "*_`":
            out.append(ch.lower())
            idx.append(i)
    return "".join(out), idx


def recover(raw: str, quote: str) -> Optional[str]:
    """Дословный отрывок raw от начала до конца цитаты: якоря — первые и последние слова (3, 2 или 1), дословно.
    Длина — от половины до двух длин цитаты. Похожесть отрывка на цитату проверяет вызывающий."""
    words = quote.split()
    qlen = len(norm(quote))
    text, idx = _norm_map(raw)
    for k in (3, 2, 1):
        if len(words) < 2 * k + 1:
            continue
        head, tail = norm(" ".join(words[:k])), norm(" ".join(words[-k:]))
        start = text.find(head)
        while start >= 0:
            end = text.find(tail, start + len(head))
            if end >= 0 and qlen / 2 <= end + len(tail) - start <= qlen * 2:
                return raw[idx[start]: idx[end + len(tail) - 1] + 1].strip()
            start = text.find(head, start + 1)
    return None


def unit_pages(units: list[Unit]) -> dict[int, str]:
    """Текст страниц по единицам ingest: колонтитулы убраны, разорванные страницей абзацы склеены."""
    pages: dict[int, str] = {}
    for u in units:
        pages[u.page_pdf] = pages.get(u.page_pdf, "") + "\n" + u.text
    return pages


def find(pages: dict[int, str], quote: str, page: int) -> Optional[int]:
    """Страница, где цитата начинается: сначала указанная, потом соседние. Иначе None."""
    q = norm(quote)
    if not q:
        return None
    for p in (page, page - 1, page + 1):
        if p not in pages:
            continue
        body = norm(pages[p])
        i = (body + norm(pages.get(p + 1, ""))).find(q)
        if 0 <= i < len(body):
            return p
    return None
