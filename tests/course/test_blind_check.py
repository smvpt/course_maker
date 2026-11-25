"""Слепая проверка ответа: модель видит только цитаты из claim_ids, условие и варианты без отметки верного."""
import json
import re
from pathlib import Path

import pytest

from pipeline.course import tasks as T
from pipeline.course.steptext import LlmError
from tests.course.test_tasks_gen import FakeLLM, RES, _fake_task, _layer, _node

pytestmark = pytest.mark.blind
ROOT = Path(__file__).resolve().parents[2]
PLAN = [{"type": t, "kind": k} for t, k in (("single", "recall"), ("multiple", "understanding"), ("order", "transfer"), ("gap", "recall"))]


def _built():
    node = _node(_layer())
    llm = [_fake_task(node, s) for s in PLAN]
    return node, [T.build_task(node, t, f"{node.id}.t{i + 1}") for i, t in enumerate(llm)]


def _phrase(node, task):
    q = next(c for c in node.claims if c.id == task.claim_ids[0]).quote
    return " ".join(q.split()[:4])


def _agree(node, built, wrong=()):
    """Мок слепой модели: отвечает верно (или неверно для номеров из wrong), опираясь на фразу из цитаты."""
    def pick(task, i):
        ans = task.answer if isinstance(task.answer, list) else [task.answer]
        if i in wrong:
            ids = [o.id for o in task.options]
            ans = [next(x for x in ids if x not in ans)] if task.type in ("single", "multiple") else list(reversed(ans))
        return T.AnswerPick(n=i, answer=[str(a) for a in ans], claim_id=task.claim_ids[0], evidence=_phrase(node, task))
    return lambda **kw: T.AnswerPicks(picks=[pick(t, i) for i, t in enumerate(built, 1)])


def test_agreement_on_all_four_types_gives_no_problems(monkeypatch):
    node, built = _built()
    monkeypatch.setattr(T, "complete_json", _agree(node, built))
    assert T.blind_check(node, built) == {}


def test_model_sees_only_cited_claims_and_no_marks(monkeypatch):
    node, built = _built()
    seen = {}
    inner = _agree(node, built)
    monkeypatch.setattr(T, "complete_json", lambda **kw: seen.update(kw) or inner(**kw))
    T.blind_check(node, built)
    assert seen["prompt"] == "course/answer_check"
    cited = {cid for t in built for cid in t.claim_ids}
    claims = json.loads(seen["vars"]["claims"])
    assert set(claims) == cited and all(claims[c] == next(x.quote for x in node.claims if x.id == c) for c in cited)
    blob = seen["vars"]["items"]
    assert '"correct"' not in blob and "explanation" not in blob and "misconception" not in blob
    right_texts = [o.text for t in built if t.type == "single" for o in t.options if o.id == t.answer]
    assert right_texts and all(t in blob for t in right_texts)       # варианты показаны, но без отметки


def test_marked_answer_contradicting_the_quote_is_reported(monkeypatch):
    node, built = _built()
    monkeypatch.setattr(T, "complete_json", _agree(node, built, wrong={1, 3}))
    out = T.blind_check(node, built)
    assert set(out) == {built[0].id, built[2].id}
    assert "не совпал" in out[built[0].id][0] and built[0].claim_ids[0] in out[built[0].id][0]


def test_evidence_must_be_verbatim_in_the_cited_claim(monkeypatch):
    node, built = _built()
    good = _agree(node, built)

    def bad(**kw):
        p = good(**kw)
        p.picks[0].evidence = "эту фразу автор нигде не писал"
        p.picks[1].claim_id = "mini.resistivity_depends_on_fluid#c99"
        return p
    monkeypatch.setattr(T, "complete_json", bad)
    out = T.blind_check(node, built)
    assert set(out) == {built[0].id, built[1].id}
    assert "дословно" in out[built[0].id][0] and "claim_ids задания" in out[built[1].id][0]


def test_evidence_matching_ignores_spaces_case_and_line_breaks(monkeypatch):
    node, built = _built()
    good = _agree(node, built)

    def spaced(**kw):
        p = good(**kw)
        for pk in p.picks:
            pk.evidence = pk.evidence.upper().replace(" ", "\n  ")
        return p
    monkeypatch.setattr(T, "complete_json", spaced)
    assert T.blind_check(node, built) == {}


def test_missing_pick_is_a_problem_and_calc_is_not_checked(monkeypatch):
    node, built = _built()
    calc = T.build_task(node, _fake_task(node, {"type": "calc", "kind": "data"}), f"{node.id}.t9")
    inner = _agree(node, built)
    monkeypatch.setattr(T, "complete_json", lambda **kw: T.AnswerPicks(picks=inner(**kw).picks[:-1]))
    out = T.blind_check(node, built + [calc])
    assert set(out) == {built[-1].id}                                 # у calc проверять нечего: ответ считает код


