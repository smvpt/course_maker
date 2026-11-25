import json
from pathlib import Path

import pytest

from pipeline.verify.pages import load_pages, normalize, parse_pages
from pipeline.verify.quotes import check_quote, check_quote_md

ROOT = Path(__file__).resolve().parents[2]
BAREN = ROOT / "data/books/ctrl_barenblatt.md"
LATYSH = ROOT / "data/books/train_latyshova.md"
ORG_LAYER = ROOT / "fixtures/core/example_layer_organizers.json"


def test_parse_pages_by_markers():
    pages = parse_pages("шапка\n<!-- page 3 -->\nтретья\n<!-- page 4 -->\nчетвертая\n")
    assert pages == {3: "\nтретья\n", 4: "\nчетвертая\n"}


def test_parse_pages_no_markers_fails():
    with pytest.raises(ValueError):
        parse_pages("текст без меток")


def test_normalize_ocr_noise():
    # латинские o, c, p внутри кириллических слов, ё, перенос через дефис, кавычки, LaTeX
    raw = "Плaстовое «давлeние» растёт в кол-\nлекторе $\\varkappa$ при 10⁴"
    assert normalize(raw) == normalize("пластовое давление растет в коллекторе при 10^{4}")


def test_organizers_example_layer_quote_found():
    layer = json.loads(ORG_LAYER.read_text(encoding="utf-8"))
    claim = layer["nodes"][0]["claims"][0]
    r = check_quote_md(LATYSH, claim["page_pdf"], claim["quote"])
    assert r.status == "found" and r.page == 95


def test_quote_with_ocr_typos_found():
    # в книге: «Наиболее интересны случаи, для которых в начальный момент времени движение в пласте стационарно»
    q = "Наибoлее интересны «случаи», для котoрых в началь-\nный момент времени движение в плаcте стационарно"
    r = check_quote_md(BAREN, 40, q)
    assert r.status == "found" and r.page == 40


def test_quote_matches_despite_book_ocr_error():
    # в md OCR-ошибка «автомобильно» вместо «автомодельно»
    q = "Решение (II.93) автомодельно: независимые переменные x и t входят в него лишь в комбинации"
    r = check_quote_md(BAREN, 41, q)
    assert r.status == "found"


def test_invented_quote_not_found():
    q = ("При увеличении проницаемости пласта в десять раз характерное время выхода "
         "на стационарный режим возрастает ровно в сто раз")
    r = check_quote_md(BAREN, 41, q)
    assert r.status == "not_found" and r.page is None


def test_quote_from_neighbour_page():
    q = "Ряд (II.92) сходится при всех t и x. Рассмотрим вначале асимптотику при условии"
    r = check_quote_md(BAREN, 40, q)
    assert r.status == "other_page" and r.page == 41


def test_quote_from_far_page():
    q = "Ряд (II.92) сходится при всех t и x. Рассмотрим вначале асимптотику при условии"
    r = check_quote_md(BAREN, 47, q)
    assert r.status == "other_page" and r.page == 41


def test_quote_crossing_page_break_found_on_start_page():
    q = ("в коллекторах с высокой проницаемостью имеет порядок 10⁴ см²/с. Тогда из (II.97) следует, "
         "что характерное время переходных процессов")
    r = check_quote_md(BAREN, 41, q)
    assert r.status == "found" and r.page == 41


def test_check_quote_by_chapter_id_uses_units_json(tmp_path, monkeypatch):
    out = tmp_path / "out" / "baren_test"
    out.mkdir(parents=True)
    (out / "units.json").write_text(json.dumps({"chapter": "baren_test", "source": str(BAREN)}),
                                    encoding="utf-8")
    monkeypatch.setenv("OUT_DIR", str(tmp_path / "out"))
    r = check_quote("baren_test", 41, "Ряд (II.92) сходится при всех t и x")
    assert r.status == "found"


def test_check_quote_unknown_chapter_fails_loudly(tmp_path, monkeypatch):
    monkeypatch.setenv("OUT_DIR", str(tmp_path / "out"))
    with pytest.raises(FileNotFoundError):
        check_quote("no_such_chapter", 1, "любая цитата длиннее")


def test_load_pages_has_chapter_range():
    pages = load_pages(BAREN)
    assert all(p in pages for p in range(38, 52))


def test_quote_across_page_with_footnote_and_page_number(tmp_path):
    from pipeline.verify.quotes import check_quote_md
    md = tmp_path / "ch.md"
    md.write_text("<!-- page 38 -->\n## § 4. Линейная теория$^1$\n\nПростейший случай фильтрации — движение одно-\n\n"
                  "$^1$ См. также [47, 6, 12, 44].\n\n38\n<!-- page 39 -->\n"
                  "родной слабосжимаемой жидкости в упруго деформируемом пласте. Дальше текст.\n", encoding="utf-8")
    r = check_quote_md(md, 38, "Простейший случай фильтрации — движение однородной слабосжимаемой жидкости "
                               "в упруго деформируемом пласте.")
    assert r.status == "found" and r.page == 38
    # начало на следующей странице — не «found» на 38
    assert check_quote_md(md, 38, "слабосжимаемой жидкости в упруго деформируемом пласте. Дальше текст").page == 39
