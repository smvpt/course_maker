"""Один случайный отказ модели не должен обнулять курс: повторы временных ошибок, отказ только на своём узле/слоте,
«модель недоступна» — после 3 отказов подряд или при ошибке авторизации. Без сети и без настоящих пауз."""
import json
import re
import sys
import types
from pathlib import Path

import jsonschema
import pytest

from contracts.models import Layer
from pipeline.course import generate, steptext, tasks as T
from pipeline.course.build import build
from pipeline.course.steptext import LlmAuthError, LlmError, LlmState, StepTextOut
from test_steptext import _paras
from test_tasks_gen import FakeLLM, MISC

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"
SCHEMA = ROOT / "data/organizers/01_схемы/task.schema.json"
IDS = ["mini.resistivity_depends_on_fluid", "mini.porosity_basics", "mini.reservoir_decision", "mini.history_note"]


class RateLimitError(Exception):
    status_code = 429


class ServiceError(Exception):
    status_code = 503


class AuthenticationError(Exception):
    status_code = 401


class Timeout(Exception):
    pass


def _layer() -> Layer:
    return Layer.model_validate_json(MINI.read_text(encoding="utf-8"))


def _out(tmp_path) -> Path:
    layer = _layer()
    d = tmp_path / "out" / layer.chapter
    d.mkdir(parents=True)
    (d / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    (d / "units.json").write_text(json.dumps({"domain": "geology"}), encoding="utf-8")
    return tmp_path / "out"


def _report(course: Path) -> dict:
    return json.loads((course / "build_report.json").read_text(encoding="utf-8"))


def _codes(rep, code):
    return [w for w in rep["warnings"] if w["code"] == code]


@pytest.fixture
def pauses(monkeypatch):
    """Паузы не спим, а записываем."""
    spent = []
    monkeypatch.setattr(steptext, "_pause", spent.append)
    return spent


def _fake_provider(monkeypatch, script):
    """Подменяет pipeline.llm: script(n, kw) вызывается на каждый обращение, n — номер с 1; вернуть ответ или бросить."""
    calls = []
    mod = types.ModuleType("pipeline.llm")

    def complete_json(**kw):
        calls.append(kw)
        return script(len(calls), kw)
    mod.complete_json = complete_json
    monkeypatch.setitem(sys.modules, "pipeline.llm", mod)
    return calls


def _text_reply(kw):
    return StepTextOut(paragraphs=_paras(json.loads(kw["vars"]["node"])["id"]))


# ---------------------------------------------------------------- классификация и повторы в call_llm

def test_transient_errors_are_retried_with_2_5_10_second_pauses(monkeypatch, pauses):
    def script(n, kw):
        if n <= 3:
            raise [RateLimitError("429"), ServiceError("503"), Timeout("timed out")][n - 1]
        return "ответ"
    calls = _fake_provider(monkeypatch, script)
    assert steptext.call_llm(prompt="x") == "ответ"
    assert len(calls) == 4 and pauses == [2, 5, 10]


def test_transient_error_that_never_clears_becomes_llm_error_after_three_retries(monkeypatch, pauses):
    calls = _fake_provider(monkeypatch, lambda n, kw: (_ for _ in ()).throw(RateLimitError("429 слишком часто")))
    with pytest.raises(LlmError, match="429 слишком часто") as e:
        steptext.call_llm(prompt="x")
    assert not isinstance(e.value, LlmAuthError)
    assert len(calls) == 4 and pauses == [2, 5, 10]


@pytest.mark.parametrize("exc", [AuthenticationError("неверный ключ"), type("PermissionDeniedError", (Exception,), {"status_code": 403})("нельзя"),
                                 type("X", (Exception,), {"status_code": 401})("401"), RuntimeError("LLM_API_KEY содержит не-ASCII символы")])
def test_auth_errors_are_not_retried_and_marked_unavailable(monkeypatch, pauses, exc):
    calls = _fake_provider(monkeypatch, lambda n, kw: (_ for _ in ()).throw(exc))
    with pytest.raises(LlmAuthError):
        steptext.call_llm(prompt="x")
    assert len(calls) == 1 and pauses == []


def test_non_transient_provider_errors_fail_at_once_without_retry(monkeypatch, pauses):
    class LLMJSONError(RuntimeError):
        pass
    calls = _fake_provider(monkeypatch, lambda n, kw: (_ for _ in ()).throw(LLMJSONError("не JSON после повторов")))
    with pytest.raises(LlmError, match="не JSON") as e:
        steptext.call_llm(prompt="x")
    assert not isinstance(e.value, LlmAuthError) and len(calls) == 1 and pauses == []


@pytest.mark.parametrize("exc", [KeyError("нет переменной"), TypeError("не тот тип"), FileNotFoundError("нет промпта")])
def test_prompt_errors_stay_loud_and_are_not_retried(monkeypatch, pauses, exc):
    calls = _fake_provider(monkeypatch, lambda n, kw: (_ for _ in ()).throw(exc))
    with pytest.raises(type(exc)):
        steptext.call_llm(prompt="x")
    assert len(calls) == 1 and pauses == []


def test_llm_state_rules():
    s = LlmState()
    s.failure(LlmError("раз"))
    s.failure(LlmError("два"))
    s.success()                                     # ответ получен: подряд сброшено
    s.failure(LlmError("три"))
    s.failure(LlmError("четыре"))
    assert s.down is None
    s.failure(LlmError("пять"))
    assert s.down and "3 отказа подряд" in s.down and "пять" in s.down
    t = LlmState()
    t.failure(LlmAuthError("нет ключа"))
    assert t.down and "нет ключа" in t.down


# ---------------------------------------------------------------- текст шагов через настоящий call_llm

def test_429_twice_then_ok_still_gives_model_text_everywhere(tmp_path, monkeypatch, pauses):
    def script(n, kw):
        if n <= 2:
            raise RateLimitError("429")
        return _text_reply(kw)
    calls = _fake_provider(monkeypatch, script)
    nodes = steptext.ensure_step_text(_layer(), tmp_path / "course")
    assert set(nodes) == set(IDS) and pauses == [2, 5] and len(calls) == 4 + 2


def test_one_failed_node_degrades_only_that_node(tmp_path, monkeypatch):
    calls = []

    def fake(**kw):
        calls.append(json.loads(kw["vars"]["node"])["id"])
        if len(calls) == 2:
            raise LlmError("AuthError? нет, просто случайный сбой")
        return _text_reply(kw)
    monkeypatch.setattr(steptext, "complete_json", fake)
    state = LlmState()
    nodes = steptext.ensure_step_text(_layer(), tmp_path / "course", state=state)
    assert set(nodes) == {IDS[0], IDS[2], IDS[3]} and len(calls) == 4
    st = steptext.read_step_text(tmp_path / "course/step_text.json", "mini_test")
    assert list(st.failed) == [IDS[1]] and "случайный сбой" in st.failed[IDS[1]].errors[0]
    assert state.down is None and state.failures == 1


def test_three_failures_in_a_row_stop_calling_the_model(tmp_path, monkeypatch):
    calls = []

    def fake(**kw):
        calls.append(1)
        raise LlmError(f"сбой {len(calls)}")
    monkeypatch.setattr(steptext, "complete_json", fake)
    state = LlmState()
    nodes = steptext.ensure_step_text(_layer(), tmp_path / "course", state=state)
    assert nodes == {} and len(calls) == 3                       # четвёртый узел модель уже не зовёт
    st = steptext.read_step_text(tmp_path / "course/step_text.json", "mini_test")
    assert "3 отказа подряд" in st.failed[IDS[3]].errors[0] and st.failed[IDS[3]].errors[0].startswith("модель недоступна")
    assert st.failed[IDS[0]].errors[0].startswith("отказ модели")


def test_failures_that_are_not_consecutive_do_not_trip_the_breaker(tmp_path, monkeypatch):
    calls = []

    def fake(**kw):
        calls.append(1)
        if len(calls) in (1, 3):
            raise LlmError("сбой")
        return _text_reply(kw)
    monkeypatch.setattr(steptext, "complete_json", fake)
    state = LlmState()
    nodes = steptext.ensure_step_text(_layer(), tmp_path / "course", state=state)
    assert set(nodes) == {IDS[1], IDS[3]} and state.down is None and len(calls) == 4


def test_validation_failure_counts_as_an_answer_not_as_a_model_failure(tmp_path, monkeypatch):
    def fake(**kw):
        p = _paras(json.loads(kw["vars"]["node"])["id"])
        p[0].claim_ids = ["zzz#c1"]
        return StepTextOut(paragraphs=p)
    monkeypatch.setattr(steptext, "complete_json", fake)
    state = LlmState()
    steptext.ensure_step_text(_layer(), tmp_path / "course", state=state)
    assert state.down is None and state.failures == 0           # модель отвечала, просто неверно


# ---------------------------------------------------------------- задания: отказ только на своём слоте/узле

def test_model_failure_in_one_task_call_drops_only_that_nodes_pending_slots(tmp_path, monkeypatch):
    layer = _layer()
    fake = FakeLLM(layer)
    calls = []

    def flaky(**kw):
        calls.append(json.loads(kw["vars"]["node"])["id"])
        if len(calls) == 2:
            raise LlmError("оборвалось соединение")
        return fake(**kw)
    monkeypatch.setattr(T, "complete_json", flaky)
    state = LlmState()
    res = T.ensure_tasks(layer, tmp_path / "course", MISC, state=state)
    dropped = res.ext["course"]["dropped"]
    assert {d["node"] for d in dropped} == {IDS[1]} and len(dropped) == 4 and all("отказ модели" in d["errors"][0] for d in dropped)
    assert len(res.tasks) == 12 and state.down is None and len(calls) == 4


def test_three_task_nodes_failing_in_a_row_stop_the_model(tmp_path, monkeypatch):
    layer = _layer()
    calls = []

    def always(**kw):
        calls.append(1)
        raise LlmError("сбой")
    monkeypatch.setattr(T, "complete_json", always)
    state = LlmState()
    res = T.ensure_tasks(layer, tmp_path / "course", MISC, state=state)
    assert len(calls) == 3 and state.down
    d4 = [d for d in res.ext["course"]["dropped"] if d["node"] == IDS[3]]
    assert d4 and all(d["errors"][0].startswith("модель недоступна") for d in d4)


def test_shared_state_text_phase_outage_skips_the_task_phase(tmp_path, monkeypatch):
    layer = _layer()
    state = LlmState()
    state.failure(LlmAuthError("нет ключа"))
    called = []
    monkeypatch.setattr(T, "complete_json", lambda **kw: called.append(1))
    res = T.ensure_tasks(layer, tmp_path / "course", MISC, state=state)
    assert called == [] and len(res.ext["course"]["dropped"]) == 16


# ---------------------------------------------------------------- сборка целиком

def _build_with(tmp_path, monkeypatch, provider):
    out = _out(tmp_path)
    monkeypatch.setattr(generate, "load_misconceptions", lambda domain: MISC)
    layer = _layer()
    calls = _fake_provider(monkeypatch, lambda n, kw: provider(n, kw, layer))
    return build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True), calls


