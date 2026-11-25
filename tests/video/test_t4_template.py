"""T4: параметры до озвучки, скважины и график из одного состояния, заморозка вопроса и финала."""
import copy
import json
from pathlib import Path

import numpy as np
import pytest

from contracts.models import SceneSpec, Script
from pipeline.video.inputs import VideoInputError
from pipeline.video.t4_model import P_ATM
from pipeline.video.t4_template import auto_checks, prepare, pressure_curves, states, top_at
from pipeline.video.templates import load_template_config

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "fixtures" / "video" / "t4_demo"
CFG = load_template_config(ROOT / "domain" / "geology" / "templates", "T4")
SPEC = json.loads((FIX / "scene_spec.json").read_text(encoding="utf-8"))
SCRIPT = Script.model_validate_json((FIX / "script.json").read_text(encoding="utf-8"))


def _prep(mut=None):
    d = copy.deepcopy(SPEC)
    if mut:
        mut(d)
    return prepare(SceneSpec.model_validate(d), SCRIPT, CFG)


def test_demo_spec_is_valid():
    prep = _prep()
    assert prep["exaggeration"] == 400 and prep["true_scale_shot_id"] == "s4" and prep["casing_shoe"] == 600
    assert prep["evolve_phrase_ids"] == {"p6", "p7"}                       # p5 — вопрос: газ стоит


def _p(**kw):
    return lambda d: d["params"].update(**kw)


@pytest.mark.parametrize("mut,needle", [
    (lambda d: d["params"].pop("mud_density_kg_m3"), "mud_density_kg_m3"),
    (_p(flow=1), "flow"),
    (_p(depth_m=0), "depth_m"),
    (_p(mud_density_kg_m3=1.2), "единицы"),                               # г/см³ вместо кг/м³
    (_p(hole_diameter_m=8.5), "hole_diameter_m"),                         # дюймы вместо метров
    (_p(gas_volume_m3=20), "больше"),                                     # пачка длиннее 0,1 ствола
    (_p(casing_shoe_m=2000), "башмак"),
    (_p(top_stop_m=1470), "не выше"),
    (_p(top_stop_m=1200), "лишь на"),
    (_p(top_stop_m=20), "не помещается"),
    (_p(horizontal_exaggeration=0.5), "horizontal_exaggeration"),
    (_p(horizontal_exaggeration=5000), "шире"),
    (_p(evolve_shot_ids=["s9"]), "evolve_shot_ids"),
    (lambda d: d["shots"][1].update(label="схема"), "симуляция"),
    (lambda d: d["shots"][1].update(plaque="не в масштабе: ствол шире в 50 раз"), "400"),
    (lambda d: d.update(true_scale_shot_id=None), "true_scale_shot_id"),
    (lambda d: d.update(true_scale_shot_id="s2"), "плашк"),
    (_p(horizontal_exaggeration=1), "истинном масштабе"),
])
def test_invalid_params_fail_before_render(mut, needle):
    with pytest.raises(VideoInputError, match=needle):
        _prep(mut)


def test_wells_volume_and_graph_come_from_one_state():
    prep = _prep()
    for prog in (0.0, 0.4, 1.0):
        top = top_at(prep, prog)
        o, c = states(prep, top)
        cur = pressure_curves(prep, top)
        assert cur["open_state"] == o and cur["closed_state"] == c        # график — то же состояние, что скважины
        x = cur["x"]
        for s, key in ((o, "open"), (c, "closed")):
            # давление на устье и на забое графика = давления состояния; в пачке — давление газа
            assert cur[key][0] == pytest.approx((s["p_surface"] - P_ATM) / 1e6)
            assert cur[key][-1] == pytest.approx((s["p_bottom"] - P_ATM) / 1e6)
            in_gas = (x >= s["top"]) & (x <= s["bottom"])
            assert np.allclose(cur[key][in_gas], (s["p_gas"] - P_ATM) / 1e6)
            assert s["length"] == pytest.approx(s["volume"] / prep["model"].area)   # геометрия пачки = объём / сечение


def test_open_and_closed_differ_as_physics_says():
    prep = _prep()
    o0, c0 = states(prep, prep["top_start"])
    o1, c1 = states(prep, prep["top_stop"])
    assert o1["volume"] > o0["volume"] and c1["volume"] == pytest.approx(c0["volume"])
    assert o1["p_bottom"] < o0["p_bottom"] and c1["p_bottom"] > c0["p_bottom"]
    assert c1["p_surface"] > c0["p_surface"] and o1["p_surface"] == pytest.approx(P_ATM)
    cur = pressure_curves(prep, prep["top_stop"])
    assert np.all(cur["closed"] >= cur["initial"] - 1e-9)                 # закрытая: выше по всему стволу


def test_prediction_and_final_freeze_gas():
    from pipeline.video.timeline import progress_at, progress_knots
    prep = _prep(lambda d: d["params"].update(evolve_shot_ids=["s2", "s3", "s4"]))
    assert "p5" not in prep["evolve_phrase_ids"] and "p8" not in prep["evolve_phrase_ids"]
    segs, t = [], 0.3
    for p in SCRIPT.phrases:
        segs.append((p.id, t, t + 3.0))
        t += 3.0 + p.pause_after_s
    knots = progress_knots(segs, prep["evolve_phrase_ids"], 1.0)
    seg = {pid: (a, b) for pid, a, b in segs}
    frozen = progress_at(seg["p5"][0], knots)
    for tau in np.linspace(seg["p5"][0], seg["p6"][0], 20):              # весь вопрос и пауза
        assert progress_at(tau, knots) == pytest.approx(frozen)
    assert progress_at(seg["p6"][1], knots) > frozen                       # на ответе газ поднимается


def test_auto_checks_do_not_claim_what_is_not_shown():
    res = auto_checks(_prep())
    assert res["hydrostatic"][0] is None and "циркуляция" in res["hydrostatic"][1]   # частично — не «да»
    assert res["gas_open_closed"][0] is True and res["mass_balance"][0] is True


def test_initial_profile_keeps_constant_pressure_inside_gas():
    prep = _prep()
    cur = pressure_curves(prep, prep["top_stop"])
    x, p0 = cur["x"], cur["initial"]
    in_gas = x >= prep["top_start"]                                      # пачка у забоя до подъёма
    assert in_gas.sum() >= 3 and np.allclose(p0[in_gas], p0[in_gas][0])   # постоянное давление в газе
    straight = p0[0] + (p0[-1] - p0[0]) * x / x[-1]
    assert np.max(np.abs(p0 - straight)) > 0.1                           # не прямая между концами
