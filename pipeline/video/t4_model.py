"""T4 «Ствол скважины»: гидростатика и подъём газовой пачки в открытой и закрытой скважине.

Состояние — глубина кровли газовой пачки z_t (м). Из неё одна модель считает геометрию пачки, объём газа,
вытесненный раствор и профиль давления по стволу — для открытой и для закрытой скважины.

Допущения: вертикальный ствол постоянного сечения A = π·d²/4; раствор несжимаем, плотность ρ постоянна;
одна газовая пачка во всё сечение; газ идеальный, изотермический (Бойль: p·V = const), вес газа не учитывается;
циркуляции нет (статика), трения нет; стенки и колонна жёсткие. Начальное состояние — пачка объёма V0 у забоя,
уравновешенная столбом раствора: давление в пачке p_g0 = p_атм + ρ·g·(D − L0), L0 = V0/A.
Уравнения (давления абсолютные, Па):
  гидростатика     p(x) = p_устье + ρ·g·x                           выше пачки
  открытая         p_устье = p_атм, p_g = p_атм + ρ·g·z_t, V = p_g0·V0 / p_g, вытеснено в ёмкость ΔV = V − V0
  закрытая         V = V0, p_g = p_g0, p_устье = p_g − ρ·g·z_t
  в пачке          p = p_g;   ниже пачки  p(x) = p_g + ρ·g·(x − z_низ),  z_низ = z_t + V/A
Избыточное давление = абсолютное − p_атм.
Ограничения: нет циркуляции, растворения газа, сжимаемости раствора и колонны, температурного профиля; модель
открытой скважины верна, пока пачка помещается в ствол (выброс раствора не моделируется); скорость всплытия
газа не моделируется — глубина пачки задаётся ходом ролика.
Единицы: м, кг/м³, м³, Па (в кадре — МПа).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

G = 9.80665          # м/с²
P_ATM = 101_325.0    # Па, нормальное атмосферное давление


def _positive(name: str, v: float) -> float:
    v = float(v)
    if not math.isfinite(v) or v <= 0:
        raise ValueError(f"{name} должно быть конечным числом > 0, получено {v}")
    return v


@dataclass(frozen=True)
class WellModel:
    depth_m: float           # D — глубина ствола, м
    mud_density: float       # ρ — плотность раствора, кг/м³
    gas_volume_m3: float     # V0 — объём газовой пачки у забоя, м³
    hole_diameter_m: float   # d — диаметр ствола, м

    def __post_init__(self) -> None:
        for k in ("depth_m", "mud_density", "gas_volume_m3", "hole_diameter_m"):
            _positive(k, getattr(self, k))
        if self.start_length >= self.depth_m:
            raise ValueError(f"газовая пачка ({self.start_length:.0f} м) длиннее ствола ({self.depth_m:g} м)")

    @property
    def area(self) -> float:
        return math.pi * self.hole_diameter_m ** 2 / 4

    @property
    def start_length(self) -> float:
        return self.gas_volume_m3 / self.area

    @property
    def start_top(self) -> float:
        """Глубина кровли пачки в начальный момент (пачка у забоя)."""
        return self.depth_m - self.start_length

    @property
    def p_gas0(self) -> float:
        return P_ATM + self.mud_density * G * self.start_top

    def hydrostatic(self, x: np.ndarray) -> np.ndarray:
        """Абсолютное давление столба раствора без газа: p_атм + ρ·g·x."""
        return P_ATM + self.mud_density * G * np.asarray(x, dtype=float)

    def state(self, top_m: float, closed: bool) -> dict:
        """Состояние при глубине кровли пачки top_m: геометрия, объём и давления (абсолютные, Па)."""
        if not math.isfinite(top_m) or top_m < 0 or top_m > self.start_top + 1e-9:
            raise ValueError(f"кровля пачки должна быть в 0…{self.start_top:.1f} м, получено {top_m}")
        rg = self.mud_density * G
        if closed:
            p_gas, volume = self.p_gas0, self.gas_volume_m3
            p_surface = p_gas - rg * top_m
        else:
            p_gas = P_ATM + rg * top_m
            volume = self.p_gas0 * self.gas_volume_m3 / p_gas
            p_surface = P_ATM
        length = volume / self.area
        bottom = top_m + length
        return {"top": top_m, "length": length, "bottom": bottom, "volume": volume, "p_gas": p_gas,
                "p_surface": p_surface, "p_bottom": p_gas + rg * (self.depth_m - bottom),
                "pit_gain": volume - self.gas_volume_m3, "closed": closed}

    def profile(self, s: dict, x: np.ndarray) -> np.ndarray:
        """Абсолютное давление по глубине x для состояния s — та же модель, что геометрия и объём."""
        x = np.asarray(x, dtype=float)
        rg = self.mud_density * G
        return np.where(x < s["top"], s["p_surface"] + rg * x,
                        np.where(x <= s["bottom"], s["p_gas"], s["p_gas"] + rg * (x - s["bottom"])))
