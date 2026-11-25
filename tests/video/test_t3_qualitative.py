"""T3: качественный режим (схема без чисел) на настоящем узле ядра, расчётный режим без изменений, формат 16:9.

Узел — fixtures/core/live_baraboshkin_par1-2 (настоящий выход ядра, только чтение). Пара fixtures/video/t3_deltas
написана вручную для проверки рендера и проверок — не ответ модели. LLM подменён, без сети и без рендера видео.
"""
import copy
import json
import sys
import types
from pathlib import Path

import numpy as np
import pytest

from contracts.models import Layer, SceneSpec, Script
from pipeline.video import build, coverage, spec as vspec, t3_template
from pipeline.video.inputs import VideoInputError
from pipeline.video.layout import LONG_SAFE_ZONE, REF_LONG, Layout, LayoutError
from pipeline.video.passport import checklist_answers, load_checklist, DEFAULT_CHECKLIST
from pipeline.video.templates import format_problem, load_template_config, template_contract

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "fixtures" / "core" / "live_baraboshkin_par1-2"
CH = "baraboshkin_par1-2"
NODE = CH + ".deltas_overview"
TPL = ROOT / "domain" / "geology" / "templates"
CFG = load_template_config(TPL, "T3")
FIX = ROOT / "fixtures" / "video" / "t3_deltas"
DEMO = ROOT / "fixtures" / "video" / "t3_demo"
LAYER = Layer.model_validate_json((LIVE / "layer.json").read_text(encoding="utf-8"))
NODE_OBJ = next(n for n in LAYER.nodes if n.id == NODE)


def _pair(path=FIX):
    return (Script.model_validate_json((path / "script.json").read_text(encoding="utf-8")),
            SceneSpec.model_validate_json((path / "scene_spec.json").read_text(encoding="utf-8")))


def _spec(mut=None):
    script, spec = _pair()
    d = spec.model_dump(by_alias=True)
    if mut:
        mut(d)
    return script, SceneSpec.model_validate(d)


def _problems(mut=None, script_mut=None):
    script, spec = _spec(mut)
    if script_mut:
        d = script.model_dump(by_alias=True)
        script_mut(d)
        script = Script.model_validate(d)
    try:
        t3_template.prepare(spec, script, CFG)
    except VideoInputError as e:
        return e.problems
    return []


# ---------------------------------------------------------------- качественный режим: проверки

def test_live_node_has_no_numbers_so_only_qualitative():
    assert not vspec.claims_have_numbers(NODE_OBJ)
    assert "нет ни одного числа" in vspec._mode_hint(CFG, NODE_OBJ)


def test_fixture_pair_passes_all_checks_on_live_node():
    script, spec = _pair()
    assert vspec.pair_problems(script, spec, NODE_OBJ, "long", TPL) == []
    prep = t3_template.prepare(spec, script, CFG)
    assert prep["mode"] == "qualitative" and prep["n_lobes"] == 3
    assert prep["elements"] == {"cone": NODE + "#c1", "zones": NODE + "#c3", "depocenter": NODE + "#c4",
                                "lobe_cycles": NODE + "#c5"}
    assert prep["appear_at"] == {"cone": "p1", "zones": "p6", "depocenter": "p10", "lobe_cycles": "p13"}


def _set(**kw):
    return lambda d: d["params"].update(kw)


def _shot(**kw):
    return lambda d: d["shots"][0].update(kw)


