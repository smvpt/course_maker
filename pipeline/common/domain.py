"""Доступ к доменному пакету domain/<имя>/ (структура — 05_шаблоны/domain_pack_template.md, пишет П2).

    from pipeline.common import domain
    pack = domain.load("geology")
    pack.misconceptions            # список {"id": "misc.*", "text": ...}
    pack.text("glossary.md")       # любой файл пакета; нет файла — понятная ошибка
"""
import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from pipeline.common import paths


@dataclass(frozen=True)
class Domain:
    name: str
    path: Path

    def has(self, rel: str) -> bool:
        return (self.path / rel).exists()

    def file(self, rel: str) -> Path:
        p = self.path / rel
        if not p.exists():
            raise FileNotFoundError(f"в доменном пакете '{self.name}' нет {rel} ({p})")
        return p

    def text(self, rel: str) -> str:
        return self.file(rel).read_text(encoding="utf-8")

    def json(self, rel: str) -> Any:
        return json.loads(self.text(rel))

    @property
    def misconceptions(self) -> list[dict]:
        return self.json("misconceptions.json")

    @property
    def physics_checklist(self) -> list[dict]:
        return self.json("physics_checklist.json")

    @property
    def styleguide(self) -> dict:
        return self.json("styleguide.json")


@lru_cache(maxsize=None)
def load(name: str) -> Domain:
    path = paths.DOMAIN / name
    if not path.is_dir():
        raise FileNotFoundError(
            f"нет доменного пакета {path}. Собери его: python -m domain.build --domain {name} --ch <id главы>")
    return Domain(name=name, path=path)
