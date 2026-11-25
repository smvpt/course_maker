from pathlib import Path

import pytest

from pipeline.verify.numbers import extract_numbers, missing_numbers, words_to_numbers
from pipeline.verify.pages import load_pages

ROOT = Path(__file__).resolve().parents[2]
BAREN = ROOT / "data/books/ctrl_barenblatt.md"


@pytest.mark.parametrize("text,expected", [
    ("коэффициент 0,25 при давлении", [0.25]),
    ("пористость 0.25", [0.25]),
    ("толщина 5–20 м", [5, 20]),
    ("Re ~ 0,1—1,0", [0.1, 1.0]),
    ("около 10⁻² м", [0.01]),
    ("порядка 10⁴ см²/с", [10000, 2]),
    ("модуль $5 \\cdot 10^2 - 2 \\cdot 10^{3}$ МПа", [500, 2000]),
    ("снижается на 40 %", [40]),
    ("тираж 2 800 экз.", [2800]),
    ("τ ≈ 10⁹ с ≈ 30 лет", [1e9, 30]),
])
def test_extract_numbers(text, expected):
    assert extract_numbers(text) == pytest.approx(expected)


@pytest.mark.parametrize("text,expected", [
    ("двадцать пять метров", [25]),
    ("триста метров", [300]),
    ("около трёх часов", [3]),
    ("две тысячи восемьсот", [2800]),
    ("ноль целых одна десятая секунды", [0.1]),
    ("четыре целых одна десятая процента", [4.1]),
    ("полтора метра", [1.5]),
    ("сто суток и тридцать лет", [100, 30]),
    ("десять миллионов", [10_000_000]),
    ("одна из причин и двадцать один метр", [21]),
    ("одна тысяча", [1000]),
])
def test_words_to_numbers(text, expected):
    assert words_to_numbers(text) == pytest.approx(expected)


def test_extract_numbers_includes_words():
    assert extract_numbers("при L = 300 м — около трёх часов") == pytest.approx([300, 3])


def test_numbers_from_source_found():
    src = [load_pages(BAREN)[42]]
    course = "При длине блока триста метров время установления около трёх часов, а для 10 км — 100 сут."
    assert missing_numbers(course, src) == []


def test_number_from_thin_air():
    src = [load_pages(BAREN)[42]]
    course = "При L = 300 м время установления около 7,5 ч."
    assert missing_numbers(course, src) == pytest.approx([7.5])
