"""Общий стиль серии (pipeline/video/style.py): чистые функции движения и появления, фактура, лупа, приёмы Kit."""
import math

import numpy as np
import pytest

from pipeline.video import style
from pipeline.video.layout import LONG_SAFE_ZONE, REF_LONG, Layout, LayoutError

COLORS = {"text": "#ECEFF4", "muted": "#8A96A3", "panel": "#1A2129", "background": "#0F1419"}


def test_smooth_progress_keeps_ends_and_is_monotonic():
    xs = np.linspace(0, 10, 201)
    ys = [style.smooth_progress(x, 10) for x in xs]
    assert ys[0] == 0 and ys[-1] == pytest.approx(10)
    assert all(b >= a - 1e-12 for a, b in zip(ys, ys[1:]))
    assert ys[10] < xs[10] and ys[-11] > xs[-11]                       # разгон и торможение


def test_reveal_fades_in_rises_and_respects_window():
    assert style.reveal(0.9, 1.0) == (0.0, 1.0)
    op0, r0 = style.reveal(1.0, 1.0)
    op1, r1 = style.reveal(1.0 + style.FADE_S, 1.0)
    assert op0 == 0 and r0 == 1 and op1 == pytest.approx(1) and r1 == pytest.approx(0)
    assert style.reveal(5.0, 1.0, 4.0)[0] == 0                         # после конца окна не виден
    mid = style.reveal(1.0 + style.FADE_S / 2, 1.0)
    assert 0 < mid[0] < 1 and 0 < mid[1] < 1


def test_pulse_runs_two_waves_then_stops():
    assert style.pulse_state(0.0, 1.0) == (0.0, 0.0)
    k, op = style.pulse_state(1.0 + 0.1, 1.0)
    assert k > 0 and op > 0
    assert style.pulse_state(1.0 + 2 * style.PULSE_S + 0.01, 1.0) == (0.0, 0.0)


def test_texture_is_deterministic_and_circle_masked():
    a = style.texture(40, 60, "#1A2129", "#8A96A3", seed=3)
    b = style.texture(40, 60, "#1A2129", "#8A96A3", seed=3)
    assert np.array_equal(a, b) and a.shape == (40, 60, 4)
    c = style.texture(50, 50, "#1A2129", "#8A96A3", seed=3, circle=True)
    assert c[0, 0, 3] == 0 and c[25, 25, 3] == 255
    g = style.grain_overlay(30, 30, "#ECEFF4", alpha=40, seed=1)
    assert set(np.unique(g[..., 3])) <= {0, 40}                        # прозрачный слой, цвета данных не меняет


def test_lens_magnification():
    assert style.lens_magnification(90, 2.0, 0.5) == pytest.approx(22.5)


@pytest.fixture
def kit(tmp_path):
    from manim import ValueTracker, tempconfig
    lay = Layout(LONG_SAFE_ZONE, 44, ref=REF_LONG)
    with tempconfig({"frame_height": 8.0, "frame_width": 8.0 * 16 / 9, "media_dir": str(tmp_path)}):
        from pipeline.video import build
        font = build._styleguide(build.DEFAULT_STYLEGUIDE)["font"]
        yield style.Kit(None, lay, COLORS, font, ValueTracker(0.0))


def test_callout_connects_anchor_to_pill_edge(kit):
    anchor = np.array([0.0, 0.0, 0.0])
    g = kit.callout("метка", anchor, [2.0, 0.5, 0])
    line, dot, pill = g
    assert np.allclose(line.get_start(), anchor) and np.allclose(dot.get_center(), anchor)
    assert line.get_end()[0] == pytest.approx(pill[0].get_left()[0])   # к ближнему краю таблетки


def test_arrow_tip_ends_at_target(kit):
    a = kit.arrow([0, 0, 0], [1, 0, 0])
    assert a[1].get_right()[0] == pytest.approx(1.0) and a[0].get_end()[0] < 1.0


def test_show_from_fades_in_with_rise(kit):
    t = kit.text("появление")
    base = t.get_center().copy()
    kit.show_from(t, 2.0)
    kit.tau.set_value(1.0)
    t.update(0)
    assert t.get_fill_opacity() == 0 and t.get_center()[1] < base[1]
    kit.tau.set_value(2.0 + style.FADE_S + 0.01)
    t.update(0)
    assert t.get_fill_opacity() == pytest.approx(1) and np.allclose(t.get_center(), base)


def test_lens_label_is_kept_inside_safe_zone_and_lines_are_tangent(kit):
    from manim import Group
    left, right, bottom, top = kit.lay.safe_box()
    c = np.array([left + 1.0, 0.0, 0.0])
    lens, lines = kit.lens(c, 0.9, Group(), lambda: np.array([3.0, 0.0, 0.0]), "увеличено в 38 раз")
    label = lens[-1]
    assert label.get_left()[0] >= left - 1e-9
    for ln in lines:
        p = ln.get_start()
        assert np.linalg.norm(p[:2] - c[:2]) == pytest.approx(0.9)   # линия начинается на кольце
    with pytest.raises(LayoutError):
        kit.lens(np.array([left, 0, 0]), 0.9, Group(), lambda: np.zeros(3), None)   # кольцо за безопасной зоной
