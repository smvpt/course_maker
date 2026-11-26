"""Реструктуризация под реальных пользователей: поиск, подсказки терминов, словарь, ярусы шага, «Повторение», клавиатура, моушн."""
import json
import re
from pathlib import Path

from tests.course.test_gen_build import _build

ROOT = Path(__file__).resolve().parents[2]
JS = (ROOT / "pipeline/course/assets/course.js").read_text(encoding="utf-8")
CSS = (ROOT / "pipeline/course/assets/course.css").read_text(encoding="utf-8")
RES, PORO = "mini.resistivity_depends_on_fluid", "mini.porosity_basics"


def _course(tmp_path):
    return _build(tmp_path, tasks=True)


def _html(course, name):
    return (course / name).read_text(encoding="utf-8")


def _course_data(course):
    text = (course / "assets/course-data.js").read_text(encoding="utf-8")
    return json.loads(text[len("window.COURSE_DATA = "):].rstrip().rstrip(";"))


def _json(html, ident):
    return json.loads(re.search(rf'id="{ident}">(.*?)</script>', html, re.S).group(1))


# ---------------------------------------------------------------- 2. поиск
def test_search_index_is_one_data_file_per_course_and_covers_titles_terms_and_blocks(tmp_path):
    course = _course(tmp_path)
    for page in course.glob("*.html"):
        html = _html(course, page.name)
        assert 'id="search-index"' not in html and 'src="assets/course-data.js"' in html, page.name     # индекс — один файл на курс, не копия в каждой странице
        assert len(html.encode()) < 80_000, (page.name, len(html.encode()))                              # вес страницы < 80 КБ
    index = _course_data(course)["search"]
    assert isinstance(index, list) and index
    kinds = {e["k"] for e in index}
    assert {"step", "para", "term"} <= kinds
    assert all({"k", "s", "t", "b", "a", "x"} <= set(e) for e in index)
    assert any(e["k"] == "step" and "пористость" in e["x"].lower() for e in index)
    assert any(e["k"] == "term" and e["x"].lower().startswith("параметр насыщения") for e in index)
    anchors = [e for e in index if e["k"] == "para" and e["s"] == RES and e["a"].startswith("p-")]
    assert anchors
    step = _html(course, f"step-{RES}.html")
    for e in anchors:
        assert f'id="{e["a"]}"' in step, e["a"]                                  # переход «к абзацу» есть куда
    assert "[[" not in json.dumps(index, ensure_ascii=False)                      # метки терминов в индекс не попадают


def test_search_is_offline_and_has_keyboard_and_stem_matching():
    assert "fetch(" not in JS and "XMLHttpRequest" not in JS
    for needle in ('DATA.search', "function stem(w)", 'ev.key === "/"', 'ev.key === "ArrowDown"', 'ev.key === "Enter"', ".replace(/ё/g, \"е\")",
                   "document.querySelector(\"dialog[open]\")", "function goTo(href)", "history.pushState"):
        assert needle in JS, needle


def test_header_search_field_hero_search_and_mobile_toggle(tmp_path):
    course = _course(tmp_path)
    for name in ("index.html", f"step-{RES}.html", "glossary.html"):
        html = _html(course, name)
        assert 'id="search-input"' in html and 'placeholder="Найти термин или тему"' in html and 'id="open-search"' in html and 'role="listbox"' in html
    assert 'id="hero-search-input"' not in _html(course, "index.html")                      # на главной курса одно поле поиска — в шапке
    assert re.search(r"@media \(max-width: 767\.98px\)[^@]*\.search \{ display: none; \}", CSS, re.S) and ".top.search-open .search" in CSS


# ---------------------------------------------------------------- 3. термины и словарь
def test_term_tooltips_have_definition_page_and_link_to_the_introducing_step(tmp_path):
    course = _course(tmp_path)
    html = _html(course, f"step-{RES}.html")
    terms = _json(html, "term-data")
    info = terms["параметр насыщения"]
    assert "параметр насыщения" in info["def"].lower() and "[[" not in info["def"] and info["page"] == 11
    assert info["claim"].startswith(RES + "#c") and info["href"].startswith(f"step-{RES}.html#p-")
    assert f'id="{info["href"].split("#")[1]}"' in html                           # якорь, куда ведёт «к шагу, где вводится»
    assert "<dfn>параметр насыщения</dfn>" in html                                # разметка термина прежняя; подсказку вешает JS
    for needle in ('readJSON("term-data")', '"К шагу, где вводится"', "mouseenter", '"focus"', 'addEventListener("click"', 'role", "tooltip"', "dfn.term"):
        assert needle in JS, needle
    assert re.search(r"\.term-tip \{[^}]*transition: opacity 120ms", CSS)          # fade 120 мс


