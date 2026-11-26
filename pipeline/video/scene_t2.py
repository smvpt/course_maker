"""Шаблон T2 «Каротаж», 16:9: признаки → правило → вывод.

Одна переменная — глубина прибора d (м, растёт вниз; через progress_at от времени ролика, со сглаживанием
разгона и торможения) — задаёт положение прибора в стволе, раскрытие кривых до этой глубины, значения на глубине,
колонку решения, полосы интервалов, линию глубины и сопровождение камерой. Положение по вертикали везде одно:
t2_template.depth_frac.

Шаги открываются по очереди с первой фразы своего бита (display.steps в T2.json): признаки (кривые и значения),
правило (пороги на треках, колонка решения, полосы интервалов), вывод (вывод с ограничением). Текст — в одном
нижнем слоте по очереди: короткая атрибуция данных → правило → вывод; полная атрибуция — в паспорте.

Общий стиль (style.py): служебный слой (метка, шаги, плашка, обозначения, слот, подписи фразы) стоит на месте;
камера приближается к порогам на правиле и перелетает к значениям на текущей глубине на данных, сопровождая
прибор; на выводе — общий вид и выделение колонки решения. Врезка — СХЕМА прибора («размеры условные»): вырастает
из прибора и скрыта в кадре истинного масштаба. Ствол и прибор — схема (своя метка); кривые — данные с меткой
набора. Пропуски кривых — разрывы линии; «нет данных» в колонке решения — серая штриховка.
"""
from __future__ import annotations

import math

import numpy as np
from manim import (DashedLine, Group, Line, MovingCameraScene, Polygon, Rectangle, RoundedRectangle, Text,
                   ValueTracker, VGroup, VMobject, always_redraw)
from manim.utils.color import ManimColor

from pipeline.video import style
from pipeline.video.layout import FRAME_H, Layout, LayoutError
from pipeline.video.scene_parts import add_badges, add_captions, add_plaques, inside, play_timeline, shot_windows, \
    visibility, wrap
from pipeline.video.style import DataImage, Focus, Kit, check_no_overlap
from pipeline.video.t1_template import fmt_num, nice_ceil
from pipeline.video.t2_art import tool_detail
from pipeline.video.t2_template import curve_frac, decision_rows, depth_frac, revealed, value_at
from pipeline.video.timeline import progress_at, progress_knots

TEXT_PX = 44
GAP_PX = 24
SECTION_PX, DEPTH_COL_PX, TRACK_PX, TRACK_GAP_PX, DECISION_PX = 420, 120, 285, 40, 120
BORE_X_PX, INSET_X_PX, INSET_R_PX = 40, 195, 100     # ствол и центр врезки от левого края разреза; радиус врезки


def _rgba(hex_color: str, alpha: int = 255) -> np.ndarray:
    return np.array([*np.round(np.array(ManimColor(hex_color).to_rgb()) * 255), alpha], dtype=np.uint8)


def _op_txt(op: str) -> str:
    return {"<": "<", ">": ">", "<=": "≤", ">=": "≥"}[op]


