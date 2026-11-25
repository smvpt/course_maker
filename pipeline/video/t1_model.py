"""T1 «Распространение давления»: расчётная модель.

Модель — уравнение пьезопроводности в радиальной постановке:

    ∂p/∂t = κ · (1/r) · ∂/∂r (r · ∂p/∂r)

Допущения: бесконечный однородный изотропный горизонтальный пласт постоянной толщины,
однофазная слабосжимаемая жидкость, κ постоянна; скважина — линейный источник в r = 0,
с момента t = 0 отбирает жидкость с постоянным дебитом q.
Начальное условие: p(r, 0) = p0 всюду.
Граничные: p → p0 при r → ∞; r·∂p/∂r → q·μ/(2π·k·h) при r → 0 (постоянный приток).
Решение (линейный источник):

    Δp(r, t) = p0 − p(r, t) = A · E1(r² / (4·κ·t)),   A = q·μ / (4π·k·h)

E1 — интегральная показательная функция. Единицы: r — м, t — с, κ — м²/с, A и Δp — МПа.
Ограничения: нет границ пласта, скин-фактора и объёма ствола; у самой скважины решение
верно при r_w² / (4·κ·t) ≪ 1. Это диффузия: возмущение есть сразу всюду и затухает
с расстоянием, резкого фронта нет.

«Радиус влияния» здесь — условная граница, где Δp равно выбранному порогу δ:
E1(x*) = δ/A, r*(t) = √(4·κ·t·x*), то есть r* растёт как √t (а не линейно).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import brentq
from scipy.special import exp1

EULER_GAMMA = 0.5772156649015329


def _positive(name: str, v: float) -> float:
    v = float(v)
    if not math.isfinite(v) or v <= 0:
        raise ValueError(f"{name} должно быть конечным числом > 0, получено {v}")
    return v


@dataclass(frozen=True)
class PressureModel:
    kappa: float       # пьезопроводность, м²/с
    scale_mpa: float   # A = q·μ / (4π·k·h), МПа

    def __post_init__(self) -> None:
        _positive("kappa", self.kappa)
        _positive("scale_mpa", self.scale_mpa)

    def delta_p(self, r: np.ndarray, t: float) -> np.ndarray:
        """Падение давления Δp(r, t), МПа. Одна функция и для поля, и для графика."""
        r = np.asarray(r, dtype=float)
        if not math.isfinite(t) or t < 0:
            raise ValueError(f"время должно быть ≥ 0, получено {t}")
        if np.any(r <= 0):
            raise ValueError("расстояние до скважины должно быть > 0 (в r = 0 решение особое)")
        if t == 0:
            return np.zeros_like(r)
        return self.scale_mpa * exp1(r ** 2 / (4 * self.kappa * t))

    def x_star(self, threshold_mpa: float) -> float:
        """Корень E1(x) = δ/A — безразмерная координата условной границы."""
        ratio = _positive("threshold_mpa", threshold_mpa) / self.scale_mpa
        f = lambda u: exp1(math.exp(u)) - ratio      # ищем в log x: E1 монотонно убывает
        lo, hi = -700.0, 6.5
        if f(lo) < 0 or f(hi) > 0:
            raise ValueError(f"порог {threshold_mpa} МПа недостижим при масштабе {self.scale_mpa} МПа")
        return math.exp(brentq(f, lo, hi, xtol=1e-14, rtol=1e-14))

    def influence_radius(self, t: float, threshold_mpa: float) -> float:
        """Условный радиус влияния: где Δp = порог. Не физический фронт."""
        x = self.x_star(threshold_mpa)
        if t < 0:
            raise ValueError(f"время должно быть ≥ 0, получено {t}")
        return math.sqrt(4 * self.kappa * t * x) if t > 0 else 0.0


# время симуляции по звуку — общая функция таймлайна (используется и T2)
from pipeline.video.timeline import progress_at as sim_time, progress_knots as sim_time_knots  # noqa: E402,F401
