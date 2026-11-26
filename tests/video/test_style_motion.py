"""Общий стиль серии: появление групп с растрами (регрессия), камера, служебный слой, пересечения подписей."""
import math

import numpy as np
import pytest
from manim import Circle, Group, ImageMobject, Text, ValueTracker, VGroup

from pipeline.video import build, style
from pipeline.video.layout import LONG_SAFE_ZONE, REF_LONG, Layout, LayoutError

COLORS = {"text": "#ECEFF4", "muted": "#8A96A3", "panel": "#1A2129", "background": "#0F1419"}


@pytest.fixture
def kit(tmp_path):
    from manim import tempconfig
    lay = Layout(LONG_SAFE_ZONE, 44, ref=REF_LONG)
    font = build._styleguide(build.DEFAULT_STYLEGUIDE)["font"]
    with tempconfig({"frame_height": 8.0, "frame_width": 8.0 * 16 / 9, "media_dir": str(tmp_path)}):
        yield style.Kit(None, lay, COLORS, font, ValueTracker(0.0))


def _masked_rgba(n=16, value=200):
    """RGBA с прозрачной маской (круг) и полупрозрачной полосой — альфа данных не равна 255 везде."""
    arr = np.zeros((n, n, 4), dtype=np.uint8)
    arr[..., :3] = value
    arr[..., 3] = 255
    arr[n // 2:, :, 3] = 128
    arr[style.circle_mask(n, n), 3] = 0
    return arr


# ---------------------------------------------------------------- ошибка А: растр с собственным обновлением

def test_self_updating_image_in_appearing_group_stays_hidden_until_reveal(kit):
    calls = {"n": 0}

    def source():                                         # растр каждый кадр пересчитывает pixel_array
        calls["n"] += 1
        arr = _masked_rgba()
        arr[..., 0] = (calls["n"] * 7) % 255              # содержимое меняется
        return arr

    img = style.DataImage(source)
    group = Group(img, Circle(radius=0.5))
    kit.show_from(group, 2.0)
    mask_out = style.circle_mask(16, 16)
    base_alpha = _masked_rgba()[..., 3].astype(float)

    def step(t):
        kit.tau.set_value(t)
        group.update(0)                                   # порядок как в сцене: группа, затем её элементы

    step(1.0)
    assert img.pixel_array[..., 3].max() == 0             # до появления — полностью скрыто
    step(2.0 + style.FADE_S / 2)
    op = style.reveal(2.0 + style.FADE_S / 2, 2.0)[0]
    assert 0 < op < 1
    assert np.allclose(img.pixel_array[..., 3], np.round(base_alpha * op), atol=1)   # во время появления — доля
    for _ in range(5):                                    # многократные обновления — без накопления
        step(2.0 + style.FADE_S + 1.0)
    assert np.array_equal(img.pixel_array[..., 3], _masked_rgba()[..., 3])          # после — данные как есть
    assert img.pixel_array[mask_out, 3].max() == 0        # прозрачные области маски сохраняются
    assert calls["n"] > 5                                 # растр действительно обновлялся сам


def test_plain_image_with_own_updater_is_rejected(kit):
    img = ImageMobject(_masked_rgba())
    img.add_updater(lambda m: m.pixel_array.__setitem__(slice(None), _masked_rgba()))
    with pytest.raises(TypeError, match="DataImage"):
        kit.show_from(Group(img), 1.0)


def test_outline_without_fill_stays_without_fill_when_appearing(kit):
    ring = Circle(radius=1.0, stroke_width=3)              # контур без заливки (кольцо врезки)
    g = VGroup(ring)
    kit.show_from(g, 1.0)
    kit.tau.set_value(5.0)
    g.update(0)
    assert ring.get_fill_opacity() == 0 and ring.get_stroke_opacity() == pytest.approx(1)


def test_grow_from_scales_from_origin_without_accumulation(kit):
    c = Circle(radius=1.0).move_to([2, 0, 0])
    g = VGroup(c)
    kit.grow_from(g, [0, 0, 0], 1.0)
    for _ in range(4):
        kit.tau.set_value(5.0)
        g.update(0)
    assert c.width == pytest.approx(2.0) and np.allclose(c.get_center(), [2, 0, 0])
    kit.tau.set_value(1.0 + style.GROW_S / 4)
    g.update(0)
    assert c.width < 2.0 and c.get_center()[0] < 2.0       # растёт из точки объекта


# ---------------------------------------------------------------- камера

AREA = (-6.0, 6.0, -3.0, 3.0)


def test_camera_overview_focus_and_fit():
    rig = style.CameraRig(AREA, [style.Focus(2.0, 6.0, (1.0, 3.0, 0.0, 1.0), "цель")])
    assert rig.state(0.0) == (0.0, 0.0, 1.0)
    st = rig.state(4.0)
    assert st[2] == pytest.approx(min(12 / 2, 6 / 1, style.MAX_ZOOM))            # кратность из геометрии цели
    for p in ((1.0, 0.0), (3.0, 1.0)):
        s = style.to_screen(p, st)
        assert AREA[0] - 1e-9 <= s[0] <= AREA[1] + 1e-9 and AREA[2] - 1e-9 <= s[1] <= AREA[3] + 1e-9
    assert rig.state(6.0 + style.TRANS_S + 0.01) == (0.0, 0.0, 1.0)             # возврат к общему виду


def test_camera_transitions_are_continuous_and_eased():
    rig = style.CameraRig(AREA, [style.Focus(2.0, 6.0, (1.0, 3.0, 0.0, 1.0), "a"),
                                 style.Focus(6.5, 9.0, (-5.0, -3.0, -2.0, -1.0), "b")])
    ts = np.linspace(0, 12, 2401)
    sts = np.array([rig.state(t) for t in ts])
    assert np.max(np.abs(np.diff(sts, axis=0))) < 0.2                            # без скачков
    a0 = rig.state(2.0 + 1e-3)
    assert a0[2] == pytest.approx(1.0, abs=1e-3)                                  # разгон с нуля
    # близкий следующий фокус — перелёт без возврата к общему виду
    k_mid = rig.state(6.0 + 0.5 * style.TRANS_S)[2]
    assert k_mid > 1.5


def test_camera_never_moves_in_true_scale_window():
    with pytest.raises(ValueError, match="истинного масштаба"):
        style.CameraRig(AREA, [style.Focus(2.0, 6.0, AREA, "x")], forbidden=[(6.5, 9.0)])
    rig = style.plan_camera(AREA, [style.Focus(2.0, 6.0, (1.0, 3.0, 0.0, 1.0), "x")], [(6.5, 9.0)])
    f = rig.focuses[0]
    assert f.b + style.TRANS_S <= 6.5                                             # обрезан до кадра истинного масштаба
    for t in np.linspace(6.5, 9.0, 11):
        assert rig.state(t) == (0.0, 0.0, 1.0)
    rig2 = style.plan_camera(AREA, [style.Focus(6.0, 7.0, AREA, "коротко")], [(7.2, 9.0)])
    assert not rig2.focuses and rig2.dropped


def test_hud_layer_keeps_screen_position_under_any_camera(kit):
    t = Text("метка", font=kit.font, font_size=20).move_to([1.0, 2.0, 0])
    snap = t.get_center().copy()
    states = iter([(0.0, 0.0, 1.0), (1.5, -0.7, 2.2), (-3.0, 1.0, 1.4)])
    cur = {"s": (0.0, 0.0, 1.0)}
    layer = style.HudLayer(lambda: cur["s"])
    layer.register(t)
    for st in states:
        cur["s"] = st
        layer.update(0)
        assert np.allclose(style.to_screen(t.get_center(), st)[:2], snap[:2], atol=1e-9)


# ---------------------------------------------------------------- пересечения подписей

def test_check_no_overlap(kit):
    a = kit.text("размеры условные").move_to([0, 0, 0])
    b = kit.text("м").move_to([a.get_right()[0] - 0.05, 0, 0])
    with pytest.raises(LayoutError, match="пересекается"):
        style.check_no_overlap([("пометка", a), ("м", b)])
    b.move_to([a.get_right()[0] + 0.5, 0, 0])
    style.check_no_overlap([("пометка", a), ("м", b)])


def test_beat_and_shot_windows():
    segs = [{"phrase_id": "p1", "beat": "hook", "start": 0, "hold_end": 2, "shot_id": "s1"},
            {"phrase_id": "p2", "beat": "naming", "start": 2, "hold_end": 4, "shot_id": "s1"},
            {"phrase_id": "p3", "beat": "prediction", "start": 4, "hold_end": 7, "shot_id": "s2"},
            {"phrase_id": "p4", "beat": "data", "start": 7, "hold_end": 9, "shot_id": "s2"}]
    assert style.beat_window(segs, {"naming", "prediction"}) == (2, 7)
    assert style.beat_window(segs, {"data"}, after=5) == (7, 9)
    assert style.beat_window(segs, {"decision"}) is None
    assert style.shot_window(segs, "s2") == (4, 9) and style.shot_window(segs, None) is None


def test_filled_pill_fades_from_its_own_opacity(kit):
    pill = kit.pill(kit.text("подпись"), opacity=0.8)
    box, txt = pill
    kit.show_from(pill, 1.0)
    kit.tau.set_value(0.5)
    pill.update(0)
    assert box.get_fill_opacity() == 0 and txt.get_fill_opacity() == 0           # до появления — не видна
    t = 1.0 + style.FADE_S / 2
    op = style.reveal(t, 1.0)[0]
    kit.tau.set_value(t)
    pill.update(0)
    assert box.get_fill_opacity() == pytest.approx(0.8 * op, rel=1e-3)           # от исходной прозрачности
    kit.tau.set_value(10.0)
    for _ in range(3):
        pill.update(0)
    assert box.get_fill_opacity() == pytest.approx(0.8) and txt.get_fill_opacity() == pytest.approx(1.0)
