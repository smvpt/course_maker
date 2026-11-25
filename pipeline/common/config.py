"""Конфиг главы и LLM.

Глава задаётся одним из двух способов:
  * id из config/chapters.yaml (наши обучающие и контрольные главы): chapter("kuznetsov_gl10");
  * аргументами, без правки файлов (тестовые главы, жюри): from_args(md=..., pdf=..., pages="a-b", ...).
Все модули получают ChapterSpec через resolve(...) и не знают, откуда он взялся.
"""
import re
from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, ConfigDict, field_validator

from pipeline.common import paths

ID_RE = re.compile(r"^[a-z0-9_.-]+$")

_TRANSLIT = dict(zip(
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
    ["a", "b", "v", "g", "d", "e", "e", "zh", "z", "i", "y", "k", "l", "m", "n", "o", "p", "r", "s", "t",
     "u", "f", "kh", "ts", "ch", "sh", "shch", "", "y", "", "e", "yu", "ya"]))


class ChapterSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    md: Path
    pdf: Optional[Path] = None
    pages: Optional[list[tuple[int, int]]] = None   # None — все метки файла
    start_heading: Optional[str] = None
    end_heading: Optional[str] = None
    language: Optional[Literal["ru", "en"]] = None  # None — определить по тексту
    domain: str = "geology"
    prereading: Optional[Path] = None
    prereq_cards: Optional[Path] = None
    errata: Optional[Path] = None
    author: Optional[str] = None                    # для шапки курса; нет — из имени PDF «Автор - Книга - год»
    book: Optional[str] = None

    @field_validator("id")
    @classmethod
    def _id(cls, v: str) -> str:
        if not ID_RE.match(v):
            raise ValueError(f"id главы '{v}' — только [a-z0-9_.-]")
        return v

    @field_validator("md", "pdf", "prereading", "prereq_cards", "errata")
    @classmethod
    def _abs_existing(cls, v: Optional[Path]) -> Optional[Path]:
        if v is None:
            return None
        p = v if v.is_absolute() else paths.ROOT / v
        if not p.exists():
            raise ValueError(f"файл не найден: {p}")
        return p

    @field_validator("pages")
    @classmethod
    def _pages(cls, v):
        if v is not None:
            for a, b in v:
                if a > b:
                    raise ValueError(f"диапазон страниц {a}-{b}: начало больше конца")
        return v

    def page_set(self) -> Optional[set[int]]:
        if self.pages is None:
            return None
        return {p for a, b in self.pages for p in range(a, b + 1)}


def slug_id(name: str) -> str:
    """id главы из имени файла: транслит, нижний регистр, [a-z0-9_.-]."""
    s = "".join(_TRANSLIT.get(c, c) for c in name.lower())
    s = re.sub(r"[^a-z0-9_.-]+", "_", s).strip("_.-")
    s = re.sub(r"_+", "_", s)
    if not s:
        raise ValueError(f"не удалось получить id главы из имени '{name}' — задай --ch")
    return s


def parse_pages(s: str) -> list[tuple[int, int]]:
    """'90-108' или '9-14,20-30' или '38'."""
    out = []
    for part in s.split(","):
        m = re.fullmatch(r"\s*(\d+)\s*(?:[-–]\s*(\d+))?\s*", part)
        if not m:
            raise ValueError(f"не понял диапазон страниц '{s}': нужно 'a-b' или 'a-b,c-d'")
        a = int(m.group(1))
        out.append((a, int(m.group(2) or a)))
    return out


@lru_cache(maxsize=None)
def chapters() -> dict[str, dict]:
    raw = yaml.safe_load((paths.CONFIG / "chapters.yaml").read_text(encoding="utf-8")) or {}
    return raw.get("chapters") or {}


def spec_path(ch: str) -> Path:
    """Спецификация главы, запущенной через --md: ingest пишет, остальные этапы читают по --ch."""
    return paths.out_dir(ch) / "chapter.json"


def save_spec(spec: ChapterSpec) -> Path:
    p = spec_path(spec.id)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(spec.model_dump_json(indent=2), encoding="utf-8")
    return p


def chapter(ch: str) -> ChapterSpec:
    known = chapters()
    if ch in known:
        return ChapterSpec(id=ch, **known[ch])
    if spec_path(ch).exists():
        return ChapterSpec.model_validate_json(spec_path(ch).read_text(encoding="utf-8"))
    raise KeyError(f"главы '{ch}' нет ни в config/chapters.yaml (есть: {', '.join(known)}), ни в {spec_path(ch)}. "
                   f"Новую главу запускай без конфига: --md <путь к md>")


def from_args(md: str, ch: Optional[str] = None, pdf: Optional[str] = None, pages: Optional[str] = None,
              errata: Optional[str] = None, prereq: Optional[str] = None, domain: Optional[str] = None,
              language: Optional[str] = None, author: Optional[str] = None,
              book: Optional[str] = None) -> ChapterSpec:
    return ChapterSpec(
        id=ch or slug_id(Path(md).stem),
        md=Path(md),
        pdf=Path(pdf) if pdf else None,
        pages=parse_pages(pages) if pages else None,
        errata=Path(errata) if errata else None,
        prereq_cards=Path(prereq) if prereq else None,
        domain=domain or "geology",
        language=language or None,
        author=author or None,
        book=book or None,
    )


def resolve(ch: Optional[str] = None, md: Optional[str] = None, **kw) -> ChapterSpec:
    """--ch без --md — глава из конфига; с --md — из аргументов (тогда --ch лишь задаёт id)."""
    if md:
        return from_args(md=md, ch=ch, **kw)
    if ch:
        return chapter(ch)
    raise ValueError("нужна глава: --ch <id из config/chapters.yaml> или --md <путь к md>")


def add_chapter_args(parser) -> None:
    """Единые аргументы главы для всех точек входа П1."""
    parser.add_argument("--ch", help="id главы из config/chapters.yaml (или id для --md)")
    parser.add_argument("--md", help="путь к md главы — запуск без конфига")
    parser.add_argument("--pdf")
    parser.add_argument("--pages", help="диапазоны страниц PDF: a-b[,c-d]")
    parser.add_argument("--errata")
    parser.add_argument("--prereq")
    parser.add_argument("--domain")
    parser.add_argument("--language", choices=["ru", "en"])
    parser.add_argument("--author", help="автор книги (для шапки курса)")
    parser.add_argument("--book", help="название книги (для шапки курса)")


def spec_from_ns(ns) -> ChapterSpec:
    return resolve(ch=ns.ch, md=ns.md, pdf=ns.pdf, pages=ns.pages, errata=ns.errata,
                   prereq=ns.prereq, domain=ns.domain, language=ns.language,
                   author=ns.author, book=ns.book)


@lru_cache(maxsize=None)
def llm() -> dict:
    return yaml.safe_load((paths.CONFIG / "llm.yaml").read_text(encoding="utf-8"))
