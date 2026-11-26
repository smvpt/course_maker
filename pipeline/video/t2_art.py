"""Векторные элементы схемы T2: текстура породы, кабельный прибор с секциями, лупа, выноски.

Всё — схема (метка «схема»): размеры прибора условные, литология не изображается (порода — однородная
текстура, границ пластов нет: их нет в данных). Цвета — из стайлгайда, переданы вызывающим кодом.
"""
from __future__ import annotations

import numpy as np
from manim import (Arc, Circle, Dot, Line, Polygon, Rectangle, RoundedRectangle, Text, VGroup)
from manim.utils.color import ManimColor


def rgba(hex_color: str, alpha: int = 255) -> np.ndarray:
    return np.array([*np.round(np.array(ManimColor(hex_color).to_rgb()) * 255), alpha], dtype=np.uint8)


def stipple(h: int, w: int, base: str, speck: str, density: float, size: int, seed: int,
            circle: bool = False, alpha: float = 1.0) -> np.ndarray:
    """RGBA-текстура породы: фон base и детерминированный крап speck, смешанный с фоном в доле alpha
    (без границ пластов — их нет в данных)."""
    rng = np.random.default_rng(seed)
    img = np.empty((h, w, 4), dtype=np.uint8)
    img[:] = rgba(base)
    n = int(h * w * density)
    ys, xs = rng.integers(0, h, n), rng.integers(0, w, n)
    sp = np.round(rgba(base).astype(float) * (1 - alpha) + rgba(speck).astype(float) * alpha).astype(np.uint8)
    for dy in range(size):
        for dx in range(size):
            img[np.clip(ys + dy, 0, h - 1), np.clip(xs + dx, 0, w - 1)] = sp
    if circle:
        yy, xx = np.mgrid[0:h, 0:w]
        r = min(h, w) / 2
        img[(yy - h / 2 + 0.5) ** 2 + (xx - w / 2 + 0.5) ** 2 > r * r, 3] = 0
    return img


def tool_detail(cx: float, top: float, bottom: float, width: float, sections: list[tuple[str, str]],
                c: dict) -> tuple[VGroup, list[np.ndarray]]:
    """Кабельный прибор вертикально от top до bottom: кабельная головка, секции (цвет кривой), центраторы,
    носовой обтекатель. Возвращает (фигура, точки привязки выносок — середины секций справа)."""
    g = VGroup()
    h = top - bottom
    head_h, nose_h = 0.12 * h, 0.08 * h
    w2 = width / 2
    # кабельная головка (конус) и переходник
    g.add(Polygon([cx - w2 * 0.45, top, 0], [cx + w2 * 0.45, top, 0], [cx + w2, top - head_h, 0],
                  [cx - w2, top - head_h, 0], stroke_color=c["text"], stroke_width=2, fill_color=c["muted"],
                  fill_opacity=1))
    body_top, body_bottom = top - head_h, bottom + nose_h
    n = len(sections)
    gap = 0.05 * h
    sec_h = (body_top - body_bottom - gap * (n - 1)) / n
    anchors = []
    for i, (kind, color) in enumerate(sections):
        st = body_top - i * (sec_h + gap)
        sb = st - sec_h
        g.add(RoundedRectangle(width=width, height=sec_h, corner_radius=width * 0.12, stroke_color=c["text"],
                               stroke_width=2, fill_color=color, fill_opacity=1).move_to([cx, (st + sb) / 2, 0]))
        if kind == "RES":                     # электроды — кольца
            for f in (0.25, 0.5, 0.75):
                y = st - f * sec_h
                g.add(Line([cx - w2, y, 0], [cx + w2, y, 0], color=c["background"], stroke_width=4))
        elif kind == "NEUTRON":               # источник и два детектора
            g.add(Circle(radius=width * 0.16, stroke_width=0, fill_color=c["background"], fill_opacity=1)
                  .move_to([cx, st - 0.22 * sec_h, 0]))
            for f in (0.55, 0.8):
                g.add(Rectangle(width=width * 0.4, height=sec_h * 0.12, stroke_width=0, fill_color=c["background"],
                                fill_opacity=1).move_to([cx, st - f * sec_h, 0]))
        else:                                 # детектор ГК — кристалл
            g.add(Rectangle(width=width * 0.35, height=sec_h * 0.45, stroke_width=0, fill_color=c["background"],
                            fill_opacity=0.85).move_to([cx, (st + sb) / 2, 0]))
        anchors.append(np.array([cx + w2, (st + sb) / 2, 0]))
        if i < n - 1:                         # центратор между секциями — две дуги-рессоры
            yc = sb - gap / 2
            g.add(Line([cx, sb, 0], [cx, sb - gap, 0], color=c["text"], stroke_width=6))
            for sgn in (-1, 1):
                g.add(Arc(radius=gap * 0.9, start_angle=-np.pi / 2 if sgn > 0 else np.pi / 2, angle=np.pi,
                          color=c["muted"], stroke_width=3).stretch(0.8, 0).move_to([cx + sgn * (w2 + gap * 0.25), yc, 0]))
    # носовой обтекатель
    g.add(Polygon([cx - w2, body_bottom, 0], [cx + w2, body_bottom, 0], [cx, bottom, 0], stroke_color=c["text"],
                  stroke_width=2, fill_color=c["muted"], fill_opacity=1))
    return g, anchors


def callout(text: Text, anchor: np.ndarray, box_center: np.ndarray, c: dict, pad: float) -> VGroup:
    """Выноска: плашка с текстом, линия к точке привязки и точка."""
    box = RoundedRectangle(width=text.width + 2 * pad, height=text.height + 1.4 * pad, corner_radius=pad,
                           stroke_color=c["muted"], stroke_width=2, fill_color=c["panel"], fill_opacity=0.95)
    box.move_to(box_center)
    text.move_to(box)
    edge = np.array([box.get_left()[0], box_center[1], 0])
    return VGroup(Line(anchor, edge, color=c["text"], stroke_width=2), Dot(anchor, radius=pad * 0.35,
                                                                        color=c["text"]), box, text)
