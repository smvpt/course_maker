"""Шаблон T4 «Ствол скважины», 9:16: открытая и закрытая скважина и график давления из одного состояния.

Одна переменная — время ролика tau — через progress_at задаёт прогресс подъёма газа, а он — глубину кровли
пачки. Из неё t4_template.states/pressure_curves (одна модель WellModel) считают пачку в обеих скважинах,
объём газа, вытесненный раствор и профили давления. Скважины и график делят функцию «глубина → y».
Конструкция обеих скважин одинакова во всех кадрах; превентор — схема из assets/video (SVG), у закрытой
скважины плашки сомкнуты. Давление на графике и в подписях — избыточное.
"""
from __future__ import annotations

import numpy as np
from manim import (DashedVMobject, Line, Rectangle, Scene, SVGMobject, Text, ValueTracker, VGroup, VMobject,
                   always_redraw)

from pipeline.video.layout import Layout, LayoutError
from pipeline.video.scene_parts import add_badges, add_captions, add_plaques, inside, play_timeline, shot_windows, wrap
from pipeline.video.t1_template import fmt_num, nice_ceil
from pipeline.video.t4_model import P_ATM
from pipeline.video.t4_template import pressure_curves, states, top_at
from pipeline.video.timeline import progress_at, progress_knots

TEXT_PX = 44
GAP_PX = 24
COL_PX = 190
BOP_PX = 70


