"""Общая основа для данных «по узлу», которые модель создаёт, а код проверяет: интерактив и вопрос «сначала угадай».

Хранилище — один JSON на вид данных (out/<ch>/course/interactive.json, guesses.json):
  nodes[id] = {hash, data}    данные узла и хэш узла, по которому они сделаны (узел изменился — данные пересоздаются)
  failed[id] = {hash, errors} узлы, где не вышло; такие узлы пробуются снова при каждой генерации
Отказ модели на узле деградирует только этот узел; «модель недоступна» — по правилам LlmState (3 подряд / авторизация).
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

from contracts.models import Base, Layer
from pipeline.course.steptext import GenerationFailed, LlmError, LlmState, node_hash


class Entry(Base):
    hash: str
    data: dict


class Failure(Base):
    hash: str
    errors: list[str]


class NodeStore(Base):
    chapter: str
    nodes: dict[str, Entry] = {}
    failed: dict[str, Failure] = {}


class NotFeasible(ValueError):
    """Модель сказала, что по данным узла это построить нельзя. Не ошибка: узел просто остаётся без этого элемента."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.errors = [reason]


def read_store(path: Path, ch: str) -> Optional[NodeStore]:
    if not path.exists():
        return None
    st = NodeStore.model_validate_json(path.read_text(encoding="utf-8"))
    if st.chapter != ch:
        raise ValueError(f"{path}: chapter={st.chapter!r}, а запрошена глава {ch!r}")
    return st


def ensure_per_node(layer: Layer, path: Path, wanted: set[str], make: Callable, state: LlmState,
                    only: Optional[str] = None) -> NodeStore:
    """Дописывает хранилище: нужные узлы без данных, изменившиеся и неудавшиеся генерируются через make(node) → dict."""
    old = read_store(path, layer.chapter)
    nodes = {k: v for k, v in (old.nodes if old else {}).items() if k in wanted}
    failed = {k: v for k, v in (old.failed if old else {}).items() if k in wanted}
    for n in layer.nodes:
        if n.id not in wanted or (only is not None and n.id != only):
            continue
        h = node_hash(n)
        if n.id in nodes and nodes[n.id].hash == h:
            continue
        nodes.pop(n.id, None)
        if state.down is not None:
            failed[n.id] = Failure(hash=h, errors=[f"модель недоступна: {state.down}"])
            continue
        try:
            nodes[n.id] = Entry(hash=h, data=make(n))
            failed.pop(n.id, None)
            state.success()
        except (GenerationFailed, NotFeasible) as e:
            failed[n.id] = Failure(hash=h, errors=e.errors)
            state.success()                                  # модель ответила, просто неверно или «нельзя»
        except LlmError as e:
            state.failure(e)
            reason = f"модель недоступна: {state.down}" if state.down else f"отказ модели: {e}"
            failed[n.id] = Failure(hash=h, errors=[reason])
    path.parent.mkdir(parents=True, exist_ok=True)
    store = NodeStore(chapter=layer.chapter, nodes=nodes, failed=failed)
    path.write_text(store.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    return store
