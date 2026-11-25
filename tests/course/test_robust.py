"""Устойчивость на незнакомой главе: цикл, нет частей, нет сканов, произвольный id, название главы."""
import json
import re
from pathlib import Path

import pytest

from contracts.models import Layer, Link
from pipeline.course.build import build
from pipeline.course.order import break_cycles, order_nodes

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"


def _layer() -> Layer:
    return Layer.model_validate_json(MINI.read_text(encoding="utf-8"))


def _put(tmp_path: Path, layer: Layer) -> Path:
    d = tmp_path / "out" / layer.chapter
    d.mkdir(parents=True)
    (d / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    return tmp_path / "out"


def _cyclic() -> Layer:
    # resistivity → porosity (уже есть), reservoir → resistivity (уже есть), porosity → reservoir замыкает цикл
    layer = _layer()
    poro = next(n for n in layer.nodes if n.id == "mini.porosity_basics")
    poro.links = [Link(type="prerequisite", target="mini.reservoir_decision")]
    return layer


def _report(course: Path) -> dict:
    return json.loads((course / "build_report.json").read_text(encoding="utf-8"))


def test_break_cycles_is_deterministic_and_leaves_input_untouched():
    layer = _cyclic()
    before = [[(l.type, l.target) for l in n.links] for n in layer.nodes]
    nodes1, cycles1 = break_cycles(layer.nodes)
    nodes2, cycles2 = break_cycles(layer.nodes)
    assert cycles1 == cycles2
    assert [[(l.type, l.target) for l in n.links] for n in layer.nodes] == before
    assert len(cycles1) == 1
    # обход идёт по порядку узлов в layer.json: рвётся ребро, замыкающее цикл при обходе с первого узла
    assert cycles1[0]["cycle"] == ["mini.resistivity_depends_on_fluid", "mini.porosity_basics", "mini.reservoir_decision"]
    assert cycles1[0]["dropped"] == ["mini.reservoir_decision", "mini.resistivity_depends_on_fluid"]
    order_nodes(nodes1)  # после разрыва граф ацикличен: строгая сортировка проходит


def test_break_cycles_without_cycles_changes_nothing():
    layer = _layer()
    nodes, cycles = break_cycles(layer.nodes)
    assert cycles == []
    assert [(n.id, [(l.type, l.target) for l in n.links]) for n in nodes] == \
           [(n.id, [(l.type, l.target) for l in n.links]) for n in layer.nodes]


def test_build_survives_cycle_and_reports_it(tmp_path, capsys):
    out = _put(tmp_path, _cyclic())
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    err = capsys.readouterr().err
    assert "WARNING" in err
    for nid in ("mini.resistivity_depends_on_fluid", "mini.porosity_basics", "mini.reservoir_decision"):
        assert nid in err
    rep = _report(course)
    w = [x for x in rep["warnings"] if x["code"] == "prerequisite_cycle"]
    assert len(w) == 1
    assert w[0]["nodes"] == ["mini.resistivity_depends_on_fluid", "mini.porosity_basics", "mini.reservoir_decision"]
    assert (course / "index.html").exists()
    # порядок воспроизводим: вторая сборка даёт тот же индекс
    first = (course / "index.html").read_text(encoding="utf-8")
    build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    assert (course / "index.html").read_text(encoding="utf-8") == first


def test_duplicate_node_id_still_fails_loudly_in_build(tmp_path):
    layer = _layer()
    layer.nodes[1].id = layer.nodes[0].id
    out = _put(tmp_path, layer)
    with pytest.raises(ValueError, match="повторяющиеся"):
        build("mini_test", out_root=out, pages_dir=tmp_path / "pages")


def test_clean_layer_has_no_warnings(tmp_path, capsys):
    out = _put(tmp_path, _layer())
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    assert _report(course)["warnings"] == []
    assert "WARNING" not in capsys.readouterr().err


def test_no_parts_warns(tmp_path, capsys):
    layer = _layer()
    for n in layer.nodes:
        n.ext = {}
    out = _put(tmp_path, layer)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    assert "WARNING" in capsys.readouterr().err
    assert [x["code"] for x in _report(course)["warnings"]] == ["no_parts"]
    # курс при этом собран одной частью
    assert 'class="part-tabs"' not in (course / "index.html").read_text(encoding="utf-8")


def test_some_nodes_without_part_warns_with_ids(tmp_path):
    layer = _layer()
    layer.nodes[0].ext = {}
    out = _put(tmp_path, layer)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    w = [x for x in _report(course)["warnings"] if x["code"] == "partial_parts"]
    assert w and w[0]["nodes"] == ["mini.resistivity_depends_on_fluid"]


def test_build_without_scans_records_missing_pages(tmp_path):
    out = _put(tmp_path, _layer())
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "no_such_dir")
    assert _report(course)["missing_scans"] == [10, 11, 12]
    html = (course / "step-mini.porosity_basics.html").read_text(encoding="utf-8")
    assert not (course / "assets/pages").exists()
    assert "step-data" in html


def test_arbitrary_chapter_id_without_config(tmp_path):
    layer = _layer()
    layer.chapter = "zz_never.seen-9"
    out = _put(tmp_path, layer)
    course = build("zz_never.seen-9", out_root=out, pages_dir=tmp_path / "pages")
    html = (course / "index.html").read_text(encoding="utf-8")
    assert 'data-ch="zz_never.seen-9"' in html


def test_h1_uses_human_title_from_layer(tmp_path):
    layer = _layer()
    layer.ext = {"core": {"title": "Сопротивление и насыщение пласта"}}
    out = _put(tmp_path, layer)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    html = (course / "index.html").read_text(encoding="utf-8")
    assert re.search(r"<h1>\s*Сопротивление и насыщение пласта\s*</h1>", html)
    assert "<title>Сопротивление и насыщение пласта</title>" in html


def test_h1_falls_back_to_chapter_id(tmp_path):
    layer = _layer()
    layer.ext = {}                       # в фикстуре теперь есть название главы; здесь проверяем случай без него
    out = _put(tmp_path, layer)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    html = (course / "index.html").read_text(encoding="utf-8")
    assert re.search(r"<h1>\s*mini_test\s*</h1>", html)


def test_no_title_warns_and_falls_back_to_chapter_id(tmp_path, capsys):
    layer = _layer()
    layer.ext = {}                       # в фикстуре теперь есть название главы; здесь проверяем случай без него
    out = _put(tmp_path, layer)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    assert "WARNING" in capsys.readouterr().err
    w = [x for x in _report(course)["warnings"] if x["code"] == "no_title"]
    assert len(w) == 1 and "title" in w[0]["message"]
    assert re.search(r"<h1>\s*mini_test\s*</h1>", (course / "index.html").read_text(encoding="utf-8"))


def test_title_present_means_no_title_warning(tmp_path, capsys):
    layer = _layer()
    layer.ext = {"core": {"title": "Сопротивление и насыщение пласта"}}
    out = _put(tmp_path, layer)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    assert "no_title" not in [x["code"] for x in _report(course)["warnings"]]
    assert "WARNING" not in capsys.readouterr().err
