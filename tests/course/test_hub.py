"""Главная всех курсов (hub): out/index.html по собранным курсам; шапка с хлебными крошками «Курсы / название»."""
import json
import re
import shutil
from pathlib import Path

import pytest

from pipeline.course import hub
from pipeline.course.build import build

ROOT = Path(__file__).resolve().parents[2]
BB = ROOT / "fixtures/core/live_baraboshkin_par1-2"


def _courses(tmp_path):
    """Два курса, собранные из фикстур: Барабошкин (слой П1) и мини-глава."""
    out = tmp_path / "out"
    d = out / "baraboshkin_par1-2"
    d.mkdir(parents=True)
    for f in ("layer.json", "units.json"):
        shutil.copy2(BB / f, d / f)
    m = out / "mini_test"
    m.mkdir()
    shutil.copy2(ROOT / "fixtures/course/mini_layer.json", m / "layer.json")
    (m / "units.json").write_text(json.dumps({"domain": "geology"}), encoding="utf-8")
    for ch in ("baraboshkin_par1-2", "mini_test"):
        build(ch, out_root=out, pages_dir=tmp_path / "pages", hub=True)
    return out


def test_hub_lists_both_courses_with_valid_relative_links_and_no_network(tmp_path):
    out = _courses(tmp_path)
    home = hub.build_hub(out)
    html = home.read_text(encoding="utf-8")
    assert home == out / "index.html" and (out / "assets/hub.js").exists() and (out / "assets/tokens.css").exists() and (out / "assets/brand/logo.svg").exists()
    cards = re.findall(r'<li class="course-card" data-ch="([^"]+)">', html)
    assert cards == ["baraboshkin_par1-2", "mini_test"]
    for ch in cards:
        assert (out / ch / "course/index.html").exists() and f'href="{ch}/course/index.html"' in html
    for href in re.findall(r'(?:href|src)="([^"#]+)"', html):
        assert not href.startswith(("http", "//", "/")), href                              # только относительные ссылки
        assert (out / href).exists(), href                                                 # и все они ведут на существующие файлы
    assert not re.search(r'(?:href|src)="https?:', html)
    js = (out / "assets/hub.js").read_text(encoding="utf-8")
    assert "fetch(" not in js and "XMLHttpRequest" not in js and "fetch(" not in html
    assert re.search(r"<p class=\"course-meta\">\d+ (шаг|шага|шагов) · ≈ \d+ мин", html)
    assert "Курсы по главам книг для тех, кто работает с данными. Каждое утверждение — со страницей книги." in html
    assert "#C9A66B" in html and 'class="brand-logo"' in html                              # цветной логотип крупно — только здесь
    assert re.search(r'<section id="hub-review"[^>]*\bhidden>', html)                      # «Повторить сегодня» скрыт, пока нечего повторять


def test_hub_data_and_search_are_embedded_json_for_all_courses(tmp_path):
    out = _courses(tmp_path)
    html = hub.build_hub(out).read_text(encoding="utf-8")
    data = json.loads(re.search(r'id="hub-data">(.*?)</script>', html, re.S).group(1))
    assert [c["ch"] for c in data] == ["baraboshkin_par1-2", "mini_test"]
    for c in data:
        assert {"title", "author", "book", "minutes", "tasks", "steps", "task_ids"} <= set(c) and c["steps"] and all("id" in s for s in c["steps"])
    search = json.loads(re.search(r'id="hub-search">(.*?)</script>', html, re.S).group(1))
    assert {e["c"] for e in search} == {"baraboshkin_par1-2", "mini_test"} and all(e["ct"] for e in search)
    assert any(e["c"] == "mini_test" and "сопротивлен" in e["x"].lower() for e in search)


def test_hub_state_logic_is_in_js_with_graceful_fallback_without_localstorage():
    js = (ROOT / "pipeline/course/assets/hub.js").read_text(encoding="utf-8")
    for needle in ('get("course:last"', '"course:" + c.ch + ":done"', '"course:" + c.ch + ":tasks"', '"course:" + c.ch + ":understood"', "Не начат", "В процессе", "Пройден",
                   "Продолжить:", "/course/mistakes.html", "/course/step-", "review.hidden = anyBad === 0"):
        assert needle in js, needle
    assert "Начните с:" in (ROOT / "pipeline/course/templates/hub.html.j2").read_text(encoding="utf-8")        # ничего не начато — подсказка из разметки
    assert re.search(r"function get\(k, dflt\) \{\s*try \{[^}]*\} catch \(e\) \{ return dflt; \}", js)      # localStorage недоступен → значения по умолчанию


