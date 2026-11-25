"""Задача 3: генерация заданий. Без сети: LLM — мок, который строит задания по плану из текста узла."""
import json
import re
from pathlib import Path

import jsonschema
import pytest

from contracts.models import Layer, Tasks
from pipeline.course import tasks as T
from pipeline.course.steptext import node_hash, numbers_in, source_text

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"
SCHEMA = ROOT / "data/organizers/01_схемы/task.schema.json"
RES = "mini.resistivity_depends_on_fluid"
REF = "misc.high_res_is_oil"
MISC = [{"id": REF, "text": "Высокое сопротивление всегда означает нефть."}, {"id": "misc.other", "text": "Другое заблуждение."}]


def _layer() -> Layer:
    return Layer.model_validate_json(MINI.read_text(encoding="utf-8"))


def _node(layer, nid=RES):
    return next(n for n in layer.nodes if n.id == nid)


def _fake_task(node, slot, with_ref=True) -> T.LlmTask:
    """Правдоподобное задание нужного типа, собранное из текста узла."""
    claim = next(c for c in node.claims if c.source_kind == "text")
    base = dict(type=slot["type"], kind=slot["kind"], claim_ids=[claim.id], explanation="Так сказано в тексте шага.")
    ref = node.misconception.ref if node.misconception and with_ref else None
    if slot["type"] == "single":
        return T.LlmTask(**base, prompt="Что утверждает автор в этом шаге?", options=[
            T.LlmOption(text=claim.text, correct=True),
            T.LlmOption(text="Автор считает это утверждение неверным.", misconception=ref),
            T.LlmOption(text="Автор об этом вообще не пишет.")])
    if slot["type"] == "multiple":
        return T.LlmTask(**base, prompt="Что из перечисленного говорит автор?", options=[
            T.LlmOption(text=claim.text, correct=True),
            T.LlmOption(text="Автор подтверждает это примером.", correct=True),
            T.LlmOption(text="Автор опровергает это на практике.", misconception=ref),
            T.LlmOption(text="Автор оставляет вопрос открытым.")])
    if slot["type"] == "order":
        return T.LlmTask(**base, prompt="Расставь шаги по порядку.", options=[
            T.LlmOption(text="Сначала читаем условие."), T.LlmOption(text="Потом выбираем метод."), T.LlmOption(text="В конце делаем вывод.")])
    if slot["type"] == "gap":
        word = next(w for w in re.findall(r"[а-яё]{6,}", claim.quote.lower()))
        return T.LlmTask(**base, prompt="В тексте шага встречается слово {{1}}.", gap_answers=[word])
    return T.LlmTask(**base, prompt="Сопротивление пласта 40 Ом·м, водоносного — 5 Ом·м. Чему равен параметр насыщения?",
                     calc=T.LlmCalc(variables={"rho_oil": 40, "rho_water": 5}, expression="rho_oil / rho_water", unit="безразмерная величина"))


class FakeLLM:
    def __init__(self, layer, with_ref=True, tamper=None):
        self.by_id = {n.id: n for n in layer.nodes}
        self.calls = []
        self.with_ref = with_ref
        self.tamper = tamper

    def __call__(self, **kw):
        self.calls.append(kw)
        node_id = json.loads(kw["vars"]["node"])["id"]
        planned = json.loads(kw["vars"]["requested"])
        tasks = [_fake_task(self.by_id[node_id], s, self.with_ref) for s in planned]
        if self.tamper:
            tasks = self.tamper(len(self.calls), tasks)
        return T.LlmTasks(tasks=tasks)


@pytest.fixture
def llm(monkeypatch):
    def install(fake):
        monkeypatch.setattr(T, "complete_json", fake)
        return fake
    return install


# ---------------------------------------------------------------- план