@pytest.mark.parametrize("mut,needle", [
    (_set(depth_m=20), "не задаются в режиме qualitative"),               # выдуманная глубина
    (_set(t_end_yr=1000, supply_m3_per_yr=5e5), "не задаются в режиме qualitative"),
    (_set(mode="semi"), "params.mode"),
    (_shot(label="симуляция"), "меткой «схема»"),
    (_shot(frame_class="A"), "класс B"),
    (_shot(plaque="не в масштабе: вертикаль увеличена в 10 раз"), "plaque"),
    (lambda d: d.update(exaggerations=["вертикаль увеличена в 10 раз"]), "exaggerations"),
    (lambda d: d.update(true_scale_shot_id="s1"), "true_scale_shot_id"),
    (lambda d: d["params"]["elements"].append({"element": "reef", "claim_id": NODE + "#c1"}), "неизвестен"),
    (lambda d: d["params"]["elements"].append({"element": "zones", "claim_id": NODE + "#c3"}), "дважды"),
    (lambda d: d["params"]["elements"].__setitem__(0, {"element": "cone", "claim_id": "other.ch#c1"}), "не из узла"),
    (lambda d: d["params"].update(elements=[e for e in d["params"]["elements"] if e["element"] != "cone"]),
     "обязательного элемента «cone»"),
    (lambda d: d["params"].update(elements=[]), "непустой список"),
    (lambda d: d["params"]["elements"].__setitem__(0, "cone"), "объект {element, claim_id}"),
    (lambda d: d["params"].update(elements=[e for e in d["params"]["elements"] if e["element"] != "lobe_cycles"]),
     "только с элементом lobe_cycles"),
    (_set(n_lobes=1), "нужно n_lobes ≥ 2"),
    (_set(n_lobes=9), "params.n_lobes"),
    (_set(evolve_shot_ids=["s5"]), "до первой фразы о стадиях"),
])
def test_invalid_qualitative_spec_fails_before_render(mut, needle):
    probs = _problems(mut)
    assert any(needle in p for p in probs), probs


def test_element_whose_claim_is_not_voiced_is_rejected():
    def mute_c4(d):
        for p in d["phrases"]:
            if p["claim_id"].endswith("#c4"):
                p["claim_id"] = NODE + "#c1"
    probs = _problems(script_mut=mute_c4)
    assert any("depocenter" in p and "не звучит" in p for p in probs), probs


def test_element_must_be_named_by_its_claim():
    script, spec = _spec(lambda d: d["params"]["elements"].__setitem__(2, {"element": "depocenter",
                                                                           "claim_id": NODE + "#c2"}))
    probs = t3_template.node_problems(spec, script, NODE_OBJ, CFG)
    assert any("depocenter" in p and "не называет" in p for p in probs), probs


def test_invented_units_in_text_are_rejected():
    script, spec = _pair()
    d = script.model_dump(by_alias=True)
    d["phrases"][3]["text"] = "Конус выноса растёт на двадцать метров за сто лет."
    d["phrases"][4]["on_screen"] = "Рост за тысячу лет"
    probs = t3_template.node_problems(spec, Script.model_validate(d), NODE_OBJ, CFG)
    assert any("p4.text" in p and "метров" in p for p in probs) and any("p5.on_screen" in p for p in probs), probs


def test_units_present_in_claims_are_allowed():
    node = NODE_OBJ.model_copy(deep=True)
    node.claims[0].quote += " Ширина конуса — десятки метров."
    script, spec = _pair()
    d = script.model_dump(by_alias=True)
    d["phrases"][3]["text"] = "Ширина конуса — десятки метров."
    assert t3_template.node_problems(spec, Script.model_validate(d), node, CFG) == []


def test_quantitative_mode_rejects_qualitative_params():
    script, spec = _pair(DEMO)
    d = spec.model_dump(by_alias=True)
    d["params"]["elements"] = [{"element": "cone", "claim_id": "x#c1"}]
    with pytest.raises(VideoInputError, match="не относятся к режиму quantitative"):
        t3_template.prepare(SceneSpec.model_validate(d), script, CFG)
    assert t3_template.prepare(spec, script, CFG)["mode"] == "quantitative"     # демо расчётного режима — как было


# ---------------------------------------------------------------- одно состояние → два вида

def _prep():
    script, spec = _pair()
    return t3_template.prepare(spec, script, CFG)


