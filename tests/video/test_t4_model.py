"""T4: гидростатика и газовая пачка в открытой и закрытой скважине — одна модель состояния."""
import math

import numpy as np
import pytest

from pipeline.video.t4_model import G, P_ATM, WellModel

M = WellModel(depth_m=1500.0, mud_density=1200.0, gas_volume_m3=1.5, hole_diameter_m=0.2159)   # условные


def test_hydrostatic_grows_with_depth_and_density():
    x = np.array([0.0, 500.0, 1500.0])
    p = M.hydrostatic(x)
    assert p[0] == pytest.approx(P_ATM)                                   # на устье — атмосферное (абсолютное)
    assert p - P_ATM == pytest.approx(1200 * G * x)                       # избыточное = ρ·g·h
    heavy = WellModel(1500.0, 1500.0, 1.5, 0.2159)
    assert np.all(heavy.hydrostatic(x[1:]) > p[1:])                       # тяжелее раствор — выше давление


def test_initial_state_is_the_same_for_open_and_closed():
    o, c = M.state(M.start_top, closed=False), M.state(M.start_top, closed=True)
    for k in ("top", "length", "bottom", "volume", "p_gas", "p_surface", "p_bottom"):
        assert o[k] == pytest.approx(c[k])
    assert o["bottom"] == pytest.approx(1500.0) and o["volume"] == pytest.approx(1.5)
    assert o["p_surface"] == pytest.approx(P_ATM)
    # вес газа не учитывается: забой легче полного столба раствора ровно на ρ·g·L0
    assert o["p_bottom"] == pytest.approx(M.hydrostatic(np.array([1500.0]))[0] - 1200 * G * M.start_length)


def test_open_well_gas_expands_most_near_surface_and_displaces_mud():
    tops = np.linspace(M.start_top, 150.0, 60)
    v = np.array([M.state(t, closed=False)["volume"] for t in tops])
    assert np.all(np.diff(v) > 0)                                         # расширяется при подъёме
    dv = np.diff(v) / -np.diff(tops)                                      # прирост объёма на метр подъёма
    assert np.all(np.diff(dv) > 0)                                        # сильнее всего у устья
    s = M.state(150.0, closed=False)
    assert s["p_gas"] * s["volume"] == pytest.approx(M.state(M.start_top, False)["p_gas"] * 1.5)   # Бойль
    assert s["pit_gain"] == pytest.approx(s["volume"] - 1.5)              # вытеснено в ёмкость = расширение
    assert s["p_surface"] == pytest.approx(P_ATM)
    assert s["p_bottom"] < M.state(M.start_top, False)["p_bottom"]       # столб раствора короче — забой легче


def test_closed_well_gas_keeps_volume_and_raises_pressure_everywhere():
    s0, s = M.state(M.start_top, closed=True), M.state(150.0, closed=True)
    assert s["volume"] == pytest.approx(1.5) and s["p_gas"] == pytest.approx(s0["p_gas"])
    assert s["pit_gain"] == 0
    x = np.linspace(0, 1500, 301)
    assert np.all(M.profile(s, x) >= M.profile(s0, x) - 1e-6)            # давление выросло по всему стволу
    assert s["p_surface"] - s0["p_surface"] == pytest.approx(1200 * G * (s0["top"] - 150.0))
    assert s["p_bottom"] - s0["p_bottom"] == pytest.approx(1200 * G * (s0["top"] - 150.0))


def test_profile_is_consistent_with_state():
    for closed in (False, True):
        s = M.state(400.0, closed)
        x = np.array([0.0, s["top"], (s["top"] + s["bottom"]) / 2, s["bottom"], 1500.0])
        p = M.profile(s, x)
        assert p[0] == pytest.approx(s["p_surface"]) and p[-1] == pytest.approx(s["p_bottom"])
        assert p[1] == pytest.approx(s["p_gas"]) and p[2] == pytest.approx(s["p_gas"]) and p[3] == pytest.approx(s["p_gas"])
        assert s["length"] == pytest.approx(s["volume"] / (math.pi * 0.2159 ** 2 / 4))


def test_bad_parameters():
    base = dict(depth_m=1500.0, mud_density=1200.0, gas_volume_m3=1.5, hole_diameter_m=0.2159)
    for kw in (dict(depth_m=0), dict(mud_density=-1), dict(gas_volume_m3=0), dict(hole_diameter_m=float("nan")),
               dict(gas_volume_m3=500.0)):                                # пачка длиннее ствола
        with pytest.raises(ValueError):
            WellModel(**{**base, **kw})
    with pytest.raises(ValueError):
        M.state(-1.0, closed=False)
    with pytest.raises(ValueError):
        M.state(1499.0, closed=False)                                     # кровля ниже начального положения
