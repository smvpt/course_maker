"""Параллельная обработка узлов: COURSE_WORKERS, потокобезопасное состояние модели, детерминизм выходов."""
import json
import threading
import time

import pytest

from pipeline.course import steptext, tasks as T
from pipeline.course.pernode import ensure_per_node
from pipeline.course.steptext import LlmAuthError, LlmError, LlmState, StepTextOut, ensure_step_text, run_parallel, workers
from tests.course.test_steptext import _layer, _paras
from tests.course.test_tasks_gen import FakeLLM


def test_workers_default_env_and_loud_errors(monkeypatch):
    monkeypatch.delenv("COURSE_WORKERS", raising=False)
    assert workers() == 4
    monkeypatch.setenv("COURSE_WORKERS", "7")
    assert workers() == 7
    monkeypatch.setenv("COURSE_WORKERS", "1")
    assert workers() == 1
    for bad in ("0", "-2", "много", "2.5", ""):
        monkeypatch.setenv("COURSE_WORKERS", bad)
        with pytest.raises(ValueError, match="COURSE_WORKERS"):
            workers()


def test_run_parallel_keeps_input_order_and_really_runs_concurrently(monkeypatch):
    monkeypatch.setenv("COURSE_WORKERS", "4")
    live, peak, lock = 0, 0, threading.Lock()

    def job(i):
        nonlocal live, peak
        with lock:
            live += 1
            peak = max(peak, live)
        time.sleep(0.05 * (8 - i))                        # поздние элементы заканчиваются раньше ранних
        with lock:
            live -= 1
        return i * i
    assert run_parallel(list(range(8)), job) == [i * i for i in range(8)]
    assert 2 <= peak <= 4


def test_run_parallel_propagates_a_bug_instead_of_hiding_it(monkeypatch):
    monkeypatch.setenv("COURSE_WORKERS", "3")

    def job(i):
        if i == 2:
            raise ZeroDivisionError("баг в коде, а не отказ модели")
        return i
    with pytest.raises(ZeroDivisionError):
        run_parallel([1, 2, 3], job)


def test_llm_state_counters_are_exact_under_threads_and_three_in_a_row_still_works():
    st = LlmState()
    threads = [threading.Thread(target=lambda: [st.success() for _ in range(2000)]) for _ in range(8)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert st.calls == 16000 and st.down is None
    threads = [threading.Thread(target=lambda: [st.failure(LlmError("503")) for _ in range(1)]) for _ in range(3)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert st.failures == 3 and st.down is not None and "3 отказа подряд" in st.down
    st2 = LlmState()
    st2.failure(LlmError("503"))
    st2.failure(LlmError("503"))
    st2.success()
    st2.failure(LlmError("503"))
    assert st2.down is None                                # ответ между отказами сбрасывает счётчик
    st2.failure(LlmAuthError("ключ"))
    assert st2.down == "ключ"


def _slow_text(monkeypatch, delays=True):
    order = []

    def fake(**kw):
        nid = json.loads(kw["vars"]["node"])["id"]
        if delays:
            time.sleep({"mini.resistivity_depends_on_fluid": 0.30, "mini.porosity_basics": 0.20,
                        "mini.reservoir_decision": 0.10}.get(nid, 0.0))
        order.append(nid)
        return StepTextOut(paragraphs=_paras(nid))
    monkeypatch.setattr(steptext, "complete_json", fake)
    return order


def test_step_text_output_does_not_depend_on_worker_count_or_completion_order(tmp_path, monkeypatch):
    layer = _layer()
    blobs, orders = {}, {}
    for w in ("1", "4"):
        monkeypatch.setenv("COURSE_WORKERS", w)
        orders[w] = _slow_text(monkeypatch)
        d = tmp_path / w
        ensure_step_text(layer, d)
        blobs[w] = (d / "step_text.json").read_bytes()
    assert blobs["1"] == blobs["4"]
    assert orders["1"] != orders["4"] or len(orders["4"]) < 2             # при 4 потоках порядок завершения другой, файл — тот же


def test_tasks_output_does_not_depend_on_worker_count_or_completion_order(tmp_path, monkeypatch):
    layer = _layer()
    blobs = {}
    for w in ("1", "4"):
        monkeypatch.setenv("COURSE_WORKERS", w)
        fake = FakeLLM(layer)

        def slow(**kw):
            nid = json.loads(kw["vars"]["node"])["id"]
            time.sleep(0.05 * (len(nid) % 4))
            return fake(**kw)
        monkeypatch.setattr(T, "complete_json", slow)
        d = tmp_path / w
        T.ensure_tasks(layer, d, [])
        data = json.loads((d / "tasks.json").read_text(encoding="utf-8"))
        blobs[w] = data
    assert blobs["1"] == blobs["4"]
    ids = [t["id"] for t in blobs["4"]["tasks"]]
    assert ids == sorted(ids, key=lambda x: [n.id for n in layer.nodes].index(x.rsplit(".t", 1)[0]) * 100 + int(x.rsplit(".t", 1)[1]))


def test_auth_failure_stops_new_calls_even_with_parallel_workers(tmp_path, monkeypatch):
    monkeypatch.setenv("COURSE_WORKERS", "2")
    layer = _layer()
    calls = []

    def fake(**kw):
        calls.append(1)
        time.sleep(0.05)
        raise LlmAuthError("ключ не принят")
    monkeypatch.setattr(steptext, "complete_json", fake)
    ensure_step_text(layer, tmp_path, state=LlmState())
    assert len(calls) <= 2                                                # остальные узлы уже не доходят до модели
    data = json.loads((tmp_path / "step_text.json").read_text(encoding="utf-8"))
    assert len(data["failed"]) == len(layer.nodes)


def test_per_node_store_is_identical_for_one_and_four_workers(tmp_path, monkeypatch):
    layer = _layer()
    ids = {n.id for n in layer.nodes}
    blobs = {}
    for w in ("1", "4"):
        monkeypatch.setenv("COURSE_WORKERS", w)

        def make(n):
            time.sleep(0.03 * (len(n.id) % 3))
            return {"id": n.id}
        ensure_per_node(layer, tmp_path / w / "x.json", ids, make, LlmState())
        blobs[w] = (tmp_path / w / "x.json").read_bytes()
    assert blobs["1"] == blobs["4"]