def test_qualitative_plan_and_section_share_zones():
    prep, x = _prep(), np.linspace(0.0, 1.0, 2001)
    for s in np.linspace(0.0, 1.0, 41):
        st = t3_template.stages(prep, s)
        stack = t3_template.stack_profiles(prep, s, x)
        assert [b["growth"] for b in stack] == [a["growth"] for a in st]
        for b in stack:
            zb = t3_template.zone_bounds(prep, b["growth"])       # те же границы рисует план (секторы)
            assert b["zones"] == zb
            prof = b["top"] - b["bottom"]
            plain, front, pro = zb
            inner = (x > 1e-6) & (x < plain["to"] - 1e-6)
            assert np.allclose(prof[inner], CFG["qualitative"]["zones"][0]["top"])   # равнина плоская
            assert np.all(prof[x > pro["to"] + 1e-3] == 0)                         # вне конуса тела нет
            # авандельта круче продельты
            slope = lambda z: abs(np.polyfit(x[(x > z["from"]) & (x < z["to"])],
                                             prof[(x > z["from"]) & (x < z["to"])], 1)[0]) if z["to"] > z["from"] + 0.01 else 0
            if b["growth"] > 0.1:
                assert slope(front) > slope(pro)
        assert 0 < t3_template.depocenter_extent(prep, s) <= min(a["growth"] for a in st)


def test_stages_order_check_and_growth():
    prep = _prep()
    ok, note = t3_template.qualitative_checks(prep)["stages_order"]
    assert ok and "моложе" in note
    assert len(t3_template.stages(prep, 0.0)) == 1 and t3_template.stages(prep, 0.0)[0]["growth"] == pytest.approx(0.2)
    assert len(t3_template.stages(prep, 1.0)) == 3 and [s["active"] for s in t3_template.stages(prep, 1.0)] == [False, False, True]


def test_first_stage_completes_before_lobe_phrases():
    prep = _prep()
    script, _ = _pair()
    segs = [(p.id, 4.0 * i, 4.0 * i + 3.5) for i, p in enumerate(script.phrases)]
    knots = t3_template.phase_knots(segs, prep["phases"])
    from pipeline.video.timeline import progress_at
    start = dict((pid, a) for pid, a, _ in segs)
    assert progress_at(start["p13"], knots) == pytest.approx(1 / 3)               # первая стадия выросла
    assert len(t3_template.stages(prep, progress_at(start["p13"] - 0.01, knots))) == 1
    assert progress_at(segs[-1][2], knots) == pytest.approx(1.0)
    assert progress_at(start["p10"], knots) == progress_at(start["p12"] + 3.5, knots)   # s4 (вопрос, депоцентр) — стоит


# ---------------------------------------------------------------- формат long

def test_t3_supports_long_and_short_others_unchanged():
    assert format_problem("T3", "long") is None and format_problem("T3", "short") is None
    assert format_problem("T1", "long") is not None and format_problem("T4", "long") is not None


def test_contract_lists_modes():
    txt = template_contract("T3", CFG)
    assert "qualitative" in txt and "quantitative" in txt and "только в режиме quantitative" in txt


def _scene_plan(script, spec, layout):
    sg = build._styleguide(build.DEFAULT_STYLEGUIDE)
    tpl_plan, tpl_colors, info = build._prepare_t3(spec, script, sg, TPL)
    t = 0.0
    segs = []
    shot_of = {pid: s for s in spec.shots for pid in s.phrase_ids}
    for ph in script.phrases:
        segs.append({"phrase_id": ph.id, "start": t, "end": t + 4.0, "hold_end": t + 4.0 + ph.pause_after_s,
                     "on_screen": ph.on_screen, "shot_id": shot_of[ph.id].id, "plaque": shot_of[ph.id].plaque,
                     "label": shot_of[ph.id].label, "label_color": sg["provenance"][shot_of[ph.id].label]})
        t += 4.0 + ph.pause_after_s
    return {"layout": layout, "font": sg["font"], "fps": 15, "segments": segs, "total": t, "speech_total": t,
            **tpl_plan, "colors": {"text": sg["text"], "muted": sg["muted"], "panel": sg["panel"], **tpl_colors}}, info


