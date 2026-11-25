"""Шаблон «hello»: проверка конвейера, 9:16.

Всем кадром управляет одна переменная — время t (ValueTracker). Полоса хода
озвучки растёт только пока звучит фраза и стоит в паузах; подпись фразы видна
от её начала до начала следующей; последняя подпись держится до конца.
Границы фраз приходят из таймлайна, то есть из фактической длительности аудио.
"""
from __future__ import annotations

from manim import Rectangle, Scene, ValueTracker, always_redraw

from pipeline.video.layout import Layout
from pipeline.video.scene_parts import add_badges, add_captions, inside, play_timeline, wrap

TITLE_PX = 64


class HelloScene(Scene):
    plan: dict  # задаётся build.py перед render()

    def construct(self) -> None:
        p = self.plan
        lay: Layout = p["layout"]
        c, font, fps = p["colors"], p["font"], p["fps"]
        segs, total, speech_total = p["segments"], p["total"], p["speech_total"]
        left, right, _, _ = lay.safe_box()
        width = right - left
        t = ValueTracker(0.0)

        badge_bottom = add_badges(self, lay, segs, t, font)

        title = wrap(p["title"], font, lay.font_size(TITLE_PX), width, c["text"])
        title.move_to([0, badge_bottom - lay.units(40) - title.height / 2, 0])
        inside(lay, "заголовок", title)
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
        add_captions(self, lay, segs, t, font, c["text"])
        play_timeline(self, t, total, fps)