def test_plan_covers_chapter_requirements_and_is_deterministic():
    layer = _layer()
    p1, p2 = T.plan(layer.nodes), T.plan(layer.nodes)
    assert p1 == p2
    slots = [s for ss in p1.values() for s in ss]
    assert len(slots) >= 15
    assert {s["type"] for s in slots} == set(T.ROTATION)
    assert any(s["kind"] == "data" for s in slots)
    calc_nodes = {nid for nid, ss in p1.items() for s in ss if s["type"] == "calc"}
    assert calc_nodes == {RES}                                  # расчёт только там, где есть формула и числа
    assert any(s["kind"] == "data" for s in p1[RES])            # у узла с решением на данных своё задание «на данных»


def test_plan_fails_loudly_for_chapter_too_small():
    layer = _layer()
    with pytest.raises(ValueError, match="нужно ≥15"):
        T.plan(layer.nodes[:1])


def test_plan_without_numbers_has_no_calc_and_still_has_data():
    layer = _layer()
    node = _node(layer)
    node.claims = [c for c in node.claims if c.source_kind == "text"]
    node.worked_examples = []
    slots = [s for ss in T.plan(layer.nodes).values() for s in ss]
    assert "calc" not in {s["type"] for s in slots} and any(s["kind"] == "data" for s in slots)


# ---------------------------------------------------------------- расчёт кодом

def test_safe_eval_computes_and_rejects_anything_else():
    nums = {"40", "5"}
    assert T.safe_eval("a / b", {"a": 40, "b": 5}, nums) == 8
    assert T.safe_eval("sqrt(a) * 2", {"a": 40}, nums) == pytest.approx(12.649110640673518)
    for bad in ("__import__('os').system('x')", "a.real", "a / c", "[a][0]", "a if 1 else 2", "open('f')", "lambda: 1"):
        with pytest.raises(ValueError):
            T.safe_eval(bad, {"a": 40, "b": 5}, nums)
    with pytest.raises(ValueError, match="не используются"):
        T.safe_eval("a * 2", {"a": 40, "b": 5}, nums)
    with pytest.raises(ValueError, match="нет в узле"):
        T.safe_eval("a * 37", {"a": 40}, nums)
    with pytest.raises(ValueError, match="не вычисляется"):
        T.safe_eval("a / (b - b)", {"a": 40, "b": 5}, nums)


def test_calc_answer_comes_from_code_not_from_model():
    layer = _layer()
    node = _node(layer)
    task = T.build_task(node, _fake_task(node, {"type": "calc", "kind": "transfer"}), "t")
    assert task.answer == 8.0 and task.tolerance == 0.08 and task.unit == "безразмерная величина"
    assert "answer" not in T.LlmCalc.model_fields and "answer" not in T.LlmTask.model_fields


# ---------------------------------------------------------------- отбраковка заданий

def _errs(mutate, slot=None, nid=RES) -> list[str]:
    layer = _layer()
    node = _node(layer, nid)
    slot = slot or {"type": "single", "kind": "understanding"}
    t = _fake_task(node, slot)
    mutate(t)
    return T.validate_task(node, t, slot, {m["id"] for m in MISC}, "задание 1")


def test_valid_fake_tasks_pass_validation_for_every_type():
    layer = _layer()
    node = _node(layer)
    for ty in T.ROTATION:
        slot = {"type": ty, "kind": "recall"}
        assert T.validate_task(node, _fake_task(node, slot), slot, {m["id"] for m in MISC}, "x") == [], ty


def test_wrong_type_unknown_claim_and_unknown_misconception_are_rejected():
    e = _errs(lambda t: setattr(t, "type", "multiple"))
    assert any("нужен type=single" in x for x in e)
    e = _errs(lambda t: setattr(t, "claim_ids", ["mini.nope#c1"]))
    assert any("mini.nope#c1" in x for x in e)
    e = _errs(lambda t: setattr(t.options[1], "misconception", "misc.invented"))
    assert any("misc.invented" in x for x in e)
    e = _errs(lambda t: setattr(t.options[0], "misconception", REF))
    assert any("только у неверных" in x for x in e)


def test_single_needs_exactly_one_correct_and_explanation_one_sentence():
    e = _errs(lambda t: setattr(t.options[1], "correct", True))
    assert any("ровно один верный" in x for x in e)
    e = _errs(lambda t: setattr(t, "explanation", "Это так. И вот почему."))
    assert any("одной фразой" in x for x in e)