class T2Scene(MovingCameraScene):
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
        depth_at = lambda t: prep["top"] + style.smooth_progress(progress_at(t, knots), span)
        depth = lambda: depth_at(tau.get_value())
        kit = Kit(self, lay, c, font, tau)
        t_evolve = min((s["start"] for s in segs if s["phrase_id"] in prep["evolve_phrase_ids"]), default=0.0)
        ts_win = style.shot_window(segs, prep["true_scale_shot_id"])

        # ---- шаги показа: признаки → правило → вывод (с первой фразы своего бита)
        start_of = {s["phrase_id"]: s["start"] for s in segs}
        steps = [dict(st, t=start_of[st["phrase_id"]]) for st in prep["step_starts"] if st["phrase_id"] is not None]
        step_t = {st["key"]: st["t"] for st in steps}
        shown = lambda key: visibility(step_t[key], math.inf, style.FADE_S)(tau.get_value()) if key in step_t else 0.0

        def current_step() -> str:
            tv = tau.get_value()
            return [st["key"] for st in steps if st["t"] <= tv][-1] if steps and tv >= steps[0]["t"] else steps[0]["key"]

        # ---- служебный слой: метка, индикатор шагов, плашка, обозначения
        badge_bottom = add_badges(self, lay, segs, tau, font, add=kit.hud, fill=c["background"])
        row1_y = (top + badge_bottom) / 2
        badge_w = max(txt(lbl).width for lbl in {x["label"] for x in segs}) + 2 * u(14)   # как в add_badges
        x = left + badge_w + gap
        step_mobs = {}
        for i, st in enumerate(steps):
            if i:
                arr = txt("→", c["muted"])
                arr.move_to([x + arr.width / 2, row1_y, 0])
                kit.hud(arr)
                x += arr.width + gap / 2
            on, off = txt(st["label"]), txt(st["label"], c["muted"])
            for m in (on, off):
                m.move_to([x + m.width / 2, row1_y, 0])
            under = Line([x, row1_y - text_h / 2 - u(6), 0], [x + on.width, row1_y - text_h / 2 - u(6), 0],
                         color=c["tool"], stroke_width=style.STROKE["accent"] - 1)
            k = st["key"]
            on.add_updater(lambda m, k=k: m.set_opacity(1.0 if current_step() == k else 0.0))
            under.add_updater(lambda m, k=k: m.set_stroke(opacity=1.0 if current_step() == k else 0.0))
            off.add_updater(lambda m, k=k: m.set_opacity(0.0 if current_step() == k else 1.0))
            for m in (off, on, under):
                kit.hud(m)
            step_mobs[k] = on
            x += on.width + gap / 2

        plaque_top = badge_bottom - gap / 2
        ds = prep["dataset"]
        plaque_texts = {sid: next(s["plaque"] for s in segs if s["shot_id"] == sid) for sid, _, _ in shot_windows(segs)}
        school = kit.pill(txt(p["school_label"], c["muted"]), stroke=False, opacity=0.9)
        school.move_to([right - school.width / 2, plaque_top - school.height / 2, 0])
        kit.show_from(school, 0.0, step_t.get("rule", math.inf), rise=False, hud=True)

        # ---- нижний слот: атрибуция → правило → вывод с ограничением (по очереди, одно место)
        cap_h = add_captions(self, lay, segs, tau, font, c["text"], pill=c["panel"], add=kit.hud)
        rule = prep["rule"]
        unit_of = {x["mnemonic"]: x["unit_display"] for x in prep["curves"]}
        label_of = {x["mnemonic"]: x["label"] for x in prep["curves"]}
        conds = " и ".join(f"{label_of[k['curve']]} {_op_txt(k['op'])} {fmt_num(k['value'])} {unit_of[k['curve']]}"
                           for k in rule["conditions"])
        short = ds.attribution.split(";")[0].split(",")[0].strip()
        data_line = short if short.lower().startswith("данные") else f"данные: {short}"
        slot_w = width - 2 * kit.pad
        slot_items = [(wrap(f"{data_line} · полностью — в паспорте", font, fs, slot_w, c["muted"]),
                       0.0, step_t.get("rule", math.inf)),
                      (wrap(f"{rule['status_label']}: {conds}", font, fs, slot_w, c["text"]),
                       step_t.get("rule", math.inf), step_t.get("conclusion", math.inf)),
                      (wrap(f"вывод: {rule['conclusion']} — {rule['caveat']}", font, fs, slot_w, c["text"]),
                       step_t.get("conclusion", math.inf), math.inf)]
        slot_h = max(g.height for g, _, _ in slot_items) + 1.4 * kit.pad
        slot_bottom = bottom + cap_h + gap
        slot_top = slot_bottom + slot_h
        for g, a, b in slot_items:
            for line in g:
                line.align_to([left + kit.pad, 0, 0], direction=[-1, 0, 0])
            g.move_to([g.get_center()[0], slot_top - kit.pad * 0.7 - g.height / 2, 0])
            pill = kit.pill(g, stroke=False, opacity=0.9)
            pill[0].stretch_to_fit_width(width).move_to([0, pill[0].get_center()[1], 0]).align_to([left, 0, 0], [-1, 0, 0])
            inside(lay, "нижний слот", pill)
            if a < math.inf:
                kit.show_from(pill, a, b, hud=True)

        # ---- вертикальная разметка мира
        header_top = plaque_top - text_h - 1.4 * kit.pad - gap / 2
        panel_top = header_top - text_h - gap / 2
        scale_row_y = slot_top + gap / 2 + text_h / 2
        panel_bottom = scale_row_y + text_h / 2 + gap / 2
        panel_h = panel_top - panel_bottom
        if panel_h < u(300):
            raise LayoutError(f"панелям T2 не хватает высоты: {panel_h / u(1):.0f} px опорного кадра")
        y_of = lambda d: panel_top - depth_frac(prep, d) * panel_h        # глубина растёт вниз
        px_per_m = (panel_h / u(1)) / span                                # px опорного кадра на метр по вертикали

        # ---- колонки
        x = left
        bh_l, x = x, x + u(SECTION_PX) + gap
        dc_l, x = x, x + u(DEPTH_COL_PX) + gap
        tracks = []
        for _ in prep["curves"]:
            tracks.append(x)
            x += u(TRACK_PX) + u(TRACK_GAP_PX)
        dec_l = x - u(TRACK_GAP_PX) + gap
        dw = u(DECISION_PX)
        if dec_l + dw > right + 1e-9:
            raise LayoutError("колонки T2 не помещаются по ширине")
        mid_y = (panel_top + panel_bottom) / 2

        def panel(l, w):
            return Rectangle(width=w, height=panel_h, stroke_color=c["muted"], stroke_width=style.STROKE["line"],
                             fill_color=c["panel"], fill_opacity=1).move_to([l + w / 2, mid_y, 0])

        # ---- разрез (схема): порода с крапом, ствол с раствором и стенками, кабель и прибор
        sec_w = u(SECTION_PX)
        self.add(panel(bh_l, sec_w))
        rock = DataImage(style.texture(max(int(panel_h / u(1)), 1), max(int(sec_w / u(1)), 1), c["panel"], c["muted"],
                                       density=0.0035, size=2, seed=7, mix=0.35))
        rock.stretch_to_fit_width(sec_w).stretch_to_fit_height(panel_h).move_to([bh_l + sec_w / 2, mid_y, 0])
        self.add(rock, Rectangle(width=sec_w, height=panel_h, stroke_color=c["muted"],
                                 stroke_width=style.STROKE["line"]).move_to([bh_l + sec_w / 2, mid_y, 0]))
        bh_cx = bh_l + u(BORE_X_PX)
        sch = Text("схема", font=font, font_size=fs, color=c["schema"])
        pad = u(10)
        sch_box = RoundedRectangle(width=sch.width + 2 * pad, height=sch.height + 2 * pad, corner_radius=pad,
                                   stroke_color=c["schema"], stroke_width=style.STROKE["line"])
        sch_g = VGroup(sch_box, sch).move_to([bh_l + (sch.width + 2 * pad) / 2, header_top - text_h / 2, 0])
        sch.move_to(sch_box)
        self.add(sch_g)
        true_w = prep["borehole_diameter_m"] * px_per_m                   # px опорного кадра в истинном масштабе
        if prep["true_scale_shot_id"] is not None:
            plaque_texts[prep["true_scale_shot_id"]] = ("истинный масштаб: ствол тоньше линии" if true_w < 1.5
                                                        else "истинный масштаб")
        add_plaques(self, lay, segs, tau, font, c["text"], plaque_top, plaque_texts, add=kit.hud, pill=c["panel"])
        tool_th = u(70)
        for sid, a, b in shot_windows(segs):
            k = prep["exaggeration"] if sid in prep["exaggerated_shots"] else 1.0
            w = max(u(true_w * k), u(1))
            vis = visibility(a, b, 0.0)
            hole = VGroup(Rectangle(width=w, height=panel_h, stroke_width=0, fill_color=c["mud"], fill_opacity=1)
                          .move_to([bh_cx, mid_y, 0]),
                          *[Line([bh_cx + sg_ * w / 2, panel_top, 0], [bh_cx + sg_ * w / 2, panel_bottom, 0],
                                 color=c["text"], stroke_width=style.STROKE["hair"]) for sg_ in (-1, 1)])
            hole.add_updater(lambda m, v=vis: m.set_opacity(v(tau.get_value())))
            self.add(hole)

            def tool(w=w, v=vis):
                yy = y_of(depth())
                o = v(tau.get_value())
                if o <= 0:
                    return VGroup()
                cable = Line([bh_cx, panel_top, 0], [bh_cx, yy, 0], color=c["text"], stroke_width=style.STROKE["line"])
                tw_ = max(w * 0.7, u(14))
                yc = min(max(yy, panel_bottom + tool_th / 2), panel_top - tool_th / 2)   # корпус — в панели
                body, _ = tool_detail(bh_cx, yc + tool_th / 2, yc - tool_th / 2, tw_,
                                      [(cv["kind"], c["curve_colors"][cv["mnemonic"]]) for cv in prep["curves"]], c)
                return VGroup(cable, body)

            self.add(always_redraw(tool))
        up = kit.callout("к устью", [bh_cx + u(4), panel_top - u(24), 0], [bh_cx + u(120), panel_top - u(40), 0])
        self.add(up, kit.arrow([bh_cx + u(16), panel_top - u(70), 0], [bh_cx + u(16), panel_top - u(10), 0],
                               width="line"))

        # ---- врезка: СХЕМА прибора (размеры условные); порода в ней едет вверх, пока прибор идёт вниз
        R = u(INSET_R_PX)
        note = "схема прибора,\nразмеры условные"
        note_h = kit.text(note).height + 1.4 * kit.pad + kit.gap / 3
        ic = np.array([bh_l + u(INSET_X_PX), mid_y + note_h / 2, 0])
        if ic[1] + R > panel_top - u(70) or ic[1] - R - note_h < panel_bottom:
            raise LayoutError("врезке T2 не хватает высоты панели")
        D = max(int(round(2 * R / u(1))), 8)
        big = style.texture(D * 4, D, c["panel"], c["muted"], density=0.0025, size=5, seed=11, mix=0.45)
        outside = style.circle_mask(D, D)

        def lens_rgba():
            off = int(round((depth() - prep["top"]) / span * (big.shape[0] - D)))
            arr = big[off:off + D].copy()
            arr[outside, 3] = 0
            return arr

        lens_rock = DataImage(lens_rgba)
        lens_rock.stretch_to_fit_width(2 * R).stretch_to_fit_height(2 * R).move_to(ic)
        a_ = R * 0.36                                       # полуширина ствола во врезке
        xs = np.linspace(-a_, a_, 40)
        ys = np.sqrt(np.maximum(R * R - xs ** 2, 0))
        mud = Polygon(*np.column_stack([ic[0] + np.r_[xs, xs[::-1]], ic[1] + np.r_[ys, -ys[::-1]], np.zeros(80)]),
                      stroke_width=0, fill_color=c["mud"], fill_opacity=1)
        walls = VGroup(*[Line([ic[0] + s_ * a_, ic[1] + ys[0], 0], [ic[0] + s_ * a_, ic[1] - ys[0], 0],
                              color=c["text"], stroke_width=style.STROKE["line"]) for s_ in (-1, 1)])
        sections = [(cv["kind"], c["curve_colors"][cv["mnemonic"]]) for cv in prep["curves"]]
        t_top, t_bot = ic[1] + R * 0.62, ic[1] - R * 0.85
        tool_g, anchors = tool_detail(ic[0], t_top, t_bot, a_ * 1.1, sections, c)
        cable_in = Line([ic[0], ic[1] + R, 0], [ic[0], t_top, 0], color=c["text"], stroke_width=style.STROKE["bold"])
        labels = []
        box_h = text_h + 1.4 * kit.pad
        for i, (cv, anc) in enumerate(zip(prep["curves"], anchors)):
            w_lbl = kit.text(cv["label"]).width + 2 * kit.pad
            yb = ic[1] + (len(anchors) - 1) / 2 * (box_h + u(14)) - i * (box_h + u(14))
            labels.append(kit.callout(cv["label"], anc, [ic[0] + R + gap / 2 + w_lbl / 2, yb, 0]))
        t_lens = t_evolve
        t_lens_end = ts_win[0] if ts_win else math.inf
        lens_vis = lambda: style.reveal(tau.get_value(), t_lens, t_lens_end)[0]
        lens, lens_lines = kit.lens(ic, R, Group(lens_rock, mud, walls, cable_in, tool_g, *labels),
                                    lambda: np.array([bh_cx, min(max(y_of(depth()), panel_bottom), panel_top), 0]),
                                    note, visible=lens_vis, bounds=(bh_l + kit.pad / 2, bh_l + sec_w - kit.pad / 2))
        for name, m in (("врезка", lens[-2]), ("пометка врезки", lens[-1]),
                        *[(f"выноска {i}", lb) for i, lb in enumerate(labels)]):
            inside(lay, name, m)
            if m.get_right()[0] > bh_l + sec_w + 1e-9 or m.get_left()[0] < bh_l - 1e-9:
                raise LayoutError(f"«{name}» выходит за панель разреза")
        kit.grow_from(lens, [bh_cx, y_of(depth_at(t_lens)), 0], t_lens, t_lens_end)

        def moving_arrow():                                # стрелка спуска во врезке — пока прибор движется
            t = tau.get_value()
            if lens_vis() < 0.99 or progress_at(t + 0.1, knots) <= progress_at(t, knots) + 1e-9:
                return VGroup()
            x_a = ic[0] - a_ - (R - a_) / 2
            return kit.arrow([x_a, ic[1] + R * 0.35, 0], [x_a, ic[1] - R * 0.35, 0])

        # ---- шкала глубины
        step = nice_ceil(span / 5)
        first = math.ceil(prep["top"] / step) * step
        depth_lbls = []
        for dv in np.arange(first, prep["bottom"] + 1e-9, step):
            t = txt(fmt_num(float(dv), 6), c["muted"])
            t.move_to([dc_l + u(DEPTH_COL_PX) - t.width / 2, y_of(float(dv)), 0])
            depth_lbls.append(t)
            self.add(t, Line([dc_l + u(DEPTH_COL_PX) + gap / 4, y_of(float(dv)), 0],
                             [dc_l + u(DEPTH_COL_PX) + gap * 0.9, y_of(float(dv)), 0], color=c["muted"]))
        m_lbl = txt("м", c["muted"])
        m_lbl.move_to([dc_l + u(DEPTH_COL_PX) - m_lbl.width / 2, header_top - text_h / 2, 0])
        self.add(m_lbl)

        # ---- панели треков и колонки решения
        for tl in tracks:
            self.add(panel(tl, u(TRACK_PX)))
        self.add(panel(dec_l, dw))

        # интервалы, где правило выполнено: полосы через разрез, треки и решение (с шага «правило», до глубины)
        img_h, img_w = max(int(round(panel_h / u(1))), 1), 16              # строка ≈ 1 px опорного кадра
        state_rows = decision_rows(prep["depth"], prep["rule_state"], prep["top"], prep["bottom"], img_h)
        depth_rows = prep["top"] + (np.arange(img_h) + 0.5) * span / img_h   # глубина центра строки
        band_base = np.zeros((img_h, 2, 4), dtype=np.uint8)
        band_base[state_rows == 1] = _rgba(c["rule_true"], int(round(255 * p["band_opacity"])))

        def band_rgba():
            arr = band_base.copy()
            arr[depth_rows > depth() + 1e-9, :, 3] = 0
            arr[..., 3] = (arr[..., 3] * shown("rule")).astype(np.uint8)
            return arr

        band = DataImage(band_rgba)
        band.stretch_to_fit_width(dec_l + dw - bh_l).stretch_to_fit_height(panel_h)
        band.move_to([(bh_l + dec_l + dw) / 2, mid_y, 0])
        self.add(band, lens_lines, lens, always_redraw(moving_arrow),
                 kit.pulse(lambda: np.array([bh_cx, y_of(depth()), 0]), t_evolve, u(40)))

        # ---- треки: заголовок, шкала, кривая до глубины прибора, значение на глубине, порог правила
        vcache: dict[str, VGroup] = {}
        cond_of = {k["curve"]: k for k in rule["conditions"]}
        thr_labels, heads, scale_lbls = [], [], []
        for cv, tl in zip(prep["curves"], tracks):
            tw = u(TRACK_PX)
            col = c["curve_colors"][cv["mnemonic"]]
            head = txt(f"{cv['label']}, {cv['unit_display']}", col)
            head.move_to([tl + head.width / 2, header_top - text_h / 2, 0])
            lo_t = txt(fmt_num(cv["range"][0]), c["muted"])
            hi_t = txt(fmt_num(cv["range"][1]) + (" лог." if cv["log"] else ""), c["muted"])
            lo_t.move_to([tl + lo_t.width / 2, scale_row_y, 0])
            hi_t.move_to([tl + tw - hi_t.width / 2, scale_row_y, 0])
            heads.append((f"заголовок {cv['label']}", head))
            scale_lbls += [(f"шкала {cv['label']} min", lo_t), (f"шкала {cv['label']} max", hi_t)]
            for name, m in (("заголовок трека", head), ("шкала", lo_t), ("шкала", hi_t)):
                inside(lay, name, m)
            self.add(head, lo_t, hi_t)
            cond = cond_of.get(cv["mnemonic"])
            if cond is not None:                        # порог правила на треке — с шага «правило»
                fx = float(np.clip(curve_frac(np.array([cond["value"]]), cv["range"], cv["log"])[0], 0, 1))
                xx = tl + fx * tw
                thr = DashedLine([xx, panel_top, 0], [xx, panel_bottom, 0], color=c["text"],
                                 stroke_width=style.STROKE["line"], dash_length=u(10))
                thr_t = txt(f"{_op_txt(cond['op'])} {fmt_num(cond['value'])}")
                tx = min(max(xx + u(8) + thr_t.width / 2, tl + thr_t.width / 2 + u(6)), tl + tw - thr_t.width / 2 - u(6))
                if cond["op"] in ("<", "<="):
                    tx = min(max(xx - u(8) - thr_t.width / 2, tl + thr_t.width / 2 + u(6)), tl + tw - thr_t.width / 2 - u(6))
                thr_p = kit.pill(thr_t).move_to([tx, panel_top - text_h / 2 - kit.pad * 1.2, 0])
                thr.add_updater(lambda m: m.set_stroke(opacity=shown("rule")))
                thr.set_stroke(opacity=0)
                self.add(thr)
                inside(lay, "порог правила", thr_p)
                if "rule" in step_t:
                    thr_labels.append(kit.show_from(thr_p, step_t["rule"]))

            def curve(cv=cv, tl=tl, tw=tw, col=col):
                dep, val = revealed(prep, cv["mnemonic"], depth())
                g = VGroup()
                if dep.size < 2:
                    return g
                xs_ = tl + np.clip(curve_frac(val, cv["range"], cv["log"]), 0, 1) * tw
                ys_ = np.array([y_of(float(d)) for d in dep])
                ok = np.isfinite(val)
                # непрерывные участки без пропусков — пропуск остаётся разрывом
                edges = np.flatnonzero(np.diff(np.concatenate([[0], ok.astype(int), [0]])))
                for a, b in zip(edges[::2], edges[1::2]):
                    if b - a >= 2:
                        pts = np.column_stack([xs_[a:b], ys_[a:b], np.zeros(b - a)])
                        g.add(VMobject(color=col, stroke_width=4).set_points_as_corners(pts))
                return g

            def readout(cv=cv, tl=tl, tw=tw):
                v = value_at(prep, cv["mnemonic"], depth())
                s = "нет данных" if not math.isfinite(v) else fmt_num(v)
                if s not in vcache:
                    vcache[s] = kit.pill(txt(s), stroke=False, opacity=0.9)
                g = vcache[s].copy()
                yy = min(max(y_of(depth()) - text_h * 0.95, panel_bottom + g.height / 2 + u(4)),
                         panel_top - g.height / 2 - u(4))
                return g.move_to([tl + tw - g.width / 2 - u(6), yy, 0])

            self.add(always_redraw(curve), always_redraw(readout))

        self.add(*thr_labels)

        # ---- колонка решения: 1 — правило выполнено, -1 — нет данных (штриховка), 0 — пусто; с шага «правило»
        dec_head = txt("решение")
        dec_head.move_to([dec_l + dw / 2, header_top - text_h / 2, 0])
        inside(lay, "решение", dec_head)
        if "rule" in step_t:
            self.add(kit.show_from(dec_head, step_t["rule"]))
        yy_, xx_ = np.mgrid[0:img_h, 0:img_w]
        hatch = ((xx_ + yy_) // 2) % 4 == 0
        base = np.zeros((img_h, img_w, 4), dtype=np.uint8)
        base[state_rows == 1] = _rgba(c["rule_true"])
        unk = state_rows == -1
        base[unk] = _rgba(c["uncertainty"], 90)
        base[unk[:, None].repeat(img_w, 1) & hatch] = _rgba(c["uncertainty"])

        def decision_rgba():
            arr = base.copy()
            arr[depth_rows > depth() + 1e-9, :, 3] = 0
            arr[..., 3] = (arr[..., 3] * shown("rule")).astype(np.uint8)
            return arr

        dec_img = DataImage(decision_rgba)
        dec_img.stretch_to_fit_width(dw * 0.7).stretch_to_fit_height(panel_h)
        dec_img.move_to([dec_l + dw / 2, mid_y, 0])
        self.add(dec_img)

        # ---- текущая глубина: линия через все панели и бирка на шкале — одна глубина для всего
        dcache: dict[str, VGroup] = {}

        def depth_marker():
            yv = y_of(depth())
            # в разрезе — отрезок у ствола (врезка не перечёркивается), дальше — через шкалу, треки и решение
            line = VGroup(Line([bh_l, yv, 0], [bh_l + u(BORE_X_PX) * 2, yv, 0], color=c["tool"],
                               stroke_width=style.STROKE["bold"]),
                          Line([dc_l, yv, 0], [dec_l + dw, yv, 0], color=c["tool"], stroke_width=style.STROKE["bold"]))
            s = f"{fmt_num(depth(), 5)} м"
            if s not in dcache:
                dcache[s] = kit.tag(s, c["tool"])          # бирка текущего значения — общий приём
            g = dcache[s].copy()
            cx = dc_l + u(DEPTH_COL_PX) + gap * 0.9 - g.width / 2
            cx = max(cx, dc_l - gap / 2 + g.width / 2)
            g.move_to([cx, min(max(yv, panel_bottom + g.height / 2), panel_top - g.height / 2), 0])
            return VGroup(line, g)

        self.add(always_redraw(depth_marker))

        # ---- проверка пересечений: строка заголовков, шкалы, выноска «к устью»
        check_no_overlap([("метка схемы", sch_g), ("м", m_lbl), ("решение", dec_head), *heads])
        check_no_overlap(scale_lbls)
        check_no_overlap([("к устью", up[2]), ("врезка", lens[-2])])
        for name, m in (("метка схемы", sch_g), ("м", m_lbl), *[(f"шаг {k}", m) for k, m in step_mobs.items()]):
            inside(lay, name, m)

        # ---- камера: пороги (правило) → значения на текущей глубине (данные, камера ведёт прибор) → общий вид
        area = (left, right, slot_top + kit.pad, plaque_top - u(70))
        cands = []
        w_rule = style.beat_window(segs, {"naming", "prediction"})
        if w_rule and "rule" in step_t:
            cands.append(Focus(max(w_rule[0], step_t["rule"]), w_rule[1],
                               (tracks[0] - u(10), dec_l + dw, panel_top - panel_h * 0.42, header_top + kit.pad),
                               "пороги правила"))

        def depth_box(t: float):
            yv = y_of(depth())
            hh = panel_h * 0.4                              # высота цели: значения заполняют кадр
            y0 = max(yv - hh, panel_bottom - text_h - gap)            # у забоя — со строкой шкал
            y1 = min(y0 + 2 * hh, panel_top)
            return dc_l - u(70), dec_l + dw, y0, y1

        w_data = style.beat_window(segs, {"data"}, after=w_rule[1] if w_rule else -math.inf)
        if w_data:
            cands.append(Focus(w_data[0], w_data[1], depth_box, "значения на глубине прибора", max_zoom=2.0))
        rig = style.plan_camera(area, cands, [ts_win] if ts_win else [])
        kit.use_camera(rig)
        if "conclusion" in step_t:
            self.add(kit.highlight(lambda: (dec_l, dec_l + dw, panel_bottom, panel_top), step_t["conclusion"] + 0.2))
        kit.set_zoom_tag_top(plaque_top - u(70) + kit.pad)
        kit.finish(scrim_bands=[(plaque_top - u(70) + kit.pad / 2, FRAME_H / 2), (-FRAME_H / 2, slot_top + kit.pad / 2)])
        self.t2_layout = {"panel_h_px_ref": panel_h / u(1), "px_per_m_ref": px_per_m, "true_borehole_px": true_w}
        self.t2_camera = rig
        self.t2_lens_window = (t_lens, t_lens_end)
        play_timeline(self, tau, p["total"], fps)
