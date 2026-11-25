"""T3 «Рост тела»: модель проградации лопасти (дельта, клиноформа) с балансом объёма.

Профиль по радиусу r от точки питания (в плане — сектор с углом φ, разрез — по оси сектора):
    z(r) = 0                      при r ≤ R            кровля (топсет) на уровне моря
    z(r) = −(r − R)·tg θ          при R < r < R + L    фронтальный склон (форсет), L = h / tg θ
    z(r) = −h                     при r ≥ R + L        дно бассейна
Объём над дном бассейна: V(R) = φ·h·(R²/2 + R·L/2 + L²/6).
Приток осадка Q постоянен: V(R(t)) = V(R0) + Q·t → R(t) — положительный корень квадратного уравнения.

Допущения: уровень моря и глубина бассейна постоянны, погружения нет (кровля не наращивается вверх —
чистая проградация); угол склона постоянен, дно плоское; размыва и перерывов нет; лопасть симметрична.
Следствия: поверхность только наращивается — слои не пересекаются и не исчезают, молодые лежат на старых
и мористее; объём каждого слоя равен Q·Δt; береговая линия продвигается всё медленнее (объём растёт как R²).
Ограничения: не описывает вертикальный рост (риф, агградацию кровли), размыв, несогласия, уплотнение.
Единицы: м, годы, м³/год, градусы.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def _check(name: str, v: float, lo: float = 0.0, hi: float = math.inf, lo_open: bool = True) -> None:
    if not math.isfinite(v) or (v <= lo if lo_open else v < lo) or v > hi:
        raise ValueError(f"{name} = {v} вне допустимого диапазона ({lo}; {hi}]")


@dataclass(frozen=True)
class LobeModel:
    depth_m: float            # h — глубина бассейна, м
    angle_deg: float          # θ — угол фронтального склона, °
    supply_m3_per_yr: float   # Q — приток осадка, м³/год
    r0_m: float               # R0 — начальный радиус береговой линии, м
    lobe_deg: float = 180.0   # φ — угол раскрытия лопасти в плане, °

    def __post_init__(self) -> None:
        _check("depth_m", self.depth_m)
        _check("angle_deg", self.angle_deg, hi=45.0)
        _check("supply_m3_per_yr", self.supply_m3_per_yr)
        _check("r0_m", self.r0_m, lo_open=False)
        _check("lobe_deg", self.lobe_deg, hi=180.0)

    @property
    def foreset_length(self) -> float:
        """L = h / tg θ — горизонтальная длина фронтального склона, м."""
        return self.depth_m / math.tan(math.radians(self.angle_deg))

    def volume(self, R: float) -> float:
        h, L, phi = self.depth_m, self.foreset_length, math.radians(self.lobe_deg)
        return phi * h * (R * R / 2 + R * L / 2 + L * L / 6)

    def radius(self, t: float) -> float:
        """Радиус береговой линии R(t), м — единственное состояние, из которого строятся план и разрез."""
        if not math.isfinite(t) or t < 0:
            raise ValueError(f"время должно быть ≥ 0, получено {t}")
        h, L, phi = self.depth_m, self.foreset_length, math.radians(self.lobe_deg)
        a, b = phi * h / 2, phi * h * L / 2
        c = phi * h * L * L / 6 - (self.volume(self.r0_m) + self.supply_m3_per_yr * t)
        return (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)

    def surface(self, r: np.ndarray, t: float) -> np.ndarray:
        """Отметка поверхности z(r, t), м (уровень моря — 0, вниз — минус)."""
        r = np.asarray(r, dtype=float)
        R = self.radius(t)
        tg = math.tan(math.radians(self.angle_deg))
        return np.where(r <= R, 0.0, np.maximum(-(r - R) * tg, -self.depth_m))

    @staticmethod
    def layer_times(n: int, t_end: float) -> np.ndarray:
        """Границы слоёв по времени: n равных интервалов на [0, t_end]."""
        return np.linspace(0.0, t_end, n + 1)