def _good_provider(layer, flaky=None):
    fake = FakeLLM(layer)

    def provider(n, kw, _layer):
        if flaky:
            flaky(n, kw)
        if kw["prompt"] == "course/step_page":
            return _text_reply(kw)
        return fake(**kw)
    return provider


def test_401_degrades_the_whole_chapter_with_one_clear_warning(tmp_path, monkeypatch, pauses, capsys):
    def provider(n, kw, layer):
        raise AuthenticationError("Invalid API key")
    course, calls = _build_with(tmp_path, monkeypatch, provider)
    err = capsys.readouterr().err
    assert len(calls) == 1 and pauses == []                      # одна попытка, без повторов и без остальных узлов
    warn_lines = [l for l in err.splitlines() if l.startswith("WARNING")]
    assert len(warn_lines) == 1 and "модель недоступна" in warn_lines[0] and "Invalid API key" in warn_lines[0]
    rep = _report(course)
    assert len(_codes(rep, "model_unavailable")) == 1
    assert len(_codes(rep, "step_text_fallback")) == 4 and len(_codes(rep, "task_dropped")) == 16
    assert (course / "index.html").exists() and rep["tasks"] == 0
    assert rep["summary"]["model"].startswith("недоступна") and "Invalid API key" in rep["summary"]["model"]


