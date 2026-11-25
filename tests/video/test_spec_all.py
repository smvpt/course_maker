"""video.spec --all: пакетная подготовка спецификаций всех видеоузлов главы. LLM подменён, без сети и рендера."""
import json
import sys
import types
from pathlib import Path

import pytest

from pipeline.video import spec

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "fixtures" / "video" / "spec"
CH = "video_spec_fixture"
T1, T2, T3, T4 = (CH + s for s in (".pressure_t1", ".mixed_section", ".delta_t3", ".well_t4"))
DATASET = ROOT / "fixtures" / "video" / "t2_demo" / "dataset.json"


def _answer(name, claim=None):
    d = json.loads((FIX / name).read_text(encoding="utf-8"))
    if claim:
        for p in d["phrases"]:
            p["claim_id"] = claim
    return d


SCRIPTS = {T1: lambda: _answer("llm_script.json", T1 + "#c1"), T3: lambda: _answer("llm_script.json", T3 + "#c1"),
           T4: lambda: _answer("llm_script.json", T4 + "#c1"), T2: lambda: _answer("llm_script_long.json")}
SCENES = {T1: "llm_scene_t1.json", T3: "llm_scene_t3.json", T4: "llm_scene_t4.json", T2: "llm_scene_t2.json"}


class NodeLLM:
    """Подмена complete_json: ответ по узлу из переменных промпта; fail — узлы, на которых модель «ломается»."""

    def __init__(self, fail=()):
        self.fail, self.calls = set(fail), []

    def complete_json(self, prompt, vars, schema, tier="default", images=None):
        node = vars["node"]["id"]
        self.calls.append((prompt, node))
        if node in self.fail:
            raise RuntimeError(f"сбой модели на {node}")
        ans = SCRIPTS[node]() if prompt == "video/script" else _answer(SCENES[node])
        return schema.model_validate(ans)


@pytest.fixture
def llm(monkeypatch):
    def install(fail=()):
        fake = NodeLLM(fail)
        mod = types.ModuleType("pipeline.llm")
        mod.complete_json = fake.complete_json
        monkeypatch.setitem(sys.modules, "pipeline.llm", mod)
        return fake
    return install


@pytest.fixture
def routing(tmp_path):
    """Маршруты главы: T1 шортс; T3 — видео дополнительным форматом; T4 шортс; T2 длинное видео; text_only — без видео."""
    r = json.loads((FIX / "routing.json").read_text(encoding="utf-8"))
    by = {x["node_id"]: x for x in r["routes"]}
    t2 = json.loads((FIX / "routing_t2.json").read_text(encoding="utf-8"))["routes"][0]
    routes = [by[T1], dict(by[T3], format="интерактив", secondary_format="шортс"), by[T4], t2, by[CH + ".text_only"]]
    p = tmp_path / "routing.json"
    p.write_text(json.dumps({**r, "routes": routes}, ensure_ascii=False), encoding="utf-8")
    return p


def _all(tmp_path, routing, *extra):
    return spec.main(["--ch", CH, "--all", "--layer", str(FIX / "layer.json"), "--routing", str(routing),
                      "--out-root", str(tmp_path), *extra])


def _report(tmp_path):
    return json.loads((tmp_path / CH / "videos" / "spec_report.json").read_text(encoding="utf-8"))


def _entry(rep, node):
    return next(e for e in rep["nodes"] if e["node_id"] == node)


def _dir(tmp_path, node, fmt="short"):
    return tmp_path / CH / "videos" / f"{node}.{fmt}"


def test_all_video_nodes_are_generated(tmp_path, routing, llm):
    fake = llm()
    assert _all(tmp_path, routing, "--dataset", str(DATASET)) == 0
    rep = _report(tmp_path)
    assert [e["node_id"] for e in rep["nodes"]] == [T1, T3, T4, T2]               # text_only — не видео
    assert {e["status"] for e in rep["nodes"]} == {"создана"}
    assert _entry(rep, T3)["format_source"] == "secondary_format" and _entry(rep, T3)["format"] == "short"
    for node, fmt in ((T1, "short"), (T3, "short"), (T4, "short"), (T2, "long")):
        assert (_dir(tmp_path, node, fmt) / "script.json").is_file() and (_dir(tmp_path, node, fmt) / "scene_spec.json").is_file()
    # набор данных — только шаблону, которому он нужен
    t2_spec = json.loads((_dir(tmp_path, T2, "long") / "scene_spec.json").read_text(encoding="utf-8"))
    assert t2_spec["params"]["dataset"] == "fixtures/video/t2_demo/dataset.json"
    t1_spec = json.loads((_dir(tmp_path, T1) / "scene_spec.json").read_text(encoding="utf-8"))
    assert "dataset" not in t1_spec["params"]
    assert _entry(rep, T2)["dataset_used"] and not _entry(rep, T1)["dataset_used"]
    assert rep["summary"] == {"создана": 4, "готова, без LLM": 0, "ошибка": 0}
    assert len(fake.calls) == 8


