"""Шаблон T3 «Рост тела», 9:16: план лопасти и разрез А–Б из одного состояния.

Одна переменная — время ролика tau — через progress_at задаёт время симуляции t; от t зависит радиус
береговой линии R(t) модели, а из него — и план (t3_template.plan_field), и разрез (section_profile,
layer_bands): одна функция LobeModel.surface. Слой k — осадок интервала [t_k, t_{k+1}]; в плане цвет
показывает, какой слой выходит на поверхность, в разрезе — сами слои; темнее — старше.
Вертикаль разреза увеличена в vertical_exaggeration раз только на кадрах с плашкой.
"""
from __future__ import annotations

import numpy as np
from manim import (DashedLine, ImageMobject, Line, Polygon, Rectangle, Scene, Text, ValueTracker, VGroup, VMobject,
                   always_redraw)
from manim.utils.color import ManimColor

from pipeline.video.layout import Layout, LayoutError
from pipeline.video.scene_parts import add_badges, add_captions, add_plaques, inside, play_timeline, shot_windows, wrap
from pipeline.video.t1_template import fmt_num, nice_ceil
from pipeline.video.t3_template import layer_bands, plan_field, shoreline_radii
from pipeline.video.timeline import progress_at, progress_knots

TEXT_PX = 44
GAP_PX = 24
SEA_MARGIN_PX, FLOOR_MARGIN_PX = 64, 24


def _rgb(hex_color: str) -> np.ndarray:
    return np.array(ManimColor(hex_color).to_rgb(), dtype=float)