def _construct(scene_mod, cls, plan, monkeypatch, tmp_path):
    """Строит сцену без рендера видео: проверки безопасной зоны срабатывают при построении."""
    from manim import tempconfig
    monkeypatch.setattr(scene_mod, "play_timeline", lambda *a, **k: None)
    lay = plan["layout"]
    with tempconfig({"frame_height": 8.0, "frame_width": 8.0 * lay.ref_w / lay.ref_h, "pixel_width": lay.ref_w // 4,
                     "pixel_height": lay.ref_h // 4, "disable_caching": True, "verbosity": "WARNING",
                     "media_dir": str(tmp_path / "manim")}):
        scene = cls()
        scene.plan = plan
        scene.construct()
    return scene


def _layouts():
    sg = build._styleguide(build.DEFAULT_STYLEGUIDE)
    return {"short": Layout(sg["safe_zone"], sg["min_caption_px"]),
            "long": Layout(LONG_SAFE_ZONE, sg["min_caption_px"], ref=REF_LONG)}


@pytest.mark.parametrize("fmt", ["short", "long"])
def test_qualitative_scene_fits_safe_zone(fmt, monkeypatch, tmp_path):
    from pipeline.video import scene_t3q
    script, spec = _pair()
    plan, info = _scene_plan(script, spec, _layouts()[fmt])
    scene = _construct(scene_t3q, scene_t3q.T3SchemeScene, plan, monkeypatch, tmp_path)
    assert len(scene.mobjects) > 10
    assert info["mode"] == "qualitative" and {e["element"] for e in info["elements"]} ==         {"cone", "zones", "depocenter", "lobe_cycles"}


@pytest.mark.parametrize("fmt", ["short", "long"])
def test_quantitative_scene_fits_safe_zone(fmt, monkeypatch, tmp_path):
    from pipeline.video import scene_t3
    script, spec = _pair(DEMO)
    plan, info = _scene_plan(script, spec, _layouts()[fmt])
    _construct(scene_t3, scene_t3.T3Scene, plan, monkeypatch, tmp_path)
    assert info["mode"] == "quantitative"


# ---------------------------------------------------------------- паспорт: свой чек-лист схемы

def test_qualitative_checklist_is_honest():
    script, spec = _pair()
    _, _, info = build._prepare_t3(spec, script, build._styleguide(build.DEFAULT_STYLEGUIDE), TPL)
    auto = build._auto_checks(spec, info)
    items = load_checklist(DEFAULT_CHECKLIST)
    ans = {a.item: a for a in checklist_answers(items, CFG["qualitative"]["physics_checklist"], auto)}
    assert ans["pc.layers_order"].answer == "да" and ans["pc.views_consistent"].answer == "да"
    for pid in ("pc.balance", "pc.exaggeration_named", "pc.plausible_numbers", "pc.depth_down"):
        assert ans[pid].answer == "н/п", pid
    assert ans["pc.causality"].status == "не проверено"                       # смысл проверяет ментор
    assert "«схема»" in ans["pc.label_matches"].note


# ---------------------------------------------------------------- генератор и покрытие на настоящем маршруте

def _llm_answers():
    script, spec = _pair()
    s = script.model_dump(by_alias=True)
    sd = {k: s[k] for k in ("phrases", "prediction_question", "transfer_question", "data_it_bridge")}
    c = spec.model_dump(by_alias=True)
    cd = {k: v for k, v in c.items() if k not in ("video_id", "node_id", "template", "ext")}
    cd.update(param_sources={}, missing_params=["depth_m", "foreset_angle_deg", "supply_m3_per_yr"])
    return sd, cd


@pytest.fixture
def fake_llm(monkeypatch):
    sd, cd = _llm_answers()
    calls = []

    def complete_json(prompt, vars, schema, tier="default", images=None):
        calls.append((prompt, vars))
        return schema.model_validate(copy.deepcopy(sd if prompt == "video/script" else cd))
    mod = types.ModuleType("pipeline.llm")
    mod.complete_json = complete_json
    monkeypatch.setitem(sys.modules, "pipeline.llm", mod)
    return calls


