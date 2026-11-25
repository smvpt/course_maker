"""Проверки кодом сценария и спецификации сцены против узла учебного слоя."""
import json
from pathlib import Path

import pytest

from contracts.models import Layer, SceneSpec, Script
from pipeline.video.spec_check import (check_scene, check_script, estimate_duration, source_language,
                                       sources_table)

FIX = Path(__file__).resolve().parents[2] / "fixtures" / "video" / "spec"
NODE_ID = "video_spec_fixture.mixed_section"
CLAIM = NODE_ID + "#c1"


@pytest.fixture
def layer():
    return Layer.model_validate_json((FIX / "layer.json").read_text(encoding="utf-8"))


@pytest.fixture
def node(layer):
    return next(n for n in layer.nodes if n.id == NODE_ID)


def _script(mutate=None):
    d = json.loads((FIX / "llm_script.json").read_text(encoding="utf-8"))
    if mutate:
        mutate(d)
    return Script(video_id=NODE_ID + ".short", node_id=NODE_ID, format="short", **d)


def _scene(mutate=None):
    d = json.loads((FIX / "llm_scene.json").read_text(encoding="utf-8"))
    if mutate:
        mutate(d)
    return SceneSpec(video_id=NODE_ID + ".short", node_id=NODE_ID, template="T2", **d)


def test_fixture_script_and_scene_pass(node):
    s = _script()
    assert check_script(s, node, "short") == []
    assert check_scene(_scene(), s) == []
    assert 40 <= estimate_duration(s) <= 75


def _set(i, **kw):
    return lambda d: d["phrases"][i].update(**kw)


@pytest.mark.parametrize("mutate,needle", [
    (_set(1, claim_id="video_spec_fixture.other#c1"), "video_spec_fixture.other#c1"),
    (_set(1, claim_id=None), "claim_id"),
    (_set(1, text="Слово " * 19), "18"),
    (_set(1, text="Пласт толщиной 20 метров."), "цифр"),
    (_set(1, on_screen="раз два три четыре пять шесть семь восемь девять"), "8"),
    (_set(1, on_screen="Давление Δp растёт"), "формул"),
    (_set(1, on_screen="p = 20"), "формул"),
    (_set(1, on_screen="Ровно 37 метров"), "37"),
    (_set(0, beat="problem"), "hook"),
    (_set(5, pause_after_s=0.5), "1.0–1.5"),
    (_set(5, text="Хватит ли одного взгляда на кривые."), "«?»"),
    (_set(8, beat="final"), "transfer"),
    (_set(6, beat="decision"), "data"),
    (_set(1, is_analogy=True), "аналог"),
    (_set(3, pause_after_s=-0.1), "пауза"),
    (_set(2, id="p1"), "повторяются"),
    (lambda d: d.update(transfer_question=" "), "transfer_question"),
    (lambda d: d["phrases"].__setitem__(slice(1, 8), d["phrases"][1:2] * 0), "длительность"),
])
def test_script_rules(node, mutate, needle):
    problems = check_script(_script(mutate), node, "short")
    assert any(needle in p for p in problems), problems


def test_on_screen_number_from_claim_id_is_not_a_source(node):
    # единственная «1» в узле рядом с фразой — часть id утверждения «…#c1»; это не числовой факт
    problems = check_script(_script(_set(1, on_screen="Pressure 1 MPa")), node, "short")
    assert any("число 1 " in p for p in problems), problems


def test_on_screen_number_confirmed_by_linked_claim_passes(node):
    claim = node.claims[0].model_copy(update={"text": node.claims[0].text + " Давление 1 MPa."})
    node = node.model_copy(update={"claims": [claim]})
    assert check_script(_script(_set(1, on_screen="Pressure 1 MPa")), node, "short") == []


def test_on_screen_number_from_other_node_fields_is_not_a_source(node):
    # число есть в узле, но не в тексте и цитате связанного утверждения
    layers = node.layers.model_copy(update={"main": node.layers.main.model_copy(update={"text": "Ровно 37 метров."})})
    node = node.model_copy(update={"layers": layers})
    problems = check_script(_script(_set(1, on_screen="Ровно 37 метров")), node, "short")
    assert any("37" in p for p in problems), problems


def test_long_format_needs_longer_script(node):
    s = _script()
    s.format = "long"
    assert any("90–180" in p for p in check_script(s, node, "long"))


