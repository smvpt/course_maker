"""Сцены T1–T4 без рендера видео: безопасная зона, связь видов, шаги T2, камера и маркировка масштаба.

Тайминги условные (4 с на фразу); сцена строится, затем обновляется в разные моменты (как при рендере).
"""
import importlib
import math
from pathlib import Path

import numpy as np
import pytest

from contracts.models import SceneSpec, Script
from pipeline.video import build, style
from pipeline.video.layout import LONG_SAFE_ZONE, REF_LONG, Layout

ROOT = Path(__file__).resolve().parents[2]
TPL = ROOT / "domain" / "geology" / "templates"
SCENES = {"T1": ("scene_t1", "T1Scene"), "T2": ("scene_t2", "T2Scene"), "T3": ("scene_t3", "T3Scene"),
          "T4": ("scene_t4", "T4Scene")}


def _pair(name):
    d = ROOT / "fixtures" / "video" / name
    return (Script.model_validate_json((d / "script.json").read_text(encoding="utf-8")),
            SceneSpec.model_validate_json((d / "scene_spec.json").read_text(encoding="utf-8")))


@pytest.fixture
def scene_of(monkeypatch, tmp_path):
    from manim import tempconfig
    opened = []

    def make(name, fmt=None, times=None):
        script, spec = _pair(name)
        sg = build._styleguide(build.DEFAULT_STYLEGUIDE)
        tpl_plan, tpl_colors, _ = build._prepare_template(spec, script, sg, TPL)
        f = fmt or script.format
        lay = (Layout(sg["safe_zone"], sg["min_caption_px"]) if f == "short"
               else Layout(LONG_SAFE_ZONE, sg["min_caption_px"], ref=REF_LONG))
        shot_of = {pid: s for s in spec.shots for pid in s.phrase_ids}
        segs, t = [], 0.0
        for ph in script.phrases:
            segs.append({"phrase_id": ph.id, "start": t, "end": t + 4.0, "hold_end": t + 4.0 + ph.pause_after_s,
                         "on_screen": ph.on_screen, "shot_id": shot_of[ph.id].id, "plaque": shot_of[ph.id].plaque,
                         "label": shot_of[ph.id].label, "label_color": sg["provenance"][shot_of[ph.id].label],
                         "beat": ph.beat})
            t += 4.0 + ph.pause_after_s
        plan = {"layout": lay, "font": sg["font"], "fps": 15, "segments": segs, "total": t, "speech_total": t,
                **tpl_plan, "colors": {"text": sg["text"], "muted": sg["muted"], "panel": sg["panel"], **tpl_colors}}
        mod_name, cls_name = SCENES[spec.template]
        if spec.template == "T3" and tpl_plan["t3"]["mode"] == "qualitative":
            mod_name, cls_name = "scene_t3q", "T3SchemeScene"
        mod = importlib.import_module(f"pipeline.video.{mod_name}")
        cap = {}
        monkeypatch.setattr(mod, "play_timeline", lambda scene, tau, total, fps: cap.update(tau=tau))
        cfg = tempconfig({"frame_height": 8.0, "frame_width": 8.0 * lay.ref_w / lay.ref_h,
                          "pixel_width": lay.ref_w // 4, "pixel_height": lay.ref_h // 4, "disable_caching": True,
                          "verbosity": "WARNING", "media_dir": str(tmp_path / "manim")})
        cfg.__enter__()
        opened.append(cfg)
        scene = getattr(mod, cls_name)()
        scene.plan = plan
        scene.construct()                   # проверки безопасной зоны, кегля и пересечений — при построении
        for tv in (times if times is not None else (0.5, t / 2, t - 0.1)):
            cap["tau"].set_value(tv)
            scene.update_mobjects(0)
        return scene, plan, segs, cap["tau"]

    yield make
    for cfg in reversed(opened):
        cfg.__exit__(None, None, None)


def _at(scene, tau, t):
    tau.set_value(t)
    scene.update_mobjects(0)


def _rig(scene):
    for k in ("t1_camera", "t2_camera", "t3_camera", "t3q_camera", "t4_camera"):
        if hasattr(scene, k):
            return getattr(scene, k)
    raise AssertionError("сцена без камеры")


def test_t1_map_fills_width_and_graph_shares_its_x_scale(scene_of):
    scene, plan, _, _ = scene_of("t1_demo")
    lay = plan["layout"]
    left, right, _, _ = lay.safe_box()
    L = scene.t1_layout
    assert L["map_w_px_ref"] == pytest.approx((right - left) / lay.units(1))      # карта во всю ширину зоны
    assert L["map_h_px_ref"] >= 360 and L["graph_h_px_ref"] >= 160
    assert L["m_per_px_ref"] == pytest.approx(2 * plan["t1"]["r_max"] / L["map_w_px_ref"])


def test_t1_camera_zooms_the_model_and_flies_to_the_graph(scene_of):
    scene, plan, segs, tau = scene_of("t1_demo")
    rig = scene.t1_camera
    assert [f.name for f in rig.focuses] == ["область влияния", "тот же радиус на графике"]
    f0, f1 = rig.focuses
    assert f1.a - f0.b <= 1.5 * style.TRANS_S                                    # перелёт без возврата к общему виду
    for f in rig.focuses:
        t = (f.a + f.b) / 2 + style.TRANS_S / 2
        _at(scene, tau, t)
        st = rig.state(t)
        assert st[2] > 1.2                                                       # настоящее приближение камеры
        x0, x1, y0, y1 = f.box_at(t)
        ax0, ax1, ay0, ay1 = rig.area
        for p in ((x0, y0), (x1, y1)):                                           # цель целиком в рабочей области
            s = style.to_screen(p, st)
            assert ax0 - 1e-6 <= s[0] <= ax1 + 1e-6 and ay0 - 1e-6 <= s[1] <= ay1 + 1e-6
        assert scene.camera.frame.width == pytest.approx(8.0 * 9 / 16 / st[2], rel=1e-6)


