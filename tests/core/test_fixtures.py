"""fixtures/core/mini_chapter согласован сам с собой — им кормятся тесты П2–П4."""
import json
import re
from pathlib import Path

from contracts import models as m
from pipeline.common import io, paths

MINI = paths.ROOT / "fixtures" / "core" / "mini_chapter"
norm = lambda s: re.sub(r"\s+", "", s).lower()  # noqa: E731


def pages(md: str) -> dict[int, str]:
    parts = re.split(r"<!-- page (\d+) -->", md)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


def test_mini_chapter_consistent():
    units = io.load(m.ChapterUnits, MINI / "units.json")
    layer = io.load(m.Layer, MINI / "layer.json")
    cov = io.load(m.Coverage, MINI / "coverage.json")
    routing = io.load(m.Routing, MINI / "routing.json")
    text = pages((MINI / "chapter.md").read_text(encoding="utf-8"))

    unit_ids = [u.unit_id for u in units.units]
    assert len(set(unit_ids)) == len(unit_ids)
    assert all(re.fullmatch(r"p\d{3}\.\d{2}", u) for u in unit_ids)
    assert units.chapter == layer.chapter == cov.chapter == routing.chapter

    # покрытие: каждая единица ровно одной строкой; без узла — с причиной
    assert [r.unit_id for r in cov.rows] == unit_ids
    for r in cov.rows:
        assert r.node_ids or (r.reason and r.reason.strip().lower() != "непоказуемо")

    node_ids = {n.id for n in layer.nodes}
    misc = {x["id"] for x in json.loads((paths.ORGANIZERS / "04_доменные_заготовки" / "misconceptions.json")
                                        .read_text(encoding="utf-8"))}
    for n in layer.nodes:
        assert set(n.unit_ids) <= set(unit_ids)
        for c in n.claims:
            assert c.id.startswith(n.id + "#c")
            assert norm(c.quote) in norm(text[c.page_pdf]), c.id
        for l in n.links:
            if l.type == "refutes_misconception":
                assert l.target in misc
            elif l.type == "to_data":
                assert l.target.startswith("data.")
            else:
                assert l.target in node_ids
        if n.misconception and n.misconception.ref:
            assert n.misconception.ref in misc
    for r in cov.rows:
        assert set(r.node_ids) <= node_ids

    assert [r.node_id for r in routing.routes] == [n.id for n in layer.nodes]
    assert [n.order for n in layer.nodes] == list(range(1, len(layer.nodes) + 1))
