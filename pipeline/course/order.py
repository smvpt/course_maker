"""Порядок шагов курса: топологическая сортировка по links.prerequisite.

Правило: узел-предпосылка идёт раньше узла, который на него ссылается.
Среди узлов, готовых одновременно, раньше идёт тот, что раньше в layer.json.
Без связей порядок совпадает с порядком узлов в layer.json.

Части главы (node.ext["core"]["part"]) по возможности держатся вместе:
второй проход сортировки предпочитает часть, которая встретилась раньше.
Граф при этом не нарушается никогда.
"""
from __future__ import annotations

import heapq

from contracts.models import Node

NO_PART = "Глава"


def part_of(node: Node) -> str:
    part = node.ext.get("core", {}).get("part")
    return part if part else NO_PART


def _prereqs(nodes: list[Node]) -> dict[str, set[str]]:
    ids = {n.id for n in nodes}
    if len(ids) != len(nodes):
        seen, dup = set(), []
        for n in nodes:
            if n.id in seen:
                dup.append(n.id)
            seen.add(n.id)
        raise ValueError(f"повторяющиеся id узлов в layer.json: {sorted(set(dup))}")
    # ссылки на misc.*, data.* и чужие главы — не узлы этой главы, их пропускаем
    return {n.id: {l.target for l in n.links if l.type == "prerequisite" and l.target in ids and l.target != n.id}
            for n in nodes}


def _kahn(nodes: list[Node], prio: dict[str, tuple]) -> list[Node]:
    pre = _prereqs(nodes)
    by_id = {n.id: n for n in nodes}
    dependents: dict[str, list[str]] = {n.id: [] for n in nodes}
    left = {nid: len(p) for nid, p in pre.items()}
    for nid, p in pre.items():
        for t in p:
            dependents[t].append(nid)
    heap = [(prio[nid], nid) for nid, k in left.items() if k == 0]
    heapq.heapify(heap)
    out: list[Node] = []
    while heap:
        _, nid = heapq.heappop(heap)
        out.append(by_id[nid])
        for d in dependents[nid]:
            left[d] -= 1
            if left[d] == 0:
                heapq.heappush(heap, (prio[d], d))
    if len(out) != len(nodes):
        stuck = sorted(nid for nid, k in left.items() if k > 0)
        raise ValueError(f"цикл в links.prerequisite, узлы: {stuck}")
    return out


def order_nodes(nodes: list[Node]) -> list[Node]:
    index = {n.id: i for i, n in enumerate(nodes)}
    plain = _kahn(nodes, {nid: (i,) for nid, i in index.items()})
    part_rank: dict[str, int] = {}
    for n in plain:
        part_rank.setdefault(part_of(n), len(part_rank))
    return _kahn(nodes, {n.id: (part_rank[part_of(n)], index[n.id]) for n in nodes})


def group_parts(ordered: list[Node]) -> list[tuple[str, list[Node]]]:
    """Подряд идущие узлы одной части — одна группа (часть может повториться, если так велит граф)."""
    groups: list[tuple[str, list[Node]]] = []
    for n in ordered:
        p = part_of(n)
        if groups and groups[-1][0] == p:
            groups[-1][1].append(n)
        else:
            groups.append((p, [n]))
    return groups


def break_cycles(nodes: list[Node]) -> tuple[list[Node], list[dict]]:
    """Мягко рвёт циклы в links.prerequisite, чтобы курс собрался.

    Обход в глубину идёт по порядку узлов в layer.json (и по порядку целей среди опор узла);
    ребро, замыкающее цикл на текущем пути, отбрасывается. Результат зависит только от layer.json.
    Возвращает копии узлов в исходном порядке (входные узлы не меняются) и список разрывов
    [{"cycle": [id, ...], "dropped": [узел, опора]}]. Повтор id — по-прежнему ValueError.
    """
    pre = _prereqs(nodes)
    index = {n.id: i for i, n in enumerate(nodes)}
    state: dict[str, int] = {}   # 1 — на текущем пути, 2 — обработан
    dropped: set[tuple[str, str]] = set()
    breaks: list[dict] = []

    def visit(nid: str, path: list[str]) -> None:
        state[nid] = 1
        path.append(nid)
        for target in sorted(pre[nid], key=index.__getitem__):
            if state.get(target) == 1:
                dropped.add((nid, target))
                breaks.append({"cycle": path[path.index(target):], "dropped": [nid, target]})
            elif target not in state:
                visit(target, path)
        path.pop()
        state[nid] = 2

    for n in nodes:
        if n.id not in state:
            visit(n.id, [])

    if not dropped:
        return list(nodes), []
    fixed = [n.model_copy(update={"links": [l for l in n.links
                                            if not (l.type == "prerequisite" and (n.id, l.target) in dropped)]})
             for n in nodes]
    return fixed, breaks