def test_contradicting_task_never_reaches_the_course_and_good_ones_stay(monkeypatch):
    layer = _layer()
    node = _node(layer)
    fake = FakeLLM(layer)
    monkeypatch.setattr(T, "complete_json", fake)
    calls = []

    def blind(node_, built):
        calls.append([t.id for t in built])
        return {built[0].id: ["ответ слепой проверки не совпал с помеченным"]} if built[0].id.endswith(".t1") else {}
    monkeypatch.setattr(T, "blind_check", blind)
    tasks, dropped, _, failure = T.generate_node_tasks(node, [dict(s) for s in PLAN], [], "ru", "новичок")
    assert failure is None and [t.id for t in tasks] == [f"{node.id}.t{i}" for i in (2, 3, 4)]
    assert [(d["slot"], d["type"]) for d in dropped] == [(1, "single")] and "не совпал" in dropped[0]["errors"][0]
    assert len(fake.calls) == 3 and len(calls) == 3                   # три попытки, слот 1 каждый раз возвращается в генерацию
    assert "не совпал" in fake.calls[1]["vars"]["feedback"]


def test_slot_fixed_on_second_attempt_is_accepted(monkeypatch):
    layer = _layer()
    node = _node(layer)
    monkeypatch.setattr(T, "complete_json", FakeLLM(layer))
    seen = []

    def blind(node_, built):
        seen.append(len(built))
        return {built[0].id: ["не совпал"]} if len(seen) == 1 else {}
    monkeypatch.setattr(T, "blind_check", blind)
    tasks, dropped, _, _ = T.generate_node_tasks(node, [dict(s) for s in PLAN], [], "ru", "новичок")
    assert len(tasks) == 4 and dropped == [] and seen == [4, 1]       # вторая проверка — только заново сгенерированный слот


def test_model_failure_in_check_drops_unverified_tasks_and_reports_failure(monkeypatch):
    layer = _layer()
    node = _node(layer)
    monkeypatch.setattr(T, "complete_json", FakeLLM(layer))

    def down(node_, built):
        raise LlmError("провайдер недоступен")
    monkeypatch.setattr(T, "blind_check", down)
    tasks, dropped, _, failure = T.generate_node_tasks(node, [dict(s) for s in PLAN], [], "ru", "новичок")
    assert tasks == [] and len(dropped) == 4 and isinstance(failure, LlmError)
    assert "проверка ответа" in dropped[0]["errors"][0]


def test_prompt_variables_match_what_code_passes():
    text = (ROOT / "prompts/course/answer_check.md").read_text(encoding="utf-8")
    assert set(re.findall(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}", text)) == {"claims", "items", "language"}


def test_course_report_names_the_mismatch_code(tmp_path, monkeypatch):
    from pipeline.course.build import build
    layer = _layer()
    out = tmp_path / "out" / layer.chapter
    out.mkdir(parents=True)
    (out / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    monkeypatch.setattr(T, "complete_json", FakeLLM(layer))
    monkeypatch.setattr(T, "blind_check", lambda node_, built: {built[0].id: ["ответ слепой проверки не совпал с помеченным: …"]}
                        if built[0].id.endswith(".t1") else {})
    from pipeline.course import generate
    from tests.course.test_gen_build import _fake_text_llm
    _fake_text_llm(monkeypatch)
    monkeypatch.setattr(generate, "load_misconceptions", lambda domain: [])
    course = build(layer.chapter, out_root=tmp_path / "out", pages_dir=tmp_path / "p", generate=True, extras=False, domain="geology")
    rep = json.loads((course / "build_report.json").read_text(encoding="utf-8"))
    assert [w for w in rep["warnings"] if w["code"] == "task_answer_mismatch"], [w["code"] for w in rep["warnings"]]


# ---------------------------------------------------------------- «Суть» для новичка: термины

def test_main_block_has_at_most_one_marked_term_and_no_bold():
    from tests.course.test_steptext import _errors
    errs = _errors(RES, lambda ps: setattr(ps[0], "text", "Это [[первый]] и [[второй]] термин. Вторая фраза."))
    assert any("«Суть»" in e and "не больше одного" in e for e in errs)
    errs = _errors(RES, lambda ps: setattr(ps[0], "text", "Это **важно** для новичка. Вторая фраза."))
    assert any("жирн" in e for e in errs)


def test_other_blocks_have_at_most_two_marked_terms_per_paragraph():
    from tests.course.test_steptext import _errors
    errs = _errors(RES, lambda ps: setattr(ps[2], "text", "Тут [[один]], [[два]] и [[три]] термина."))
    assert any("не больше двух" in e for e in errs)
    errs = _errors(RES, lambda ps: setattr(ps[2], "text", "Тут [[один]] и [[два]] термина."))
    assert not any("не больше двух" in e for e in errs)


def test_step_prompt_states_the_rules():
    t = (ROOT / "prompts/course/step_page.md").read_text(encoding="utf-8")
    assert "не больше одного" in t and "в скобках" in t and "жирн" in t
