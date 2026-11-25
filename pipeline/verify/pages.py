"""Индекс «страница PDF → текст» по меткам <!-- page N --> и нормализация для сверки."""
import os
import re
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def out_root():
    """Корень out/ (OUT_DIR переопределяет — как pipeline.common.paths.out_root у П1)."""
    return Path(os.environ.get("OUT_DIR") or ROOT / "out")


PAGE_RE = re.compile(r"<!--\s*page\s+(\d+)\s*-->")

# латиница, похожая на кириллицу: OCR путает их внутри русских слов
_LAT2CYR = str.maketrans("aceopxykmtbhABCEHKMOPTXY", "асеорхукмтвнАВСЕНКМОРТХУ")
_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻₀₁₂₃₄₅₆₇₈₉", "0123456789-0123456789")
_CYR = re.compile(r"[а-яёА-ЯЁ]")
_LAT = re.compile(r"[A-Za-z]")
_WORD = re.compile(r"\w+")
_SUPRUN = re.compile(r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+|[₀₁₂₃₄₅₆₇₈₉]+")


def parse_pages(md_text):
    """{номер страницы: сырой текст}. Без меток — ошибка: страницы взять неоткуда."""
    parts = PAGE_RE.split(md_text)
    if len(parts) < 3:
        raise ValueError("в md нет меток <!-- page N -->")
    pages = {}
    for num, body in zip(parts[1::2], parts[2::2]):
        n = int(num)
        pages[n] = pages.get(n, "") + body
    return pages


@lru_cache(maxsize=16)
def _load(path):
    return parse_pages(Path(path).read_text(encoding="utf-8"))


def load_pages(md_path):
    """Сырые страницы md (для чисел — там важны запятые и степени)."""
    return _load(str(Path(md_path).resolve()))


@lru_cache(maxsize=16)
def _load_norm(path):
    return {n: normalize(t) for n, t in _load(path).items()}


def load_norm_pages(md_path):
    """Нормализованные страницы (для цитат)."""
    return _load_norm(str(Path(md_path).resolve()))


def _fix_mixed(m):
    w = m.group(0)
    if _CYR.search(w) and _LAT.search(w):
        return w.translate(_LAT2CYR)
    return w


def normalize(text):
    """Текст для нечёткой сверки: без переносов, LaTeX, пунктуации, регистра, ё и OCR-латиницы."""
    t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)                 # пере-\nнос
    t = _SUPRUN.sub(lambda m: " " + m.group(0).translate(_SUP), t)  # 10⁴ ≡ 10^{4}
    t = re.sub(r"\\tag\{[^}]*\}", " ", t)
    t = re.sub(r"\\[A-Za-z]+", " ", t)                              # \varkappa, \cdot, \mathrm
    t = t.replace("ё", "е").replace("Ё", "Е")
    t = _WORD.sub(_fix_mixed, t)
    t = t.lower()
    t = re.sub(r"[\W_]+", " ", t)                                   # кавычки, тире, $, {}, ^
    return t.strip()
