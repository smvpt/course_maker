"""Общие элементы кадра для всех шаблонов: метка происхождения, плашка, подписи, ход времени.

Всё видимое — функция одной переменной tau (время ролика, ValueTracker), границы — из
звукового таймлайна (segments: phrase_id, shot_id, start, end, …).
"""
from __future__ import annotations

import math

from manim import DOWN, RoundedRectangle, Scene, Text, ValueTracker, VGroup, linear

from pipeline.video.layout import Layout, LayoutError

FADE_S = 0.2
LABEL_PX, PLAQUE_PX, CAPTION_PX = 44, 44, 52


def visibility(a: float, b: float, fade: float):
    def f(t: float) -> float:
        if t < a or t > b:
            return 0.0
        fin = 1.0 if fade == 0 else min(1.0, (t - a) / fade)
        fout = 1.0 if fade == 0 or math.isinf(b) else min(1.0, (b - t) / fade)
        return max(0.0, min(fin, fout))
    return f


def wrap(text: str, font: str, font_size: float, max_width: float, color: str) -> VGroup:
    """Переносит по словам так, чтобы каждая строка влезала в ширину; слово шире строки — ошибка."""
    lines: list[Text] = []
    cur: list[str] = []
    for word in text.split():
        trial = Text(" ".join(cur + [word]), font=font, font_size=font_size, color=color)
        if trial.width <= max_width:
            cur.append(word)
            continue
        if not cur:
            raise LayoutError(f"слово «{word}» шире безопасной зоны при кегле {font_size:.1f}")
        lines.append(Text(" ".join(cur), font=font, font_size=font_size, color=color))
        cur = [word]
    if cur:
        lines.append(Text(" ".join(cur), font=font, font_size=font_size, color=color))
    return VGroup(*lines).arrange(DOWN, buff=font_size / 72 * 0.25)


def inside(lay: Layout, name: str, m) -> None:
    lay.check_inside(name, m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1])


def shot_windows(segs: list[dict]) -> list[tuple[str, float, float]]:
    """(shot_id, начало, конец) окна каждого кадра: от его первой фразы до первой фразы следующего."""
    starts: list[tuple[str, float]] = []
    for s in segs:
        if not starts or starts[-1][0] != s["shot_id"]:
            starts.append((s["shot_id"], s["start"]))
    out = []
    for i, (sid, a) in enumerate(starts):
        out.append((sid, 0.0 if i == 0 else a, math.inf if i == len(starts) - 1 else starts[i + 1][1]))
    return out


def add_badges(scene: Scene, lay: Layout, segs: list[dict], tau: ValueTracker, font: str, add=None,
               fill: str | None = None) -> float:
    """Метка происхождения кадра в левом верхнем углу безопасной зоны. Возвращает её нижний край.
    add — куда добавить (служебный слой общего стиля; по умолчанию сцена); fill — подложка метки."""
    add = add or scene.add
    left, _, _, top = lay.safe_box()
    shot_label = {s["shot_id"]: (s["label"], s["label_color"]) for s in segs}
    bottom = top
    for sid, a, b in shot_windows(segs):
        text, color = shot_label[sid]
        label = Text(text, font=font, font_size=lay.font_size(LABEL_PX), color=color)
        pad = lay.units(14)
        box = RoundedRectangle(width=label.width + 2 * pad, height=label.height + 2 * pad,
                               corner_radius=pad, stroke_color=color, stroke_width=2,
                               fill_color=fill or color, fill_opacity=0.9 if fill else 0)
        badge = VGroup(box, label)
        badge.move_to([left + badge.width / 2, top - badge.height / 2, 0])
        label.move_to(box)
        inside(lay, "метка происхождения", badge)
        vis = visibility(a, b, 0.0)
        label.add_updater(lambda m, v=vis: m.set_opacity(v(tau.get_value())))
        box.add_updater(lambda m, v=vis, f=bool(fill): (m.set_stroke(opacity=v(tau.get_value())),
                                                        m.set_fill(opacity=0.9 * v(tau.get_value()) if f else 0)))
        add(badge)
        bottom = min(bottom, badge.get_bottom()[1])
    return bottom


def add_plaques(scene: Scene, lay: Layout, segs: list[dict], tau: ValueTracker, font: str, color: str,
                y_top: float, texts: dict[str, str | None], add=None, pill: str | None = None) -> float:
    """Плашка кадра (shot_id → текст или None) под меткой. Возвращает нижний край самой высокой.
    add — куда добавить (служебный слой); pill — цвет подложки-«таблетки» (общий стиль)."""
    add = add or scene.add
    pad = lay.units(12) if pill else 0.0
    left, right, _, _ = lay.safe_box()
    bottom = y_top
    for sid, a, b in shot_windows(segs):
        if not texts.get(sid):
            continue
        g = wrap(texts[sid], font, lay.font_size(PLAQUE_PX), right - left - 2 * pad, color)
        for line in g:
            line.align_to([left + pad, 0, 0], direction=[-1, 0, 0])
        if pill:
            box = RoundedRectangle(width=g.width + 2 * pad, height=g.height + 1.4 * pad, corner_radius=pad,
                                   stroke_width=0, fill_color=pill, fill_opacity=0.95).move_to(g)
            g = VGroup(box, g)
        g.move_to([g.get_center()[0], y_top - g.height / 2, 0])
        inside(lay, f"плашка {sid}", g)
        vis = visibility(a, b, 0.0)
        g.add_updater(lambda m, v=vis: m.set_opacity(v(tau.get_value())))
        add(g)
        bottom = min(bottom, g.get_bottom()[1])
    return bottom


def add_captions(scene: Scene, lay: Layout, segs: list[dict], tau: ValueTracker, font: str, color: str,
                 pill: str | None = None, add=None) -> float:
    """Ключевые слова фразы (on_screen) внизу безопасной зоны. Возвращает высоту самой высокой подписи.
    pill — цвет плашки-«таблетки» под подписью (None — без плашки)."""
    left, right, bottom, _ = lay.safe_box()
    h = 0.0
    pad = lay.units(18) if pill else 0.0
    for i, s in enumerate(segs):
        if not s["on_screen"]:
            continue
        cap = wrap(s["on_screen"], font, lay.font_size(CAPTION_PX), right - left - 2 * pad, color)
        if pill:
            box = RoundedRectangle(width=cap.width + 2 * pad, height=cap.height + 1.2 * pad, corner_radius=pad,
                                   stroke_width=0, fill_color=pill, fill_opacity=1).move_to(cap)
            cap = VGroup(box, cap)
        cap.move_to([0, bottom + cap.height / 2, 0])
        inside(lay, f"подпись {s['phrase_id']}", cap)
        b = math.inf if i == len(segs) - 1 else segs[i + 1]["start"]
        vis = visibility(s["start"], b, FADE_S)
        cap.add_updater(lambda m, v=vis: m.set_opacity(v(tau.get_value())))
        cap.set_opacity(0)
        (add or scene.add)(cap)
        h = max(h, cap.height)
    return h


def play_timeline(scene: Scene, tau: ValueTracker, total: float, fps: int) -> None:
    """Ровно round(total·fps) кадров: np.arange(0, (n-0.5)/fps, 1/fps) даёт n отсчётов, кадр k — tau = k/fps."""
    n = round(total * fps)
    rt = (n - 0.5) / fps
    scene.play(tau.animate(rate_func=linear).set_value(rt), run_time=rt)
