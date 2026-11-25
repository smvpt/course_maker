"""ingest: md → единицы главы. Без сети и без PDF (vision и сканы — отдельно)."""
import re

import pytest

from pipeline.common import config, paths
from pipeline.ingest import parse

SYNTH = """<!-- page 10 -->
ХВОСТ ПРОШЛОЙ ГЛАВЫ

10

Последний абзац прошлой главы.

# Глава 2. Давление

Первый абзац главы, он обрывается на пере-

$^1$ Сноска к странице.

<!-- page 11 -->
ХВОСТ ПРОШЛОЙ ГЛАВЫ

11

носе страницы и продолжается здесь.

$$p = p_0 + \\rho g h \\quad (2.1)$$

Рис. 3. Схема пласта

----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━

Ось X: давление, от 0 до 10.

KEYWORDS: давление
----

Таблица 2.1. Свойства

| Порода | Пористость |
| --- | --- |
| песчаник | 20 % |

<!-- page 12 -->
ХВОСТ ПРОШЛОЙ ГЛАВЫ

12

Пример 1. Найти давление на глубине 100 м.

Задачи

1. Найти давление на забое.
2. Объяснить знак поправки.

\\[
q = -\\frac{k}{\\mu} \\nabla p
\\]

а

Уровень моря

# Глава 3. Следующая

Это уже не наша глава.
"""


def build(md=SYNTH, **kw):
    kw.setdefault("start_heading", r"^#\s*Глава 2")
    kw.setdefault("end_heading", r"^#\s*Глава 3")
    return parse.build_units(md, chapter="synth", source="synth.md", **kw)


def kinds(cu):
    return [(u.unit_id, u.kind) for u in cu.units]


def test_synthetic_chapter_units():
    cu = build()
    texts = [u.text for u in cu.units]
    assert texts[0].startswith("# Глава 2")                         # обрезка по start_heading
    assert not any("не наша глава" in t or "прошлой главы" in t for t in texts)  # end_heading и колонтитулы
    assert not any(t.strip() in {"10", "11", "12"} for t in texts)
    assert cu.ext["core"]["page_printed"] == {"10": 10, "11": 11, "12": 12}

    glued = [u for u in cu.units if u.text.startswith("Первый абзац")][0]
    assert "переносе страницы и продолжается здесь" in glued.text  # склейка через страницу и сноску
    assert glued.page_pdf == 10 and glued.ext["core"]["pages"] == [10, 11]
    foot = [u for u in cu.units if u.text.startswith("$^1$")][0]
    assert foot.kind == "paragraph" and foot.ext["core"]["footnote"] is True

    by = {u.text.splitlines()[0][:12]: u for u in cu.units}
    assert by["$$p = p_0 + "].kind == "formula"
    fig = by["Рис. 3. Схем"]
    assert fig.kind == "figure" and fig.figure_ref == "Рис. 3"
    assert "FORMAT 6" in fig.ext["core"]["figure_description"]       # описание конвертера — к подписи
    assert fig.ext["core"]["figure_description_by_model"] is True
    assert by["Таблица 2.1."].kind == "table"
    assert by["| Порода | П"].kind == "table"
    assert by["Пример 1. На"].kind == "worked_example"
    assert by["Задачи"].kind == "heading"
    tasks = [u for u in cu.units if u.kind == "task"]
    assert [t.text[:2] for t in tasks] == ["1.", "2."]                # каждая задача — своя единица
    disp = [u for u in cu.units if u.text.startswith("\\[")][0]
    assert disp.kind == "formula" and disp.text.endswith("\\]")         # \[ … \] целиком
    frag = by["а"]
    assert frag.kind == "figure" and frag.ext["core"]["fragment"] is True

    ids = [u.unit_id for u in cu.units]
    assert len(ids) == len(set(ids)) and all(re.fullmatch(r"p\d{3}\.\d{2}", i) for i in ids)
    assert cu.pdf_pages == [10, 11, 12] and cu.language == "ru"
    assert cu.ext["core"]["outside_chapter"]["before"] and cu.ext["core"]["outside_chapter"]["after"]