@pytest.mark.parametrize("name", ["t1_demo", "t2_volve", "t2_demo", "t3_demo", "t4_demo"])
def test_true_scale_shot_is_unambiguous(name, scene_of):
    """Кадр истинного масштаба: камера на общем виде, условных врезок и приближений нет."""
    scene, plan, segs, tau = scene_of(name)
    prep = next(v for k, v in plan.items() if k in ("t1", "t2", "t3", "t4"))
    win = style.shot_window(segs, prep["true_scale_shot_id"])
    assert win is not None
    rig = _rig(scene)
    for t in np.linspace(win[0], win[1] - 1e-3, 9):
        assert rig.state(t) == (0.0, 0.0, 1.0)
    if hasattr(scene, "t2_lens_window"):                                         # врезка-схема T2 скрыта
        a, b = scene.t2_lens_window
        assert b <= win[0]
        for t in np.linspace(win[0], win[1] - 1e-3, 5):
            assert style.reveal(t, a, b)[0] == 0


@pytest.mark.parametrize("name", ["t2_demo", "t2_volve"])
def test_t2_layout_steps_and_single_text_slot(name, scene_of):
    scene, plan, segs, tau = scene_of(name)
    steps = plan["t2"]["step_starts"]
    assert [s["key"] for s in steps] == ["features", "rule", "conclusion"]
    order = [s["phrase_id"] for s in segs]
    idx = [order.index(s["phrase_id"]) for s in steps]
    assert idx[0] == 0 and idx == sorted(idx) and len(set(idx)) == 3
    assert scene.t2_layout["panel_h_px_ref"] >= 300
    # нижний слот: атрибуция → правило → вывод; вне переходов одновременно виден один текст
    start = {s["key"]: next(x["start"] for x in segs if x["phrase_id"] == s["phrase_id"]) for s in steps}
    wins = [(0.0, start["rule"]), (start["rule"], start["conclusion"]), (start["conclusion"], math.inf)]
    for t in np.linspace(0.6, segs[-1]["hold_end"] - 0.1, 40):
        vis = [style.reveal(t, a, b)[0] for a, b in wins]
        if all(abs(t - x) > style.FADE_S for x in (start["rule"], start["conclusion"])):
            assert sum(v > 0.01 for v in vis) == 1


def test_t2_steps_follow_script_beats():
    from pipeline.video import t2_template
    from pipeline.video.templates import load_template_config
    cfg = load_template_config(TPL, "T2")
    script, _ = _pair("t2_volve")
    by_id = {p.id: p.beat for p in script.phrases}
    st = {s["key"]: s["phrase_id"] for s in t2_template.step_starts(script, cfg)}
    assert by_id[st["rule"]] == "naming" and by_id[st["conclusion"]] == "decision"
    d = script.model_dump(by_alias=True)
    for p in d["phrases"]:
        if p["beat"] in ("decision", "final", "transfer"):
            p["beat"] = "data"
    st2 = {s["key"]: s["phrase_id"] for s in t2_template.step_starts(Script.model_validate(d), cfg)}
    assert st2["conclusion"] is None                                              # нет фразы вывода — шаг не открывается


def test_t2_camera_moves_from_thresholds_to_the_tool_depth(scene_of):
    scene, plan, segs, tau = scene_of("t2_volve")
    rig = scene.t2_camera
    assert [f.name for f in rig.focuses] == ["пороги правила", "значения на глубине прибора"]
    f = rig.focuses[1]
    boxes = []
    for t in (f.a + style.TRANS_S + 0.1, f.b - 0.2):
        _at(scene, tau, t)
        boxes.append(f.box_at(t))
        assert rig.state(t)[2] > 1.2
    assert all(b[1] > b[0] and b[3] > b[2] for b in boxes)


@pytest.mark.parametrize("name,fmt", [("t3_demo", "short"), ("t3_demo", "long"), ("t3_deltas", "long"),
                                      ("t3_deltas", "short"), ("t4_demo", "short")])
def test_t3_t4_scenes_use_the_common_camera(name, fmt, scene_of):
    scene, plan, segs, tau = scene_of(name, fmt=fmt)
    rig = _rig(scene)
    assert rig.focuses, rig.dropped                                               # приближение выбрано по сценарию
    for f in rig.focuses:
        t = min(f.a + style.TRANS_S + 0.2, f.b - 0.1)
        _at(scene, tau, t)
        assert rig.state(t)[2] > 1.15


def test_hud_stays_on_screen_while_camera_moves(scene_of):
    """Служебный слой: при любом положении камеры элементы стоят на месте экрана и сохраняют размер."""
    scene, plan, segs, tau = scene_of("t1_demo")
    rig = scene.t1_camera
    hud = next(m for m in scene.mobjects if isinstance(m, style.HudLayer))
    static = [it for it in hud.items if it["snap"] is not None and it["rise"] is None]
    assert static
    t = rig.focuses[0].a + style.TRANS_S + 0.3
    _at(scene, tau, t)
    st = rig.state(t)
    assert st[2] > 1.2
    for it in static:
        for sm, pts in it["snap"]:
            on_screen = np.array([style.to_screen(p, st)[:2] for p in sm.points])
            assert np.allclose(on_screen, pts[:, :2], atol=1e-6)