def test_rerun_reuses_ready_pairs_without_llm(tmp_path, routing, llm, monkeypatch):
    llm()
    assert _all(tmp_path, routing, "--dataset", str(DATASET)) == 0
    monkeypatch.setitem(sys.modules, "pipeline.llm", None)                     # второй запуск — без LLM вовсе
    assert _all(tmp_path, routing, "--dataset", str(DATASET)) == 0
    assert {e["status"] for e in _report(tmp_path)["nodes"]} == {"готова, без LLM"}


def test_partial_failure_is_recorded_and_others_continue(tmp_path, routing, llm, capsys):
    llm(fail={T3})
    assert _all(tmp_path, routing, "--dataset", str(DATASET)) == 3
    rep = _report(tmp_path)
    e = _entry(rep, T3)
    assert e["status"] == "ошибка" and "сбой модели" in e["error"]
    assert not _dir(tmp_path, T3).exists()
    assert {_entry(rep, n)["status"] for n in (T1, T4, T2)} == {"создана"}
    assert rep["summary"]["ошибка"] == 1
    assert T3 in capsys.readouterr().err


def test_damaged_pair_is_an_error_and_is_not_overwritten(tmp_path, routing, llm):
    llm()
    assert _all(tmp_path, routing, "--dataset", str(DATASET)) == 0
    p = _dir(tmp_path, T1) / "script.json"
    s = json.loads(p.read_text(encoding="utf-8"))
    s["phrases"][0]["claim_id"] = "other.chapter#c1"
    damaged = json.dumps(s, ensure_ascii=False)
    p.write_text(damaged, encoding="utf-8")
    fake = llm()
    assert _all(tmp_path, routing, "--dataset", str(DATASET)) == 3
    e = _entry(_report(tmp_path), T1)
    assert e["status"] == "ошибка" and "other.chapter#c1" in e["error"]
    assert p.read_text(encoding="utf-8") == damaged                             # не перезаписана
    assert fake.calls == []                                                     # остальные пары — без LLM


def test_incomplete_pair_is_an_error(tmp_path, routing, llm):
    llm()
    assert _all(tmp_path, routing, "--dataset", str(DATASET)) == 0
    (_dir(tmp_path, T4) / "scene_spec.json").unlink()
    llm()
    assert _all(tmp_path, routing, "--dataset", str(DATASET)) == 3
    e = _entry(_report(tmp_path), T4)
    assert e["status"] == "ошибка" and "неполная" in e["error"]
    assert not (_dir(tmp_path, T4) / "scene_spec.json").exists()


def test_t2_without_dataset_fails_only_t2(tmp_path, routing, llm):
    llm()
    assert _all(tmp_path, routing) == 3
    rep = _report(tmp_path)
    assert _entry(rep, T2)["status"] == "ошибка" and "--dataset" in _entry(rep, T2)["error"]
    assert {_entry(rep, n)["status"] for n in (T1, T3, T4)} == {"создана"}


def test_missing_llm_module_is_an_honest_error_per_node(tmp_path, routing, monkeypatch):
    monkeypatch.setitem(sys.modules, "pipeline.llm", None)
    assert _all(tmp_path, routing, "--dataset", str(DATASET)) == 3
    rep = _report(tmp_path)
    assert all(e["status"] == "ошибка" and "pipeline.llm" in e["error"] for e in rep["nodes"])
    assert not any(_dir(tmp_path, n, f).exists() for n, f in ((T1, "short"), (T3, "short"), (T4, "short"), (T2, "long")))


def test_all_and_node_are_mutually_exclusive(tmp_path, routing):
    with pytest.raises(SystemExit):
        spec.main(["--ch", CH, "--all", "--node", T1, "--routing", str(routing), "--out-root", str(tmp_path)])
    with pytest.raises(SystemExit):
        spec.main(["--ch", CH, "--routing", str(routing), "--out-root", str(tmp_path)])


def test_wrong_chapter_stops_before_any_node(tmp_path, routing, llm, capsys):
    fake = llm()
    assert spec.main(["--ch", "other_chapter", "--all", "--layer", str(FIX / "layer.json"), "--routing",
                      str(routing), "--out-root", str(tmp_path)]) == 2
    assert "other_chapter" in capsys.readouterr().err and fake.calls == []
