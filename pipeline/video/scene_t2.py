"""Шаблон T2 «Каротаж», 16:9: измерение → правило → вывод.

Одна переменная — глубина прибора d (м, растёт вниз; через progress_at от времени ролика) —
задаёт положение прибора в стволе, раскрытие кривых до этой глубины, колонку решения и пунктир
глубины через все панели. Положение по вертикали везде одно: t2_template.depth_frac.
Ствол и прибор — схема (своя метка); кривые — данные с меткой набора («симуляция» или
«реальные данные»). Пропуски кривых — разрывы линии; в колонке решения «нет данных» — серая штриховка.
"""
from __future__ import annotations

import math

import numpy as np
from manim import (DashedLine, ImageMobject, Line, Rectangle, RoundedRectangle, Scene, Text, ValueTracker, VGroup,
                   VMobject, always_redraw)
from manim.utils.color import ManimColor

from pipeline.video.layout import Layout, LayoutError
from pipeline.video.scene_parts import (add_badges, add_captions, add_plaques, inside, play_timeline,
                                        shot_windows, visibility, wrap)
from pipeline.video.t1_template import fmt_num, nice_ceil
from pipeline.video.t2_template import curve_frac, decision_rows, depth_frac, revealed, value_at
from pipeline.video.timeline import progress_at, progress_knots

TEXT_PX = 44
GAP_PX = 24
BOREHOLE_PX, DEPTH_COL_PX, TRACK_PX, TRACK_GAP_PX, DECISION_PX = 200, 120, 320, 48, 160


def _rgba(hex_color: str, alpha: int = 255) -> np.ndarray:
    return np.array([*np.round(np.array(ManimColor(hex_color).to_rgb()) * 255), alpha], dtype=np.uint8)


def _op_txt(op: str) -> str:
    return {"<": "<", ">": ">", "<=": "≤", ">=": "≥"}[op]


