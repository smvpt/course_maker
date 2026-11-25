"""Чтение и запись моделей контрактов. Сериализация по CLAUDE.md §1б: by_alias, indent=2, без exclude_none."""
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

M = TypeVar("M", bound=BaseModel)


def load(model: type[M], path: Path) -> M:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"нет входного файла {path} (нужен {model.__name__}) — запусти предыдущий этап")
    return model.model_validate_json(path.read_text(encoding="utf-8"))


def save(obj: BaseModel, path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(obj.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    tmp.replace(path)
    return path