def test_course_header_has_breadcrumbs_only_when_the_hub_exists(tmp_path):
    out = _courses(tmp_path)
    with_hub = (out / "mini_test/course/step-mini.porosity_basics.html").read_text(encoding="utf-8")
    head = with_hub[with_hub.index('<header class="top">'):with_hub.index("</header>")]
    assert re.search(r'<a href="\.\./\.\./index\.html">Курсы</a>', head) and 'class="crumb-sep"' in head
    assert head.index("brand-logo") < head.index(">Курсы<") < head.index('class="brand-title"') < head.index('id="search-input"') < head.index('id="open-menu"')
    no_hub = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")                     # библиотека по умолчанию: хаба нет
    page = (no_hub / "index.html").read_text(encoding="utf-8")
    header = page[page.index('<header class="top">'):page.index("</header>")]
    assert "Курсы" not in header and 'class="brand-title"' in header and "../../index.html" not in header


def test_hub_requires_built_courses_and_warns_about_old_builds(tmp_path, capsys):
    with pytest.raises(FileNotFoundError, match="нет собранных курсов"):
        (tmp_path / "out").mkdir()
        hub.build_hub(tmp_path / "out")
    out = _courses(tmp_path / "x")
    (out / "mini_test/course/course.json").unlink()
    hub.build_hub(out)
    assert "course.json" in capsys.readouterr().err
    assert 'data-ch="mini_test"' not in (out / "index.html").read_text(encoding="utf-8")


def test_course_cli_builds_the_hub_after_the_course():
    import inspect
    from pipeline.course import build as B
    src = inspect.getsource(B.main)
    assert "hub=True" in src and "hub.build_hub(a.out)" in src
    assert "hub:" in (ROOT / "mk/course.mk").read_text(encoding="utf-8") or "pipeline.course.build" in (ROOT / "mk/course.mk").read_text(encoding="utf-8")


# ---------------------------------------------------------------- тема без мигания, логичные пустые места
def test_theme_is_applied_before_first_paint_in_course_and_hub(tmp_path):
    out = _courses(tmp_path)
    pages = [out / "index.html", out / "mini_test/course/index.html", out / "mini_test/course/step-mini.porosity_basics.html"]
    hub.build_hub(out)
    for page in pages:
        html = page.read_text(encoding="utf-8")
        head = html[html.index("<head>"):html.index("</head>")]
        script = head.index("<script>")
        assert script < head.index("<title>") and script < head.index('rel="stylesheet"'), page.name          # скрипт темы — до стилей
        assert 'JSON.parse(localStorage.getItem("course:theme"))' in head, page.name                           # значение хранится как JSON ("dark" с кавычками)
        assert "try {" in head and "catch (e)" in head, page.name
    js = (ROOT / "pipeline/course/assets/course.js").read_text(encoding="utf-8")
    assert "requestAnimationFrame(function () { requestAnimationFrame(function () { root.classList.add(\"theme-ready\"); }); })" in js
    css = (ROOT / "pipeline/course/assets/course.css").read_text(encoding="utf-8")
    assert re.search(r"html\.theme-ready body[^{]*\{[^}]*transition: background-color", css)                  # плавность цвета — только после первого кадра


def test_glossary_has_only_terms_with_a_definition_and_cards_filter_waits_for_a_mark(tmp_path):
    from tests.course.test_gen_build import _build
    course = _build(tmp_path, tasks=True)
    html = (course / "glossary.html").read_text(encoding="utf-8")
    assert "Определение — в тексте шага" not in html and html.count('class="gloss"') == html.count("<dd>")
    cards = (course / "cards.html").read_text(encoding="utf-8")
    assert re.search(r'<p class="filter" hidden>', cards) and 'id="only-repeat"' in cards
    js = (ROOT / "pipeline/course/assets/course.js").read_text(encoding="utf-8")
    assert "showFilter" in js and 'cardMarks[k] === "repeat"' in js
    assert 'if (mastery(s.id) === "new")' in js                                                                 # у «Не начато» нет кружков «не решено»
