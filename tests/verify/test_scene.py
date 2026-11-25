import json
import sys
import types

import pytest

from contracts.models import ChecklistAnswer, SceneSpec, Script
from pipeline.verify import scene

CLAIMS = {"n.clay#c1"}
SOURCES = ["При глинистости выше 30 % пласт перестает быть коллектором."]


def _script(**kw):
    d = dict(video_id="v1", node_id="n.clay", format="short",
             prediction_question="Что будет с пластом при глинистости выше тридцати процентов?",
             transfer_question="А если глина рассеяна в порах?", data_it_bridge="порог как признак в модели",
             phrases=[
                 dict(id="p1", text="Глина забивает поры.", beat="hook", claim_id="n.clay#c1",
                      on_screen="Глина забивает поры"),
                 dict(id="p2", text="Как думаете, останется ли пласт коллектором?", beat="prediction",
                      claim_id="n.clay#c1", pause_after_s=1.2),
                 dict(id="p3", text="Выше тридцати процентов глины пласт уже не коллектор.", beat="solution",
                      claim_id="n.clay#c1"),
             ])
    d.update(kw)
    return Script.model_validate(d)


def _spec(**kw):
    d = dict(video_id="v1", node_id="n.clay", template="T2", params={}, objects=["пласт"],
             invariants=["глубина растёт вниз"], assumptions=[],
             exaggerations=["поры увеличены в 10 000 раз"],
             shots=[
                 dict(id="s1", phrase_ids=["p1", "p2"], frame_class="B", label="симуляция", shows="поры с глиной",
                      plaque="не в масштабе: поры увеличены в 10 000 раз"),
                 dict(id="s2", phrase_ids=["p3"], frame_class="A", label="реальные данные",
                      shows="пласт 20 м на разрезе 5 км в истинном масштабе"),
             ],
             true_scale_shot_id="s2")
    d.update(kw)
    return SceneSpec.model_validate(d)


def _targets(remarks):
    return {r.target: r for r in remarks}


def test_clean_spec_and_script():
    assert scene.check_scene(_spec(), _script(), CLAIMS, SOURCES, domain="geology") == []


def test_no_true_scale_shot_is_critical():
    by = _targets(scene.check_scene(_spec(true_scale_shot_id=None), _script(), CLAIMS, SOURCES))
    assert by["v1"].severity == "critical" and "истинном масштабе" in by["v1"].problem


def test_true_scale_shot_must_exist():
    by = _targets(scene.check_scene(_spec(true_scale_shot_id="s9"), _script(), CLAIMS, SOURCES))
    assert by["v1"].severity == "critical"


def test_exaggeration_without_number():
    spec = _spec(exaggerations=["поры увеличены"])
    spec.shots[0].plaque = "не в масштабе"
    by = _targets(scene.check_scene(spec, _script(), CLAIMS, SOURCES))
    assert by["v1"].severity == "critical" and "числом" in by["v1"].problem
    assert by["v1.s1"].category == "frame_error"


def test_exaggeration_without_any_plaque():
    spec = _spec()
    spec.shots[0].plaque = None
    by = _targets(scene.check_scene(spec, _script(), CLAIMS, SOURCES))
    assert by["v1"].severity == "critical" and "плашк" in by["v1"].problem


def test_generated_ab_frame_is_critical():
    spec = _spec()
    spec.shots[1].shows = "разрез, сгенерирован нейросетью"
    by = _targets(scene.check_scene(spec, _script(), CLAIMS, SOURCES))
    assert by["v1.s2"].severity == "critical" and by["v1.s2"].category == "frame_error"


def test_data_frame_labelled_scheme():
    spec = _spec()
    spec.shots[1].label = "схема"
    by = _targets(scene.check_scene(spec, _script(), CLAIMS, SOURCES))
    assert by["v1.s2"].category == "frame_error"


