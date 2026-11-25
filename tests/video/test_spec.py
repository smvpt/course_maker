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
    assert (scene.video_id, scene.node_id, scene.template) == (NODE + ".short", NODE, "T3")
    assert [c["prompt"] for c in fake.calls] == ["video/script", "video/scene_spec"]
    v = scene.ext["video"]
    assert v["sources"][0]["claim_id"] == NODE + "#c1" and v["sources"][0]["page_or_dataset"] == "стр. 95"
    assert v["route"]["template"] == "T3" and v["route"]["format"] == "шортс"
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


# ---------------------------------------------------------------- стыковка с T1

T1_NODE = CH + ".pressure_t1"


def _t1_script():
    claim = T1_NODE + "#c1"
    return _answer("llm_script.json", lambda d: [p.update(claim_id=claim) for p in d["phrases"]])


def _t1_scene(mutate=None):
    return _answer("llm_scene_t1.json", mutate)


def test_t1_spec_is_saved_and_passes_t1_checks(tmp_path, llm):
    from pipeline.video.t1_template import load_config, prepare
    fake = llm([_t1_script()], [_t1_scene()])
    assert _run(tmp_path, node=T1_NODE) == 0
    contract = fake.calls[1]["vars"]["template_contract"]
    assert "kappa_m2_s" in contract and "симуляция" in contract and "missing_params" in contract
    out = _out(tmp_path, T1_NODE + ".short")
    script = Script.model_validate_json((out / "script.json").read_text(encoding="utf-8"))
    scene = SceneSpec.model_validate_json((out / "scene_spec.json").read_text(encoding="utf-8"))
    assert scene.template == "T1"
    prep = prepare(scene, script, load_config(ROOT / "domain" / "geology" / "templates"))   # то, что сделает build
    assert prep["exaggeration"] == 100 and prep["true_scale_shot_id"] == "s5"
    src = scene.ext["video"]["param_sources"]
    assert set(src) == {"kappa_m2_s", "pressure_scale_mpa", "r_well_m"}
    assert "param_sources" not in scene.params and "missing_params" not in scene.params


@pytest.mark.parametrize("mutate,needle", [
    (lambda d: d["shots"][1].update(label="схема"), "симуляция"),
    (lambda d: d["shots"][1].update(label="реальные данные"), "симуляция"),
    (lambda d: d["shots"][0].update(frame_class="D", label="схема"), "симуляция"),
    (lambda d: d["shots"][2].update(plaque="не в масштабе: скважина крупнее в 50 раз"), "100"),
    (lambda d: d["params"].update(r_max_m=100), "выходит за окно"),
    (lambda d: d["params"].update(speed_m_s=2), "speed_m_s"),
    (lambda d: d["params"].update(evolve_shot_ids=["s42"]), "evolve_shot_ids"),
])
def test_t1_incompatible_scene_fails_after_repair(tmp_path, llm, capsys, mutate, needle):
    bad = _t1_scene(mutate)
    fake = llm([_t1_script()], [bad, bad])
    assert _run(tmp_path, node=T1_NODE) == 2
    err = capsys.readouterr().err
    assert needle in err
    assert needle in fake.calls[2]["vars"]["feedback"]          # замечание ушло в повторную попытку
    assert not _out(tmp_path, T1_NODE + ".short").exists()


def test_t1_repair_attempt_fixes_labels(tmp_path, llm):
    bad = _t1_scene(lambda d: d["shots"][1].update(label="схема"))
    fake = llm([_t1_script()], [bad, _t1_scene()])
    assert _run(tmp_path, node=T1_NODE) == 0
    assert "симуляция" in fake.calls[2]["vars"]["feedback"]


@pytest.mark.parametrize("mutate,needle", [
    (lambda d: d["param_sources"].pop("kappa_m2_s"), "kappa_m2_s"),
    (lambda d: d["param_sources"]["kappa_m2_s"].update(numbers=["0,7"]), "0,7"),
    (lambda d: d["param_sources"]["kappa_m2_s"].update(claim_ids=["other.node#c1"]), "other.node#c1"),
    (lambda d: d["param_sources"]["kappa_m2_s"].update(numbers=[]), "kappa_m2_s"),
])
def test_t1_physical_params_need_a_source_in_the_node(tmp_path, llm, capsys, mutate, needle):
    bad = _t1_scene(mutate)
    fake = llm([_t1_script()], [bad, bad])
    assert _run(tmp_path, node=T1_NODE) == 2
    assert needle in capsys.readouterr().err
    assert needle in fake.calls[2]["vars"]["feedback"]


def test_t1_missing_physical_params_are_a_clear_error_not_invented(tmp_path, llm, capsys):
    def missing(d):
        d["params"].pop("pressure_scale_mpa")
        d["param_sources"].pop("pressure_scale_mpa")
        d["missing_params"] = ["pressure_scale_mpa"]
    fake = llm([_t1_script()], [_t1_scene(missing)])
    assert _run(tmp_path, node=T1_NODE) == 2
    err = capsys.readouterr().err
    assert "pressure_scale_mpa" in err and "нет данных" in err
    assert len(fake.calls) == 2                                # без повторной попытки: данных в узле нет
    assert not _out(tmp_path, T1_NODE + ".short").exists()


def test_template_without_config_gets_generic_contract(tmp_path, llm):
    fake = llm()
    assert _run(tmp_path) == 0                                 # узел с T2: конфигурации T2 пока нет
    assert "не описаны" in fake.calls[1]["vars"]["template_contract"]


# ---------------------------------------------------------------- стыковка с T2

