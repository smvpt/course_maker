"""T1: решение уравнения пьезопроводности (линейный источник) на контрольных случаях."""
import math

import numpy as np
import pytest

from pipeline.video.t1_model import EULER_GAMMA, PressureModel, sim_time_knots, sim_time

M = PressureModel(kappa=0.5, scale_mpa=0.2)   # тестовые значения, не факты


def _laplacian_radial(m, r, t, h):
    f = lambda rr: m.delta_p(np.array([rr]), t)[0]
    d1 = (f(r + h) - f(r - h)) / (2 * h)
    d2 = (f(r + h) - 2 * f(r) + f(r - h)) / h ** 2
    return d2 + d1 / r


@pytest.mark.parametrize("r,t", [(5.0, 100.0), (20.0, 500.0), (40.0, 3000.0)])
def test_solution_satisfies_diffusivity_equation(r, t):
    # dΔp/dt = κ (1/r) d/dr (r dΔp/dr) — то же уравнение для Δp = p0 - p
    dt = t * 1e-4
    dpdt = (M.delta_p(np.array([r]), t + dt)[0] - M.delta_p(np.array([r]), t - dt)[0]) / (2 * dt)
    rhs = M.kappa * _laplacian_radial(M, r, t, r * 1e-3)
    assert dpdt == pytest.approx(rhs, rel=1e-3)


def test_source_condition_constant_rate_near_well():
    # r dΔp/dr -> -2A при r -> 0: постоянный приток к линейному источнику
    t, r, h = 1000.0, 0.01, 1e-5
    d = (M.delta_p(np.array([r + h]), t)[0] - M.delta_p(np.array([r - h]), t)[0]) / (2 * h)
    assert r * d == pytest.approx(-2 * M.scale_mpa, rel=1e-3)


def test_log_approximation_for_small_argument():
    # E1(x) ≈ -γ - ln x при x << 1 (приближение логарифмического профиля)
    r, t = 0.5, 1e5
    x = r ** 2 / (4 * M.kappa * t)
    assert M.delta_p(np.array([r]), t)[0] == pytest.approx(M.scale_mpa * (-EULER_GAMMA - math.log(x)), rel=1e-5)


def test_initial_state_and_far_field():
    r = np.linspace(0.1, 100, 50)
    assert np.all(M.delta_p(r, 0.0) == 0)                 # t = 0: пласт не возмущён
    assert M.delta_p(np.array([1e4]), 10.0)[0] == 0        # далеко — возмущения нет
    p = M.delta_p(r, 200.0)
    assert np.all(np.diff(p) < 0)                           # убывает с расстоянием
    assert np.all(M.delta_p(r, 400.0) > p)                  # растёт со временем


def test_influence_radius_is_threshold_defined_and_grows_as_sqrt_t():
    thr = 0.05
    r1, r4, r9 = (M.influence_radius(t, thr) for t in (100.0, 400.0, 900.0))
    assert M.delta_p(np.array([r1]), 100.0)[0] == pytest.approx(thr, rel=1e-9)
    assert r4 / r1 == pytest.approx(2.0, rel=1e-9)
    assert r9 / r1 == pytest.approx(3.0, rel=1e-9)
    assert M.influence_radius(0.0, thr) == 0.0


def test_not_a_constant_speed_ring():
    thr = 0.05
    r = [M.influence_radius(t, thr) for t in (100.0, 200.0, 300.0)]
    assert r[1] - r[0] > r[2] - r[1]                       # замедляется, а не идёт с постоянной скоростью


@pytest.mark.parametrize("kw", [dict(kappa=0, scale_mpa=1), dict(kappa=1, scale_mpa=-1),
                                dict(kappa=float("nan"), scale_mpa=1), dict(kappa=float("inf"), scale_mpa=1)])
def test_bad_model_params(kw):
    with pytest.raises(ValueError):
        PressureModel(**kw)


def test_bad_arguments():
    with pytest.raises(ValueError):
        M.delta_p(np.array([1.0]), -1.0)
    with pytest.raises(ValueError):
        M.delta_p(np.array([0.0, 1.0]), 10.0)
    with pytest.raises(ValueError):
        M.influence_radius(10.0, 0.0)


# ---------------------------------------------------------------- время симуляции по звуку

SEGS = [("p1", 0.3, 2.3), ("p2", 3.0, 6.0), ("p3", 7.2, 9.2), ("p4", 9.2, 12.2)]


def test_sim_time_runs_only_while_evolving_phrases_sound():
    knots = sim_time_knots(SEGS, {"p2", "p3"}, t_end=1000.0)
    st = lambda tau: sim_time(tau, knots)
    assert st(0.0) == 0 and st(2.9) == 0                    # до первой «живой» фразы — начальный момент
    assert st(4.5) == pytest.approx(300.0)                  # 1.5 с из 5 с речи
    assert st(6.5) == st(7.1) == pytest.approx(600.0)       # пауза: время стоит
    assert st(9.2) == pytest.approx(1000.0)
    assert st(11.0) == st(50.0) == 1000.0                    # финальное состояние держится
    taus = np.linspace(0, 13, 200)
    assert np.all(np.diff([st(x) for x in taus]) >= 0)


def test_sim_time_needs_an_evolving_phrase():
    with pytest.raises(ValueError):
        sim_time_knots(SEGS, set(), t_end=10.0)
