"""Деградация вместо падения: курс обязан собраться (условие допуска). Падаем громко только при нехватке входных
файлов, битом layer.json и повторе id узла."""
import json
from pathlib import Path

import jsonschema
import pytest

from contracts.models import Layer, Tasks
from pipeline.course import generate, steptext, tasks as T
from pipeline.course.build import build
from pipeline.course.steptext import LlmAuthError, LlmError, StepTextOut
from test_steptext import _paras
from test_tasks_gen import FakeLLM, MISC, RES

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"
SCHEMA = ROOT / "data/organizers/01_схемы/task.schema.json"


def _layer(keep=None) -> Layer:
    layer = Layer.model_validate_json(MINI.read_text(encoding="utf-8"))
    if keep:
        layer.nodes = [n for n in layer.nodes if n.id in keep]
    return layer


def _out(tmp_path, layer=None) -> Path:
    layer = layer or _layer()
    d = tmp_path / "out" / layer.chapter
    d.mkdir(parents=True)
    (d / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    (d / "units.json").write_text(json.dumps({"domain": "geology"}), encoding="utf-8")
    return tmp_path / "out"


def _report(course: Path) -> dict:
    return json.loads((course / "build_report.json").read_text(encoding="utf-8"))


def _codes(rep, code):
    return [w for w in rep["warnings"] if w["code"] == code]


def _model(monkeypatch, layer, text="good", tamper=None, text_error=None, tasks_error=None):
    """text: 'good' — валидный текст из фикстуры, 'bad' — всегда с неверным claim_id."""
    text_calls, task_calls = [], []

    def fake_text(**kw):
        text_calls.append(kw)
        if text_error:
            raise text_error
        paras = _paras(json.loads(kw["vars"]["node"])["id"])
        if text == "bad":
            paras[0].claim_ids = ["zzz#c1"]
        return StepTextOut(paragraphs=paras)

    fake_tasks = FakeLLM(layer, tamper=tamper)
    orig = fake_tasks.__call__

    def tasks_call(**kw):
        task_calls.append(kw)
        if tasks_error:
            raise tasks_error
        return orig(**kw)

    monkeypatch.setattr(steptext, "complete_json", fake_text)
    monkeypatch.setattr(T, "complete_json", tasks_call)
    monkeypatch.setattr(generate, "load_misconceptions", lambda domain: MISC)
    return text_calls, task_calls


# ---------------------------------------------------------------- текст шага

def test_model_that_always_breaks_the_rules_still_gives_a_course(tmp_path, monkeypatch, capsys):
    layer = _layer()
    out = _out(tmp_path, layer)
    text_calls, task_calls = _model(monkeypatch, layer, text="bad", tamper=lambda n, ts: [setattr(t, "claim_ids", ["zzz#c1"]) or t for t in ts])
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)   # не падает
    assert (course / "index.html").exists()
    err = capsys.readouterr().err
    rep = _report(course)
    fb = _codes(rep, "step_text_fallback")
    assert sorted(w["node"] for w in fb) == sorted(n.id for n in layer.nodes)
    assert all(w["errors"] and "zzz#c1" in " ".join(w["errors"]) for w in fb)
    assert "WARNING" in err and "step_text_fallback" not in err and "mini.porosity_basics" in err
    assert len(text_calls) == 4 * steptext.ATTEMPTS
    # страницы собраны из полей слоя, как без step_text.json
    for p in course.glob("step-*.html"):
        assert 'data-claims="' not in p.read_text(encoding="utf-8")
    assert "Пористость — доля пустот в объёме породы." in (course / "step-mini.porosity_basics.html").read_text(encoding="utf-8")
    assert rep["step_text_nodes"] == 0


def test_fallback_is_remembered_and_reported_on_rebuild_without_llm(tmp_path, monkeypatch):
    layer = _layer()
    out = _out(tmp_path, layer)
    _model(monkeypatch, layer, text="bad")
    build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")          # --no-llm
    assert len(_codes(_report(course), "step_text_fallback")) == 4