def test_spec_on_live_route_generates_qualitative_long(tmp_path, fake_llm):
    assert vspec.main(["--ch", CH, "--node", NODE, "--layer", str(LIVE / "layer.json"), "--routing",
                       str(LIVE / "routing.json"), "--out-root", str(tmp_path)]) == 0
    d = tmp_path / CH / "videos" / f"{NODE}.long"
    spec = json.loads((d / "scene_spec.json").read_text(encoding="utf-8"))
    assert spec["params"]["mode"] == "qualitative" and spec["template"] == "T3"
    assert spec["ext"]["video"]["missing_params"] == ["depth_m", "foreset_angle_deg", "supply_m3_per_yr"]
    contract = next(v for p, v in fake_llm if p == "video/scene_spec")["template_contract"]
    assert "нет ни одного числа" in contract and "qualitative" in contract
    script = json.loads((d / "script.json").read_text(encoding="utf-8"))
    assert script["format"] == "long" and 90 <= script["ext"]["video"]["duration_estimate"]["seconds"] <= 180


def test_quantitative_answer_without_numbers_is_rejected_on_live_node(tmp_path, monkeypatch):
    sd, cd = _llm_answers()
    _, demo = _pair(DEMO)
    cd = {**cd, "params": {k: v for k, v in demo.params.items() if k != "evolve_shot_ids"}, "missing_params": [],
          "shots": [dict(s, label="симуляция") for s in cd["shots"]]}
    mod = types.ModuleType("pipeline.llm")
    mod.complete_json = lambda prompt, vars, schema, tier="default", images=None: \
        schema.model_validate(copy.deepcopy(sd if prompt == "video/script" else cd))
    monkeypatch.setitem(sys.modules, "pipeline.llm", mod)
    assert vspec.main(["--ch", CH, "--node", NODE, "--layer", str(LIVE / "layer.json"), "--routing",
                       str(LIVE / "routing.json"), "--out-root", str(tmp_path)]) == 2
    assert not (tmp_path / CH / "videos" / f"{NODE}.long").exists()


def test_coverage_on_live_route_reports_mode(tmp_path, fake_llm):
    def run():
        assert coverage.main(["--ch", CH, "--layer", str(LIVE / "layer.json"), "--routing", str(LIVE / "routing.json"),
                              "--out-root", str(tmp_path)]) == 0
        rep = json.loads((tmp_path / CH / "videos" / "coverage.json").read_text(encoding="utf-8"))
        return rep, next(r for r in rep["nodes"] if r["node_id"] == NODE)
    rep, row = run()
    assert row["status"] == "спецификация ещё не создана" and row["format"] == "long"
    assert row["format_supported"] and set(row["modes"]) == {"quantitative", "qualitative"}
    assert row["claims_have_numbers"] is False and "qualitative" in row["notes"][0]
    assert vspec.main(["--ch", CH, "--node", NODE, "--layer", str(LIVE / "layer.json"), "--routing",
                       str(LIVE / "routing.json"), "--out-root", str(tmp_path)]) == 0
    rep, row = run()
    assert row["status"] == "поддерживается" and row["pair"]["mode"] == "qualitative"
    assert row["model"] == CFG["qualitative"]["model"]
    assert not any("уровень моря и глубина бассейна" in a for a in row["assumptions"])   # допущения расчёта не переносятся
    # чужие маршруты не исправляются: T1 на узлах о дельтах честно в отчёте
    t1 = [r for r in rep["nodes"] if r["template"] == "T1"]
    assert t1 and all(r["status"] == "формат не поддерживается" for r in t1)


# ---------------------------------------------------------------- таблица источников паспорта

