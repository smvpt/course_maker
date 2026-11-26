"""Шаблон T1 «Распространение давления», 9:16.

Компоновка: карта во всю ширину (одинаковый масштаб по осям, сетка расчёта обрезана по высоте карты), под ней
график Δp вдоль линии А–Б через скважину — ось x графика совпадает с картой метр в метр, поэтому пунктир
условной границы на графике стоит ровно под окружностью на карте.

Одна переменная — время ролика tau — через sim_time задаёт время симуляции t. От t и
только от него зависят карта поля Δp (план пласта) и график Δp(r): оба считаются
t1_template.field_values / profile, то есть одной функцией PressureModel.delta_p.
Пунктир на карте и на графике — условная граница Δp = порог (не физический фронт).
Время симуляции идёт только на фразах кадров evolve_shot_ids; в паузах и в финале стоит.

Общий стиль (style.py): камера приближается к области влияния на вопросе-предсказании, перелетает к тому же
пунктиру на графике на фразе с данными и возвращается к общему виду до кадра истинного масштаба; служебный слой
(метка, часы, плашка, подпись фразы) стоит на месте при движении камеры.
"""
from __future__ import annotations

import numpy as np
from manim import (RESAMPLING_ALGORITHMS, Circle, DashedLine, DashedVMobject, Dot, ImageMobject, Line, MovingCameraScene,
                   Rectangle, Text, ValueTracker, VGroup, VMobject, always_redraw)
from manim.utils.color import ManimColor

from pipeline.video.layout import FRAME_H, Layout, LayoutError
from pipeline.video.scene_parts import (add_badges, add_captions, add_plaques, inside, play_timeline,
                                        shot_windows, visibility, wrap)
from pipeline.video.t1_model import sim_time, sim_time_knots
from pipeline.video.t1_template import field_values, fmt_num, nice_ceil, profile
from pipeline.video import style
from pipeline.video.style import DataImage, Focus, Kit, check_no_overlap

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


