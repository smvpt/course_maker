"""T1: проверка параметров SceneSpec до рендера и согласованность карты и графика."""
import json
from pathlib import Path

import numpy as np
import pytest

from contracts.models import SceneSpec, Script
from pipeline.video.inputs import VideoInputError
from pipeline.video.t1_template import field_values, load_config, prepare, profile

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "fixtures" / "video" / "t1_demo"
CFG = load_config(ROOT / "domain" / "geology" / "templates")


def _load(spec_mut=None):
    script = Script.model_validate_json((FIX / "script.json").read_text(encoding="utf-8"))
    d = json.loads((FIX / "scene_spec.json").read_text(encoding="utf-8"))
    if spec_mut:
        spec_mut(d)
    return SceneSpec.model_validate(d), script


def test_demo_params_are_valid():
    prep = prepare(*_load(), CFG)
    assert prep["exaggeration"] == 100 and prep["true_scale_shot_id"] == "s4"
    assert prep["evolve_phrase_ids"] == {"p2", "p3", "p4", "p5", "p6"}
    assert prep["exaggerated_shots"] == {"s1", "s2", "s3", "s5"}
    assert 0 < prep["r_influence_end"] < prep["r_max"]
    assert prep["color_max"] <= prep["graph_max"]


def _p(**kw):
    return lambda d: d["params"].update(**kw)


def _drop(key):
    return lambda d: d["params"].pop(key)


@pytest.mark.parametrize("mut,needle", [
    (_drop("kappa_m2_s"), "kappa_m2_s"),
    (_p(speed_m_s=3), "speed_m_s"),
    (_p(kappa_m2_s=0), "kappa_m2_s"),
    (_p(kappa_m2_s=-1), "kappa_m2_s"),
    (_p(kappa_m2_s=float("nan")), "kappa_m2_s"),
    (_p(kappa_m2_s="быстро"), "kappa_m2_s"),
    (_p(kappa_m2_s=True), "kappa_m2_s"),
    (_p(r_max_m=150), "выходит за окно"),
    (_p(r_max_m=5000), "не будет видно"),
    (_p(t_end_s=0.001), "неприменимо"),
    (_p(r_well_m=5), "r_well_m"),
    (_p(threshold_mpa=0), "threshold_mpa"),
    (_p(well_exaggeration=0.5), "well_exaggeration"),
    (_p(well_exaggeration=1000), "значок скважины"),
    (_p(evolve_shot_ids=["s9"]), "evolve_shot_ids"),
    (_p(evolve_shot_ids=[]), "evolve_shot_ids"),
    (lambda d: d["shots"][1].update(label="схема"), "симуляция"),
    (lambda d: d["shots"][1].update(label="реальные данные"), "симуляция"),
    (lambda d: d["shots"][1].update(plaque="не в масштабе: скважина крупнее в 50 раз"), "100"),
    (lambda d: d.update(exaggerations=["скважина крупнее"]), "100"),
    (lambda d: d.update(true_scale_shot_id=None), "true_scale_shot_id"),
    (lambda d: d.update(true_scale_shot_id="s2"), "плашк"),
    (lambda d: d.update(true_scale_shot_id="s9"), "s9"),
    (_p(well_exaggeration=1), "истинном масштабе"),
])
def test_invalid_params_fail_before_render(mut, needle):
    with pytest.raises(VideoInputError, match=needle):
        prepare(*_load(mut), CFG)


def test_field_and_graph_come_from_one_function():
    prep = prepare(*_load(), CFG)
    for t in (0.0, 600.0, prep["t_end"] / 2, prep["t_end"]):
        field, xs = field_values(prep, t)
        row = field[len(xs) // 2]                         # строка через скважину
        right = xs > prep["r_min"]
        r, dp = profile(prep, t)
        # значения карты на луче от скважины = кривая графика в тех же точках
        np.testing.assert_allclose(row[right], np.interp(xs[right], r, dp), rtol=2e-2, atol=1e-6)
        np.testing.assert_allclose(row[right], prep["model"].delta_p(xs[right], t), rtol=1e-12)


def test_initial_moment_is_undisturbed():
    prep = prepare(*_load(), CFG)
    field, _ = field_values(prep, 0.0)
    assert np.all(field == 0)
    assert np.all(profile(prep, 0.0)[1] == 0)
