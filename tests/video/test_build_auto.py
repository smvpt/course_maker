"""video.build одной командой: явная пара, готовая пара из каталога video.spec, генерация через LLM (подменён).

Сама сборка (озвучка, рендер) подменена — проверяется выбор входов и передача параметров. Без сети.
"""
import json
import shutil
import sys
import types
from pathlib import Path

import pytest

from pipeline.video import build

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "fixtures" / "video" / "spec"
CH = "video_spec_fixture"
NODE = CH + ".mixed_section"
T1_NODE = CH + ".pressure_t1"
T2_DATASET = ROOT / "fixtures" / "video" / "t2_demo" / "dataset.json"


def _answer(name, mutate=None):
    d = json.loads((FIX / name).read_text(encoding="utf-8"))
    if mutate:
        mutate(d)
    return d


class FakeLLM:
    def __init__(self, scripts, scenes):
        self.answers = {"video/script": list(scripts), "video/scene_spec": list(scenes)}
        self.calls = []

    def complete_json(self, prompt, vars, schema, tier="default", images=None):
        self.calls.append(prompt)
        a = self.answers[prompt].pop(0)
        if isinstance(a, Exception):
            raise a
        return schema.model_validate(a)


@pytest.fixture
def llm(monkeypatch):
    def install(scripts=(), scenes=()):
        fake = FakeLLM(scripts, scenes)
        mod = types.ModuleType("pipeline.llm")
        mod.complete_json = fake.complete_json
        monkeypatch.setitem(sys.modules, "pipeline.llm", mod)
        return fake
    return install


@pytest.fixture
def no_llm(monkeypatch):
    monkeypatch.setitem(sys.modules, "pipeline.llm", None)     # любой вызов генератора — ошибка


REPORT = {"probe": {"width": 1, "height": 1, "video_codec": "h264", "video_duration_s": 1.0, "audio_codec": "aac",
                    "audio_duration_s": 1.0, "integrated_lufs": -16.0, "true_peak_dbtp": -1.5},
          "mp4": "x.mp4", "vtt": "x.vtt", "wpm": 130, "subtitle_timing": ["word"], "warnings": [],
          "passport": "passport.json", "checklist_status": {}, "audio_ok": True, "audio_problem": None}


@pytest.fixture
def builds(monkeypatch):
    calls = []

    def fake_build(ch, node, script_path, spec_path, draft, fmt, voice, styleguide, out_root, cache_dir, domain,
                   skip_asr, asr_model, layer_path, checklist, tts_rate="+0%"):
        calls.append({"script": Path(script_path), "spec": Path(spec_path), "fmt": fmt, "layer": layer_path,
                      "draft": draft, "domain": domain, "tts_rate": tts_rate})
        return dict(REPORT)
    monkeypatch.setattr(build, "build", fake_build)
    return calls


GENERIC_NODES = {NODE, CH + ".en_quote", CH + ".text_only"}   # общие проверки — домен без описаний шаблонов


def _auto(tmp_path, node=NODE, routing=FIX / "routing.json", *extra):
    domain = "no_templates_fixture" if (node in GENERIC_NODES and routing == FIX / "routing.json") else "geology"
    return build.main(["--ch", CH, "--node", node, "--layer", str(FIX / "layer.json"), "--routing", str(routing),
                       "--out-root", str(tmp_path), "--draft", "--domain", domain, *extra])


def _pair_dir(tmp_path, node=NODE, fmt="short"):
    return tmp_path / CH / "videos" / f"{node}.{fmt}"


# ---------------------------------------------------------------- явная пара и неполные входы

def test_explicit_pair_is_used_as_is(tmp_path, builds, no_llm):
    hello = ROOT / "fixtures" / "video" / "hello"
    rc = build.main(["--ch", "video_hello", "--node", "video_hello.pipeline_check", "--script",
                     str(hello / "script.json"), "--scene-spec", str(hello / "scene_spec.json"),
                     "--out-root", str(tmp_path)])
    assert rc == 0 and builds[0]["script"] == hello / "script.json" and builds[0]["layer"] is None