class T2Scene(Scene):
    plan: dict  # задаётся build.py перед render()

    def construct(self) -> None:
        p = self.plan
        lay: Layout = p["layout"]
        prep = p["t2"]
        c, font, fps, segs = p["colors"], p["font"], p["fps"], p["segments"]
        fs = lay.font_size(TEXT_PX)
        u = lay.units
        gap = u(GAP_PX)
        left, right, bottom, top = lay.safe_box()
        width = right - left
        txt = lambda s, color=None: Text(s, font=font, font_size=fs, color=color or c["text"])
        text_h = txt("Жу0").height
        tau = ValueTracker(0.0)
        span = prep["bottom"] - prep["top"]
        knots = progress_knots([(s["phrase_id"], s["start"], s["end"]) for s in segs], prep["evolve_phrase_ids"], span)
        depth = lambda: prep["top"] + progress_at(tau.get_value(), knots)

        # ---- верхняя строка: метка данных, цепочка, глубина прибора
        badge_bottom = add_badges(self, lay, segs, tau, font)
        row1_y = (top + badge_bottom) / 2
        chain = txt(" → ".join(p["chain"]))
        chain.move_to([left + u(300) + chain.width / 2, row1_y, 0])         # сразу после метки, слева от глубины
        self.add(chain)
        dcache: dict[str, Text] = {}

        def depth_readout():
            s = f"глубина прибора: {fmt_num(depth(), 5)} м"
            if s not in dcache:
                dcache[s] = txt(s)
            m = dcache[s].copy()
            return m.move_to([right - m.width / 2, row1_y, 0])

        self.add(always_redraw(depth_readout))

        # ---- плашка кадра и школа обозначений
        plaque_top = badge_bottom - gap / 2
        school = txt(p["school_label"], c["muted"])
        school.move_to([right - school.width / 2, plaque_top - text_h / 2, 0])
        self.add(school)

        # ---- вертикальная разметка
        header_top = plaque_top - text_h - gap
        panel_top = header_top - text_h - gap / 2
        cap_h = add_captions(self, lay, segs, tau, font, c["text"])
        rule = prep["rule"]
        conds = " и ".join(f"{next(x['label'] for x in prep['curves'] if x['mnemonic'] == k['curve'])} "
                           f"{_op_txt(k['op'])} {fmt_num(k['value'])} "
                           f"{next(x['unit_display'] for x in prep['curves'] if x['mnemonic'] == k['curve'])}"
                           for k in rule["conditions"])
        rule_lines = [wrap(f"{rule['status_label']}: {conds}", font, fs, width, c["text"]),
                      wrap(f"вывод: {rule['conclusion']}", font, fs, width, c["text"]),
                      wrap(f"ограничение: {rule['caveat']}", font, fs, width, c["muted"])]
        block_h = sum(g.height for g in rule_lines) + gap / 2 * (len(rule_lines) - 1)
        block_bottom = bottom + cap_h + gap
        y = block_bottom + block_h
        for g in rule_lines:
            for line in g:
                line.align_to([left, 0, 0], direction=[-1, 0, 0])
            g.move_to([g.get_center()[0], y - g.height / 2, 0])
            inside(lay, "правило", g)
            self.add(g)
            y -= g.height + gap / 2
        scale_row_y = block_bottom + block_h + gap / 2 + text_h / 2
        panel_bottom = scale_row_y + text_h / 2 + gap / 2
        panel_h = panel_top - panel_bottom
        if panel_h < u(300):
            raise LayoutError(f"панелям T2 не хватает высоты: {panel_h / u(1):.0f} px опорного кадра")
        y_of = lambda d: panel_top - depth_frac(prep, d) * panel_h        # глубина растёт вниз
        px_per_m = (panel_h / u(1)) / span                                # px опорного кадра на метр по вертикали

        # ---- колонки
        x = left
        bh_l, x = x, x + u(BOREHOLE_PX) + gap
        dc_l, x = x, x + u(DEPTH_COL_PX) + gap
        tracks = []
        for _ in prep["curves"]:
            tracks.append(x)
            x += u(TRACK_PX) + u(TRACK_GAP_PX)
        dec_l = x - u(TRACK_GAP_PX) + gap
        if dec_l + u(DECISION_PX) > right + 1e-9:
            raise LayoutError("колонки T2 не помещаются по ширине")
        mid_y = (panel_top + panel_bottom) / 2

        def panel(l, w):
            return Rectangle(width=w, height=panel_h, stroke_color=c["muted"], stroke_width=2,
                             fill_color=c["panel"], fill_opacity=1).move_to([l + w / 2, mid_y, 0])

        # ствол и прибор — схема
        bh_w = u(BOREHOLE_PX)
        bh_cx = bh_l + bh_w / 2
        self.add(panel(bh_l, bh_w))
        sch = Text("схема", font=font, font_size=fs, color=c["schema"])
        pad = u(10)
        sch_box = RoundedRectangle(width=sch.width + 2 * pad, height=sch.height + 2 * pad, corner_radius=pad,
                                   stroke_color=c["schema"], stroke_width=2)
        sch_g = VGroup(sch_box, sch).move_to([bh_l + (sch.width + 2 * pad) / 2, header_top - text_h / 2, 0])
        sch.move_to(sch_box)
        self.add(sch_g)
        true_w = prep["borehole_diameter_m"] * px_per_m                   # px опорного кадра в истинном масштабе
        plaque_texts = {sid: next(s["plaque"] for s in segs if s["shot_id"] == sid) for sid, _, _ in shot_windows(segs)}
        if prep["true_scale_shot_id"] is not None:
            plaque_texts[prep["true_scale_shot_id"]] = ("истинный масштаб: ствол тоньше линии" if true_w < 1.5
                                                        else "истинный масштаб")
        add_plaques(self, lay, segs, tau, font, c["text"], plaque_top, plaque_texts)
        for sid, a, b in shot_windows(segs):
            k = prep["exaggeration"] if sid in prep["exaggerated_shots"] else 1.0
            w = max(u(true_w * k), u(1))
            vis = visibility(a, b, 0.0)
            hole = Rectangle(width=w, height=panel_h, stroke_width=0, fill_color=c["mud"],
                             fill_opacity=1).move_to([bh_cx, mid_y, 0])
            hole.add_updater(lambda m, v=vis: m.set_fill(opacity=v(tau.get_value())))
            self.add(hole)

            def tool(w=w, v=vis):
                d = depth()
                yy = y_of(d)
                o = v(tau.get_value())
                cable = Line([bh_cx, panel_top, 0], [bh_cx, yy, 0], color=c["text"], stroke_width=2,
                             stroke_opacity=o)
                body = Rectangle(width=w * 0.6, height=max(u(40), w * 1.5), stroke_width=0, fill_color=c["tool"],
                                 fill_opacity=o).move_to([bh_cx, yy, 0])
                return VGroup(cable, body)

            self.add(always_redraw(tool))

        # шкала глубины
        step = nice_ceil(span / 5)
        first = math.ceil(prep["top"] / step) * step
        for dv in np.arange(first, prep["bottom"] + 1e-9, step):
            t = txt(fmt_num(float(dv), 6))
            t.move_to([dc_l + u(DEPTH_COL_PX) - t.width / 2, y_of(float(dv)), 0])
            self.add(t, Line([dc_l + u(DEPTH_COL_PX) + gap / 4, y_of(float(dv)), 0],
                             [dc_l + u(DEPTH_COL_PX) + gap * 0.9, y_of(float(dv)), 0], color=c["muted"]))
        m_lbl = txt("м", c["muted"])
        m_lbl.move_to([dc_l + u(DEPTH_COL_PX) - m_lbl.width / 2, header_top - text_h / 2, 0])
        self.add(m_lbl)

        # треки кривых
        vcache: dict[str, Text] = {}
        for cv, tl in zip(prep["curves"], tracks):
            tw = u(TRACK_PX)
            self.add(panel(tl, tw))
            head = txt(f"{cv['label']}, {cv['unit_display']}", c["curve_colors"][cv["mnemonic"]])
            head.move_to([tl + head.width / 2, header_top - text_h / 2, 0])
            lo_t = txt(fmt_num(cv["range"][0]), c["muted"])
            hi_t = txt(fmt_num(cv["range"][1]) + (" лог." if cv["log"] else ""), c["muted"])
            lo_t.move_to([tl + lo_t.width / 2, scale_row_y, 0])
            hi_t.move_to([tl + tw - hi_t.width / 2, scale_row_y, 0])
            for name, m in (("заголовок трека", head), ("шкала", lo_t), ("шкала", hi_t)):
                inside(lay, name, m)
            self.add(head, lo_t, hi_t)

            def curve(cv=cv, tl=tl, tw=tw):
                dep, val = revealed(prep, cv["mnemonic"], depth())
                g = VGroup()
                if dep.size < 2:
                    return g
                xs = tl + np.clip(curve_frac(val, cv["range"], cv["log"]), 0, 1) * tw
                ys = np.array([y_of(float(d)) for d in dep])
                ok = np.isfinite(val)
                # непрерывные участки без пропусков — пропуск остаётся разрывом
                edges = np.flatnonzero(np.diff(np.concatenate([[0], ok.astype(int), [0]])))
                for a, b in zip(edges[::2], edges[1::2]):
                    if b - a >= 2:
                        pts = np.column_stack([xs[a:b], ys[a:b], np.zeros(b - a)])
                        g.add(VMobject(color=c["curve_colors"][cv["mnemonic"]], stroke_width=4)
                              .set_points_as_corners(pts))
                return g

            def readout(cv=cv, tl=tl, tw=tw):
                v = value_at(prep, cv["mnemonic"], depth())
                s = "нет данных" if not math.isfinite(v) else fmt_num(v)
                if s not in vcache:
                    vcache[s] = txt(s)
                m = vcache[s].copy()
                yy = min(max(y_of(depth()) - text_h * 0.8, panel_bottom + text_h / 2), panel_top - text_h / 2)
                return m.move_to([tl + tw - m.width / 2 - u(8), yy, 0])

            self.add(always_redraw(curve), always_redraw(readout))

        # колонка решения: 1 — правило выполнено, -1 — нет данных (серая штриховка), 0 — пусто
        dw = u(DECISION_PX)
        self.add(panel(dec_l, dw))
        dec_head = txt("решение")
        dec_head.move_to([dec_l + dw / 2, header_top - text_h / 2, 0])
        inside(lay, "решение", dec_head)
        self.add(dec_head)
        img_h, img_w = max(int(round(panel_h / u(1))), 1), 16              # строка ≈ 1 px опорного кадра
        state_rows = decision_rows(prep["depth"], prep["rule_state"], prep["top"], prep["bottom"], img_h)
        yy, xx = np.mgrid[0:img_h, 0:img_w]
        hatch = ((xx + yy) // 2) % 4 == 0
        base = np.zeros((img_h, img_w, 4), dtype=np.uint8)
        base[state_rows == 1] = _rgba(c["rule_true"])
        unk = state_rows == -1
        base[unk] = _rgba(c["uncertainty"], 90)
        base[unk[:, None].repeat(img_w, 1) & hatch] = _rgba(c["uncertainty"])
        depth_rows = prep["top"] + (np.arange(img_h) + 0.5) * span / img_h   # глубина центра строки
        dec_img = ImageMobject(base.copy())
        dec_img.stretch_to_fit_width(dw * 0.7).stretch_to_fit_height(panel_h)
        dec_img.move_to([dec_l + dw / 2, mid_y, 0])

        def reveal_decision(m):
            arr = base.copy()
            arr[depth_rows > depth() + 1e-9, :, 3] = 0
            m.pixel_array[:] = arr

        dec_img.add_updater(reveal_decision)
        self.add(dec_img)

        # пунктир глубины прибора через все панели — одна глубина для прибора, кривых и решения
        def depth_line():
            yv = y_of(depth())
            return DashedLine([bh_l, yv, 0], [dec_l + dw, yv, 0], color=c["tool"], stroke_width=2,
                              dash_length=u(14))

        self.add(always_redraw(depth_line))
        for name, m in (("цепочка", chain), ("школа", school), ("метка схемы", sch_g), ("м", m_lbl)):
            inside(lay, name, m)
        self.t2_layout = {"panel_h_px_ref": panel_h / u(1), "px_per_m_ref": px_per_m, "true_borehole_px": true_w}
        play_timeline(self, tau, p["total"], fps)