def test_unclosed_figure_description_does_not_swallow_page():
    md = ("<!-- page 5 -->\nТекст до рисунка.\n\n----\n━━━ FORMAT 7: NOMOGRAM ━━━\n\nОси: …\n\n"
          "KEYWORDS: палетка\n\n#### Задачи\n\n96. Привести примеры.\n97. Определить толщину.\n")
    cu = parse.build_units(md, chapter="x", source="x.md")
    assert [u.kind for u in cu.units] == ["paragraph", "figure", "heading", "task", "task"]
    assert "KEYWORDS" in cu.units[1].text and "Задачи" not in cu.units[1].text


def test_boundaries_must_exist():
    with pytest.raises(ValueError, match="start_heading"):
        build(start_heading=r"^# Нет такого")
    with pytest.raises(ValueError, match="end_heading"):
        build(end_heading=r"^# Нет такого")


def test_page_filter():
    cu = build(pages={11}, start_heading=None, end_heading=None)
    assert {u.page_pdf for u in cu.units} == {11}


def test_language_en():
    md = "<!-- page 1 -->\n# Drilling basics\n\nThe drill bit rotates and crushes the rock.\n\nFig. 2. Bit\n"
    cu = parse.build_units(md, chapter="en", source="en.md")
    assert cu.language == "en"
    assert [u.kind for u in cu.units] == ["heading", "paragraph", "figure"]


def test_errata_applied_and_marked(tmp_path):
    e = tmp_path / "errata.md"
    e.write_text("| стр. | было | стало |\n|---|---|---|\n| 11 | 20 % | 25 % |\n| 12 | нет такого | x |\n",
                 encoding="utf-8")
    cu = build(errata=parse.load_errata(e))
    row = [u for u in cu.units if u.text.startswith("| Порода")][0]
    assert "25 %" in row.text and "20 %" not in row.text
    assert row.ext["core"]["errata"] == [{"page": 11, "wrong": "20 %", "right": "25 %"}]
    assert "исправлено" in row.ext["core"]["table_note"]
    assert cu.ext["core"]["errata_unapplied"] == [{"page": 12, "wrong": "нет такого", "right": "x"}]


# ---------------------------------------------------------------- реальные главы

def real(ch):
    spec = config.chapter(ch)
    return parse.build_units(spec.md.read_text(encoding="utf-8"), chapter=ch, source=str(spec.md),
                             pages=spec.page_set(), start_heading=spec.start_heading,
                             end_heading=spec.end_heading)


def test_latyshova_boundaries():
    cu = real("latyshova_gl5_par17-20")
    assert cu.units[0].text.startswith("# Глава V")
    assert not any("85. Выделить коллекторы" in u.text for u in cu.units)   # задача гл. IV
    assert not any("§ 21" in u.text for u in cu.units if u.kind == "heading")
    assert sum(u.kind == "task" for u in cu.units) >= 6


def test_basniev_glue_over_running_header():
    cu = real("basniev_gl23-24")
    assert not any("Пирвердяна" in u.text for u in cu.units)
    assert not any(u.text == "НЕУСТАНОВИВШЕЕСЯ ДВИЖЕНИЕ УПРУГОЙ ЖИДКОСТИ" for u in cu.units)
    glued = [u for u in cu.units if "упруговодонапорным" in u.text]
    assert glued and glued[0].page_pdf == 474


def test_single_chapter_md_from_control_package():
    md = paths.ORGANIZERS / "02_модуль_проверки" / "контрольный_пакет" / "vendelshtein_gl1.md"
    cu = parse.build_units(md.read_text(encoding="utf-8"), chapter="vendelshtein_gl1", source=str(md))
    assert cu.units and cu.language == "ru"
    assert len(cu.pdf_pages) >= 10


@pytest.mark.parametrize("ch", list(config.chapters()))
def test_all_configured_chapters_parse(ch):
    cu = real(ch)
    assert len(cu.units) > 30
    assert all(u.text.strip() for u in cu.units)