def test_cli_passes_requested_tts_rate_to_synthesis(tmp_path, builds, no_llm):
    hello = ROOT / "fixtures/video/hello"
    assert build.main(["--ch", "video_hello", "--node", "video_hello.pipeline_check",
                       "--script", str(hello / "script.json"), "--scene-spec", str(hello / "scene_spec.json"),
                       "--out-root", str(tmp_path), "--tts-rate=+25%"] ) == 0
    assert builds[0]["tts_rate"] == "+25%"


@pytest.mark.parametrize("flag", ["--script", "--scene-spec"])
def test_half_of_explicit_pair_is_an_error_before_build(tmp_path, builds, no_llm, capsys, flag):
    rc = build.main(["--ch", CH, "--node", NODE, flag, str(FIX / "llm_script.json"), "--out-root", str(tmp_path)])
    assert rc == 2 and builds == []
    assert "--script и --scene-spec" in capsys.readouterr().err


def test_routing_or_dataset_with_explicit_pair_is_an_error(tmp_path, builds, capsys):
    hello = ROOT / "fixtures" / "video" / "hello"
    rc = build.main(["--ch", "video_hello", "--node", "video_hello.pipeline_check", "--script",
                     str(hello / "script.json"), "--scene-spec", str(hello / "scene_spec.json"),
                     "--dataset", str(T2_DATASET), "--out-root", str(tmp_path)])
    assert rc == 2 and builds == [] and "--dataset" in capsys.readouterr().err


# ---------------------------------------------------------------- генерация отсутствующей пары

def test_missing_pair_is_generated_then_built(tmp_path, builds, llm):
    fake = llm([_answer("llm_script.json")], [_answer("llm_scene.json")])
    assert _auto(tmp_path) == 0
    assert fake.calls == ["video/script", "video/scene_spec"]
    d = _pair_dir(tmp_path)
    assert builds[0]["script"] == d / "script.json" and builds[0]["spec"] == d / "scene_spec.json"
    assert builds[0]["fmt"] == "short" and builds[0]["layer"] == FIX / "layer.json" and builds[0]["draft"]


def test_ready_pair_is_reused_without_llm(tmp_path, builds, llm, monkeypatch):
    llm([_answer("llm_script.json")], [_answer("llm_scene.json")])
    assert _auto(tmp_path) == 0
    monkeypatch.setitem(sys.modules, "pipeline.llm", None)
    assert _auto(tmp_path) == 0                                    # второй запуск — без LLM
    assert len(builds) == 2 and builds[1]["script"] == _pair_dir(tmp_path) / "script.json"


def test_generation_error_stops_build(tmp_path, builds, llm, capsys):
    class LLMJSONError(RuntimeError):
        pass
    llm([LLMJSONError("невалидный JSON после 3 попыток")], [])
    assert _auto(tmp_path) == 2 and builds == []
    err = capsys.readouterr().err
    assert "video.spec" in err and "LLMJSONError" in err
    assert not _pair_dir(tmp_path).exists()


def test_missing_llm_module_without_pair_is_a_clear_error(tmp_path, builds, no_llm, capsys):
    assert _auto(tmp_path) == 2 and builds == []
    assert "pipeline.llm" in capsys.readouterr().err


# ---------------------------------------------------------------- готовая пара: проверки

def _ready(tmp_path, llm):
    llm([_answer("llm_script.json")], [_answer("llm_scene.json")])
    assert _auto(tmp_path) == 0
    return _pair_dir(tmp_path)


def test_corrupt_ready_pair_is_an_error_not_regenerated(tmp_path, builds, llm, capsys, monkeypatch):
    d = _ready(tmp_path, llm)
    (d / "scene_spec.json").write_text("{", encoding="utf-8")
    fake = llm([_answer("llm_script.json")], [_answer("llm_scene.json")])
    assert _auto(tmp_path) == 2
    assert "SceneSpec" in capsys.readouterr().err and fake.calls == [] and len(builds) == 1