class T1Scene(MovingCameraScene):
    plan: dict  # задаётся build.py перед render()

    def construct(self) -> None:
        p = self.plan
        lay: Layout = p["layout"]
        prep = p["t1"]
        c, font, fps, segs = p["colors"], p["font"], p["fps"], p["segments"]
        fs = lay.font_size(TEXT_PX)
        u = lay.units
        gap = u(GAP_PX)
        left, right, bottom, top = lay.safe_box()
        width = right - left
        txt = lambda s, color=None: Text(s, font=font, font_size=fs, color=color or c["text"])
        text_h = txt("Ж0").height
        tau = ValueTracker(0.0)
        knots = sim_time_knots([(s["phrase_id"], s["start"], s["end"]) for s in segs],
                               prep["evolve_phrase_ids"], prep["t_end"])
        # плавный разгон и торможение времени модели — одно время для карты, графика, лупы и часов
        sim_t = lambda: style.smooth_progress(sim_time(tau.get_value(), knots), prep["t_end"])
        kit = Kit(self, lay, c, font, tau)
        t_evolve = min((s["start"] for s in segs if s["phrase_id"] in prep["evolve_phrase_ids"]), default=0.0)
        model, r_max, thr = prep["model"], prep["r_max"], prep["threshold"]

        # ---- верх: метка, часы симуляции, плашка
        badge_bottom = add_badges(self, lay, segs, tau, font, add=kit.hud, fill=c["background"])
        unit, div = prep["time_unit"]
        clock_cache: dict[str, Text] = {}

        def clock():
            s = f"время: {fmt_num(sim_t() / div, 2)} {unit}"
            if s not in clock_cache:
                clock_cache[s] = txt(s)
            m = clock_cache[s].copy()
            return m.move_to([right - m.width / 2, (top + badge_bottom) / 2, 0])

        kit.hud_redraw(clock)
        plaque_texts = {sid: next(s["plaque"] for s in segs if s["shot_id"] == sid) for sid, _, _ in shot_windows(segs)}
        ts = prep["true_scale_shot_id"]
        plaque_bottom = badge_bottom - gap / 2
        cap_h = add_captions(self, lay, segs, tau, font, c["text"], pill=c["panel"], add=kit.hud)
        plaque_h = max(wrap(t_, font, fs, width - 2 * kit.pad, c["text"]).height + 1.4 * kit.pad
                       for t_ in [*filter(None, plaque_texts.values()), "истинный масштаб: скважина меньше точки"])

        # ---- вертикальная разметка: карта во всю ширину → легенда → график (та же ось x) → шкала цвета
        legend_h = text_h
        cbar_h = u(16) + u(6) + text_h
        x_lbl_h = gap / 3 + text_h
        map_top = plaque_bottom - plaque_h - gap
        g_floor = bottom + cap_h + gap                       # низ блока графика и шкалы
        fixed = gap + legend_h + gap + text_h + gap / 2 + x_lbl_h + gap + cbar_h
        avail = map_top - g_floor - fixed
        map_w = width
        graph_min_h = u(300)
        map_h = min(map_w, avail - graph_min_h)
        if map_h < u(360):
            raise LayoutError(f"карте T1 не хватает места: {map_h / u(1):.0f} px опорного кадра")
        m_per_unit = 2 * r_max / map_w                      # одинаковый масштаб по x и y: окружность — окружность
        half_h_m = map_h / 2 * m_per_unit
        px_ref = lambda metres: metres / m_per_unit / u(1)   # м → px опорного кадра
        true_txt = "истинный масштаб: скважина меньше точки" if px_ref(prep["r_well"]) * 2 < 1 else "истинный масштаб"
        if ts is not None:
            plaque_texts[ts] = true_txt
        add_plaques(self, lay, segs, tau, font, c["text"], plaque_bottom, plaque_texts, add=kit.hud,
                    pill=c["panel"])

        center = np.array([left + map_w / 2, map_top - map_h / 2, 0.0])
        c0, c1 = _rgb(c["panel"]), _rgb(c["field"])
        field0, xs = field_values(prep, 0.0)
        rows = np.abs(xs) <= half_h_m + 1e-9                  # та же сетка, обрезанная по высоте карты
        crop = lambda f: f[rows]
        img = DataImage(lambda: _colorize(crop(field_values(prep, sim_t())[0]), prep["color_max"], c0, c1))
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        y_span = 2 * float(np.abs(xs[rows]).max()) / m_per_unit
        img.stretch_to_fit_width(map_w).stretch_to_fit_height(y_span).move_to(center)
        frame = Rectangle(width=map_w, height=map_h, stroke_color=c["muted"], stroke_width=2).move_to(center)
        grain = ImageMobject(style.grain_overlay(max(int(map_h / u(1)), 1), max(int(map_w / u(1)), 1), c["text"],
                                                 density=0.002, alpha=40, seed=3))
        grain.stretch_to_fit_width(map_w).stretch_to_fit_height(map_h).move_to(center)
        self.add(img, grain, frame)                            # фактура пласта поверх цвета данных, цвета не меняет
        inside(lay, "карта поля", frame)

        # линия профиля А–Б через скважину: по ней построен график ниже
        ab = Line(center + np.array([-map_w / 2, 0, 0]), center + np.array([map_w / 2, 0, 0]),
                  color=c["muted"], stroke_width=2, stroke_opacity=0.8)
        a_lbl, b_lbl = txt("А", c["muted"]), txt("Б", c["muted"])
        a_lbl.move_to(center + np.array([-map_w / 2 + u(12) + a_lbl.width / 2, a_lbl.height / 2 + u(10), 0]))
        b_lbl.move_to(center + np.array([map_w / 2 - u(12) - b_lbl.width / 2, b_lbl.height / 2 + u(10), 0]))
        self.add(ab, a_lbl, b_lbl)

        # скважина: увеличенный значок на кадрах с плашкой, истинный размер на остальных; кольцо-маркер — всегда
        for sid, a, b in shot_windows(segs):
            k = prep["exaggeration"] if sid in prep["exaggerated_shots"] else 1.0
            r_units = prep["r_well"] * k / m_per_unit
            well = Circle(radius=max(r_units, 1e-6), color=c["text"], fill_color=c["text"], fill_opacity=1,
                          stroke_width=0).move_to(center)
            vis = visibility(a, b, 0.0)
            well.add_updater(lambda m, v=vis: m.set_opacity(v(tau.get_value())))
            self.add(well)
        ring_r = u(22)
        ring = Circle(radius=ring_r, color=c["text"], stroke_width=style.STROKE["bold"]).move_to(center)
        anchor = center + ring_r * np.array([np.cos(np.pi / 4), np.sin(np.pi / 4), 0])
        well_lbl = kit.callout("скважина", anchor, center + np.array([u(170), u(80), 0]))
        self.add(ring, kit.pulse(lambda: center, t_evolve, u(60)))
        self._well_label = well_lbl                          # поверх окружности границы — добавляется последним
        inside(lay, "подпись скважины", well_lbl)

        def boundary_circle():
            # окружность Δp = порог; части вне карты (карта ниже, чем широка) не рисуются
            r = model.influence_radius(sim_t(), thr) / m_per_unit
            g = VGroup()
            if r < u(4):
                return g
            ang = np.linspace(0, 2 * np.pi, 361)
            pts = np.column_stack([center[0] + r * np.cos(ang), center[1] + r * np.sin(ang), np.zeros_like(ang)])
            ok = (np.abs(pts[:, 1] - center[1]) <= map_h / 2) & (np.abs(pts[:, 0] - center[0]) <= map_w / 2)
            edges = np.flatnonzero(np.diff(np.concatenate([[0], ok.astype(int), [0]])))
            for a_, b_ in zip(edges[::2], edges[1::2]):
                if b_ - a_ >= 2:
                    arc = VMobject(stroke_color=c["text"], stroke_width=3).set_points_as_corners(pts[a_:b_])
                    g.add(DashedVMobject(arc, num_dashes=max(2, int(48 * (b_ - a_) / 361))))
            return g

        self.add(always_redraw(boundary_circle))

        # масштабная линейка в левом нижнем углу карты
        bar_m = nice_ceil(r_max / 4)
        bar = Rectangle(width=bar_m / m_per_unit, height=u(8), stroke_width=0, fill_color=c["text"], fill_opacity=1)
        bar.move_to(center + np.array([-map_w / 2 + gap + bar.width / 2, -map_h / 2 + gap + bar.height / 2, 0]))
        bar_lbl = txt(f"{fmt_num(bar_m)} м")
        bar_lbl.next_to(bar, direction=np.array([0, 1, 0]), buff=u(8)).align_to(bar, np.array([-1, 0, 0]))
        self.add(bar, bar_lbl)

        # ---- легенда: что такое пунктир и белая точка
        leg_y = center[1] - map_h / 2 - gap - legend_h / 2
        dash = DashedLine([left, leg_y, 0], [left + u(70), leg_y, 0], color=c["text"], stroke_width=3,
                          dash_length=u(12))
        leg = txt(f"условная граница: падение {fmt_num(thr)} МПа")
        leg.move_to([dash.get_right()[0] + gap / 2 + leg.width / 2, leg_y, 0])
        if leg.get_right()[0] > right:
            raise LayoutError("легенда T1 не помещается в строку")
        self.add(dash, leg)
        inside(lay, "легенда", leg)

        # ---- график: профиль Δp вдоль А–Б, ось x совпадает с картой метр в метр
        g_title_y = leg_y - legend_h / 2 - gap - text_h / 2
        y_title = txt("падение давления вдоль А–Б, МПа", c["muted"])
        y_title.move_to([left + y_title.width / 2, g_title_y, 0])
        ax_top = g_title_y - text_h / 2 - gap / 2
        ax_bottom = g_floor + cbar_h + gap + x_lbl_h
        ax_h = ax_top - ax_bottom
        if ax_h < u(160):
            raise LayoutError(f"графику T1 не хватает места: {ax_h / u(1):.0f} px опорного кадра")
        x_of = lambda xm: center[0] + np.asarray(xm) / m_per_unit
        y_of = lambda dp: ax_bottom + np.asarray(dp) / prep["graph_max"] * ax_h
        x_axis = Line([left, ax_bottom, 0], [right, ax_bottom, 0], color=c["muted"], stroke_width=2)
        grid = [DashedLine([left, y_of(v), 0], [right, y_of(v), 0], color=c["muted"], stroke_width=1,
                           stroke_opacity=0.5, dash_length=u(8)) for v in (prep["graph_max"] / 2, prep["graph_max"])]
        y_lbls = []
        for v in (prep["graph_max"] / 2, prep["graph_max"]):
            t_ = txt(fmt_num(v), c["muted"])
            t_.move_to([left + t_.width / 2, y_of(v) - t_.height / 2 - u(6), 0])
            y_lbls.append(t_)
        x_lbls = []
        for xm, s in ((-r_max, f"{fmt_num(r_max)} м"), (0.0, "0"), (r_max, f"{fmt_num(r_max)} м")):
            t_ = txt(s, c["muted"])
            xx = min(max(float(x_of(xm)), left + t_.width / 2), right - t_.width / 2)
            t_.move_to([xx, ax_bottom - gap / 3 - text_h / 2, 0])
            x_lbls.append(t_)
        well_tick = Line([center[0], ax_bottom, 0], [center[0], ax_bottom + u(14), 0], color=c["text"], stroke_width=3)
        self.add(x_axis, *grid, *y_lbls, *x_lbls, y_title, well_tick)
        for name, m in [("подпись графика", y_title), *[(f"деление y {i}", t_) for i, t_ in enumerate(y_lbls)],
                        *[(f"деление x {i}", t_) for i, t_ in enumerate(x_lbls)]]:
            inside(lay, f"график: {name}", m)

        def curve():
            r, dp = profile(prep, sim_t())
            g = VGroup()
            for sgn in (-1, 1):                               # профиль симметричен: та же функция по |x|
                pts = np.column_stack([x_of(sgn * r), y_of(np.minimum(dp, prep["graph_max"])), np.zeros_like(r)])
                g.add(VMobject(color=c["field"], stroke_width=5).set_points_as_corners(pts))
            return g

        def boundary_lines():
            r = model.influence_radius(sim_t(), thr)
            g = VGroup()
            if r < prep["r_min"] or r > r_max:
                return g
            for sgn in (-1, 1):
                xx = float(x_of(sgn * r))
                # пунктир на графике и короткая связка до окружности на карте — одна абсцисса
                g.add(DashedLine([xx, ax_bottom, 0], [xx, y_of(prep["graph_max"]), 0], color=c["text"],
                                 stroke_width=2, dash_length=u(12)))
                g.add(DashedLine([xx, center[1], 0], [xx, center[1] - map_h / 2, 0], color=c["text"],
                                 stroke_width=1, stroke_opacity=0.5, dash_length=u(8)))
            return g

        self.add(always_redraw(curve), always_redraw(boundary_lines))

        # выноска «граница» на графике — едет вместе с пунктиром; стрелка роста границы на карте, пока идёт время
        b_pill = kit.pill(kit.text("граница"))

        def boundary_callout():
            r = model.influence_radius(sim_t(), thr)
            if r < prep["r_min"] or r > r_max:
                return VGroup()
            xx = float(x_of(r))
            yy = float(y_of(prep["graph_max"] * 0.7))
            box_x = xx + kit.gap + b_pill.width / 2
            if box_x + b_pill.width / 2 > right:
                box_x = xx - kit.gap - b_pill.width / 2
            pill = b_pill.copy().move_to([box_x, yy, 0])
            edge = pill.get_left()[0] if box_x > xx else pill.get_right()[0]
            return VGroup(Line([xx, yy, 0], [edge, yy, 0], color=c["text"], stroke_width=style.STROKE["line"]),
                          Dot([xx, yy, 0], radius=kit.pad * 0.4, color=c["text"]), pill)

        def growth_arrow():
            t_now, t_next = sim_t(), style.smooth_progress(sim_time(tau.get_value() + 0.1, knots), prep["t_end"])
            r = model.influence_radius(t_now, thr) / m_per_unit
            if t_next <= t_now + 1e-9 or r < ring_r * 3:
                return VGroup()
            y_a = center[1] + u(26)
            return kit.arrow([center[0] + ring_r * 1.6, y_a, 0], [center[0] + r - u(10), y_a, 0])

        self.add(always_redraw(boundary_callout), always_redraw(growth_arrow), self._well_label)

        # ---- шкала цвета карты (внизу, над подписями)
        cb_y = g_floor + text_h + u(6) + u(8)
        grad = np.linspace(0, prep["color_max"], 256)[None, :].repeat(2, axis=0)
        cbar = ImageMobject(_colorize(grad, prep["color_max"], c0, c1))
        cbar.stretch_to_fit_width(map_w).stretch_to_fit_height(u(16)).move_to([center[0], cb_y, 0])
        y_lbl = g_floor + text_h / 2
        lo = txt("0")
        hi = txt(f"≥ {fmt_num(prep['color_max'])} МПа")
        mid = txt("цвет карты: падение давления", c["muted"])
        lo.move_to([left + lo.width / 2, y_lbl, 0])
        hi.move_to([right - hi.width / 2, y_lbl, 0])
        mid.move_to([(lo.get_right()[0] + hi.get_left()[0]) / 2, y_lbl, 0])
        if mid.get_left()[0] < lo.get_right()[0] + gap / 2 or mid.get_right()[0] > hi.get_left()[0] - gap / 2:
            mid = txt("цвет: падение", c["muted"]).move_to([(lo.get_right()[0] + hi.get_left()[0]) / 2, y_lbl, 0])
        self.add(cbar, lo, hi, mid)
        for name, m in (("шкала цвета", hi), ("шкала цвета", mid)):
            inside(lay, name, m)
        check_no_overlap([("легенда", leg), ("подпись графика", y_title), ("шкала цвета 0", lo), ("шкала цвета", mid),
                          ("шкала цвета max", hi), ("линейка", bar_lbl), ("А", a_lbl), ("Б", b_lbl),
                          ("подпись скважины", well_lbl[2]), *[(f"деление y {i}", t_) for i, t_ in enumerate(y_lbls)],
                          *[(f"деление x {i}", t_) for i, t_ in enumerate(x_lbls)]])

        # ---- камера: приближение к области влияния (вопрос) → перелёт к тому же пунктиру на графике (данные)
        def boundary_box(t: float):
            r_u = max(model.influence_radius(sim_t(), thr) / m_per_unit, u(150))
            x0, x1 = max(center[0] - r_u, left), min(center[0] + r_u, right)
            y0, y1 = max(center[1] - r_u, center[1] - map_h / 2), min(center[1] + r_u, center[1] + map_h / 2)
            lx0, lx1, ly0, ly1 = style.bbox(well_lbl)          # выноска скважины — целиком в кадре
            return min(x0, lx0) - kit.pad, max(x1, lx1) + kit.pad, min(y0, ly0) - kit.pad, max(y1, ly1) + kit.pad

        graph_box = (center[0] - u(60), right, ax_bottom - x_lbl_h, ax_top + kit.pad)
        area = (left, right, g_floor, map_top)
        cands = []
        w_pred = style.beat_window(segs, {"prediction"})
        if w_pred:
            cands.append(Focus(w_pred[0], w_pred[1], boundary_box, "область влияния"))
        w_data = style.beat_window(segs, {"data"}, after=w_pred[1] if w_pred else -np.inf)
        if w_data:
            cands.append(Focus(w_data[0], w_data[1], graph_box, "тот же радиус на графике"))
        ts_win = style.shot_window(segs, ts)
        rig = style.plan_camera(area, cands, [ts_win] if ts_win else [])
        kit.use_camera(rig)
        if w_data and any(f.name == "тот же радиус на графике" for f in rig.focuses):
            r_now = lambda: model.influence_radius(sim_t(), thr)
            self.add(kit.highlight(lambda: (float(x_of(r_now())) - u(10), float(x_of(r_now())) + u(10), ax_bottom,
                                            float(y_of(prep["graph_max"]))), w_data[0] + style.TRANS_S))
        kit.set_zoom_tag_top(map_top - kit.pad)
        kit.finish(scrim_bands=[(map_top, FRAME_H / 2), (-FRAME_H / 2, g_floor)])
        self.t1_layout = {"map_w_px_ref": map_w / u(1), "map_h_px_ref": map_h / u(1),
                          "graph_h_px_ref": ax_h / u(1), "m_per_px_ref": m_per_unit * u(1)}
        self.t1_camera = rig
        play_timeline(self, tau, p["total"], fps)
