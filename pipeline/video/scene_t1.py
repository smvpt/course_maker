"""Шаблон T1 «Распространение давления», 9:16.

Одна переменная — время ролика tau — через sim_time задаёт время симуляции t. От t и
только от него зависят карта поля Δp (план пласта) и график Δp(r): оба считаются
t1_template.field_values / profile, то есть одной функцией PressureModel.delta_p.
Пунктир на карте и на графике — условная граница Δp = порог (не физический фронт).
Время симуляции идёт только на фразах кадров evolve_shot_ids; в паузах и в финале стоит.
"""
from __future__ import annotations

import numpy as np
from manim import (RESAMPLING_ALGORITHMS, Axes, Circle, DashedLine, DashedVMobject, ImageMobject, Rectangle, Scene, Text, ValueTracker,
                   VMobject, always_redraw)
from manim.utils.color import ManimColor

from pipeline.video.layout import REF_H, FRAME_H, Layout, LayoutError
from pipeline.video.scene_parts import (add_badges, add_captions, add_plaques, inside, play_timeline,
                                        shot_windows, visibility, wrap)
from pipeline.video.t1_model import sim_time, sim_time_knots
from pipeline.video.t1_template import field_values, fmt_num, nice_ceil, profile

TEXT_PX = 44
GAP_PX = 24


def _rgb(hex_color: str) -> np.ndarray:
    return np.array(ManimColor(hex_color).to_rgb(), dtype=float) * 255


def _colorize(values: np.ndarray, vmax: float, c0: np.ndarray, c1: np.ndarray) -> np.ndarray:
    a = np.clip(values / vmax, 0.0, 1.0)[..., None]
    rgb = c0 + (c1 - c0) * a
    out = np.empty(values.shape + (4,), dtype=np.uint8)
    out[..., :3] = np.round(rgb).astype(np.uint8)
    out[..., 3] = 255
    return out[::-1]          # строка 0 изображения — верх кадра (+y)


