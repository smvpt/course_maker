from pathlib import Path

import pytest

from contracts.models import Layer, Link
from pipeline.course.order import group_parts, order_nodes

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"


def _layer() -> Layer:
    return Layer.model_validate_json(MINI.read_text(encoding="utf-8"))


def _strip_links(layer: Layer) -> Layer:
    for n in layer.nodes:
        n.links = []
        n.ext = {}
    return layer


def test_no_links_keeps_layer_order():
    layer = _strip_links(_layer())
    assert [n.id for n in order_nodes(layer.nodes)] == [n.id for n in layer.nodes]


def test_prerequisite_comes_first_and_parts_stay_together():
    ids = [n.id for n in order_nodes(_layer().nodes)]
    # в файле узел про сопротивление стоит первым, но опирается на пористость
    assert ids == [
        "mini.porosity_basics",
        "mini.history_note",
        "mini.resistivity_depends_on_fluid",
        "mini.reservoir_decision",
    ]


def test_parts_are_contiguous_groups():
    groups = group_parts(order_nodes(_layer().nodes))
    assert [g[0] for g in groups] == ["Часть 1. Основы", "Часть 2. Насыщение"]


def test_graph_wins_over_parts():
    layer = _layer()
    # история (часть 1) теперь опирается на решение (часть 2) → часть 1 повторяется
    hist = next(n for n in layer.nodes if n.id == "mini.history_note")
    hist.links = [Link(type="prerequisite", target="mini.reservoir_decision")]
    ids = [n.id for n in order_nodes(layer.nodes)]
    assert ids.index("mini.reservoir_decision") < ids.index("mini.history_note")
    assert [g[0] for g in group_parts(order_nodes(layer.nodes))] == [
        "Часть 1. Основы", "Часть 2. Насыщение", "Часть 1. Основы"]


def test_cycle_fails_loudly():
    layer = _layer()
    poro = next(n for n in layer.nodes if n.id == "mini.porosity_basics")
    poro.links = [Link(type="prerequisite", target="mini.reservoir_decision")]
    with pytest.raises(ValueError, match="цикл"):
        order_nodes(layer.nodes)


def test_duplicate_ids_fail_loudly():
    layer = _layer()
    layer.nodes[1].id = layer.nodes[0].id
    with pytest.raises(ValueError, match="повторяющиеся"):
        order_nodes(layer.nodes)


def test_non_node_targets_ignored():
    # misc.* и data.* в links не узлы — не должны ломать сортировку
    layer = _layer()
    assert any(l.target.startswith("misc.") for n in layer.nodes for l in n.links)
    assert len(order_nodes(layer.nodes)) == len(layer.nodes)
