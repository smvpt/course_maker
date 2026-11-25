"""CLI video.build: понятные ошибки до рендера, без сети."""
import json
from pathlib import Path

import pytest

from pipeline.video import build, media, tts
from pipeline.video.tts import TtsError

FIX = Path(__file__).resolve().parents[2] / "fixtures" / "video" / "hello"
NODE = "video_hello.pipeline_check"


def _args(tmp_path, *extra):
    return ["--ch", "video_hello", "--node", NODE, "--script", str(FIX / "script.json"),
            "--scene-spec", str(FIX / "scene_spec.json"), "--draft",
            "--out-root", str(tmp_path / "out"), "--cache-dir", str(tmp_path / "cache"), *extra]


@pytest.fixture
def tools_ok(monkeypatch):
    monkeypatch.setattr(media, "require", lambda name: name)
    monkeypatch.delenv("TTS_OFFLINE", raising=False)


def test_without_explicit_input_is_an_error(tmp_path, capsys):
    assert build.main(["--ch", "video_hello", "--node", NODE]) == 2
    assert "--script" in capsys.readouterr().err


def test_missing_ffmpeg_is_reported_before_anything_else(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(media.shutil, "which", lambda name: None)
    assert build.main(_args(tmp_path)) == 2
    assert "ffmpeg не найден" in capsys.readouterr().err
    assert not (tmp_path / "out").exists()


def test_node_mismatch(tmp_path, capsys, tools_ok):
    args = _args(tmp_path)
    args[3] = "other.node"
    assert build.main(args) == 2
    assert "--node other.node" in capsys.readouterr().err


def test_unknown_template(tmp_path, capsys, tools_ok):
    spec = json.loads((FIX / "scene_spec.json").read_text(encoding="utf-8"))
    spec["template"] = "T9"
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    args = _args(tmp_path)
    args[args.index("--scene-spec") + 1] = str(p)
    assert build.main(args) == 2
    assert "T9" in capsys.readouterr().err


def test_long_format_not_yet_supported(tmp_path, capsys, tools_ok):
    assert build.main(_args(tmp_path, "--format", "long")) == 2
    assert "short" in capsys.readouterr().err


def test_bad_chapter_id(tmp_path, capsys, tools_ok):
    args = _args(tmp_path)
    args[1] = "../x"
    assert build.main(args) == 2
    assert "--ch" in capsys.readouterr().err


def test_tts_service_down_is_a_clear_error(tmp_path, capsys, tools_ok, monkeypatch):
    def down(text, params):
        raise TtsError("edge-tts недоступен после 5 попыток")
    monkeypatch.setattr(tts, "_fetch", down)
    assert build.main(_args(tmp_path)) == 2
    assert "edge-tts недоступен" in capsys.readouterr().err


def test_offline_without_cache_is_a_clear_error(tmp_path, capsys, tools_ok, monkeypatch):
    monkeypatch.setenv("TTS_OFFLINE", "1")
    assert build.main(_args(tmp_path)) == 2
    assert "TTS_OFFLINE=1" in capsys.readouterr().err


def test_t1_bad_params_fail_before_tts(tmp_path, capsys, tools_ok, monkeypatch):
    t1 = FIX.parent / "t1_demo"
    spec = json.loads((t1 / "scene_spec.json").read_text(encoding="utf-8"))
    spec["params"]["kappa_m2_s"] = -1
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")

    def no_network(text, params):
        raise AssertionError("озвучка не должна запускаться при ошибке параметров")
    monkeypatch.setattr(tts, "_fetch", no_network)
    args = ["--ch", "video_t1", "--node", "video_t1_demo.pressure_diffusion", "--script", str(t1 / "script.json"),
            "--scene-spec", str(p), "--draft", "--out-root", str(tmp_path / "out"),
            "--cache-dir", str(tmp_path / "cache")]
    assert build.main(args) == 2
    err = capsys.readouterr().err
    assert "параметры T1" in err and "kappa_m2_s" in err
    assert not (tmp_path / "out").exists()