def test_gap_answer_must_be_in_node_text():
    slot = {"type": "gap", "kind": "recall"}
    e = _errs(lambda t: setattr(t, "gap_answers", ["космонавтика"]), slot)
    assert any("не найдено в тексте узла" in x for x in e)
    e = _errs(lambda t: setattr(t, "prompt", "Слово {{2}} пропущено."), slot)
    assert any("пропуски" in x for x in e)


def test_calc_numbers_must_be_in_node_and_in_prompt():
    slot = {"type": "calc", "kind": "transfer"}
    e = _errs(lambda t: setattr(t.calc, "variables", {"rho_oil": 41, "rho_water": 5}), slot)
    assert any("rho_oil=41" in x and "нет в узле" in x for x in e)
    e = _errs(lambda t: setattr(t, "prompt", "Чему равен параметр насыщения для этого пласта?"), slot)
    assert any("нет в условии" in x for x in e)
    e = _errs(lambda t: setattr(t.calc, "expression", "rho_oil / rho_water * 37"), slot)
    assert any("нет в узле" in x for x in e)


def test_text_must_be_russian():
    e = _errs(lambda t: setattr(t, "prompt", "What does the author claim in this step about resistivity?"))
    assert any("на русском" in x for x in e)


def test_node_misconception_must_be_used_in_a_choice_task():
    layer = _layer()
    node = _node(layer)
    planned = T.plan(layer.nodes)[RES]
    tasks = [_fake_task(node, s, with_ref=False) for s in planned]
    e = T.validate_node_tasks(node, tasks, planned, {m["id"] for m in MISC})
    assert any(REF in x for x in e)
    tasks = [_fake_task(node, s, with_ref=True) for s in planned]
    assert T.validate_node_tasks(node, tasks, planned, {m["id"] for m in MISC}) == []


# ---------------------------------------------------------------- сборка и перемешивание

def test_options_are_shuffled_deterministically_and_answers_map_to_correct_texts():
    node = _node(_layer())
    lt = _fake_task(node, {"type": "multiple", "kind": "recall"})
    a, b = T.build_task(node, lt, "x.t1"), T.build_task(node, lt, "x.t1")
    assert a == b
    correct_texts = {o.text for o in lt.options if o.correct}
    assert {o.text for o in a.options if o.id in a.answer} == correct_texts
    assert all(o.misconception is None for o in a.options if o.id in a.answer)
    orders = {tuple(o.text for o in T.build_task(node, lt, f"x.t{i}").options) for i in range(12)}
    assert len(orders) > 1


def test_order_is_shown_shuffled_but_answer_is_correct_sequence():
    node = _node(_layer())
    lt = _fake_task(node, {"type": "order", "kind": "recall"})
    for i in range(20):
        t = T.build_task(node, lt, f"o.t{i}")
        shown = [o.id for o in t.options]
        assert shown != t.answer and sorted(shown) == sorted(t.answer)
        text = {o.id: o.text for o in t.options}
        assert [text[x] for x in t.answer] == [o.text for o in lt.options]


# ---------------------------------------------------------------- модель и глава

