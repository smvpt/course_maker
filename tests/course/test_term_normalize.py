"""Правила терминов чинит код, а не отказ шага: лишние выделения [[…]] снимаются, слова остаются."""
import json
from pathlib import Path

from pipeline.course import steptext
from pipeline.course.steptext import (Para, StepTextOut, generate_node, ensure_step_text, normalize_terms, unmarked_terms, validate_node)
from tests.course.test_steptext import PORO, RES, _layer, _node, _paras

ROOT = Path(__file__).resolve().parents[2]


def _para(block, text, terms=()):
    return Para(block=block, text=text, claim_ids=["x#c1"], terms=list(terms))


def _node_with_terms(*terms):
    node = _node(_layer(), RES)
    node.terms_introduced = list(terms)
    return node


def test_term_marked_twice_keeps_first_mark_and_unmarks_the_rest():
    node = _node_with_terms("пласт")
    paras = [_para("how", "Первый [[пласт]] и второй [[пласт]] рядом.", ["пласт", "пласт"]),
             _para("practice", "Ещё один [[пласт]] ниже.", ["пласт"])]
    out = normalize_terms(node, paras)
    assert out[0].text == "Первый [[пласт]] и второй пласт рядом." and out[0].terms == ["пласт"]
    assert out[1].text == "Ещё один пласт ниже." and out[1].terms == []


def test_main_keeps_one_term_others_keep_two_extra_marks_become_plain_words():
    node = _node_with_terms("а", "б", "в", "г")
    out = normalize_terms(node, [_para("main", "Это [[а]] и [[б]] вместе.", ["а", "б"]),
                                 _para("how", "Тут [[в]], [[г]] и ещё раз сразу.", ["в", "г"])])
    assert out[0].text == "Это [[а]] и б вместе." and out[0].terms == ["а"]
    node2 = _node_with_terms("в", "г", "д")
    out = normalize_terms(node2, [_para("how", "Тут [[в]], [[г]] и [[д]] вместе.", ["в", "г", "д"])])
    assert out[0].text == "Тут [[в]], [[г]] и д вместе." and out[0].terms == ["в", "г"]


def test_bold_in_main_is_stripped_and_words_stay():
    node = _node_with_terms()
    out = normalize_terms(node, [_para("main", "Это **важное** слово и __ещё одно__.")])
    assert out[0].text == "Это важное слово и ещё одно."
    out = normalize_terms(node, [_para("how", "Тут **жирный** остаётся.")])
    assert out[0].text == "Тут **жирный** остаётся."          # правило про жирный — только для «Суть»


def test_mark_of_a_term_outside_terms_introduced_is_unmarked():
    node = _node_with_terms("пласт")
    out = normalize_terms(node, [_para("how", "Тут [[пласт]] и [[чужое]].", ["пласт", "чужое"])])
    assert out[0].text == "Тут [[пласт]] и чужое." and out[0].terms == ["пласт"]


def test_normalization_changes_nothing_when_rules_hold_and_does_not_mutate_input():
    node = _node(_layer(), PORO)
    paras = _paras(PORO)
    before = [p.model_dump() for p in paras]
    out = normalize_terms(node, paras)
    assert [p.model_dump() for p in out] == before and [p.model_dump() for p in paras] == before
    bad = [_para("how", "Тут [[пористость]] и [[пористость]].", ["пористость", "пористость"])]
    normalize_terms(node, bad)
    assert bad[0].text.count("[[") == 2


def test_unmarked_term_is_a_warning_not_a_failure():
    node = _node(_layer(), PORO)
    paras = _paras(PORO)
    for p in paras:
        p.text = p.text.replace("[[", "").replace("]]", "")
        p.terms = []
    assert validate_node(node, paras) == []                                   # раньше: «должен быть выделен… (сейчас 0)»
    w = unmarked_terms(node, paras)
    assert len(w) == 1 and "пористость" in w[0] and "не выделен" in w[0]
    assert unmarked_terms(node, _paras(PORO)) == []


def test_term_marked_twice_after_normalization_is_not_a_failure_but_other_rules_still_fail():
    node = _node(_layer(), PORO)
    paras = _paras(PORO)
    paras.append(Para(block="how", text="Тут [[пористость]] ещё раз.", claim_ids=paras[0].claim_ids[:1], terms=["пористость"]))
    assert validate_node(node, normalize_terms(node, paras)) == []
    paras[-1].claim_ids = []
    assert any("пустой claim_ids" in e for e in validate_node(node, normalize_terms(node, paras)))


def test_generate_node_accepts_a_reply_that_only_breaks_term_rules_on_first_attempt(monkeypatch):
    node = _node(_layer(), PORO)
    good = _paras(PORO)
    broken = [p.model_copy(deep=True) for p in good]
    broken[0].text = "[[Пористость]] и ещё [[Пористость]] — доля пустот. " + broken[0].text.replace("[[", "").replace("]]", "")
    broken[0].terms = ["пористость", "пористость"]
    calls = []
    monkeypatch.setattr(steptext, "complete_json", lambda **kw: calls.append(1) or StepTextOut(paragraphs=broken))
    try:
        generate_node(node, "ru", "зритель")
    except steptext.GenerationFailed as e:
        assert all("термин" not in x for x in e.errors), e.errors            # могут остаться другие правила, но не термины
    assert len(calls) <= 3


def test_unmarked_terms_reach_the_step_text_file_and_the_build_report(tmp_path, monkeypatch):
    from pipeline.course.build import build
    layer = _layer()
    nodes = {n.id: _paras(n.id) for n in layer.nodes}
    for p in nodes[PORO]:
        p.text = p.text.replace("[[", "").replace("]]", "")
        p.terms = []
    monkeypatch.setattr(steptext, "complete_json", lambda **kw: StepTextOut(paragraphs=nodes[json.loads(kw["vars"]["node"])["id"]]))
    out = tmp_path / "out" / layer.chapter
    out.mkdir(parents=True)
    (out / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    ensure_step_text(layer, out / "course")
    data = json.loads((out / "course/step_text.json").read_text(encoding="utf-8"))
    assert PORO in data["nodes"] and not data["failed"]
    assert any("не выделен" in w for w in data["nodes"][PORO]["warnings"])
    course = build(layer.chapter, out_root=tmp_path / "out", pages_dir=tmp_path / "p", generate=False)
    rep = json.loads((course / "build_report.json").read_text(encoding="utf-8"))
    assert [w for w in rep["warnings"] if w["code"] == "term_not_marked" and w["node"] == PORO]


def test_capitalised_mark_is_the_same_term_and_terms_list_gets_the_canonical_name():
    node = _node_with_terms("параметр насыщения")
    out = normalize_terms(node, [_para("how", "[[Параметр насыщения]] — отношение сопротивлений. Потом [[параметр насыщения]] снова.", ["x"])])
    assert out[0].text == "[[Параметр насыщения]] — отношение сопротивлений. Потом параметр насыщения снова."
    assert out[0].terms == ["параметр насыщения"]
    assert unmarked_terms(node, out) == []