def test_one_flaky_node_in_a_full_build_keeps_the_rest_of_the_course(tmp_path, monkeypatch, pauses):
    seen = []

    def flaky(n, kw):
        if kw["prompt"] == "course/step_page":
            seen.append(json.loads(kw["vars"]["node"])["id"])
            if len(seen) == 2:
                raise ValueError("битый ответ")                   # не временная и не авторизация: отказ только узла
    layer = _layer()
    course, calls = _build_with(tmp_path, monkeypatch, _good_provider(layer, flaky))
    rep = _report(course)
    assert [w["node"] for w in _codes(rep, "step_text_fallback")] == [IDS[1]]
    assert rep["step_text_nodes"] == 3 and rep["tasks"] == 16 and not _codes(rep, "model_unavailable")
    assert not _codes(rep, "task_dropped")
    assert 'data-claims="' in (course / "step-mini.resistivity_depends_on_fluid.html").read_text(encoding="utf-8")
    assert 'data-claims="' not in (course / "step-mini.porosity_basics.html").read_text(encoding="utf-8")


# ---------------------------------------------------------------- итог сборки

def test_summary_line_is_loud_and_in_the_report(tmp_path, monkeypatch, pauses, capsys):
    seen = []

    def flaky(n, kw):
        if kw["prompt"] == "course/step_page":
            seen.append(1)
            if len(seen) == 2:
                raise ValueError("сбой")
    course, _ = _build_with(tmp_path, monkeypatch, _good_provider(_layer(), flaky))
    err = capsys.readouterr().err
    line = "ИТОГ СБОРКИ: текст модели: 3 из 4 шагов · заданий: 16 (выброшено 0) · fallback: 1 · модель: доступна"
    assert line in err.splitlines()
    s = _report(course)["summary"]
    assert s == {"text_model_steps": 3, "steps": 4, "tasks": 16, "tasks_dropped": 0, "fallback_steps": 1,
                 "model": "доступна", "line": line}


