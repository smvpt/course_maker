"""CLI video.spec: узел + маршрут → LLM (подменён) → script.json + scene_spec.json. Без сети."""
import json
import re
import sys
import types
from pathlib import Path

import pytest

from contracts.models import SceneSpec, Script
from pipeline.video import spec

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "fixtures" / "video" / "spec"
CH = "video_spec_fixture"
NODE = CH + ".mixed_section"
VAR_RE = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")


def _answer(name, mutate=None):
    d = json.loads((FIX / name).read_text(encoding="utf-8"))
    if mutate:
        mutate(d)
    return d


class FakeLLM:
    """Подмена pipeline.llm.complete_json: тот же интерфейс, переменные сверяются с файлом промпта."""

    def __init__(self, script_answers, scene_answers):
        self.answers = {"video/script": list(script_answers), "video/scene_spec": list(scene_answers)}
        self.calls = []

    def complete_json(self, prompt, vars, schema, tier="default", images=None):
        text = (ROOT / "prompts" / f"{prompt}.md").read_text(encoding="utf-8")
        assert set(VAR_RE.findall(text)) == set(vars), f"переменные промпта {prompt} не совпадают"
        self.calls.append({"prompt": prompt, "vars": vars, "tier": tier})
        ans = self.answers[prompt].pop(0)
        if isinstance(ans, Exception):
            raise ans
        return schema.model_validate(ans)


@pytest.fixture
def llm(monkeypatch):
    def install(script_answers=None, scene_answers=None):
        fake = FakeLLM(script_answers or [_answer("llm_script.json")], scene_answers or [_answer("llm_scene.json")])
        mod = types.ModuleType("pipeline.llm")
        mod.complete_json = fake.complete_json
        monkeypatch.setitem(sys.modules, "pipeline.llm", mod)
        return fake
    return install


def _run(tmp_path, *extra, ch=CH, node=NODE):
    return spec.main(["--ch", ch, "--node", node, "--layer", str(FIX / "layer.json"),
                      "--routing", str(FIX / "routing.json"), "--out-root", str(tmp_path), *extra])


def _out(tmp_path, video_id=NODE + ".short"):
    return tmp_path / CH / "videos" / video_id


def test_success_writes_contract_files(tmp_path, llm, capsys):
    fake = llm()
    assert _run(tmp_path) == 0
    out = _out(tmp_path)
    script = Script.model_validate_json((out / "script.json").read_text(encoding="utf-8"))
    scene = SceneSpec.model_validate_json((out / "scene_spec.json").read_text(encoding="utf-8"))
    assert (script.video_id, script.node_id, script.format) == (NODE + ".short", NODE, "short")
    assert (scene.video_id, scene.node_id, scene.template) == (NODE + ".short", NODE, "T2")
    assert [c["prompt"] for c in fake.calls] == ["video/script", "video/scene_spec"]
    v = scene.ext["video"]
    assert v["sources"][0]["claim_id"] == NODE + "#c1" and v["sources"][0]["page_or_dataset"] == "стр. 95"
    assert v["route"]["template"] == "T2" and v["route"]["format"] == "шортс"
    est = script.ext["video"]["duration_estimate"]
    assert 40 <= est["seconds"] <= 75 and "не замер" in est["method"]
    assert "оценка" in capsys.readouterr().out


def test_video_from_secondary_format_and_english_quotes(tmp_path, llm):
    node = CH + ".en_quote"
    claim = node + "#c1"
    fake = llm([_answer("llm_script.json", lambda d: [p.update(claim_id=claim) for p in d["phrases"]])])
    assert _run(tmp_path, node=node) == 0
    assert fake.calls[0]["vars"]["source_language"].startswith("английский")
    scene = SceneSpec.model_validate_json((_out(tmp_path, node + ".short") / "scene_spec.json").read_text(encoding="utf-8"))
    assert scene.ext["video"]["sources"][0]["quote"] == "This sentence is a neutral test quote for the video pipeline."


def test_unknown_node(tmp_path, llm, capsys):
    llm()
    assert _run(tmp_path, node=CH + ".nope") == 2
    assert "не найден" in capsys.readouterr().err


def test_chapter_mismatch(tmp_path, llm, capsys):
    llm()
    assert _run(tmp_path, ch="other_chapter") == 2
    err = capsys.readouterr().err
    assert "other_chapter" in err and CH in err


def test_node_without_video_route(tmp_path, llm, capsys):
    llm()
    assert _run(tmp_path, node=CH + ".text_only") == 2
    assert "не видео" in capsys.readouterr().err


def test_node_without_route(tmp_path, llm, capsys):
    routing = json.loads((FIX / "routing.json").read_text(encoding="utf-8"))
    routing["routes"] = [r for r in routing["routes"] if r["node_id"] != NODE]
    p = tmp_path / "routing.json"
    p.write_text(json.dumps(routing, ensure_ascii=False), encoding="utf-8")
    llm()
    assert spec.main(["--ch", CH, "--node", NODE, "--layer", str(FIX / "layer.json"), "--routing", str(p),
                      "--out-root", str(tmp_path)]) == 2
    assert "routing" in capsys.readouterr().err


def test_missing_default_layer_names_the_flag(tmp_path, llm, capsys):
    llm()
    assert spec.main(["--ch", CH, "--node", NODE, "--out-root", str(tmp_path)]) == 2
    err = capsys.readouterr().err
    assert "layer.json" in err and "--layer" in err


def test_foreign_claim_id_fails_after_repair_attempt(tmp_path, llm, capsys):
    bad = _answer("llm_script.json", lambda d: d["phrases"][2].update(claim_id="other.node#c7"))
    fake = llm([bad, bad])
    assert _run(tmp_path) == 2
    assert "other.node#c7" in capsys.readouterr().err
    assert [c["prompt"] for c in fake.calls] == ["video/script", "video/script"]
    assert "other.node#c7" in fake.calls[1]["vars"]["feedback"]
    assert not _out(tmp_path).exists()


def test_repair_attempt_can_fix_the_script(tmp_path, llm):
    bad = _answer("llm_script.json", lambda d: d["phrases"][1].update(text="Пласт толщиной 20 метров."))
    fake = llm([bad, _answer("llm_script.json")])
    assert _run(tmp_path) == 0
    assert "цифр" in fake.calls[1]["vars"]["feedback"]


def test_broken_shot_links(tmp_path, llm, capsys):
    bad = _answer("llm_scene.json", lambda d: d["shots"][1].update(phrase_ids=["p2", "p77"]))
    llm(scene_answers=[bad, bad])
    assert _run(tmp_path) == 2
    err = capsys.readouterr().err
    assert "p77" in err and "p3" in err
    assert not _out(tmp_path).exists()


def test_invalid_model_answer_is_a_clear_error(tmp_path, llm, capsys):
    class LLMJSONError(RuntimeError):
        pass
    llm([LLMJSONError("промпт video/script: невалидный JSON после 3 попыток")])
    assert _run(tmp_path) == 2
    err = capsys.readouterr().err
    assert "video/script" in err and "LLMJSONError" in err


def test_missing_llm_module_is_a_clear_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setitem(sys.modules, "pipeline.llm", None)
    assert _run(tmp_path) == 2
    assert "pipeline.llm" in capsys.readouterr().err