def test_only_the_failing_step_falls_back(tmp_path, monkeypatch):
    layer = _layer()
    out = _out(tmp_path, layer)
    calls = []

    def selective(**kw):
        node_id = json.loads(kw["vars"]["node"])["id"]
        calls.append(node_id)
        paras = _paras(node_id)
        if node_id == "mini.porosity_basics":
            paras[0].claim_ids = []
        return StepTextOut(paragraphs=paras)
    _model(monkeypatch, layer)
    monkeypatch.setattr(steptext, "complete_json", selective)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)
    rep = _report(course)
    assert [w["node"] for w in _codes(rep, "step_text_fallback")] == ["mini.porosity_basics"]
    assert 'data-claims="' in (course / "step-mini.resistivity_depends_on_fluid.html").read_text(encoding="utf-8")
    assert 'data-claims="' not in (course / "step-mini.porosity_basics.html").read_text(encoding="utf-8")
    assert rep["step_text_nodes"] == 3


def test_unavailable_model_degrades_without_hammering_it(tmp_path, monkeypatch):
    # авторизация (нет ключа) — модель недоступна для всей главы сразу; общее состояние на текст и задания:
    # к модели обращаются один раз, а не по разу на фазу. (Обычные отказы — см. test_llm_resilience.py)
    layer = _layer()
    out = _out(tmp_path, layer)
    text_calls, task_calls = _model(monkeypatch, layer, text_error=LlmAuthError("AuthenticationError: нет ключа"),
                                    tasks_error=LlmAuthError("AuthenticationError: нет ключа"))
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)
    assert len(text_calls) == 1 and len(task_calls) == 0
    rep = _report(course)
    fb = _codes(rep, "step_text_fallback")
    assert len(fb) == 4 and all("модель недоступна" in w["errors"][0] and "нет ключа" in w["errors"][0] for w in fb)
    assert len(_codes(rep, "task_dropped")) == 16 and rep["tasks"] == 0
    assert "Заданий в этой главе пока нет" in (course / "progress.html").read_text(encoding="utf-8")


def test_programming_errors_are_not_mistaken_for_model_failures(tmp_path, monkeypatch):
    layer = _layer()
    out = _out(tmp_path, layer)
    _model(monkeypatch, layer, text_error=KeyError("промпт course/step_page: не хватает переменных"))
    with pytest.raises(KeyError):
        build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)


def test_call_llm_wraps_provider_errors_but_not_our_own(monkeypatch):
    import sys
    import types
    mod = types.ModuleType("pipeline.llm")
    monkeypatch.setitem(sys.modules, "pipeline.llm", mod)
    mod.complete_json = lambda **kw: (_ for _ in ()).throw(RuntimeError("оборван ответ"))
    with pytest.raises(LlmError, match="оборван ответ") as e:
        steptext.call_llm(prompt="x")
    assert isinstance(e.value.__cause__, RuntimeError)
    mod.complete_json = lambda **kw: (_ for _ in ()).throw(FileNotFoundError("нет промпта"))
    with pytest.raises(FileNotFoundError):
        steptext.call_llm(prompt="x")


# ---------------------------------------------------------------- задания

def test_tasks_that_never_pass_are_dropped_one_by_one(tmp_path, monkeypatch, capsys):
    layer = _layer()
    out = _out(tmp_path, layer)
    seen = []

    def break_first(n, ts):
        ts[0].claim_ids = ["zzz#c1"]
        return ts
    text_calls, task_calls = _model(monkeypatch, layer, tamper=break_first)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)
    rep = _report(course)
    dropped = _codes(rep, "task_dropped")
    assert len(dropped) == 4 and {w["slot"] for w in dropped} == {1}
    assert all(w["node"] and w["type"] and "zzz#c1" in " ".join(w["errors"]) for w in dropped)
    assert rep["tasks"] == 12 and "WARNING" in capsys.readouterr().err
    data = json.loads((course / "tasks.json").read_text(encoding="utf-8"))
    jsonschema.validate(data, json.loads(SCHEMA.read_text(encoding="utf-8")))
    assert not any(t["id"].endswith(".t1") for t in data["tasks"]) and any(t["id"].endswith(".t2") for t in data["tasks"])  # id стабильны
    # на повтор модели уходит только неудавшийся слот
    first_node = [c for c in task_calls if json.loads(c["vars"]["node"])["id"] == json.loads(task_calls[0]["vars"]["node"])["id"]]
    assert [len(json.loads(c["vars"]["requested"])) for c in first_node] == [4, 1, 1]
    assert _codes(rep, "few_tasks")                                  # 12 < 15


