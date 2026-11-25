"""Задача 2: текст шагов. Валидаторы, цикл с обратной связью, инкрементальная генерация. Без сети: LLM — мок."""
import json
import re
from pathlib import Path

import pytest

from contracts.models import Layer
from pipeline.course import steptext
from pipeline.course.steptext import (Para, StepTextOut, ensure_step_text, generate_node, load_step_text, node_hash,
                                      numbers_in, sentences, validate_node)

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"
TEXT = ROOT / "fixtures/course/mini_step_text.json"
RES = "mini.resistivity_depends_on_fluid"
PORO = "mini.porosity_basics"


def _layer() -> Layer:
    return Layer.model_validate_json(MINI.read_text(encoding="utf-8"))


def _node(layer, nid):
    return next(n for n in layer.nodes if n.id == nid)


def _paras(nid) -> list[Para]:
    raw = json.loads(TEXT.read_text(encoding="utf-8"))["nodes"][nid]["paragraphs"]
    return [Para.model_validate(p) for p in raw]


def test_fixture_text_passes_every_validator_for_every_node():
    layer = _layer()
    for n in layer.nodes:
        assert validate_node(n, _paras(n.id)) == [], n.id


def _errors(nid, mutate) -> list[str]:
    layer = _layer()
    paras = _paras(nid)
    mutate(paras)
    return validate_node(_node(layer, nid), paras)


def test_unknown_or_empty_claim_ids_are_rejected():
    def m(p):
        p[0].claim_ids = ["mini.nope#c1"]
        p[1].claim_ids = []
    e = _errors(RES, m)
    assert any("mini.nope#c1" in x for x in e) and any("пустой claim_ids" in x for x in e)


def test_sentence_over_20_words_is_rejected():
    def m(p):
        p[2].text = " ".join(["слово"] * 21) + "."
    assert any("21 слов" in x for x in _errors(RES, m))


def test_numbers_must_come_from_node():
    def m(p):
        p[3].text = "Сопротивление выше в 7 раз, чем при полном водонасыщении."
    e = _errors(RES, m)
    assert any("['7']" in x and "нет в узле" in x for x in e)


def test_number_normalisation_accepts_comma_and_trailing_zero():
    assert numbers_in("3,50 и 3.5 и 10") == {"3.5", "10"}


def test_missing_block_and_extra_block_are_rejected():
    e = _errors(PORO, lambda p: p.pop(4))                      # нет nuances
    assert any("нет абзацев блока «nuances»" in x for x in e)
    e = _errors("mini.history_note", lambda p: p.append(Para(block="nuances", text="Лишний абзац про нюансы.", claim_ids=["mini.history_note#c1"])))
    assert any("блок «nuances» не нужен" in x for x in e)


def test_term_must_be_marked_exactly_once_and_match_terms_list():
    e = _errors(PORO, lambda p: setattr(p[0], "text", "Пористость — доля пустот в объёме породы. Пустоты лежат между зёрнами."))
    assert any("[[…]] в тексте 0, а в terms 1" in x for x in e)
    e = _errors(PORO, lambda p: (setattr(p[2], "text", "[[Пористость]] — это отношение объёма пор к объёму породы."), setattr(p[2], "terms", ["пористость"])))
    assert any("ровно в одном абзаце (сейчас 2)" in x for x in e)
    e = _errors(PORO, lambda p: setattr(p[0], "terms", ["чужой термин"]))
    assert any("не из terms_introduced" in x for x in e)


def test_main_must_be_two_or_three_sentences():
    e = _errors("mini.history_note", lambda p: setattr(p[0], "text", "Метод предложен в 1920-х годах."))
    assert any("2–3 фразы, сейчас 1" in x for x in e)
    e = _errors("mini.history_note", lambda p: setattr(p[0], "text", "Один. Два. Три. Четыре."))
    assert any("2–3 фразы, сейчас 4" in x for x in e)


def test_course_text_must_be_russian():
    e = _errors(RES, lambda p: setattr(p[1], "text", "This step relies on porosity because current flows through pore water."))
    assert any("на русском" in x for x in e)


def test_hypothesis_and_limit_flags_are_checked():
    e = _errors(RES, lambda p: setattr(p[0], "hypothesis", True))
    assert any("hypothesis=true допустим только в блоке data" in x for x in e)
    e = _errors(RES, lambda p: [setattr(q, "hypothesis", False) for q in p])
    assert any("нужен абзац с hypothesis=true" in x for x in e)
    e = _errors(RES, lambda p: [setattr(q, "limit", False) for q in p])
    assert any("ровно один абзац с limit=true" in x for x in e)


def test_sentences_ignore_markers():
    assert sentences("[[Пористость]] — доля. Это второе.") == ["Пористость — доля.", "Это второе."]