class T3Scene(Scene):
    plan: dict  # задаётся build.py перед render()

    def construct(self) -> None:
        p = self.plan
        lay: Layout = p["layout"]
        prep = p["t3"]
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
        knots = progress_knots([(s["phrase_id"], s["start"], s["end"]) for s in segs], prep["evolve_phrase_ids"],
                               prep["t_end"])
        sim_t = lambda: progress_at(tau.get_value(), knots)
        windows = shot_windows(segs)

        def shot_now() -> str:
            tv = tau.get_value()
            return next((sid for sid, a, b in windows if a <= tv < b), windows[-1][0])

        # ---- цвета слоёв: темнее — старше (одна шкала для плана и разреза)
        base = _rgb(c["layer"])
        lo, hi = prep["display"]["age_shade"]
        n = prep["n_layers"]
        shade = [base * (lo + (hi - lo) * k / max(n - 1, 1)) for k in range(n)]
        hex_of = lambda rgb: ManimColor(rgb.tolist()).to_hex()
        initial, basin = _rgb(c["initial"]), _rgb(c["basin"])

        # ---- верх: метка, часы, плашка
        badge_bottom = add_badges(self, lay, segs, tau, font)
        cache: dict[str, Text] = {}

        def clock():
            s = f"время: {fmt_num(sim_t(), 4)} лет"
            if s not in cache:
                cache[s] = txt(s)
            mm = cache[s].copy()
            return mm.move_to([right - mm.width / 2, (top + badge_bottom) / 2, 0])

        self.add(always_redraw(clock))
        plaque_texts = {sid: next(s["plaque"] for s in segs if s["shot_id"] == sid) for sid, _, _ in windows}
        ts = prep["true_scale_shot_id"]
        if ts is not None:
            plaque_texts[ts] = "истинный масштаб: вертикаль не увеличена"
        plaque_top = badge_bottom - gap / 2
        plaque_h = max([wrap(t_, font, fs, width, c["text"]).height for t_ in plaque_texts.values() if t_] + [0.0])
        add_plaques(self, lay, segs, tau, font, c["text"], plaque_top, plaque_texts)

        # ---- вертикальная разметка
        cap_h = add_captions(self, lay, segs, tau, font, c["text"])
        sec_w = width
        px_per_m = (sec_w / u(1)) / prep["r_max"]                              # px опорного кадра на метр по горизонтали
        h_px_max = m.depth_m * prep["exaggeration"] * px_per_m
        sec_h = u(SEA_MARGIN_PX + h_px_max + FLOOR_MARGIN_PX)
        plan_label_top = plaque_top - plaque_h - gap
        fixed = (text_h + gap / 2) * 2 + sec_h + gap + (text_h + gap / 2) * 2 + gap
        avail = plan_label_top - (bottom + cap_h + gap) - fixed
        plan_h = min(width / 2, avail)
        if plan_h < u(250):
            raise LayoutError(f"плану T3 не хватает места: {plan_h / u(1):.0f} px опорного кадра")
        plan_w = 2 * plan_h

        # ---- план
        lbl_plan = txt("план", c["muted"])
        lbl_plan.move_to([left + lbl_plan.width / 2, plan_label_top - text_h / 2, 0])
        plan_top = plan_label_top - text_h - gap / 2
        plan_cx = 0.0
        plan_center = np.array([plan_cx, plan_top - plan_h / 2, 0])
        m_per_unit_plan = 2 * prep["r_max"] / plan_w

        def plan_rgba(t: float) -> np.ndarray:
            z, xs, ys, inside_ = plan_field(prep, t)
            r = np.hypot(*np.meshgrid(xs, ys))
            R = m.radius(t)
            radii = np.array([m.radius(float(tk)) for tk in prep["layer_times"]])
            k = np.clip(np.searchsorted(radii, r, side="right") - 1, 0, n - 1)   # какой слой выходит на поверхность
            k_now = int(np.clip(np.searchsorted(prep["layer_times"], t, side="right") - 1, 0, n - 1))
            col = np.array(shade)[k]
            col[r < m.r0_m] = initial
            fore = (r > R) & (z > -m.depth_m)
            depth_frac = np.clip(-z / m.depth_m, 0, 1)[..., None]
            cur = shade[k_now] if t > 0 else initial          # в начальный момент новых слоёв нет
            col[fore] = (cur * (1 - depth_frac) + basin * depth_frac)[fore]
            col[(z <= -m.depth_m) | ~inside_] = basin
            out = np.empty(z.shape + (4,), dtype=np.uint8)
            out[..., :3] = np.round(col * 255).astype(np.uint8)
            out[..., 3] = 255
            return out

        img = ImageMobject(plan_rgba(0.0))
        img.stretch_to_fit_width(plan_w).stretch_to_fit_height(plan_h).move_to(plan_center)
        img.add_updater(lambda mob: mob.pixel_array.__setitem__(slice(None), plan_rgba(sim_t())))
        frame = Rectangle(width=plan_w, height=plan_h, stroke_color=c["muted"], stroke_width=2).move_to(plan_center)
        src = np.array([plan_cx, plan_top, 0])                         # точка питания — середина верхнего края

        def arcs():
            g = VGroup()
            for rad in shoreline_radii(prep, sim_t()):
                rr = rad / m_per_unit_plan
                ang = np.radians(np.linspace(-m.lobe_deg / 2, m.lobe_deg / 2, 90))
                pts = np.column_stack([src[0] + rr * np.sin(ang), src[1] - rr * np.cos(ang), np.zeros_like(ang)])
                g.add(VMobject(stroke_color=c["text"], stroke_width=1.5, stroke_opacity=0.6).set_points_as_corners(pts))
            return g

        line_ab = DashedLine(src, src + np.array([0, -plan_h, 0]), color=c["text"], stroke_width=2,
                             dash_length=u(12))
        a_lbl, b_lbl = txt("А"), txt("Б")
        a_lbl.next_to(src, direction=np.array([1, 0, 0]), buff=u(8)).shift([0, -a_lbl.height / 2 - u(6), 0])
        b_lbl.next_to(src + np.array([0, -plan_h, 0]), direction=np.array([1, 0, 0]), buff=u(8)) \
            .shift([0, b_lbl.height / 2 + u(6), 0])
        bar_m = nice_ceil(prep["r_max"] / 5)
        bar = Rectangle(width=bar_m / m_per_unit_plan, height=u(8), stroke_width=0, fill_color=c["text"],
                        fill_opacity=1)
        bar.move_to([plan_center[0] - plan_w / 2 + gap + bar.width / 2, plan_top - plan_h + gap + bar.height / 2, 0])
        bar_lbl = txt(f"{fmt_num(bar_m / 1000)} км" if bar_m >= 1000 else f"{fmt_num(bar_m)} м")
        bar_lbl.next_to(bar, direction=np.array([0, 1, 0]), buff=u(8)).align_to(bar, np.array([-1, 0, 0]))
        self.add(img, frame, always_redraw(arcs), line_ab, a_lbl, b_lbl, bar, bar_lbl, lbl_plan)

        # ---- разрез А–Б: те же слои, та же функция поверхности
        sec_label_top = plan_top - plan_h - gap
        lbl_sec = txt("разрез А–Б", c["muted"])
        lbl_sec.move_to([left + lbl_sec.width / 2, sec_label_top - text_h / 2, 0])
        sec_top = sec_label_top - text_h - gap / 2
        sea_y = sec_top - u(SEA_MARGIN_PX)
        x0 = left
        x_of = lambda r: x0 + np.asarray(r) / prep["r_max"] * sec_w
        sec_frame = Rectangle(width=sec_w, height=sec_h, stroke_color=c["muted"], stroke_width=2,
                              fill_color=c["basin"], fill_opacity=1).move_to([0, sec_top - sec_h / 2, 0])

        def section():
            sid = shot_now()
            ve = prep["exaggeration"] if sid in prep["exaggerated_shots"] else 1.0
            y_of = lambda z: sea_y + u(np.asarray(z) * ve * px_per_m)
            t = sim_t()
            g = VGroup()
            r = np.linspace(0.0, prep["r_max"], 801)
            z0 = m.surface(r, 0.0)
            floor = np.full_like(r, -m.depth_m)
            g.add(Polygon(*np.column_stack([x_of(np.r_[r, r[::-1]]), y_of(np.r_[z0, floor[::-1]]),
                                            np.zeros(2 * r.size)]),
                          stroke_width=0, fill_color=c["initial"], fill_opacity=1))
            for b in layer_bands(prep, t):
                pts = np.column_stack([x_of(np.r_[b["r"], b["r"][::-1]]), y_of(np.r_[b["z_top"], b["z_bottom"][::-1]]),
                                       np.zeros(2 * b["r"].size)])
                g.add(Polygon(*pts, stroke_color=c["background"], stroke_width=1, fill_color=hex_of(shade[b["k"]]),
                              fill_opacity=1))
            g.add(DashedLine([x0, sea_y, 0], [x0 + sec_w, sea_y, 0], color=c["text"], stroke_width=2,
                             dash_length=u(12)))
            g.add(Line([x0, y_of(-m.depth_m), 0], [x0 + sec_w, y_of(-m.depth_m), 0], color=c["muted"], stroke_width=2))
            return g

        sea_lbl = txt("уровень моря", c["muted"])
        sea_lbl.move_to([x0 + sec_w - sea_lbl.width / 2 - u(8), sea_y + sea_lbl.height / 2 + u(6), 0])
        if sea_lbl.get_top()[1] > sec_top:
            sea_lbl.shift([0, sec_top - sea_lbl.get_top()[1] - u(4), 0])
        self.add(sec_frame, always_redraw(section), sea_lbl, lbl_sec)

        # шкала расстояний и подпись глубины
        tick_y = sec_top - sec_h - gap / 2 - text_h / 2
        ticks = [0.0, prep["r_max"] / 2, prep["r_max"]]
        km = lambda v: f"{fmt_num(v / 1000)} км" if v else "0"
        for v in ticks:
            t_ = txt(km(v), c["muted"])
            xx = min(max(float(x_of(v)), left + t_.width / 2), right - t_.width / 2)
            t_.move_to([xx, tick_y, 0])
            self.add(t_)
            inside(lay, "шкала разреза", t_)
        depth_lbl = txt(f"глубина бассейна {fmt_num(m.depth_m)} м", c["muted"])
        legend = txt("слои: темнее — старше", c["muted"])
        legend.move_to([left + legend.width / 2, tick_y - text_h - gap / 2, 0])
        depth_lbl.move_to([right - depth_lbl.width / 2, tick_y - text_h - gap / 2, 0])
        if legend.get_right()[0] + gap > depth_lbl.get_left()[0]:
            depth_lbl.shift([0, -text_h - gap / 2, 0])
        self.add(legend, depth_lbl)
        for name, mob in (("план", frame), ("подпись плана", lbl_plan), ("разрез", sec_frame), ("подпись разреза", lbl_sec),
                          ("легенда", legend), ("глубина", depth_lbl), ("уровень моря", sea_lbl), ("масштаб", bar_lbl)):
            inside(lay, name, mob)
        play_timeline(self, tau, p["total"], fps)