class T4Scene(Scene):
    plan: dict  # задаётся build.py перед render()

    def construct(self) -> None:
        p = self.plan
        lay: Layout = p["layout"]
        prep = p["t4"]
        m = prep["model"]
        c, font, fps, segs = p["colors"], p["font"], p["fps"], p["segments"]
        fs = lay.font_size(TEXT_PX)
        u = lay.units
        gap = u(GAP_PX)
        left, right, bottom, top = lay.safe_box()
        width = right - left
        txt = lambda s, color=None: Text(s, font=font, font_size=fs, color=color or c["text"])
        text_h = txt("Жу0").height
        tau = ValueTracker(0.0)
        knots = progress_knots([(s["phrase_id"], s["start"], s["end"]) for s in segs], prep["evolve_phrase_ids"], 1.0)
        gas_top = lambda: top_at(prep, progress_at(tau.get_value(), knots))
        windows = shot_windows(segs)

        def shot_now() -> str:
            tv = tau.get_value()
            return next((sid for sid, a, b in windows if a <= tv < b), windows[-1][0])

        cache: dict[str, Text] = {}

        def cached(s: str, color=None) -> Text:
            key = f"{s}|{color}"
            if key not in cache:
                cache[key] = txt(s, color)
            return cache[key].copy()

        # ---- верх: метка, кровля газа, плашка
        badge_bottom = add_badges(self, lay, segs, tau, font)

        def readout_top():
            mm = cached(f"кровля газа: {fmt_num(gas_top(), 4)} м")
            return mm.move_to([right - mm.width / 2, (top + badge_bottom) / 2, 0])

        self.add(always_redraw(readout_top))
        plaque_texts = {sid: next(s["plaque"] for s in segs if s["shot_id"] == sid) for sid, _, _ in windows}
        ts = prep["true_scale_shot_id"]
        if ts is not None:
            plaque_texts[ts] = "истинный масштаб: ствол не расширен"
        plaque_top = badge_bottom - gap / 2
        plaque_h = max([wrap(t_, font, fs, width, c["text"]).height for t_ in plaque_texts.values() if t_] + [0.0])
        add_plaques(self, lay, segs, tau, font, c["text"], plaque_top, plaque_texts)

        # ---- вертикальная разметка
        cap_h = add_captions(self, lay, segs, tau, font, c["text"])
        note_text = f"давление избыточное; абсолютное = избыточное + {fmt_num(P_ATM / 1e6, 3)} МПа"
        note_g = wrap(note_text, font, fs, width, c["muted"])
        legend_g = wrap("толсто — закрытая, тонко — открытая, пунктир — до подъёма газа", font, fs, width, c["muted"])
        n_rows = 4                                                       # четыре строки значений
        rows_h = n_rows * (text_h + gap / 2) + legend_g.height + gap / 2 + note_g.height + gap / 2
        header_top = plaque_top - plaque_h - gap
        col_top = header_top - text_h - gap / 2 - u(BOP_PX) - gap / 2    # устье
        col_bottom = bottom + cap_h + gap + rows_h + gap + text_h + gap / 2   # + строка подписей оси давления
        col_h = col_top - col_bottom
        if col_h < u(420):
            raise LayoutError(f"стволу T4 не хватает высоты: {col_h / u(1):.0f} px опорного кадра")
        y_of = lambda d: col_top - np.asarray(d) / m.depth_m * col_h     # общая функция «глубина → y»
        px_per_m = (col_h / u(1)) / m.depth_m

        # ---- колонки: открытая, закрытая, график
        cw = u(COL_PX)
        cols = {"open": left + cw / 2, "closed": left + cw + gap + cw / 2}
        g_left = left + 2 * cw + 2 * gap + u(16)
        g_right = right - u(8)
        names = {"open": "открытая", "closed": "закрытая"}
        for key, cx in cols.items():
            h_ = txt(names[key], c["muted"])
            h_.move_to([cx, header_top - text_h / 2, 0])
            inside(lay, "подпись скважины", h_)
            self.add(h_)
            ground = Line([cx - cw / 2, col_top, 0], [cx + cw / 2, col_top, 0], color=c["muted"], stroke_width=3)
            self.add(ground)

        # конструкция одинакова в обеих скважинах; ширина — по кадру (увеличение только на кадрах с плашкой)
        def well(key: str, cx: float):
            sid = shot_now()
            k = prep["exaggeration"] if sid in prep["exaggerated_shots"] else 1.0
            w = max(u(m.hole_diameter_m * k * px_per_m), u(1.5))
            o, cl = states(prep, gas_top())
            s = o if key == "open" else cl
            g = VGroup()
            g.add(Rectangle(width=w, height=col_h, stroke_width=0, fill_color=c["mud"], fill_opacity=1)
                  .move_to([cx, (col_top + col_bottom) / 2, 0]))
            gy0, gy1 = float(y_of(s["top"])), float(y_of(min(s["bottom"], m.depth_m)))
            g.add(Rectangle(width=w, height=max(gy0 - gy1, u(2)), stroke_width=0, fill_color=c["gas"], fill_opacity=1)
                  .move_to([cx, (gy0 + gy1) / 2, 0]))
            if prep["casing_shoe"] is not None:
                ys = float(y_of(prep["casing_shoe"]))
                for sx in (-1, 1):
                    g.add(Line([cx + sx * w / 2, col_top, 0], [cx + sx * w / 2, ys, 0], color=c["casing"], stroke_width=3))
                    g.add(Line([cx + sx * (w / 2 + u(6)), ys, 0], [cx + sx * w / 2, ys, 0], color=c["casing"], stroke_width=3))
            return g

        for key, cx in cols.items():
            self.add(always_redraw(lambda key=key, cx=cx: well(key, cx)))
            bop = SVGMobject(p["equipment_svg"]).set_stroke(color=c["text"], width=2).set_fill(opacity=0)
            bop.scale_to_fit_height(u(BOP_PX)).move_to([cx, col_top + u(BOP_PX) / 2, 0])
            ram_w, ram_h = bop.width * 0.18, bop.height * 0.22
            shift = 0.0 if key == "closed" else bop.width * 0.18      # плашки: сомкнуты / разведены
            rams = VGroup(*(Rectangle(width=ram_w, height=ram_h, stroke_width=0, fill_color=c["text"], fill_opacity=1)
                            .move_to([cx + sx * (ram_w / 2 + shift), bop.get_center()[1], 0]) for sx in (-1, 1)))
            inside(lay, "превентор", bop)
            self.add(bop, rams)

        # ---- график избыточного давления по глубине (та же модель, та же глубина → y)
        p_end = pressure_curves(prep, prep["top_stop"])
        p_max = nice_ceil(float(max(p_end["closed"].max(), p_end["open"].max(), p_end["initial"].max())))
        x_of = lambda mpa: g_left + np.asarray(mpa) / p_max * (g_right - g_left)
        g_head = txt("давление, МПа", c["muted"])
        g_head.move_to([g_right - g_head.width / 2, header_top - text_h / 2, 0])
        axis_y = Line([g_left, col_top, 0], [g_left, col_bottom, 0], color=c["muted"], stroke_width=2)
        axis_x = Line([g_left, col_top, 0], [g_right, col_top, 0], color=c["muted"], stroke_width=2)
        self.add(g_head, axis_y, axis_x)
        for v in (0.0, p_max / 2, p_max):
            t_ = txt(fmt_num(v), c["muted"])
            t_.move_to([min(float(x_of(v)), g_right - t_.width / 2), col_bottom - gap / 2 - text_h / 2, 0])
            inside(lay, "шкала давления", t_)
            self.add(t_)
        for dv in (0.0, m.depth_m):
            t_ = txt(f"{fmt_num(dv)} м", c["muted"])
            t_.move_to([g_left + u(8) + t_.width / 2, float(y_of(dv)) + (-1 if dv == 0 else 1) * (text_h / 2 + u(6)), 0])
            self.add(t_)

        def curves():
            cur = pressure_curves(prep, gas_top())
            pts = lambda arr: np.column_stack([x_of(arr), y_of(cur["x"]), np.zeros(cur["x"].size)])
            g = VGroup()
            # профиль до подъёма газа — все точки модели, с участком постоянного давления внутри пачки у забоя
            g.add(DashedVMobject(VMobject(stroke_color=c["muted"], stroke_width=2).set_points_as_corners(pts(cur["initial"])),
                                 num_dashes=60))
            g.add(VMobject(stroke_color=c["pressure"], stroke_width=6).set_points_as_corners(pts(cur["closed"])))
            open_line = VMobject(stroke_color=c["pressure"], stroke_width=3).set_points_as_corners(pts(cur["open"]))
            g.add(open_line)
            return g

        self.add(always_redraw(curves))
        for name, mob in (("заголовок графика", g_head),):
            inside(lay, name, mob)

        # ---- значения из той же модели и пояснение
        rows_top = col_bottom - gap - text_h - gap / 2
        mpa = lambda pa: fmt_num((pa - P_ATM) / 1e6, 3)

        def rows():
            o, cl = states(prep, gas_top())
            lines = [f"газ, м³: откр. {fmt_num(o['volume'], 3)} · закр. {fmt_num(cl['volume'], 3)}",
                     f"устье, МПа: откр. {mpa(o['p_surface'])} · закр. {mpa(cl['p_surface'])}",
                     f"забой, МПа: откр. {mpa(o['p_bottom'])} · закр. {mpa(cl['p_bottom'])}",
                     f"в ёмкость вытеснено: {fmt_num(o['pit_gain'], 3)} м³ (откр.)"]
            g = VGroup()
            for i, s in enumerate(lines):
                mm = cached(s)
                g.add(mm.move_to([left + mm.width / 2, rows_top - i * (text_h + gap / 2) - text_h / 2, 0]))
            return g

        self.add(always_redraw(rows))
        legend = legend_g
        note = note_g
        for line in note:
            line.align_to([left, 0, 0], direction=[-1, 0, 0])
        for line in legend:
            line.align_to([left, 0, 0], direction=[-1, 0, 0])
        legend_top = rows_top - 4 * (text_h + gap / 2)
        legend.move_to([legend.get_center()[0], legend_top - legend.height / 2, 0])
        note_top = legend_top - legend.height - gap / 2
        note.move_to([note.get_center()[0], note_top - note.height / 2, 0])
        if note.get_bottom()[1] < bottom + cap_h + u(8):
            raise LayoutError("строкам значений T4 не хватает места над подписью")
        self.add(legend, note)
        for name, mob in (("легенда", legend), ("пояснение давления", note)):
            inside(lay, name, mob)
        play_timeline(self, tau, p["total"], fps)
