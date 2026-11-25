"""Шаблон T3, качественный режим: схема конуса выноса в плане и продольный разрез по его оси без масштаба.

Одна переменная — время ролика tau — через progress_at задаёт долю показа s ∈ [0, 1]; из неё
t3_template.stages даёт стадии (рост текущей, отмершие ниже), а zone_bounds и stack_profiles — границы зон;
план и разрез рисуются из этих же стадий и границ. Чисел, шкал и плашек нет: на кадре постоянная пометка
«схема без масштаба». Элемент схемы (зоны, депоцентр, стадии) появляется с первой фразы своего утверждения.
Кадр 9:16 — план над разрезом; 16:9 — план слева, разрез справа.
"""
from __future__ import annotations

import numpy as np
from manim import (AnnularSector, DashedLine, DashedVMobject, Line, Polygon, Rectangle, Scene, Square, Text,
                   ValueTracker, VGroup, VMobject, always_redraw)

from pipeline.video.layout import Layout, LayoutError
from pipeline.video.scene_parts import FADE_S, add_badges, add_captions, inside, play_timeline, visibility, wrap
from pipeline.video.t3_template import depocenter_extent, phase_knots, stack_profiles, stages, zone_bounds
from pipeline.video.timeline import progress_at

TEXT_PX = 44
GAP_PX = 24
MOUTH_FRAC = 0.12          # устье — на этой доле высоты плана от верхнего края
STAGE_GAP = 0.6            # запас по высоте разреза над верхней стадией, в толщинах стадии