def test_glossary_page_lists_every_introduced_term_alphabetically(tmp_path):
    course = _course(tmp_path)
    html = _html(course, "glossary.html")
    names = re.findall(r'<strong class="gloss-term">([^<]+)</strong>', html)
    assert names == sorted(names, key=lambda t: t.lower().replace("ё", "е")) and set(names) == {"параметр насыщения", "пористость"}
    assert re.search(r'<dd>\s*<p>[^<]*параметр насыщения[^<]+</p>', html, re.I) and re.search(r'href="step-mini\.porosity_basics\.html#', html)
    assert 'id="glossary-q"' in html and 'id="glossary-empty"' in html and "gloss-page" in html
    assert 'href="glossary.html"' in _html(course, "index.html")                  # из меню
    assert "const terms" not in JS and 'getElementById("glossary-q")' in JS


# ---------------------------------------------------------------- 5. ярусы шага
def test_step_tiers_have_no_empty_tier_and_deep_blocks_are_folded(tmp_path):
    course = _course(tmp_path)
    for name in course.glob("step-*.html"):
        html = name.read_text(encoding="utf-8")
        tiers = re.findall(r'<section class="tier[^"]*" id="tier-([a-z]+)".*?\n</section>\n', html, re.S)
        assert tiers and set(tiers) <= {"understand", "data", "check", "deep"}, name.name
        for m in re.finditer(r'<section class="tier[^"]*" id="tier-([a-z]+)"(.*?)\n</section>\n(?=<section class="tier|</div><!--/step-body-->)', html, re.S):
            assert m.group(2).count('class="block') >= 1, (name.name, m.group(1))        # пустых ярусов нет
        order = [html.index(f'id="tier-{t}"') for t in ("understand", "data", "check", "deep") if f'id="tier-{t}"' in html]
        assert order == sorted(order)
    res = _html(course, f"step-{RES}.html")
    assert res.index('id="guess"') < res.index('id="tier-understand"') if 'id="guess"' in res else True      # «сначала угадай» — перед «Понять»
    deep = res[res.index('id="tier-deep"'):]
    for block in ("b-nuances", "b-quotes", "b-tables", "b-terms", "b-source"):
        if f'id="{block}"' in deep:
            assert re.search(rf'id="{block}".*?<details class="fold">', deep, re.S), block                 # свёрнуто
    assert res.index('id="b-quiz"') > res.index('id="tier-check"') and res.index('id="b-main"') < res.index('id="tier-data"') if 'id="tier-data"' in res else True


def test_first_step_has_a_closable_hint_and_others_do_not(tmp_path):
    course = _course(tmp_path)
    steps = sorted(course.glob("step-*.html"))
    first = _html(course, "step-mini.porosity_basics.html")
    hints = [p.name for p in steps if 'id="hint-pages"' in p.read_text(encoding="utf-8")]
    assert len(hints) == 1
    hint = _html(course, hints[0])
    assert re.search(r"Нажмите «стр\. \d+» — откроется страница книги\. Наведите на термин — увидите определение\.", hint)
    assert "data-hint-close" in hint and 'K.hint = "course:hint"' in JS and "store.set(K.hint, true)" in JS
    assert hint.index('id="b-main"') < hint.index('id="hint-pages"') < hint.index('id="b-why"') if 'id="b-why"' in hint else True    # под Сутью


def test_page_buttons_have_icon_and_title(tmp_path):
    html = _html(_course(tmp_path), f"step-{RES}.html")
    buttons = re.findall(r'<button type="button" title="Открыть страницу книги" class="pg" data-(?:page|claim)="[^"]+">стр\. \d+</button>', html)
    assert len(buttons) >= 5
    assert re.search(r"\.pg::before \{[^}]*mask: var\(--i-book-open\)", CSS)


def test_source_is_compact_below_1280_and_card_on_wide_screens_with_synced_switch(tmp_path):
    html = _html(_course(tmp_path), f"step-{RES}.html")
    assert 'class="source-compact"' in html and 'class="step-aside"' in html
    assert html.count("data-by-switch") == 3 and 'id="toggle-by"' in html
    assert re.search(r"@media \(min-width: 1280px\) \{ \.source-compact \{ display: none; \} \}", CSS)
    assert "bySwitches.forEach" in JS and "sw.checked = on" in JS                    # переключатели синхронны


