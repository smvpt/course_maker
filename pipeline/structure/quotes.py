"""Проверка «цитата дословно на странице» по правилу организаторов: без учёта пробелов, переносов и регистра.
Разметка md (*, _, `) — не текст: **термин** цитируют без звёздочек. Цитата может переходить на следующую
страницу, но начинаться обязана на найденной.
"""
import re
from typing import Optional

from contracts.models import Unit

MARKUP = re.compile(r"[*_`]")


def norm(s: str) -> str:
    return re.sub(r"\s+", "", MARKUP.sub("", s)).lower()


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