def test_shot_unknown_phrase_and_uncovered_phrase():
    spec = _spec()
    spec.shots[1].phrase_ids = ["p9"]
    by = _targets(scene.check_scene(spec, _script(), CLAIMS, SOURCES))
    assert "p9" in by["v1.s2"].problem
    assert "v1.p3" in by and "кадр" in by["v1.p3"].problem


def test_script_phrase_problems():
    s = _script()
    s.phrases[0].claim_id = None                         # нет claim_id
    s.phrases[1].pause_after_s = 0.2                     # нет паузы на предсказание
    s.phrases[2].text = "Выше 45 % глины пласт уже не коллектор."   # цифрами и не из главы
    s.phrases[2].on_screen = "k = φ³ / (1 − φ)² — формула Козени для всех"
    by = _targets(scene.check_scene(_spec(), s, CLAIMS, SOURCES))
    assert "claim_id" in by["v1.p1"].problem
    assert "пауз" in by["v1.p2"].problem
    assert "45" in by["v1.p3"].problem and "цифрами" in by["v1.p3"].problem
    assert "формул" in by["v1.p3"].problem and "8 слов" in by["v1.p3"].problem


def test_missing_questions():
    by = _targets(scene.check_scene(_spec(), _script(transfer_question=" "), CLAIMS, SOURCES))
    assert "перенос" in by["v1"].problem


def test_historical_object_needs_mark():
    spec = _spec(historical_objects=["фотоэлектрический регистратор"])
    by = _targets(scene.check_scene(spec, _script(), CLAIMS, SOURCES))
    assert "исторический прибор" in by["v1"].problem
    s = _script()
    s.phrases[2].on_screen = "исторический прибор; сейчас — цифровая запись"
    assert "v1" not in _targets(scene.check_scene(spec, s, CLAIMS, SOURCES))


def test_misconception_phrase_flagged():
    s = _script()
    s.phrases[0].text = "Нефть лежит подземным озером или в пещерах."
    by = _targets(scene.check_scene(_spec(), s, CLAIMS, SOURCES, domain="geology"))
    assert "misc.oil_lake" in by["v1.p1"].problem


def test_one_remark_per_target():
    s = _script()
    s.phrases[0].claim_id = "n.clay#c7"
    s.phrases[0].text = "Целых 45 % глины."
    remarks = scene.check_scene(_spec(true_scale_shot_id=None, exaggerations=["поры увеличены"]), s,
                                CLAIMS, SOURCES)
    targets = [r.target for r in remarks]
    assert len(targets) == len(set(targets))


def test_physics_llm_uses_checklist_and_returns_answers(monkeypatch):
    calls = {}

    def fake_complete_json(prompt, vars, schema, tier="default", images=None):
        calls.update(prompt=prompt, vars=vars, tier=tier)
        ids = [i["id"] for i in json.loads(vars["checklist"])]
        answers = [dict(item=i, answer="н/п") for i in ids]
        answers[ids.index("pc.depth_down")] = dict(item="pc.depth_down", answer="нет",
                                                   note="в кадре s2 глубина растёт вверх")
        return schema.model_validate(dict(answers=answers))

    monkeypatch.setitem(sys.modules, "pipeline.llm", types.SimpleNamespace(complete_json=fake_complete_json))
    answers, remarks = scene.check_physics(_spec(), _script(), domain="geology")
    assert calls["prompt"] == "verify/scene_physics" and calls["tier"] == "strong"
    assert "v1" in calls["vars"]["scene_spec"]
    assert all(isinstance(a, ChecklistAnswer) for a in answers) and len(answers) == 24
    assert len(remarks) == 1 and remarks[0].category == "frame_error" and "pc.depth_down" in remarks[0].problem


def test_physics_llm_must_answer_every_item(monkeypatch):
    def fake(prompt, vars, schema, tier="default", images=None):
        return schema.model_validate(dict(answers=[dict(item="pc.depth_down", answer="да")]))

    monkeypatch.setitem(sys.modules, "pipeline.llm", types.SimpleNamespace(complete_json=fake))
    with pytest.raises(ValueError):
        scene.check_physics(_spec(), _script(), domain="geology")