def test_summary_without_llm_says_the_model_was_not_used(tmp_path, capsys):
    out = _out(tmp_path)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    err = capsys.readouterr().err
    assert re.search(r"ИТОГ СБОРКИ: текст модели: 0 из 4 шагов · заданий: 0 \(выброшено 0\) · fallback: 4 · модель: не использовалась", err)
    assert _report(course)["summary"]["model"].startswith("не использовалась")


def test_summary_when_everything_came_from_files_says_model_was_not_called(tmp_path, monkeypatch, capsys):
    out = _out(tmp_path)
    monkeypatch.setattr(generate, "load_misconceptions", lambda domain: MISC)
    layer = _layer()
    calls = _fake_provider(monkeypatch, lambda n, kw: _good_provider(layer)(n, kw, layer))
    build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)
    n_first = len(calls)
    capsys.readouterr()
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)
    assert len(calls) == n_first
    s = _report(course)["summary"]
    assert s["text_model_steps"] == 4 and s["tasks"] == 16 and s["model"].startswith("не вызывалась")


# ---------------------------------------------------------------- устаревший tasks.json (живая пересборка на защите)

def test_stale_tasks_are_dropped_with_warning_not_a_crash(tmp_path, capsys):
    out = _out(tmp_path)
    (out / "mini_test/course").mkdir(parents=True)
    data = json.loads((ROOT / "fixtures/course/mini_tasks.json").read_text(encoding="utf-8"))
    data["tasks"][0]["step_id"] = "mini.removed_node"                          # узел удалили из слоя
    data["tasks"][1]["claim_ids"] = ["mini.resistivity_depends_on_fluid#c9"]   # утверждение удалили
    data["tasks"][2]["answer"] = ["o1", "o2", "o9"]                             # ответ ссылается на вариант, которого нет
    (out / "mini_test/course/tasks.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    rep = _report(course)
    stale = _codes(rep, "task_stale")
    assert sorted(w["task"] for w in stale) == ["mini.t01", "mini.t02", "mini.t03"]
    assert "mini.removed_node" in " ".join(next(w for w in stale if w["task"] == "mini.t01")["errors"])
    assert "c9" in " ".join(next(w for w in stale if w["task"] == "mini.t02")["errors"])
    assert "o9" in " ".join(next(w for w in stale if w["task"] == "mini.t03")["errors"])
    assert rep["tasks"] == 2 and "WARNING" in capsys.readouterr().err
    assert (course / "index.html").exists()
    # файл на диске не трогаем: следующая генерация перезапишет его сама
    assert len(json.loads((course / "tasks.json").read_text(encoding="utf-8"))["tasks"]) == 5