T2_ROUTING = FIX / "routing_t2.json"
T2_DATASET = ROOT / "fixtures" / "video" / "t2_demo" / "dataset.json"


def _run_t2(tmp_path, *extra):
    return spec.main(["--ch", CH, "--node", NODE, "--layer", str(FIX / "layer.json"), "--routing", str(T2_ROUTING),
                      "--out-root", str(tmp_path), *extra])


def _t2_scene(mutate=None):
    return _answer("llm_scene_t2.json", mutate)


def test_t2_spec_with_dataset_is_saved_and_passes_t2_checks(tmp_path, llm):
    from pipeline.video.t2_template import prepare
    from pipeline.video.templates import load_template_config
    fake = llm([_answer("llm_script_long.json")], [_t2_scene()])
    assert _run_t2(tmp_path, "--dataset", str(T2_DATASET)) == 0
    contract = fake.calls[1]["vars"]["template_contract"]
    assert "RT [OHMM]" in contract and "«симуляция»" in contract and "rule" in contract
    out = _out(tmp_path, NODE + ".long")
    script = Script.model_validate_json((out / "script.json").read_text(encoding="utf-8"))
    scene = SceneSpec.model_validate_json((out / "scene_spec.json").read_text(encoding="utf-8"))
    assert scene.template == "T2" and script.format == "long"
    assert scene.params["dataset"] == "fixtures/video/t2_demo/dataset.json"       # подставил код
    assert scene.params["borehole_diameter_m"] == 0.2
    prov = scene.ext["video"]["dataset_provenance"]
    assert prov["kind"] == "synthetic" and prov["file"] == "synthetic_well.las" and prov["well"] == "SYNTH-1"
    prep = prepare(scene, script, load_template_config(ROOT / "domain" / "geology" / "templates", "T2"))
    assert prep["dataset"].label == "симуляция"


def test_t2_without_dataset_is_a_clear_error_before_llm(tmp_path, llm, capsys):
    fake = llm([_answer("llm_script_long.json")], [_t2_scene()])
    assert _run_t2(tmp_path) == 2
    assert "--dataset" in capsys.readouterr().err
    assert fake.calls == []


def test_t2_dataset_without_borehole_diameter_is_an_error(tmp_path, llm, capsys):
    d = json.loads(T2_DATASET.read_text(encoding="utf-8"))
    d.pop("borehole_diameter_m")
    d["las"] = str(T2_DATASET.parent / d["las"])
    p = tmp_path / "dataset.json"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    llm([_answer("llm_script_long.json")], [_t2_scene()])
    assert _run_t2(tmp_path, "--dataset", str(p)) == 2
    assert "borehole_diameter_m" in capsys.readouterr().err


@pytest.mark.parametrize("mutate,needle", [
    (lambda d: d["shots"][1].update(label="реальные данные"), "реальные данные"),
    (lambda d: d["shots"][1].update(frame_class="B", label="схема"), "класс A"),
    (lambda d: d["params"]["curves"][1].update(unit="OHM.M"), "OHM.M"),
    (lambda d: d["params"]["curves"][0].update(mnemonic="SP"), "SP"),
    (lambda d: d["params"]["rule"].update(conclusion="пласт нефтеносный"), "не доказательство нефти"),
    (lambda d: d["params"]["rule"].update(caveat=""), "caveat"),
    (lambda d: d["params"].update(interval_m=[950, 1100]), "интервал"),
    (lambda d: d["shots"][2].update(plaque="не в масштабе: ствол шире в 5 раз"), "20"),
])
def test_t2_incompatible_scene_fails_after_repair(tmp_path, llm, capsys, mutate, needle):
    bad = _t2_scene(mutate)
    fake = llm([_answer("llm_script_long.json")], [bad, bad])
    assert _run_t2(tmp_path, "--dataset", str(T2_DATASET)) == 2
    assert needle in capsys.readouterr().err
    assert needle in fake.calls[2]["vars"]["feedback"]
    assert not _out(tmp_path, NODE + ".long").exists()


def test_t2_rule_from_node_needs_sources(tmp_path, llm, capsys):
    bad = _t2_scene(lambda d: d["params"]["rule"].update(status="из узла"))
    llm([_answer("llm_script_long.json")], [bad, bad])
    assert _run_t2(tmp_path, "--dataset", str(T2_DATASET)) == 2
    assert "params.rule" in capsys.readouterr().err


def test_dataset_for_template_without_data_is_an_error(tmp_path, llm, capsys):
    llm()
    assert _run(tmp_path, "--dataset", str(T2_DATASET)) == 2
    assert "не нужен" in capsys.readouterr().err


def test_template_format_mismatch_is_rejected_before_llm(tmp_path, llm, capsys):
    r = json.loads(T2_ROUTING.read_text(encoding="utf-8"))
    r["routes"][0]["format"] = "шортс"
    p = tmp_path / "routing.json"
    p.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    fake = llm([_answer("llm_script_long.json")], [_t2_scene()])
    assert spec.main(["--ch", CH, "--node", NODE, "--layer", str(FIX / "layer.json"), "--routing", str(p),
                      "--out-root", str(tmp_path), "--dataset", str(T2_DATASET)]) == 2
    err = capsys.readouterr().err
    assert "T2" in err and "short" in err and "long" in err
    assert fake.calls == []


def test_build_and_spec_share_template_formats():
    from pipeline.video import build
    from pipeline.video.templates import TEMPLATE_FORMATS
    assert build.TEMPLATES is TEMPLATE_FORMATS
