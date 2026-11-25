"""Проверка «цитата дословно на странице» по правилу организаторов: без учёта пробелов, переносов и регистра."""
import re
from typing import Optional


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s).lower()


def find(pages: dict[int, str], quote: str, page: int) -> Optional[int]:
    """Страница, где цитата найдена: сначала указанная, потом соседние (цитата у границы страниц). Иначе None."""
    q = norm(quote)
    if not q:
        return None
    for p in (page, page - 1, page + 1):
        if p in pages and q in norm(pages[p]):
            return p
    return None
