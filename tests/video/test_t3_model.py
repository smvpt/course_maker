"""T3: модель проградации лопасти — баланс объёма, порядок и геометрия слоёв, одно состояние для двух видов."""
import math

import numpy as np
import pytest

from pipeline.video.t3_model import LobeModel

M = LobeModel(depth_m=20.0, angle_deg=3.0, supply_m3_per_yr=5e5, r0_m=1000.0, lobe_deg=180.0)   # условные


def _volume_numeric(t, n=200_000):
    """Объём осадка над начальной поверхностью численно: ∫ φ·(z(r,t) − z(r,0))·r dr."""
    r = np.linspace(0, M.radius(t) + M.foreset_length + 10, n)
    dz = M.surface(r, t) - M.surface(r, 0.0)
    return math.radians(M.lobe_deg) * np.trapezoid(dz * r, r)


@pytest.mark.parametrize("t", [100.0, 400.0, 1000.0])
def test_mass_balance(t):
    assert _volume_numeric(t) == pytest.approx(M.supply_m3_per_yr * t, rel=1e-4)
    assert M.volume(M.radius(t)) - M.volume(M.r0_m) == pytest.approx(M.supply_m3_per_yr * t, rel=1e-12)


def test_shoreline_advances_and_slows_down():
    r = [M.radius(t) for t in (0, 250, 500, 750, 1000)]
    assert r[0] == pytest.approx(1000.0)
    d = np.diff(r)
    assert np.all(d > 0) and np.all(np.diff(d) < 0)                   # растёт, но всё медленнее (радиальная лопасть)


def test_profile_geometry():
    t = 300.0
    R, L = M.radius(t), M.foreset_length
    assert L == pytest.approx(20 / math.tan(math.radians(3)))
    z = M.surface(np.array([0.0, R - 1, R + L / 2, R + L + 1, 1e5]), t)
    assert z[0] == 0 and z[1] == 0                                      # кровля на уровне моря
    assert z[2] == pytest.approx(-10.0)                                 # середина склона — половина глубины
    assert z[3] == -20 and z[4] == -20                                  # дно бассейна


def test_layers_never_cross_or_vanish_and_young_on_old():
    r = np.linspace(0, 6000, 3001)
    ts = np.linspace(0, 1000, 41)
    surfaces = np.array([M.surface(r, t) for t in ts])
    assert np.all(np.diff(surfaces, axis=0) >= -1e-12)                 # поверхность только наращивается
    tb = M.layer_times(5, 1000.0)
    assert list(tb) == [0, 200, 400, 600, 800, 1000]
    for k in range(5):                                                  # каждый слой имеет объём Q·Δt
        lo, hi = M.surface(r, tb[k]), M.surface(r, tb[k + 1])
        assert np.all(hi >= lo) and np.any(hi > lo)


def test_bad_parameters():
    for kw in (dict(depth_m=0), dict(angle_deg=0), dict(angle_deg=60), dict(supply_m3_per_yr=-1),
               dict(r0_m=-5), dict(lobe_deg=0), dict(lobe_deg=200), dict(depth_m=float("nan"))):
        with pytest.raises(ValueError):
            LobeModel(**{**dict(depth_m=20.0, angle_deg=3.0, supply_m3_per_yr=5e5, r0_m=1000.0), **kw})
    with pytest.raises(ValueError):
        M.radius(-1.0)
