"""Шаблон «hello»: проверка конвейера, 9:16.

Всем кадром управляет одна переменная — время t (ValueTracker). Полоса хода
озвучки растёт только пока звучит фраза и стоит в паузах; подпись фразы видна
от её начала до начала следующей; последняя подпись держится до конца.
Границы фраз приходят из таймлайна, то есть из фактической длительности аудио.
"""
from __future__ import annotations

import math

from manim import DOWN, VGroup, Rectangle, RoundedRectangle, Scene, Text, ValueTracker, always_redraw, linear

from pipeline.video.layout import Layout, LayoutError

FADE_S = 0.2
LABEL_PX, TITLE_PX, CAPTION_PX = 44, 64, 52


def _visibility(a: float, b: float, fade: float):
    def f(t: float) -> float:
        if t < a or t > b:
            return 0.0
        fin = 1.0 if fade == 0 else min(1.0, (t - a) / fade)
        fout = 1.0 if fade == 0 or math.isinf(b) else min(1.0, (b - t) / fade)
        return max(0.0, min(fin, fout))
    return f


def _wrap(text: str, font: str, font_size: float, max_width: float, color: str) -> VGroup:
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


class HelloScene(Scene):
    plan: dict  # задаётся build.py перед render()

    def _inside(self, lay: Layout, name: str, m) -> None:
        lay.check_inside(name, m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1])

    def construct(self) -> None:
        p = self.plan
        lay: Layout = p["layout"]
        c, font, fps = p["colors"], p["font"], p["fps"]
        segs, total, speech_total = p["segments"], p["total"], p["speech_total"]
        left, right, bottom, top = lay.safe_box()
        width = right - left
        t = ValueTracker(0.0)

        # метки происхождения: по кадру SceneSpec, левый верхний угол безопасной зоны
        for i, s in enumerate(segs):
            a = 0.0 if i == 0 else s["start"]
            b = math.inf if i == len(segs) - 1 else segs[i + 1]["start"]
            label = Text(s["label"], font=font, font_size=lay.font_size(LABEL_PX), color=s["label_color"])
            pad = lay.units(14)
            box = RoundedRectangle(width=label.width + 2 * pad, height=label.height + 2 * pad,
                                   corner_radius=pad, stroke_color=s["label_color"], stroke_width=2)
            badge = VGroup(box, label)
            badge.move_to([left + badge.width / 2, top - badge.height / 2, 0])
            label.move_to(box)
            self._inside(lay, "метка происхождения", badge)
            vis = _visibility(a, b, 0.0)
            label.add_updater(lambda m, v=vis: m.set_opacity(v(t.get_value())))
            box.add_updater(lambda m, v=vis: m.set_stroke(opacity=v(t.get_value())))
            self.add(badge)
        badge_bottom = top - (badge.height if segs else 0)

        title = _wrap(p["title"], font, lay.font_size(TITLE_PX), width, c["text"])
        title.move_to([0, badge_bottom - lay.units(40) - title.height / 2, 0])
        self._inside(lay, "заголовок", title)
        self.add(title)

        # полоса хода озвучки
        bar_h = lay.units(18)
        track = Rectangle(width=width, height=bar_h, stroke_width=0,
                          fill_color=c["muted"], fill_opacity=0.35).move_to([0, 0, 0])

        def spoken(tv: float) -> float:
            return sum(min(max(tv - s["start"], 0.0), s["end"] - s["start"]) for s in segs)

        def fill():
            w = max(width * spoken(t.get_value()) / speech_total, 1e-4)
            return Rectangle(width=w, height=bar_h, stroke_width=0, fill_color=c["text"],
                             fill_opacity=1).move_to([left + w / 2, 0, 0])

        self.add(track, always_redraw(fill))

        # подписи фраз: ключевые слова (on_screen), низ безопасной зоны
        for i, s in enumerate(segs):
            if not s["on_screen"]:
                continue
            cap = _wrap(s["on_screen"], font, lay.font_size(CAPTION_PX), width, c["text"])
            cap.move_to([0, bottom + cap.height / 2, 0])
            self._inside(lay, f"подпись {s['phrase_id']}", cap)
            b = math.inf if i == len(segs) - 1 else segs[i + 1]["start"]
            vis = _visibility(s["start"], b, FADE_S)
            cap.add_updater(lambda m, v=vis: m.set_opacity(v(t.get_value())))
            cap.set_opacity(0)
            self.add(cap)

        # ровно n кадров: np.arange(0, (n-0.5)/fps, 1/fps) даёт n отсчётов, кадр k показывает t = k/fps
        n = round(total * fps)
        rt = (n - 0.5) / fps
        self.play(t.animate(rate_func=linear).set_value(rt), run_time=rt)