def test_incomplete_ready_pair_is_an_error(tmp_path, builds, llm, capsys):
    d = _ready(tmp_path, llm)
    (d / "scene_spec.json").unlink()
    fake = llm([_answer("llm_script.json")], [_answer("llm_scene.json")])
    assert _auto(tmp_path) == 2 and fake.calls == []
    assert "неполная" in capsys.readouterr().err


def test_ready_pair_with_other_template_is_an_error(tmp_path, builds, llm, capsys):
    d = _ready(tmp_path, llm)
    spec = json.loads((d / "scene_spec.json").read_text(encoding="utf-8"))
    spec["template"] = "T1"
    (d / "scene_spec.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    assert _auto(tmp_path) == 2
    assert "шаблон" in capsys.readouterr().err


def test_ready_pair_with_other_format_is_an_error(tmp_path, builds, llm, capsys):
    d = _ready(tmp_path, llm)
    s = json.loads((d / "script.json").read_text(encoding="utf-8"))
    s["format"] = "long"
    (d / "script.json").write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
    assert _auto(tmp_path) == 2
    assert "формат" in capsys.readouterr().err


# ---------------------------------------------------------------- формат, маршрут, набор данных

def test_format_must_agree_with_route_before_llm(tmp_path, builds, llm, capsys):
    fake = llm([_answer("llm_script.json")], [_answer("llm_scene.json")])
    assert _auto(tmp_path, NODE, FIX / "routing.json", "--format", "long") == 2
    assert "маршрут" in capsys.readouterr().err and fake.calls == [] and builds == []


def test_explicit_format_equal_to_route_is_fine(tmp_path, builds, llm):
    llm([_answer("llm_script.json")], [_answer("llm_scene.json")])
    assert _auto(tmp_path, NODE, FIX / "routing.json", "--format", "short") == 0
    assert builds[0]["fmt"] == "short"


def test_dataset_is_passed_to_generator_and_checked_on_reuse(tmp_path, builds, llm, capsys):
    fake = llm([_answer("llm_script_long.json")], [_answer("llm_scene_t2.json")])
    assert _auto(tmp_path, NODE, FIX / "routing_t2.json", "--dataset", str(T2_DATASET)) == 0
    d = _pair_dir(tmp_path, NODE, "long")
    spec = json.loads((d / "scene_spec.json").read_text(encoding="utf-8"))
    assert spec["params"]["dataset"] == "fixtures/video/t2_demo/dataset.json" and builds[0]["fmt"] == "long"
    # повтор с тем же набором — без LLM; с другим — ошибка, не тихая подмена
    assert _auto(tmp_path, NODE, FIX / "routing_t2.json", "--dataset", str(T2_DATASET)) == 0
    other = tmp_path / "other"
    shutil.copytree(T2_DATASET.parent, other)
    assert _auto(tmp_path, NODE, FIX / "routing_t2.json", "--dataset", str(other / "dataset.json")) == 2
    assert "набором данных" in capsys.readouterr().err
    assert fake.calls == ["video/script", "video/scene_spec"] and len(builds) == 2


def test_t2_without_dataset_is_a_clear_error(tmp_path, builds, llm, capsys):
    fake = llm([_answer("llm_script_long.json")], [_answer("llm_scene_t2.json")])
    assert _auto(tmp_path, NODE, FIX / "routing_t2.json") == 2
    assert "--dataset" in capsys.readouterr().err and fake.calls == [] and builds == []


# ---------------------------------------------------------------- коды выхода проверки озвучки

def test_audio_check_failure_keeps_exit_code_3(tmp_path, monkeypatch, llm, capsys):
    llm([_answer("llm_script.json")], [_answer("llm_scene.json")])
    monkeypatch.setattr(build, "build", lambda *a, **k: {**REPORT, "audio_ok": False, "audio_problem": "WER"})
    assert _auto(tmp_path) == 3
    assert "WER" in capsys.readouterr().err


# ---------------------------------------------------------------- регрессия: готовая пара проходит проверки генератора

def test_ready_pair_with_foreign_claim_id_is_rejected_without_llm(tmp_path, builds, llm, capsys):
    d = _ready(tmp_path, llm)
    s = json.loads((d / "script.json").read_text(encoding="utf-8"))
    s["phrases"][0]["claim_id"] = "other.chapter#c1"
    (d / "script.json").write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
    fake = llm([_answer("llm_script.json")], [_answer("llm_scene.json")])
    assert _auto(tmp_path) == 2
    err = capsys.readouterr().err
    assert "other.chapter#c1" in err and "не подходит" in err
    assert fake.calls == [] and len(builds) == 1                  # без перегенерации и без новой сборки
    assert json.loads((d / "script.json").read_text(encoding="utf-8"))["phrases"][0]["claim_id"] == "other.chapter#c1"


def test_ready_t1_pair_without_param_sources_is_rejected(tmp_path, builds, llm, capsys):
    claim = T1_NODE + "#c1"
    llm([_answer("llm_script.json", lambda d: [p.update(claim_id=claim) for p in d["phrases"]])],
        [_answer("llm_scene_t1.json")])
    assert _auto(tmp_path, T1_NODE) == 0
    d = _pair_dir(tmp_path, T1_NODE)
    spec = json.loads((d / "scene_spec.json").read_text(encoding="utf-8"))
    spec["ext"]["video"]["param_sources"].pop("kappa_m2_s")
    (d / "scene_spec.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    fake = llm([], [])
    assert _auto(tmp_path, T1_NODE) == 2
    assert "kappa_m2_s" in capsys.readouterr().err and fake.calls == [] and len(builds) == 1


def test_ready_pair_breaking_script_rules_is_rejected(tmp_path, builds, llm, capsys):
    d = _ready(tmp_path, llm)
    s = json.loads((d / "script.json").read_text(encoding="utf-8"))
    s["phrases"][1]["text"] = "Пласт толщиной 20 метров."                 # цифры в речи
    (d / "script.json").write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
    assert _auto(tmp_path) == 2
    assert "цифр" in capsys.readouterr().err


def test_valid_ready_pair_still_reused_without_llm(tmp_path, builds, llm, monkeypatch):
    _ready(tmp_path, llm)
    monkeypatch.setitem(sys.modules, "pipeline.llm", None)
    assert _auto(tmp_path) == 0 and len(builds) == 2


# ---------------------------------------------------------------- T3: готовая пара проходит проверки шаблона

def test_ready_t3_pair_is_reused_and_rechecked(tmp_path, builds, llm, capsys, monkeypatch):
    node = CH + ".delta_t3"
    claim = node + "#c1"
    llm([_answer("llm_script.json", lambda d: [p.update(claim_id=claim) for p in d["phrases"]])],
        [_answer("llm_scene_t3.json")])
    assert _auto(tmp_path, node) == 0
    monkeypatch.setitem(sys.modules, "pipeline.llm", None)
    assert _auto(tmp_path, node) == 0 and len(builds) == 2                   # повтор без LLM
    d = _pair_dir(tmp_path, node)
    spec = json.loads((d / "scene_spec.json").read_text(encoding="utf-8"))
    spec["params"]["vertical_exaggeration"] = 20                             # плашки остались с «50»
    (d / "scene_spec.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    assert _auto(tmp_path, node) == 2 and len(builds) == 2
    assert "T3" in capsys.readouterr().err


def test_ready_t4_pair_is_reused_and_rechecked(tmp_path, builds, llm, capsys, monkeypatch):
    node = CH + ".well_t4"
    claim = node + "#c1"
    llm([_answer("llm_script.json", lambda d: [p.update(claim_id=claim) for p in d["phrases"]])],
        [_answer("llm_scene_t4.json")])
    assert _auto(tmp_path, node) == 0
    monkeypatch.setitem(sys.modules, "pipeline.llm", None)
    assert _auto(tmp_path, node) == 0 and len(builds) == 2                   # повтор без LLM
    d = _pair_dir(tmp_path, node)
    spec = json.loads((d / "scene_spec.json").read_text(encoding="utf-8"))
    spec["params"]["depth_m"] = 3000                                         # источник говорит 1500 м
    (d / "scene_spec.json").write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    assert _auto(tmp_path, node) == 2 and len(builds) == 2
    assert "depth_m" in capsys.readouterr().err