# ---------------------------------------------------------------- цикл с моделью

class FakeLLM:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    def __call__(self, **kw):
        self.calls.append(kw)
        return StepTextOut(paragraphs=self.replies.pop(0))


def test_prompt_variables_match_what_code_passes():
    text = (ROOT / "prompts/course/step_page.md").read_text(encoding="utf-8")
    names = set(re.findall(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}", text))
    assert names == {"node", "viewer", "language", "feedback"}


def test_generate_node_feeds_errors_back_then_succeeds(monkeypatch):
    layer = _layer()
    good = _paras(PORO)
    bad = _paras(PORO)
    bad[2].text = " ".join(["слово"] * 25) + "."
    llm = FakeLLM([bad, good])
    monkeypatch.setattr(steptext, "complete_json", llm)
    out = generate_node(_node(layer, PORO), "ru", "портрет")
    assert out == good and len(llm.calls) == 2
    assert set(llm.calls[0]["vars"]) == {"node", "viewer", "language", "feedback"}
    assert llm.calls[0]["prompt"] == "course/step_page" and llm.calls[0]["schema"] is StepTextOut
    assert "25 слов" in llm.calls[1]["vars"]["feedback"]
    assert '"ext"' not in llm.calls[0]["vars"]["node"]


def test_generate_node_fails_loudly_after_three_bad_attempts(monkeypatch):
    layer = _layer()
    bad = _paras(PORO)
    bad[0].claim_ids = ["zzz#c1"]
    llm = FakeLLM([bad, bad, bad])
    monkeypatch.setattr(steptext, "complete_json", llm)
    with pytest.raises(ValueError, match="zzz#c1"):
        generate_node(_node(layer, PORO), "ru", "портрет")
    assert len(llm.calls) == 3


def test_ensure_step_text_generates_only_new_and_changed_nodes(tmp_path, monkeypatch):
    layer = _layer()
    llm = FakeLLM([_paras(n.id) for n in layer.nodes])
    monkeypatch.setattr(steptext, "complete_json", llm)
    course = tmp_path / "course"
    nodes = ensure_step_text(layer, course)
    assert len(llm.calls) == 4 and set(nodes) == {n.id for n in layer.nodes}
    stored = load_step_text(course / "step_text.json", "mini_test")
    assert stored[PORO].hash == node_hash(_node(layer, PORO))

    llm2 = FakeLLM([])
    monkeypatch.setattr(steptext, "complete_json", llm2)
    ensure_step_text(layer, course)
    assert llm2.calls == []                                   # ничего не изменилось — модель не зовём

    _node(layer, PORO).layers.main.text = "Пористость — доля пустот в объёме породы, а не масса."
    llm3 = FakeLLM([_paras(PORO)])
    monkeypatch.setattr(steptext, "complete_json", llm3)
    ensure_step_text(layer, course)
    assert len(llm3.calls) == 1 and PORO in llm3.calls[0]["vars"]["node"]


def test_ensure_step_text_only_one_node_and_chapter_mismatch(tmp_path, monkeypatch):
    layer = _layer()
    llm = FakeLLM([_paras(PORO)])
    monkeypatch.setattr(steptext, "complete_json", llm)
    nodes = ensure_step_text(layer, tmp_path / "course", only=PORO)
    assert set(nodes) == {PORO} and len(llm.calls) == 1
    other = _layer()
    other.chapter = "another"
    with pytest.raises(ValueError, match="another"):
        ensure_step_text(other, tmp_path / "course", only=PORO)


def test_quote_language_detects_english_and_russian():
    assert steptext.quote_language(_layer()) == "ru"
    layer = _layer()
    for n in layer.nodes:
        for c in n.claims:
            c.quote = "the resistivity of the oil bearing formation exceeds that of the water saturated one"
    assert steptext.quote_language(layer) == "en"


def _walk(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k, v
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)


def test_node_hash_and_prompt_json_do_not_depend_on_none_valued_fields():
    """П1 меняет контракт (поля, которые при None не пишутся): хэш и JSON узла не должны от этого плыть, иначе всё пересоздаётся."""
    node = _node(_layer(), PORO)
    d = steptext.node_dict(node)
    assert not [k for k, v in _walk(d) if v is None] and "ext" not in {k for k, _ in _walk(d)}
    h = node_hash(node)
    import pipeline.course.steptext as st
    orig = st.Node.model_dump
    try:                                              # контракт «вырос»: в дамп попал лишний ключ со значением None
        st.Node.model_dump = lambda self, **kw: {**orig(self, **kw), "new_optional_field": None}
        assert node_hash(node) == h
    finally:
        st.Node.model_dump = orig
    node.layers.main.text += " Ещё одно слово."
    assert node_hash(node) != h                       # а настоящее изменение узла хэш меняет
