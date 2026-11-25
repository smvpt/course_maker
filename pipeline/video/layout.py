"""Компоновка в пикселях опорного кадра: 9:16 — 1080×1920 (так задан стайлгайд), 16:9 — 1920×1080.

Сцена Manim имеет высоту FRAME_H единиц при любом разрешении рендера, поэтому
пиксели опорного кадра переводятся в единицы сцены одинаково для черновика и финала.
Минимальный кегль стайлгайда задан «на кадре 1080 px» — это высота 16:9 и ширина 9:16;
в обоих опорных кадрах он одинаков в пикселях.
"""
from __future__ import annotations

REF_W, REF_H = 1080, 1920                  # 9:16 (по умолчанию)
REF_LONG = (1920, 1080)                    # 16:9
FRAME_H = 8.0
FRAME_W = FRAME_H * REF_W / REF_H
PT_PER_UNIT = 72  # Manim/Pango: кегль (em) в единицах сцены = font_size / 72 (замерено по Segoe UI)
# Безопасная зона 16:9 в стайлгайде не задана: допущение — title-safe 5 % (96 px по бокам, 54 сверху),
# снизу 100 px — место под элементы управления плеера.
LONG_SAFE_ZONE = {"top": 54, "bottom": 100, "side": 96}


class LayoutError(ValueError):
    pass


class Layout:
    def __init__(self, safe_zone: dict, min_caption_px: int, ref: tuple[int, int] = (REF_W, REF_H)):
        self.safe = {k: int(safe_zone[k]) for k in ("top", "bottom", "side")}
        self.min_caption_px = int(min_caption_px)
        self.ref_w, self.ref_h = ref
        self.frame_w = FRAME_H * self.ref_w / self.ref_h

    def units(self, px: float) -> float:
        return px * FRAME_H / self.ref_h

    def font_size(self, px: float) -> float:
        """font_size Manim для кегля px на опорном кадре; мельче минимума стайлгайда — ошибка."""
        if px < self.min_caption_px:
            raise LayoutError(f"кегль {px} px мельче минимума стайлгайда {self.min_caption_px} px")
        return self.units(px) * PT_PER_UNIT

    def safe_box(self) -> tuple[float, float, float, float]:
        """(left, right, bottom, top) безопасной зоны в единицах сцены."""
        return (-self.frame_w / 2 + self.units(self.safe["side"]),
                self.frame_w / 2 - self.units(self.safe["side"]),
                -FRAME_H / 2 + self.units(self.safe["bottom"]),
                FRAME_H / 2 - self.units(self.safe["top"]))

    def check_inside(self, name: str, left: float, right: float, bottom: float, top: float) -> None:
        sl, sr, sb, st = self.safe_box()
        eps = 1e-9
        if left < sl - eps or right > sr + eps or bottom < sb - eps or top > st + eps:
            px = lambda u: round(u / self.units(1))
            raise LayoutError(f"«{name}» выходит за безопасную зону {self.ref_w}×{self.ref_h} {self.safe} "
                              f"(px опорного кадра): x {px(left - sl)}…{px(right - sr)}, "
                              f"y {px(bottom - sb)}…{px(top - st)} относительно границ зоны")
