"""Компоновка 9:16 в пикселях опорного кадра 1080×1920 (стайлгайд)."""
import pytest

from pipeline.video.layout import Layout, LayoutError

SAFE = {"top": 220, "bottom": 380, "side": 70}


def test_font_size_maps_reference_px_to_manim_em():
    lay = Layout(SAFE, min_caption_px=44)
    # em в единицах сцены = font_size / 72; кадр высотой 8 единиц = 1920 px
    assert lay.font_size(44) == pytest.approx(44 * 8 / 1920 * 72)


def test_caption_smaller_than_styleguide_minimum_is_rejected():
    with pytest.raises(LayoutError, match="44"):
        Layout(SAFE, min_caption_px=44).font_size(40)


def test_safe_box_in_scene_units():
    lay = Layout(SAFE, min_caption_px=44)
    left, right, bottom, top = lay.safe_box()
    u = 8 / 1920
    assert top == pytest.approx(4 - 220 * u)
    assert bottom == pytest.approx(-4 + 380 * u)
    assert left == pytest.approx(-2.25 + 70 * u) and right == pytest.approx(2.25 - 70 * u)  # ширина 4.5


def test_check_inside_safe_zone():
    lay = Layout(SAFE, min_caption_px=44)
    left, right, bottom, top = lay.safe_box()
    lay.check_inside("ok", left, right, bottom, top)
    with pytest.raises(LayoutError, match="подпись"):
        lay.check_inside("подпись", left, right, bottom - 0.01, top)