def test_dropped_calc_makes_missing_type_warning(tmp_path, monkeypatch):
    layer = _layer()
    out = _out(tmp_path, layer)

    def break_calc(n, ts):
        for t in ts:
            if t.type == "calc":
                t.claim_ids = ["zzz#c1"]
        return ts
    _model(monkeypatch, layer, tamper=break_calc)
    rep = _report(build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True))
    assert _codes(rep, "missing_task_type")[0]["types"] == ["calc"]
    assert [w["type"] for w in _codes(rep, "task_dropped")] == ["calc"]


def test_chapter_with_too_few_nodes_builds_with_what_it_has(tmp_path, monkeypatch):
    layer = _layer(keep={RES})
    out = _out(tmp_path, layer)
    _model(monkeypatch, layer)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)
    rep = _report(course)
    assert rep["tasks"] == T.CAP_PER_NODE and _codes(rep, "few_tasks")[0]["count"] == T.CAP_PER_NODE
    jsonschema.validate(json.loads((course / "tasks.json").read_text(encoding="utf-8")), json.loads(SCHEMA.read_text(encoding="utf-8")))


def test_node_misconception_unused_is_a_warning(tmp_path, monkeypatch):
    layer = _layer()
    out = _out(tmp_path, layer)
    fake = FakeLLM(layer, with_ref=False)
    _model(monkeypatch, layer)
    monkeypatch.setattr(T, "complete_json", fake)
    rep = _report(build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True))
    w = _codes(rep, "misconception_unused")
    assert w and w[0]["node"] == RES and w[0]["ref"] == "misc.high_res_oil"


def test_retry_after_failure_regenerates_only_failed_parts(tmp_path, monkeypatch):
    layer = _layer()
    out = _out(tmp_path, layer)
    _model(monkeypatch, layer, text="bad", tamper=lambda n, ts: [setattr(t, "claim_ids", ["zzz#c1"]) or t for t in ts])
    build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)
    text_calls, task_calls = _model(monkeypatch, layer)                       # модель «починилась»
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)
    rep = _report(course)
    assert not _codes(rep, "step_text_fallback") and not _codes(rep, "task_dropped")
    assert rep["step_text_nodes"] == 4 and rep["tasks"] == 16 and len(text_calls) == 4 and len(task_calls) == 4


# ---------------------------------------------------------------- громко — только входы

def test_loud_failures_are_only_missing_inputs_broken_layer_and_duplicate_ids(tmp_path):
    with pytest.raises(FileNotFoundError, match="layer.json"):
        build("nope", out_root=tmp_path / "out", pages_dir=tmp_path / "pages")
    out = _out(tmp_path / "a")
    (out / "mini_test/layer.json").write_text("{ это не json", encoding="utf-8")
    with pytest.raises(ValueError):                                         # pydantic.ValidationError — наследник ValueError
        build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    layer = _layer()
    layer.nodes[1].id = layer.nodes[0].id
    with pytest.raises(ValueError, match="повторяющиеся"):
        build("mini_test", out_root=_out(tmp_path / "b", layer), pages_dir=tmp_path / "pages")


def test_missing_domain_with_generate_fails_loudly(tmp_path):
    out = _out(tmp_path)
    (out / "mini_test/units.json").unlink()
    with pytest.raises(ValueError, match="units.json"):
        build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)