class T3SchemeScene(Scene):
    plan: dict  # задаётся build.py перед render()

    def construct(self) -> None:
        p = self.plan
        lay: Layout = p["layout"]
        prep = p["t3"]
        q = prep["display"]
        c, font, fps, segs = p["colors"], p["font"], p["fps"], p["segments"]
        fs = lay.font_size(TEXT_PX)
        u = lay.units
        gap = u(GAP_PX)
        left, right, bottom, top = lay.safe_box()
        landscape = lay.ref_w > lay.ref_h
        txt = lambda s, color=None: Text(s, font=font, font_size=fs, color=color or c["text"])
        text_h = txt("Жу0").height
        tau = ValueTracker(0.0)
        knots = phase_knots([(s["phrase_id"], s["start"], s["end"]) for s in segs], prep["phases"])
        share = lambda: progress_at(tau.get_value(), knots)
        start_of = {s["phrase_id"]: s["start"] for s in segs}
        shown = {k: visibility(start_of[pid], float("inf"), FADE_S) for k, pid in prep["appear_at"].items()}
        vis = lambda k: shown[k](tau.get_value()) if k in shown else 0.0
        zones = q["zones"]

        # ---- верх: метка происхождения, номер стадии, пометка «схема без масштаба»
        badge_bottom = add_badges(self, lay, segs, tau, font)
        if "lobe_cycles" in prep["elements"]:
            cache: dict[str, Text] = {}

            def stage_lbl():
                st = stages(prep, share())
                s_ = f"стадия {len(st)} из {prep['n_lobes']}"
                if s_ not in cache:
                    cache[s_] = txt(s_)
                m = cache[s_].copy().set_opacity(vis("lobe_cycles"))
                return m.move_to([right - m.width / 2, (top + badge_bottom) / 2, 0])
            self.add(always_redraw(stage_lbl))
        note = wrap(q["note"], font, fs, right - left, c["muted"])
        for line in note:
            line.align_to([left, 0, 0], direction=[-1, 0, 0])
        note.move_to([note.get_center()[0], badge_bottom - gap / 2 - note.height / 2, 0])
        self.add(note)
        cap_h = add_captions(self, lay, segs, tau, font, c["text"])
        area_top = note.get_bottom()[1] - gap
        area_bottom = bottom + cap_h + gap

        # ---- легенда зон (появляется вместе с зонами)
        def legend_group(width: float) -> VGroup:
            rows = VGroup()
            for z in zones:
                sw = Square(side_length=text_h * 0.8, stroke_width=0, fill_color=c["zones"][z["key"]], fill_opacity=1)
                t_ = wrap(z["legend"], font, fs, width - sw.width - gap / 2, c["text"])
                row = VGroup(sw, t_).arrange(direction=np.array([1, 0, 0]), buff=gap / 2, aligned_edge=np.array([0, 1, 0]))
                rows.add(row)
            rows.arrange(direction=np.array([0, -1, 0]), buff=gap / 3, aligned_edge=np.array([-1, 0, 0]))
            return rows

        # ---- раскладка панелей
        if landscape:
            col_w = (right - left - 2 * gap) / 2
            plan_x0, sec_x0, plan_w0, sec_w = left, left + col_w + 2 * gap, col_w, col_w
            legend = legend_group(col_w) if "zones" in prep["elements"] else VGroup()
            plan_h = area_top - area_bottom - (text_h + gap / 2) - (legend.height + gap if len(legend) else 0)
            plan_h = min(plan_h, plan_w0 * 0.75)
            plan_w = plan_w0
            sec_top = plan_top_lbl = area_top
            sec_h = area_top - area_bottom - (text_h + gap / 2)
        else:
            plan_x0, sec_x0, plan_w, sec_w = left, left, right - left, right - left
            legend = legend_group(right - left) if "zones" in prep["elements"] else VGroup()
            avail = area_top - area_bottom - 2 * (text_h + gap / 2) - gap - (legend.height + gap if len(legend) else 0)
            plan_h = min(plan_w * 0.7, avail * 0.55)
            sec_h = avail - plan_h
            plan_top_lbl = area_top
            sec_top = area_top - (text_h + gap / 2) - plan_h - gap
        if plan_h < u(200) or sec_h < u(200):
            raise LayoutError(f"схеме T3 не хватает места: план {plan_h / u(1):.0f} px, разрез {sec_h / u(1):.0f} px "
                              f"опорного кадра")

        # ---- план: конус у устья, зоны — те же границы, что в разрезе
        lbl_plan = txt("план", c["muted"])
        lbl_plan.move_to([plan_x0 + lbl_plan.width / 2, plan_top_lbl - text_h / 2, 0])
        p_top = plan_top_lbl - text_h - gap / 2
        p_cx = plan_x0 + plan_w / 2
        plan_box = Rectangle(width=plan_w, height=plan_h, stroke_color=c["muted"], stroke_width=2,
                             fill_color=c["water"], fill_opacity=1).move_to([p_cx, p_top - plan_h / 2, 0])
        mouth = np.array([p_cx, p_top - plan_h * MOUTH_FRAC, 0])
        half = np.radians(q["lobe_half_angle_deg"])
        r_full = min(plan_h * (1 - MOUTH_FRAC) - gap / 2, (plan_w / 2 - gap / 2) / np.sin(half))
        river = Line([p_cx, p_top, 0], mouth, color=c["river"], stroke_width=6)
        river_lbl = txt(q["river_label"], c["text"])
        river_lbl.move_to([p_cx + river_lbl.width / 2 + u(14), p_top - river_lbl.height / 2 - u(6), 0])
        cone_fill = c["zones"][zones[0]["key"]]

        def sector(r0: float, r1: float, color: str, opacity: float):
            return AnnularSector(inner_radius=max(r0, 1e-4) * r_full, outer_radius=max(r1, 2e-4) * r_full,
                                 angle=2 * half, start_angle=-np.pi / 2 - half, arc_center=mouth,
                                 stroke_width=0, fill_color=color, fill_opacity=opacity)

        def plan_view():
            g = VGroup()
            s = share()
            zv, cv = vis("zones"), vis("cone")
            for st in stages(prep, s):
                if st["active"]:
                    if zv < 1:
                        g.add(sector(0, st["growth"], cone_fill, cv * (1 - zv)))
                    for zb, z in zip(zone_bounds(prep, st["growth"]), zones):
                        if zv > 0:
                            g.add(sector(zb["from"], zb["to"], c["zones"][z["key"]], cv * zv))
                else:                                   # отмершая стадия — под активной, контур
                    ang = np.linspace(-np.pi / 2 - half, -np.pi / 2 + half, 60)
                    rr = st["growth"] * r_full
                    pts = np.column_stack([mouth[0] + rr * np.cos(ang), mouth[1] + rr * np.sin(ang), np.zeros_like(ang)])
                    arc = VMobject(stroke_color=c["text"], stroke_width=2,
                                   stroke_opacity=cv * q["abandoned_opacity"]).set_points_as_corners(
                        np.vstack([mouth, pts, mouth]))
                    g.add(DashedVMobject(arc, num_dashes=40))
            dv = vis("depocenter")
            if dv > 0:
                rd = depocenter_extent(prep, s) * r_full        # тот же край, что в разрезе; контур — сектор у устья
                ang = np.linspace(-np.pi / 2 - half, -np.pi / 2 + half, 60)
                arc_pts = np.column_stack([mouth[0] + rd * np.cos(ang), mouth[1] + rd * np.sin(ang), np.zeros_like(ang)])
                ring = VMobject(stroke_color=c["text"], stroke_width=3, stroke_opacity=dv).set_points_as_corners(
                    np.vstack([mouth, arc_pts, mouth]))
                g.add(DashedVMobject(ring, num_dashes=30))
            return g

        self.add(plan_box, always_redraw(plan_view), river, river_lbl, lbl_plan)
        if len(legend):
            legend.move_to([plan_x0 + legend.width / 2, p_top - plan_h - gap - legend.height / 2, 0])
            legend.add_updater(lambda m: m.set_opacity(vis("zones")))
            legend.set_opacity(0)
            self.add(legend)
            inside(lay, "легенда зон", legend)
        if "depocenter" in prep["elements"]:
            depo_lbl = txt(q["elements"]["depocenter"]["label"], c["text"])
            depo_lbl.move_to([plan_x0 + plan_w - depo_lbl.width / 2 - gap / 2, mouth[1] - depo_lbl.height / 2 - gap / 2, 0])
            depo_lbl.add_updater(lambda m: m.set_opacity(vis("depocenter")))
            depo_lbl.set_opacity(0)
            self.add(depo_lbl)
            inside(lay, "подпись депоцентра", depo_lbl)

        # ---- разрез по оси конуса: слева устье; стадии облекают одна другую
        lbl_sec = txt("разрез по оси конуса", c["muted"])
        lbl_sec.move_to([sec_x0 + lbl_sec.width / 2, sec_top - text_h / 2, 0])
        s_top = sec_top - text_h - gap / 2
        box_h = sec_h
        stage_col = txt(f"стадия {prep['n_lobes']}").width + gap / 2 if "lobe_cycles" in prep["elements"] else 0.0
        bx0, bw = sec_x0 + stage_col, sec_w - stage_col
        sec_box = Rectangle(width=bw, height=box_h, stroke_color=c["muted"], stroke_width=2, fill_color=c["water"],
                            fill_opacity=1).move_to([bx0 + bw / 2, s_top - box_h / 2, 0])
        y_floor = s_top - box_h
        H = box_h / (prep["n_lobes"] + STAGE_GAP)        # условная толщина стадии
        x_full = bw - gap
        X = np.linspace(0.0, 1.0, 241)
        to_pts = lambda xs, ys: np.column_stack([bx0 + xs * x_full, y_floor + ys * H, np.zeros_like(xs)])

        def section_view():
            g = VGroup()
            s = share()
            zv, cv = vis("zones"), vis("cone")
            stack = stack_profiles(prep, s, X)
            for st in stack:
                parts = [(zb, c["zones"][z["key"]]) for zb, z in zip(st["zones"], zones)] if zv > 0 else []
                whole = [({"from": 0.0, "to": st["growth"]}, cone_fill)] if zv < 1 else []
                for (zb, color), op in [(w, cv * (1 - zv)) for w in whole] + [(w, cv * zv) for w in parts]:
                    m = (X >= zb["from"]) & (X <= zb["to"])
                    if m.sum() < 2:
                        continue
                    xs = X[m]
                    pts = np.vstack([to_pts(xs, st["top"][m]), to_pts(xs[::-1], st["bottom"][m][::-1])])
                    g.add(Polygon(*pts, stroke_color=c["background"], stroke_width=1, stroke_opacity=op,
                                  fill_color=color, fill_opacity=op))
            k = len(stack) - 1
            wy = y_floor + (k + q["water_level"]) * H
            g.add(DashedLine([bx0, wy, 0], [bx0 + bw, wy, 0], color=c["text"], stroke_width=2, dash_length=u(12)))
            dv = vis("depocenter")
            if dv > 0:
                xd = depocenter_extent(prep, s)
                hi = max(st["top"][X <= xd].max() for st in stack)
                rect = Rectangle(width=xd * x_full, height=hi * H, stroke_color=c["text"], stroke_width=3,
                                 stroke_opacity=dv).move_to([bx0 + xd * x_full / 2, y_floor + hi * H / 2, 0])
                g.add(DashedVMobject(rect, num_dashes=40))
            lv = vis("lobe_cycles")
            if lv > 0:
                for st in stack:
                    t_ = txt(f"стадия {st['k'] + 1}", c["muted"]).set_opacity(lv)
                    y_mid = y_floor + (st["k"] + 0.5) * H
                    g.add(t_.move_to([sec_x0 + t_.width / 2, y_mid, 0]))
            return g

        water_lbl = txt(q["water_label"], c["muted"])

        def water_label():
            k = len(stages(prep, share())) - 1
            wy = y_floor + (k + q["water_level"]) * H
            m = water_lbl.copy()
            return m.move_to([bx0 + bw - m.width / 2 - u(8), min(wy + m.height / 2 + u(6), s_top - m.height / 2 - u(4)), 0])

        self.add(sec_box, always_redraw(section_view), always_redraw(water_label), lbl_sec)
        mouth_lbl = txt("устье", c["muted"])
        mouth_lbl.move_to([mouth[0] - mouth_lbl.width / 2 - u(14), mouth[1], 0])
        self.add(mouth_lbl)
        inside(lay, "подпись устья", mouth_lbl)
        for name, mob in (("план", plan_box), ("подпись плана", lbl_plan), ("разрез", sec_box),
                          ("подпись разреза", lbl_sec), ("пометка «схема без масштаба»", note), ("река", river_lbl)):
            inside(lay, name, mob)
        play_timeline(self, tau, p["total"], fps)