def _shot(i, **kw):
    return lambda d: d["shots"][i].update(**kw)


@pytest.mark.parametrize("mutate,needle", [
    (_shot(0, phrase_ids=["p1", "p99"]), "p99"),
    (_shot(1, phrase_ids=["p3"]), "p2"),
    (_shot(1, phrase_ids=["p1", "p2", "p3"]), "p1"),
    (_shot(2, label="реальные данные"), "реальные данные"),
    (_shot(0, frame_class="C", label="схема"), "C"),
    (_shot(0, frame_class="D", label="симуляция"), "D"),
    (_shot(1, plaque="увеличено"), "не в масштабе"),
    (_shot(1, plaque="не в масштабе: толщина увеличена"), "числ"),
    (lambda d: d.update(true_scale_shot_id="s42"), "s42"),
    (lambda d: d.update(true_scale_shot_id="s2"), "плашк"),
    (lambda d: d.update(true_scale_shot_id=None), "true_scale_shot_id"),
    (lambda d: d.update(exaggerations=["пласты толще"]), "числ"),
    (lambda d: d.update(exaggerations=[]), "exaggerations"),
    (lambda d: d.update(invariants=[]), "invariants"),
    (lambda d: d.update(params={}), "params"),
    (lambda d: d["shots"].__setitem__(1, dict(d["shots"][1], id="s1")), "повторяются"),
    (lambda d: d["shots"].reverse(), "порядк"),
])
def test_scene_rules(mutate, needle):
    problems = check_scene(_scene(mutate), _script())
    assert any(needle in p for p in problems), problems


def test_empty_shot_is_rejected_even_as_true_scale_shot():
    def add_empty(d):
        d["shots"].append({"id": "s7", "phrase_ids": [], "frame_class": "B", "label": "схема",
                           "shows": "разрез в истинном масштабе", "plaque": None})
        d["true_scale_shot_id"] = "s7"
    problems = check_scene(_scene(add_empty), _script())
    assert any("s7" in p and "пуст" in p for p in problems), problems


def test_sources_table_is_built_from_node_claims(node):
    rows = sources_table(_script(), node)
    assert len(rows) == 1
    r = rows[0]
    assert r["claim_id"] == CLAIM
    assert r["page_or_dataset"] == "стр. 95"
    assert r["quote"] == node.claims[0].quote
    assert r["kind"] == "observation" and r["by_model"] is False


def test_source_language(layer):
    by_id = {n.id: n for n in layer.nodes}
    assert source_language(by_id[NODE_ID]) == "ru"
    assert source_language(by_id["video_spec_fixture.en_quote"]) == "en"


# ---------------------------------------------------------------- значение параметра и число источника

from pipeline.video.spec_check import param_source_problems  # noqa: E402

CFG_D = {"params": {"hole_diameter_m": {"kind": "physical"}, "scale": {"kind": "physical"}}}


def _with_claim(node, text):
    claim = node.claims[0].model_copy(update={"text": text})
    return node.model_copy(update={"claims": [claim]})


def _spec_with(params, sources):
    s = _scene()
    s.params = params
    s.ext = {"video": {"param_sources": sources}}
    return s


def test_unit_conversion_with_factor(node):
    n = _with_claim(node, "Диаметр ствола 215,9 мм.")
    src = {"claim_ids": [CLAIM], "numbers": ["215,9"], "derivation": "мм → м"}
    assert param_source_problems(_spec_with({"hole_diameter_m": 0.2159}, {"hole_diameter_m": {**src, "factor": 0.001}}),
                                 n, CFG_D) == []
    probs = param_source_problems(_spec_with({"hole_diameter_m": 0.2159}, {"hole_diameter_m": src}), n, CFG_D)
    assert any("factor" in p for p in probs)                       # без множителя 215,9 ≠ 0,2159


def test_derived_from_several_numbers_is_marked_unchecked(node):
    n = _with_claim(node, "Дебит 100, вязкость 2, проницаемость 50.")
    spec = _spec_with({"scale": 0.3}, {"scale": {"claim_ids": [CLAIM], "numbers": ["100", "2", "50"],
                                                 "derivation": "A = q·μ/(4π·k·h)"}})
    assert param_source_problems(spec, n, CFG_D) == []
    assert spec.ext["video"]["param_sources"]["scale"]["arithmetic_checked"] is False
