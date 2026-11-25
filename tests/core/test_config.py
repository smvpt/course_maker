"""Конфиг глав, запуск без конфига, требования к зависимостям."""
import re

import pytest

from pipeline.common import config, paths


def test_all_configured_chapters_resolve():
    chs = config.chapters()
    assert {"latyshova_gl5_par17-20", "basniev_gl23-24", "kuznetsov_gl10",
            "vendelshtein_gl1", "barenblatt_par4", "baraboshkin_par1-2"} <= set(chs)
    for ch in chs:
        spec = config.chapter(ch)        # пути существуют, id валиден, регулярки компилируются
        assert spec.md.exists()
        for rx in (spec.start_heading, spec.end_heading):
            if rx:
                re.compile(rx)


def test_vendelshtein_two_ranges():
    s = config.chapter("vendelshtein_gl1").page_set()
    assert 9 in s and 14 in s and 20 in s and 30 in s and 15 not in s and 19 not in s


def test_headings_match_book_text():
    """Регулярки границ глав находят ровно один заголовок в своих страницах."""
    for ch in config.chapters():
        spec = config.chapter(ch)
        lines = spec.md.read_text(encoding="utf-8").splitlines()
        for rx in (spec.start_heading, spec.end_heading):
            if rx:
                hits = [l for l in lines if re.search(rx, l)]
                assert len(hits) >= 1, (ch, rx)


@pytest.mark.parametrize("name,expected", [
    ("vendelshtein_gl1", "vendelshtein_gl1"),
    ("Drilling Chapter 3", "drilling_chapter_3"),
    ("Глава 5. Бурение", "glava_5._burenie"),
])
def test_slug_id(name, expected):
    assert config.slug_id(name) == expected
    assert config.ID_RE.match(config.slug_id(name))


def test_parse_pages():
    assert config.parse_pages("90-108") == [(90, 108)]
    assert config.parse_pages("9-14,20-30") == [(9, 14), (20, 30)]
    assert config.parse_pages("38") == [(38, 38)]
    with pytest.raises(ValueError):
        config.parse_pages("a-b")


def test_from_args_and_saved_spec(tmp_path, monkeypatch):
    monkeypatch.setenv("OUT_DIR", str(tmp_path))
    md = paths.ORGANIZERS / "02_модуль_проверки" / "контрольный_пакет" / "vendelshtein_gl1.md"
    spec = config.resolve(md=str(md))
    assert spec.id == "vendelshtein_gl1" and spec.pages is None and spec.domain == "geology"
    spec = config.resolve(md=str(md), ch="t.x", pages="1-3")
    config.save_spec(spec)
    assert config.chapter("t.x") == spec            # дальше этапы находят главу по --ch
    with pytest.raises(KeyError):
        config.chapter("nope")
    with pytest.raises(ValueError):
        config.resolve(md=str(tmp_path / "missing.md"))
    with pytest.raises(ValueError):
        config.resolve()


def test_requirements_include_every_module_file_pinned():
    root = paths.ROOT
    listed = set(re.findall(r"^-r\s+(\S+)", (root / "requirements.txt").read_text(encoding="utf-8"), re.M))
    files = {f"requirements/{p.name}" for p in (root / "requirements").glob("*.txt")}
    assert files == listed, f"requirements.txt должен включать ровно {sorted(files)}"
    for f in files:
        for line in (root / f).read_text(encoding="utf-8").splitlines():
            line = line.split("#")[0].strip()
            if line:
                assert "==" in line, f"{f}: версия не закреплена: {line}"
