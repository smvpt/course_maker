"""T2: проверка параметров до рендера, глубина прибора ↔ кривые, правило с пропусками."""
import copy
import json
from pathlib import Path

import numpy as np
import pytest

from contracts.models import SceneSpec, Script
from pipeline.video.inputs import VideoInputError
from pipeline.video.t2_template import curve_frac, depth_frac, prepare, revealed, rule_state, value_at
from pipeline.video.templates import load_template_config

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "fixtures" / "video" / "t2_demo"
CFG = load_template_config(ROOT / "domain" / "geology" / "templates", "T2")
SPEC = json.loads((FIX / "scene_spec.json").read_text(encoding="utf-8"))
SCRIPT = Script.model_validate_json((FIX / "script.json").read_text(encoding="utf-8"))


def _prep(mut=None):
    d = copy.deepcopy(SPEC)
    if mut:
        mut(d)
    return prepare(SceneSpec.model_validate(d), SCRIPT, CFG)


def test_demo_spec_is_valid():
    prep = _prep()
    assert [c["label"] for c in prep["curves"]] == ["ГК", "УЭС", "ННК"]
    assert prep["dataset"].label == "симуляция" and prep["rule"]["status_label"] == "условное правило"
    assert prep["exaggeration"] == 20 and prep["true_scale_shot_id"] == "s5"
    assert prep["evolve_phrase_ids"] == {"p2", "p3", "p4", "p5", "p6", "p7"}
    rt = next(c for c in prep["curves"] if c["mnemonic"] == "RT")
    assert rt["log"] and rt["unit_display"] == "Ом·м" and rt["range"][0] > 0


def _p(**kw):
    return lambda d: d["params"].update(**kw)


def _rule(**kw):
    return lambda d: d["params"]["rule"].update(**kw)


def _curve(i, **kw):
    return lambda d: d["params"]["curves"][i].update(**kw)


@pytest.mark.parametrize("mut,needle", [
    (lambda d: d["params"].pop("dataset"), "dataset"),
    (_p(dataset="fixtures/video/t2_demo/nope.json"), "не найдено"),
    (_curve(0, mnemonic="SP"), "SP"),                                   # кривой нет в наборе
    (_curve(1, unit="OHM.M"), "OHM.M"),                                 # единица не как в LAS
    (_curve(1, unit="KOHM"), "KOHM"),                                   # единица недопустима для вида
    (_curve(0, kind="GAMMA"), "GAMMA"),
    (_curve(0, label=""), "label"),
    (_p(curves=[]), "curves"),
    (_p(interval_m=[1100, 1000]), "interval_m"),
    (_p(interval_m=[990, 1100]), "интервал"),
    (_p(interval_m=[1062, 1066]), "короче"),
    (_rule(status="точное"), "status"),
    (_rule(conditions=[{"curve": "SP", "op": "<", "value": 1}]), "SP"),
    (_rule(conditions=[{"curve": "RT", "op": "≈", "value": 1}]), "op"),
    (_rule(conclusion="здесь нефть"), "не доказательство нефти"),
    (_rule(conclusion="высокое сопротивление доказывает продуктивность"), "не доказательство нефти"),
    (_rule(caveat=""), "caveat"),
    (_p(borehole_diameter_m=0.3), "borehole_diameter_m"),
    (_p(borehole_exaggeration=0.5), "borehole_exaggeration"),
    (_p(borehole_exaggeration=200), "шире"),
    (_p(evolve_shot_ids=["s9"]), "evolve_shot_ids"),
    (_p(extra_param=1), "extra_param"),
    (lambda d: d["shots"][1].update(label="реальные данные"), "не подтверждено"),
    (lambda d: d["shots"][1].update(frame_class="B", label="схема"), "класс A"),
    (lambda d: d["shots"][1].update(plaque="не в масштабе: ствол шире в 10 раз"), "20"),
    (lambda d: d.update(true_scale_shot_id=None), "true_scale_shot_id"),
    (lambda d: d.update(exaggerations=["ствол шире"]), "20"),
])
def test_invalid_spec_fails_before_render(mut, needle):
    with pytest.raises(VideoInputError, match=needle):
        _prep(mut)


def test_tool_and_curves_share_one_depth():
    prep = _prep()
    for d in (1000.0, 1017.3, 1050.0, 1064.0, 1100.0):
        for c in prep["curves"]:
            dep, val = revealed(prep, c["mnemonic"], d)
            assert dep.max() <= d + 1e-9                               # ничего глубже прибора
            nxt = prep["depth"][prep["depth"] > d + 1e-9]
            assert nxt.size == 0 or dep.size == np.searchsorted(prep["depth"], d, side="right")
        # одна и та же функция «глубина → положение» для прибора и для последнего отсчёта кривой
        assert depth_frac(prep, d) == pytest.approx((d - 1000) / 100)
    assert depth_frac(prep, 1000) == 0 and depth_frac(prep, 1100) == 1    # глубина растёт вниз


