"""Вход видео: Script и SceneSpec из contracts.models, понятные ошибки."""
import json
from pathlib import Path

import pytest

from pipeline.video.inputs import VideoInputError, load_inputs

FIX = Path(__file__).resolve().parents[2] / "fixtures" / "video" / "hello"


def _write(tmp_path, script=None, spec=None):
    s = json.loads((FIX / "script.json").read_text(encoding="utf-8"))
    c = json.loads((FIX / "scene_spec.json").read_text(encoding="utf-8"))
    if script:
        script(s)
    if spec:
        spec(c)
    sp, cp = tmp_path / "script.json", tmp_path / "scene_spec.json"
    sp.write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
    cp.write_text(json.dumps(c, ensure_ascii=False), encoding="utf-8")
    return sp, cp


def test_hello_fixture_is_valid():
    script, spec = load_inputs(FIX / "script.json", FIX / "scene_spec.json",
                               node_id="video_hello.pipeline_check")
    assert [p.id for p in script.phrases] == ["p1", "p2"]
    assert spec.template == "hello"


def test_missing_file(tmp_path):
    with pytest.raises(VideoInputError, match="не найден"):
        load_inputs(tmp_path / "nope.json", FIX / "scene_spec.json")


def test_broken_json_names_the_contract(tmp_path):
    bad = tmp_path / "script.json"
    bad.write_text("{", encoding="utf-8")
    with pytest.raises(VideoInputError, match="Script"):
        load_inputs(bad, FIX / "scene_spec.json")


def test_contract_violation(tmp_path):
    sp, cp = _write(tmp_path, script=lambda s: s["phrases"][0].update(beat="вступление"))
    with pytest.raises(VideoInputError, match="Script"):
        load_inputs(sp, cp)


@pytest.mark.parametrize("script,spec,msg", [
    (lambda s: s.update(phrases=[]), None, "нет фраз"),
    (lambda s: s["phrases"][1].update(id="p1"), None, "повторяются"),
    (lambda s: s["phrases"][0].update(text="  "), None, "пуст"),
    (lambda s: s["phrases"][0].update(pause_after_s=-1), None, "пауза"),
    (lambda s: s["phrases"][0].update(on_screen="раз два три четыре пять шесть семь восемь девять"),
     None, "on_screen"),
    (None, lambda c: c.update(video_id="other"), "video_id"),
    (None, lambda c: c.update(node_id="other.node"), "node_id"),
    (None, lambda c: c["shots"][0].update(phrase_ids=["p9"]), "p9"),
    (None, lambda c: c["shots"][1].update(phrase_ids=["p1"]), "p2"),
    (lambda s: s.update(video_id="../escape"), lambda c: c.update(video_id="../escape"), "video_id"),
])
def test_semantic_errors(tmp_path, script, spec, msg):
    sp, cp = _write(tmp_path, script, spec)
    with pytest.raises(VideoInputError, match=msg):
        load_inputs(sp, cp)


def test_node_mismatch_with_cli(tmp_path):
    with pytest.raises(VideoInputError, match="--node"):
        load_inputs(FIX / "script.json", FIX / "scene_spec.json", node_id="other.node")