# ---------------------------------------------------------------- 8. «Повторение»
def test_review_pages_share_one_tab_strip_and_progress_rows_have_start_button(tmp_path):
    course = _course(tmp_path)
    for name, current in (("progress.html", "Прогресс"), ("mistakes.html", "Ошибки"), ("cards.html", "Карточки")):
        html = _html(course, name)
        strip = re.search(r'<nav class="review-tabs" aria-label="Повторение">(.*?)</nav>', html, re.S).group(1)
        assert re.findall(r"<span>([^<]+)</span>", strip) == ["Прогресс", "Ошибки", "Карточки"]
        assert re.search(rf'aria-current="page">(?:<svg.*?</svg>)<span>{current}</span>', strip, re.S)
    assert '"Начать шаг"' in JS and 'groups.repeat.length ? "repeat"' in JS
    assert re.search(r"\.mseg \{[^}]*width: 32px[^}]*border-radius: 50%", CSS)       # мини-полоски — круги


# ---------------------------------------------------------------- 9. возврат и клавиатура
def test_resume_restores_scroll_and_arrow_keys_move_between_steps(tmp_path):
    for needle in ('K.scroll', 'history.scrollRestoration = "manual"', "window.scrollTo(0, scrolls[stepData.node_id])", 'addEventListener("pagehide"',
                   'ev.key === "ArrowLeft"', "a[rel=\"prev\"]", "a[rel=\"next\"]", 'tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT"'):
        assert needle in JS, needle
    assert re.search(r'if \(typing \|\| document\.querySelector\("dialog\[open\]"\)\) return;', JS)    # не в полях ввода и не при открытом окне
    html = _html(_course(tmp_path), f"step-{RES}.html")
    assert 'rel="prev"' in html and 'rel="next"' in html


# ---------------------------------------------------------------- 10. моушн
def test_motion_is_subtle_and_fully_disabled_by_reduced_motion():
    assert "--ease: cubic-bezier(.2, .8, .2, 1)" in CSS
    durations = [int(v) for v in re.findall(r"(?<![\d.])(\d{3})ms", CSS)]
    assert durations and all(100 <= d <= 250 for d in durations), sorted(set(durations))      # 120/150/200/250 мс
    secs = set(re.findall(r"(?<![\w.-])(\d?\.?\d+)s\b", CSS))
    assert secs <= {"1.5"}, secs                                                              # только угасание подсветки абзаца — 1,5 с
    assert "cubic-bezier" in CSS and "spring" not in CSS and not re.search(r"cubic-bezier\([^)]*-\d", CSS)   # без пружин и отскоков
    for kf in ("page-in", "fade-rise", "menu-in", "sheet-in", "tick-draw", "hl-fade"):
        assert f"@keyframes {kf}" in CSS, kf
    assert "dialog#book[open] { animation: fade-rise" in CSS and "dialog.menu[open] { animation: menu-in" in CSS
    assert re.search(r"@media \(max-width: 767\.98px\) \{ dialog#book\[open\] \{ animation: sheet-in", CSS)
    assert "details::details-content" in CSS and ".card:hover, .step-row:hover { transform: translateY(-1px); }" in CSS
    assert ".opt.correct .opt-mark .ic { animation: tick-draw" in CSS and ".term-tip" in CSS and ".theme-anim" in CSS
    rm = CSS[CSS.rindex("@media (prefers-reduced-motion: reduce)"):]
    assert "animation: none !important" in rm and "transition: none !important" in rm and "scroll-behavior: auto !important" in rm
    assert re.search(r"\*, \*::before, \*::after \{", rm)                                     # выключено для ВСЕГО
    assert 'behavior: reduceMotion ? "auto" : "smooth"' in JS and "window.matchMedia(\"(prefers-reduced-motion: reduce)\")" in JS


def test_menu_theme_switch_has_three_modes_and_system_removes_the_attribute():
    for needle in ('delete root.dataset.theme', 'data-theme-set', "root.classList.add(\"theme-anim\")", 'store.get(K.theme, "system")'):
        assert needle in JS or needle in (ROOT / "pipeline/course/templates/base.html.j2").read_text(encoding="utf-8"), needle
