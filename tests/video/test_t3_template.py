"""T3: параметры до озвучки, план и разрез из одного состояния, слои по возрасту."""
import copy
import json
from pathlib import Path

import numpy as np
import pytest

from contracts.models import SceneSpec, Script
from pipeline.video.inputs import VideoInputError
from pipeline.video.t3_template import auto_checks, layer_bands, plan_field, prepare, section_profile, shoreline_radii
from pipeline.video.templates import load_template_config

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "fixtures" / "video" / "t3_demo"
CFG = load_template_config(ROOT / "domain" / "geology" / "templates", "T3")
SPEC = json.loads((FIX / "scene_spec.json").read_text(encoding="utf-8"))
SCRIPT = Script.model_validate_json((FIX / "script.json").read_text(encoding="utf-8"))


def _prep(mut=None):
    d = copy.deepcopy(SPEC)
    if mut:
        mut(d)
    return prepare(SceneSpec.model_validate(d), SCRIPT, CFG)


def test_demo_spec_is_valid():
    prep = _prep()
    assert prep["n_layers"] == 5 and prep["exaggeration"] == 50 and prep["true_scale_shot_id"] == "s4"
    assert prep["r_end"] + prep["model"].foreset_length <= prep["r_max"]


def _p(**kw):
    return lambda d: d["params"].update(**kw)


@pytest.mark.parametrize("mut,needle", [
    (lambda d: d["params"].pop("depth_m"), "depth_m"),
    (_p(speed=1), "speed"),
    (_p(depth_m=0), "depth_m"),
    (_p(foreset_angle_deg=70), "foreset_angle_deg"),
    (_p(supply_m3_per_yr="много"), "supply_m3_per_yr"),
    (_p(n_layers=1), "n_layers"),
    (_p(n_layers=3.5), "n_layers"),
    (_p(n_layers=40), "n_layers"),
    (_p(lobe_angle_deg=270), "lobe_angle_deg"),
    (_p(r_max_m=3000), "за окно"),
    (_p(t_end_yr=1), "продвигается"),
    (_p(vertical_exaggeration=0.5), "vertical_exaggeration"),
    (_p(vertical_exaggeration=5000), "высот"),
    (_p(evolve_shot_ids=["s9"]), "evolve_shot_ids"),
    (lambda d: d["shots"][1].update(label="схема"), "симуляция"),
    (lambda d: d["shots"][1].update(label="реальные данные"), "симуляция"),
    (lambda d: d["shots"][1].update(plaque="не в масштабе: вертикаль увеличена в 10 раз"), "50"),
    (lambda d: d.update(true_scale_shot_id=None), "true_scale_shot_id"),
    (lambda d: d.update(true_scale_shot_id="s2"), "плашк"),
    (_p(vertical_exaggeration=1), "истинном масштабе"),
])
def test_invalid_params_fail_before_render(mut, needle):
    with pytest.raises(VideoInputError, match=needle):
        _prep(mut)


def test_plan_and_section_come_from_one_state():
    prep = _prep()
    for t in (0.0, 300.0, prep["t_end"]):
        z, xs, ys, inside = plan_field(prep, t)
        r_sec, z_sec = section_profile(prep, t)
        # ось лопасти в плане (x = 0, вниз) = разрез: те же отметки на тех же расстояниях
        col = np.argmin(np.abs(xs))
        axis_r, axis_z = -ys, z[:, col]
        np.testing.assert_allclose(axis_z, np.interp(axis_r, r_sec, z_sec), atol=1e-6)
        # граница тела (береговая линия) одна: в плане и в разрезе
        R = prep["model"].radius(t)
        topset_plan = axis_r[axis_z == 0].max()
        topset_sec = r_sec[z_sec == 0].max()
        step = (xs[1] - xs[0])
        assert abs(topset_plan - R) <= step and abs(topset_sec - R) <= r_sec[1] - r_sec[0]


def test_layers_appear_in_order_and_isochrons_match():
    prep = _prep()
    tb = prep["layer_times"]
    assert layer_bands(prep, 0.0) == []                                   # в начальный момент новых слоёв нет
    mid = (tb[2] + tb[3]) / 2
    bands = layer_bands(prep, mid)
    assert [b["k"] for b in bands] == [0, 1, 2] and bands[-1]["partial"] and not bands[0]["partial"]
    for b in bands:
        assert np.all(b["z_top"] >= b["z_bottom"] - 1e-12)
    for a, b in zip(bands, bands[1:]):                                    # молодой лежит на старом: низ = верх предыдущего
        np.testing.assert_allclose(b["z_bottom"], a["z_top"])
    radii = shoreline_radii(prep, mid)
    assert radii == pytest.approx([prep["model"].radius(t) for t in tb[:3]] + [prep["model"].radius(mid)])


def test_auto_checks_are_computed():
    res = auto_checks(_prep())
    assert res["layers_order"][0] is True and res["mass_balance"][0] is True
    assert "отн." in res["mass_balance"][1]


# ---------------------------------------------------------------- вопрос и финал не двигают модель

def test_prediction_and_final_phrases_do_not_move_the_model():
    from pipeline.video.timeline import progress_at, progress_knots
    # s3 = p4 (naming), p5 (prediction, пауза 1,2 с), p6 (data); s4 = p7 (final) — оба кадра в evolve_shot_ids
    prep = _prep(lambda d: d["params"].update(evolve_shot_ids=["s2", "s3", "s4"]))
    assert "p5" not in prep["evolve_phrase_ids"] and "p7" not in prep["evolve_phrase_ids"]
    assert {"p2", "p3", "p4", "p6"} <= prep["evolve_phrase_ids"]
    segs, t = [], 0.3
    for p in SCRIPT.phrases:                              # условные интервалы звучания: 3 с на фразу + пауза
        segs.append((p.id, t, t + 3.0))
        t += 3.0 + p.pause_after_s
    knots = progress_knots(segs, prep["evolve_phrase_ids"], prep["t_end"])
    st = lambda tau: progress_at(tau, knots)
    seg = {pid: (a, b) for pid, a, b in segs}
    q_start, q_end = seg["p5"]
    answer_start, answer_end = seg["p6"]
    frozen = st(q_start)
    for tau in np.linspace(q_start, answer_start, 25):    # весь вопрос и пауза перед ответом
        assert st(tau) == pytest.approx(frozen)
    assert st(answer_end) > frozen                        # на ответе рост продолжается
    f_start, f_end = seg["p7"]
    assert st(f_end) == pytest.approx(st(f_start)) == pytest.approx(prep["t_end"])   # финал стоит