def test_sources_table_from_live_claims_covers_all_used_claims():
    from pipeline.video.passport import source_problems, used_claim_ids
    from pipeline.video.spec_check import sources_table
    script, spec = _pair()
    used = used_claim_ids(script, spec)
    assert used == [NODE + f"#c{k}" for k in (1, 2, 3, 4, 5)]
    rows = build._sources(script, spec, {}, NODE_OBJ)
    assert rows == sources_table(script, NODE_OBJ, used)
    claims = {c.id: c for c in NODE_OBJ.claims}
    for r in rows:                                     # страница и цитата — дословно из claims узла
        c = claims[r["claim_id"]]
        assert r["quote"] == c.quote and r["page_or_dataset"].startswith(f"стр. {c.page_pdf}")
    assert source_problems(rows, used, NODE_OBJ) == []


def test_element_and_param_claims_are_in_sources_even_if_not_voiced():
    from pipeline.video.passport import used_claim_ids
    script, spec = _pair()
    spec.ext["video"]["param_sources"] = {"x": {"claim_ids": [NODE + "#c2"], "numbers": []}}
    d = script.model_dump(by_alias=True)
    for p in d["phrases"]:
        if p["claim_id"].endswith("#c2"):
            p["claim_id"] = NODE + "#c1"
    script = Script.model_validate(d)
    used = used_claim_ids(script, spec)
    assert NODE + "#c2" in used
    assert NODE + "#c2" in {r["claim_id"] for r in build._sources(script, spec, {}, NODE_OBJ)}


@pytest.mark.parametrize("damage,needle", [
    (lambda rows: rows.pop(2), "нет утверждения"),
    (lambda rows: rows[0].update(quote=rows[0]["quote"] + " (дополнено)"), "не совпадают"),
    (lambda rows: rows[1].update(page_or_dataset="стр. 99"), "не совпадают"),
    (lambda rows: rows[3].update(quote=""), "нет страницы или цитаты"),
    (lambda rows: rows.append({"claim_id": "other.ch#c1", "page_or_dataset": "стр. 1", "quote": "чужая цитата"}),
     "лишнее утверждение"),
])
def test_incomplete_or_wrong_sources_are_detected(damage, needle):
    from pipeline.video.passport import source_problems, used_claim_ids
    script, spec = _pair()
    rows = [dict(r) for r in build._sources(script, spec, {}, NODE_OBJ)]
    damage(rows)
    probs = source_problems(rows, used_claim_ids(script, spec), NODE_OBJ)
    assert any(needle in p for p in probs), probs


def test_build_without_layer_and_without_sources_stops_before_tts(tmp_path, monkeypatch):
    def no_tts(*a, **k):
        raise AssertionError("озвучка не должна запускаться")
    monkeypatch.setattr(build, "synthesize", no_tts)
    with pytest.raises(VideoInputError, match="таблица источников паспорта неполна.*--layer"):
        build.build(CH, NODE, FIX / "script.json", FIX / "scene_spec.json", True, None, "ru-RU-SvetlanaNeural",
                    build.DEFAULT_STYLEGUIDE, tmp_path, tmp_path / "tts")


def test_written_passport_has_all_five_sources_from_node(tmp_path):
    from pipeline.video.passport import SCHEMA_PATH, assemble, write_passport
    script, spec = _pair()
    rows = build._sources(script, spec, {}, NODE_OBJ)
    segs = [{"phrase_id": p.id, "start": float(i), "end": i + 0.9} for i, p in enumerate(script.phrases)]
    pp = assemble(script=script, spec=spec, segments=segs, frames=[{"t": 0.5, "shot_id": "s1", "file": "f.png"}],
                  node_card=build._node_card(script, NODE_OBJ), sources=rows, checklist=[], audio_check={},
                  scene_spec_path="scene_spec.json")
    data = write_passport(pp, tmp_path / "passport.json", json.loads(SCHEMA_PATH.read_text(encoding="utf-8")))
    claims = {c.id: c for c in NODE_OBJ.claims}
    assert [r["claim_id"] for r in data["sources"]] == [NODE + f"#c{k}" for k in (1, 2, 3, 4, 5)]
    for r in data["sources"]:
        assert r["quote"] == claims[r["claim_id"]].quote
        assert r["page_or_dataset"] == f"стр. {claims[r['claim_id']].page_pdf}"