def test_prompt_variables_match_what_code_passes():
    text = (ROOT / "prompts/course/tasks.md").read_text(encoding="utf-8")
    names = set(re.findall(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}", text))
    assert names == {"node", "requested", "misconceptions", "viewer", "language", "feedback"}


def test_ensure_tasks_builds_valid_chapter_and_validates_against_organizers_schema(tmp_path, llm):
    layer = _layer()
    fake = llm(FakeLLM(layer))
    res = T.ensure_tasks(layer, tmp_path / "course", MISC)
    assert len(fake.calls) == 4
    assert fake.calls[0]["prompt"] == "course/tasks" and fake.calls[0]["schema"] is T.LlmTasks
    assert set(fake.calls[0]["vars"]) == {"node", "requested", "misconceptions", "viewer", "language", "feedback"}
    data = json.loads((tmp_path / "course/tasks.json").read_text(encoding="utf-8"))
    jsonschema.validate(data, json.loads(SCHEMA.read_text(encoding="utf-8")))
    tasks = Tasks.model_validate(data)
    assert len(tasks.tasks) >= 15 and {t.type for t in tasks.tasks} == set(T.ROTATION)
    assert any(t.kind == "data" for t in tasks.tasks) and all(t.kind for t in tasks.tasks)
    assert len({t.id for t in tasks.tasks}) == len(tasks.tasks)
    assert {t.step_id for t in tasks.tasks} == {n.id for n in layer.nodes}
    assert any(o.misconception == REF for t in tasks.tasks for o in t.options)
    calc = next(t for t in tasks.tasks if t.type == "calc")
    assert calc.answer == 8.0 and calc.tolerance and calc.unit
    assert tasks.ext["course"]["hashes"][RES] == node_hash(_node(layer))
    assert res.ext["course"]["warnings"] == []


def test_ensure_tasks_is_incremental(tmp_path, llm):
    layer = _layer()
    llm(FakeLLM(layer))
    T.ensure_tasks(layer, tmp_path / "course", MISC)
    again = llm(FakeLLM(layer))
    T.ensure_tasks(layer, tmp_path / "course", MISC)
    assert again.calls == []
    _node(layer, "mini.porosity_basics").layers.main.text = "Пористость — доля пустот в объёме породы, а не масса."
    third = llm(FakeLLM(layer))
    T.ensure_tasks(layer, tmp_path / "course", MISC)
    assert [json.loads(c["vars"]["node"])["id"] for c in third.calls] == ["mini.porosity_basics"]
    only = llm(FakeLLM(layer))
    T.ensure_tasks(layer, tmp_path / "course", MISC, only=RES)
    assert only.calls == []


def test_ensure_tasks_feeds_errors_back_and_fails_loudly(tmp_path, llm):
    layer = _layer()

    def bad_first(n, tasks):
        if n == 1:
            tasks[0].claim_ids = ["zzz#c1"]
        return tasks
    fake = llm(FakeLLM(layer, tamper=bad_first))
    T.ensure_tasks(layer, tmp_path / "a", MISC)
    assert "zzz#c1" in fake.calls[1]["vars"]["feedback"] and len(fake.calls) == 5

    def always_bad(n, tasks):
        tasks[0].claim_ids = ["zzz#c1"]
        return tasks
    llm(FakeLLM(layer, tamper=always_bad))
    with pytest.raises(ValueError, match="zzz#c1"):
        T.ensure_tasks(layer, tmp_path / "b", MISC)


def test_check_chapter_hard_requirements():
    layer = _layer()
    node = _node(layer)
    mk = lambda ty, kind: T.build_task(node, _fake_task(node, {"type": ty, "kind": kind}), f"t{ty}{kind}{id(object())}")
    few = [mk("single", "data")] * 3
    with pytest.raises(ValueError, match="не меньше 15"):
        T.check_chapter(layer, few)
    no_data = [mk(t, "recall") for t in T.ROTATION] * 3
    for i, t in enumerate(no_data):
        t.id = f"x{i}"
    with pytest.raises(ValueError, match="kind=data"):
        T.check_chapter(layer, no_data)
    no_calc = [mk(t, "data") for t in T.ROTATION if t != "calc"] * 4
    with pytest.raises(ValueError, match="calc"):
        T.check_chapter(layer, no_calc)


def test_check_chapter_without_numbers_warns_instead_of_failing(capsys):
    layer = _layer()
    node = _node(layer)
    node.claims = [c for c in node.claims if c.source_kind == "text"]
    node.worked_examples = []
    tasks = [T.build_task(node, _fake_task(node, {"type": t, "kind": "data"}), f"x{i}") for i, t in enumerate([t for t in T.ROTATION if t != "calc"] * 4)]
    warnings = T.check_chapter(layer, tasks)
    assert warnings[0]["code"] == "calc_not_possible" and "WARNING" in capsys.readouterr().err