class T1Scene(Scene):
    plan: dict  # задаётся build.py перед render()

    def construct(self) -> None:
        p = self.plan
        lay: Layout = p["layout"]
        prep = p["t1"]
        c, font, fps, segs = p["colors"], p["font"], p["fps"], p["segments"]
        fs = lay.font_size(TEXT_PX)
        gap = lay.units(GAP_PX)
        left, right, bottom, top = lay.safe_box()
        width = right - left
        tau = ValueTracker(0.0)
        knots = sim_time_knots([(s["phrase_id"], s["start"], s["end"]) for s in segs],
                               prep["evolve_phrase_ids"], prep["t_end"])
        sim_t = lambda: sim_time(tau.get_value(), knots)
        model, r_max, thr = prep["model"], prep["r_max"], prep["threshold"]

        # ---- верх: метка, часы симуляции, плашка
        badge_bottom = add_badges(self, lay, segs, tau, font)
        unit, div = prep["time_unit"]
        clock_cache: dict[str, Text] = {}

        def clock():
            s = f"время: {fmt_num(sim_t() / div, 2)} {unit}"
            if s not in clock_cache:
                clock_cache[s] = Text(s, font=font, font_size=fs, color=c["text"])
            m = clock_cache[s].copy()
            return m.move_to([right - m.width / 2, (top + badge_bottom) / 2, 0])

        self.add(always_redraw(clock))

        px_ref = lambda metres, side: metres * side / (2 * r_max) / (FRAME_H / REF_H)   # м → px опорного кадра
        plaque_texts = {sid: next(s["plaque"] for s in segs if s["shot_id"] == sid) for sid, _, _ in shot_windows(segs)}
        ts = prep["true_scale_shot_id"]
        # размер карты ещё не известен; «меньше точки» проверяется ниже по фактическому размеру
        plaque_bottom = badge_bottom - gap

        # ---- низ: подписи; середина: карта, шкала цвета, график
        cap_h = add_captions(self, lay, segs, tau, font, c["text"])
        text_h = Text("Ж0", font=font, font_size=fs).height
        plaque_h = max(wrap(txt, font, fs, width, c["text"]).height
                       for txt in [*filter(None, plaque_texts.values()), "истинный масштаб: скважина меньше точки"])
        map_top = plaque_bottom - plaque_h - gap
        graph_min_h = lay.units(380)
        avail = map_top - (bottom + cap_h + gap) - (lay.units(16) + text_h + 2 * gap) - graph_min_h - gap
        side = min(width * 0.72, avail)
        if side < lay.units(360):
            raise LayoutError(f"карте T1 не хватает места: {side / lay.units(1):.0f} px опорного кадра")
        pixel_side = px_ref(2 * r_max, side)

        true_txt = "истинный масштаб: скважина меньше точки" if px_ref(prep["r_well"], side) * 2 < 1 \
            else "истинный масштаб"
        if ts is not None:
            plaque_texts[ts] = true_txt
        add_plaques(self, lay, segs, tau, font, c["text"], plaque_bottom, plaque_texts)

        center = np.array([0.0, map_top - side / 2, 0.0])
        m_per_unit = 2 * r_max / side
        c0, c1 = _rgb(c["panel"]), _rgb(c["field"])
        field0, _ = field_values(prep, 0.0)
        img = ImageMobject(_colorize(field0, prep["color_max"], c0, c1))
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        img.stretch_to_fit_width(side).stretch_to_fit_height(side).move_to(center)
        img.add_updater(lambda m: m.pixel_array.__setitem__(
            slice(None), _colorize(field_values(prep, sim_t())[0], prep["color_max"], c0, c1)))
        frame = Rectangle(width=side, height=side, stroke_color=c["muted"], stroke_width=2).move_to(center)
        self.add(img, frame)
        inside(lay, "карта поля", frame)

        # скважина: увеличенный значок на кадрах с плашкой, истинный размер на остальных
        for sid, a, b in shot_windows(segs):
            k = prep["exaggeration"] if sid in prep["exaggerated_shots"] else 1.0
            r_units = prep["r_well"] * k / m_per_unit
            well = Circle(radius=max(r_units, 1e-6), color=c["text"], fill_color=c["text"], fill_opacity=1,
                          stroke_width=0).move_to(center)
            vis = visibility(a, b, 0.0)
            well.add_updater(lambda m, v=vis: m.set_opacity(v(tau.get_value())))
            self.add(well)

        def boundary_circle():
            r = model.influence_radius(sim_t(), thr) / m_per_unit
            if r < lay.units(4):
                return VMobject()
            return DashedVMobject(Circle(radius=r, color=c["text"], stroke_width=3).move_to(center),
                                  num_dashes=48)

        self.add(always_redraw(boundary_circle))

        # масштабная линейка в левом нижнем углу карты
        bar_m = nice_ceil(r_max / 4)
        bar = Rectangle(width=bar_m / m_per_unit, height=lay.units(8), stroke_width=0,
                        fill_color=c["text"], fill_opacity=1)
        bar.move_to(center + np.array([-side / 2 + gap + bar.width / 2, -side / 2 + gap + bar.height / 2, 0]))
        bar_lbl = Text(f"{fmt_num(bar_m)} м", font=font, font_size=fs, color=c["text"])
        bar_lbl.next_to(bar, direction=np.array([0, 1, 0]), buff=lay.units(8)).align_to(bar, np.array([-1, 0, 0]))
        self.add(bar, bar_lbl)

        # шкала цвета
        cb_top = center[1] - side / 2 - gap
        grad = np.linspace(0, prep["color_max"], 256)[None, :].repeat(2, axis=0)
        cbar = ImageMobject(_colorize(grad, prep["color_max"], c0, c1))
        cbar.stretch_to_fit_width(side).stretch_to_fit_height(lay.units(16)).move_to([0, cb_top - lay.units(8), 0])
        lo = Text("0", font=font, font_size=fs, color=c["text"])
        hi = Text(f"≥ {fmt_num(prep['color_max'])} МПа", font=font, font_size=fs, color=c["text"])
        mid = Text("падение давления", font=font, font_size=fs, color=c["muted"])
        y_lbl = cb_top - lay.units(16) - lay.units(6) - text_h / 2
        lo.move_to([cbar.get_left()[0] + lo.width / 2, y_lbl, 0])
        hi.move_to([cbar.get_right()[0] - hi.width / 2, y_lbl, 0])
        mid.move_to([(lo.get_right()[0] + hi.get_left()[0]) / 2, y_lbl, 0])
        if mid.get_left()[0] < lo.get_right()[0] + gap / 2 or mid.get_right()[0] > hi.get_left()[0] - gap / 2:
            mid.set_opacity(0)
        self.add(cbar, lo, hi, mid)

        # ---- график Δp(r): та же функция, то же время
        g_top = y_lbl - text_h / 2 - gap
        g_bottom = bottom + cap_h + gap
        y_title = Text("падение, МПа", font=font, font_size=fs, color=c["muted"])
        x_title = Text("расстояние, м", font=font, font_size=fs, color=c["muted"])
        y_ticks = [prep["graph_max"] / 2, prep["graph_max"]]          # «0» общий с осью x
        x_ticks = [0.0, r_max / 2, r_max]
        y_lbls = [Text(fmt_num(v), font=font, font_size=fs, color=c["text"]) for v in y_ticks]
        x_lbls = [Text(fmt_num(v), font=font, font_size=fs, color=c["text"]) for v in x_ticks]
        lm = max(t.width for t in y_lbls) + gap / 2
        ax_top = g_top - 1.5 * text_h - gap             # над верхним делением — строка заголовков
        ax_bottom = g_bottom + 2 * text_h + gap
        ax_h = ax_top - ax_bottom
        ax_w = width - lm - max(t.width for t in x_lbls) / 2
        if ax_h < lay.units(160):
            raise LayoutError(f"графику T1 не хватает места: {ax_h / lay.units(1):.0f} px опорного кадра")
        axes = Axes(x_range=[0, r_max, r_max / 2], y_range=[0, prep["graph_max"], prep["graph_max"] / 2],
                    x_length=ax_w, y_length=ax_h, tips=False,
                    axis_config={"color": c["muted"], "stroke_width": 2, "include_numbers": False})
        axes.move_to([left + lm + ax_w / 2, ax_bottom + ax_h / 2, 0])
        for v, t in zip(y_ticks, y_lbls):
            t.move_to(axes.c2p(0, v) + np.array([-gap / 2 - t.width / 2, 0, 0]))
        for v, t in zip(x_ticks, x_lbls):
            x = min(max(axes.c2p(v, 0)[0], left + t.width / 2), right - t.width / 2)   # крайние — к краю зоны
            t.move_to([x, axes.c2p(v, 0)[1] - gap / 3 - text_h / 2, 0])
        y_title.move_to([left + y_title.width / 2, g_top - text_h / 2, 0])
        x_title.move_to([axes.c2p(r_max / 2, 0)[0], x_lbls[0].get_center()[1] - text_h - gap / 3, 0])
        thr_line = DashedLine(axes.c2p(0, thr), axes.c2p(r_max, thr), color=c["text"], stroke_width=2,
                              dash_length=lay.units(12))
        thr_lbl = Text(f"пунктир: {fmt_num(thr)} МПа", font=font, font_size=fs, color=c["text"])
        thr_lbl.move_to([right - thr_lbl.width / 2, g_top - text_h / 2, 0])
        if thr_lbl.get_left()[0] < y_title.get_right()[0] + gap:
            raise LayoutError("подписи графика T1 не помещаются в одну строку")
        self.add(axes, *y_lbls, *x_lbls, y_title, x_title, thr_line, thr_lbl)
        for name, m in [("оси", axes), ("подпись оси y", y_title), ("подпись оси x", x_title), ("порог", thr_lbl),
                        *[(f"деление y {i}", t) for i, t in enumerate(y_lbls)],
                        *[(f"деление x {i}", t) for i, t in enumerate(x_lbls)]]:
            inside(lay, f"график: {name}", m)

        o = axes.c2p(0, 0)
        ex, ey = axes.c2p(1, 0) - o, axes.c2p(0, 1) - o

        def curve():
            r, dp = profile(prep, sim_t())
            pts = o + r[:, None] * ex + dp[:, None] * ey
            return VMobject(color=c["field"], stroke_width=5).set_points_as_corners(pts)

        def boundary_line():
            r = model.influence_radius(sim_t(), thr)
            if r < prep["r_min"]:
                return VMobject()
            return DashedLine(axes.c2p(r, 0), axes.c2p(r, prep["graph_max"]), color=c["text"], stroke_width=2,
                              dash_length=lay.units(12))

        self.add(always_redraw(curve), always_redraw(boundary_line))
        self.t1_layout = {"map_side_px_ref": side / lay.units(1), "pixel_side_ref": pixel_side}
        play_timeline(self, tau, p["total"], fps)