def test_gap_is_unknown_not_false_and_values_are_not_filled():
    prep = _prep()
    st = prep["rule_state"]
    d = prep["depth"]
    gap = (d >= 1024) & (d <= 1026)
    assert np.isnan(value_at(prep, "RT", 1025.0))
    assert np.all(st[gap] == -1)                                        # пропуск в пористом пласте — «нет данных»
    assert np.all(st[(d >= 1021) & (d <= 1029) & ~gap] == 1)            # там же, где запись есть, — правило выполнено
    assert np.all(st[(d >= 1062) & (d <= 1070)] == 0)                   # плотный: УЭС высокое, пористость мала


def test_rule_state_logic():
    depth = np.arange(4.0)
    vals = {"A": np.array([1.0, np.nan, 1.0, np.nan]), "B": np.array([5.0, 5.0, 0.0, 0.0])}
    conds = [{"curve": "A", "op": ">", "value": 0}, {"curve": "B", "op": ">", "value": 1}]
    assert list(rule_state(depth, vals, conds)) == [1, -1, 0, 0]


def test_curve_frac_log_and_linear():
    assert curve_frac(np.array([10.0]), (1.0, 100.0), True)[0] == pytest.approx(0.5)
    assert curve_frac(np.array([50.0]), (0.0, 100.0), False)[0] == pytest.approx(0.5)


# ---------------------------------------------------------------- ревью: диапазон, колонка решения

from pipeline.video.t2_template import decision_rows, display_range  # noqa: E402


@pytest.mark.parametrize("value", [0.5, 1.0, 7.3])
def test_constant_log_curve_gets_positive_range(value):
    v = np.full(10, value)
    lo, hi = display_range(v, log=True)
    assert 0 < lo < value < hi
    assert curve_frac(v, (lo, hi), True) == pytest.approx(np.full(10, 0.5))


@pytest.mark.parametrize("value", [-3.0, 0.0, 0.5, 1.0, 7.3])
def test_constant_linear_curve_gets_nonempty_range(value):
    lo, hi = display_range(np.full(5, value), log=False)
    assert lo < value < hi


def test_range_ignores_gaps():
    assert display_range(np.array([np.nan, 2.0, 8.0, np.nan]), log=True) == (2.0, 8.0)


def test_constant_rt_spec_is_valid(tmp_path):
    import hashlib
    text = (FIX / "synthetic_well.las").read_text(encoding="ascii").splitlines()
    a = next(i for i, l in enumerate(text) if l.startswith("~A"))
    for v in (0.5, 1.0, 12.0):
        rows = [f"{l.split()[0]} {l.split()[1]} {v} {l.split()[3]}" for l in text[a + 1:]]
        las = tmp_path / f"rt_{v}.las"
        las.write_text("\n".join(text[:a + 1] + rows) + "\n", encoding="ascii")
        desc = json.loads((FIX / "dataset.json").read_text(encoding="utf-8"))
        desc.update(las=str(las), sha256=hashlib.sha256(las.read_bytes()).hexdigest())
        dp = tmp_path / f"dataset_{v}.json"
        dp.write_text(json.dumps(desc, ensure_ascii=False), encoding="utf-8")
        prep = _prep(lambda d: d["params"].update(dataset=str(dp)))
        rt = next(c for c in prep["curves"] if c["mnemonic"] == "RT")
        assert 0 < rt["range"][0] < v < rt["range"][1]


def test_decision_rows_follow_actual_depths_with_uneven_step():
    depth = np.array([1000.0, 1001.0, 1005.0, 1006.0])
    state = np.array([1, 0, -1, 1])
    rows = decision_rows(depth, state, 1000.0, 1010.0, n_rows=100)     # 0,1 м на строку
    centers = 1000.0 + (np.arange(100) + 0.5) * 0.1
    expect = np.full(100, -2)                                           # -2 — нет отсчёта (вне записи)
    expect[(centers >= 1000.0) & (centers < 1000.5)] = 1                # ячейка 1000: до середины к 1001
    expect[(centers >= 1000.5) & (centers < 1003.0)] = 0                # 1001: от 1000,5 до 1003
    expect[(centers >= 1003.0) & (centers < 1005.5)] = -1               # 1005 (пропуск): 1003–1005,5
    expect[(centers >= 1005.5) & (centers <= 1006.0)] = 1               # 1006: до конца записи
    assert list(rows) == list(expect)
    assert (rows == -1).sum() == 25                                      # пропуск не сжался и не исчез


def test_decision_rows_of_demo_match_rule_state_at_sample_depths():
    prep = _prep()
    rows = decision_rows(prep["depth"], prep["rule_state"], prep["top"], prep["bottom"], n_rows=1000)
    for d, s in zip(prep["depth"][1:-1], prep["rule_state"][1:-1]):
        i = int((d - prep["top"]) / (prep["bottom"] - prep["top"]) * 1000)
        assert rows[min(i, 999)] == s
