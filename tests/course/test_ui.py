"""Интерфейс курса: цвета, чипы страниц, навигация, задания (разметка), прогресс и ошибки."""
import json
import re
import shutil
from pathlib import Path

import jsonschema
import pytest

from contracts.models import Layer
from pipeline.course.build import build

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"
TASKS = ROOT / "fixtures/course/mini_tasks.json"
TASK_SCHEMA = ROOT / "data/organizers/01_схемы/task.schema.json"
ASSETS = ROOT / "pipeline/course/assets"
RES = "step-mini.resistivity_depends_on_fluid.html"


def _setup(tmp_path: Path, with_tasks: bool = False, tasks_file: Path = TASKS) -> Path:
    layer = Layer.model_validate_json(MINI.read_text(encoding="utf-8"))
    d = tmp_path / "out" / layer.chapter
    (d / "course").mkdir(parents=True)
    shutil.copy(MINI, d / "layer.json")
    if with_tasks:
        shutil.copy(tasks_file, d / "course/tasks.json")
    return tmp_path / "out"


def _course(tmp_path, with_tasks=False) -> Path:
    return build("mini_test", out_root=_setup(tmp_path, with_tasks), pages_dir=tmp_path / "pages")


def _read(course: Path, name: str) -> str:
    return (course / name).read_text(encoding="utf-8")


def course_data(course: Path) -> dict:
    """Общие данные курса: assets/course-data.js («window.COURSE_DATA = {...};»), а не копия в каждой странице."""
    text = (course / "assets/course-data.js").read_text(encoding="utf-8")
    return json.loads(text[len("window.COURSE_DATA = "):].rstrip().rstrip(";"))


# ---------------------------------------------------------------- цвета

def test_ui_css_never_uses_legend_colors():
    css = (ASSETS / "course.css").read_text(encoding="utf-8")
    for prefix in ("--lith-", "--fluid-", "--curve-", "--measurement", "--prov-"):
        assert prefix not in css, f"интерфейс не должен брать цвет легенды {prefix}"


def test_yellow_not_in_theme_part(tmp_path):
    course = _course(tmp_path)
    tokens = _read(course, "assets/tokens.css")
    theme = tokens[tokens.index("/* theme */"):]
    assert "#f1c40f" not in theme.lower()
    assert "#f1c40f" not in _read(course, "assets/course.css").lower()


def test_ui_palette_defined_in_both_themes(tmp_path):
    tokens = _read(_course(tmp_path), "assets/tokens.css")
    light = tokens[tokens.index(":root {\n  --bg: #FBFAF7"):tokens.index("@media (prefers-color-scheme: dark)")]
    dark = tokens[tokens.index(':root[data-theme="dark"]'):]
    for block in (light, dark):
        for var in ("--ui-accent", "--ui-ok", "--ui-warn", "--ui-bad", "--border"):
            assert var in block
    assert "rgba(255, 255, 255, .08)" in dark and "rgba(0, 0, 0, .08)" in light
    assert "--radius: 12px" in tokens
    assert 'font-family' not in tokens and 'system-ui, "Segoe UI", sans-serif' in tokens


def test_buttons_use_ui_accent_and_no_external_fonts():
    css = (ASSETS / "course.css").read_text(encoding="utf-8")
    assert re.search(r"\.btn \{[^}]*background: var\(--ui-accent\)", css)
    assert "@import" not in css and "@font-face" not in css


# ---------------------------------------------------------------- шаг

def test_page_chip_is_inline_at_end_of_paragraph(tmp_path):
    course = _course(tmp_path)
    html = _read(course, "step-mini.porosity_basics.html")
    assert 'class="refs"' not in html
    assert re.search(r'<p data-by="author">Пористость — доля пустот(?:(?!</p>).)*?class="pg" data-page="10">стр\. 10</button></p>',
                     html, re.S)


def test_formula_is_labeled_monospace_without_katex(tmp_path):
    html = _read(_course(tmp_path), RES)
    assert re.search(r'<span class="formula-label">формула</span><code class="tex"', html)
    assert "katex" in html.lower() and not re.search(r'(src|href)="(https?:)?//', html)   # KaTeX есть и только локальный


def test_step_is_split_into_tiers_and_has_no_page_toc(tmp_path):
    """Реструктуризация под ТЗ: вместо оглавления «Разделы» — ярусы с заголовками; оглавление и его JS убраны."""
    course = _course(tmp_path)
    html = _read(course, RES)
    body = html[html.index("<main"):html.index('<dialog id="menu"')]
    assert 'id="toc-details"' not in body and "Разделы" not in body and "На этой странице" not in body
    tiers = re.findall(r'<h2 class="tier-h" id="tier-([a-z]+)-h">(?:<svg.*?</svg>)?([^<]+)</h2>', html, re.S)
    assert [t for t, _ in tiers] == ["understand", "data", "check", "deep"] or [t for t, _ in tiers] == ["understand", "check", "deep"]
    assert {"understand": "Понять", "data": "В данных", "check": "Проверить себя", "deep": "Глубже"}.items() >= dict(tiers).items()
    assert 'getElementById("toc-details")' not in _read(course, "assets/course.js")


def test_long_blocks_are_foldable(tmp_path):
    course = _course(tmp_path)
    poro = _read(course, "step-mini.porosity_basics.html")
    res = _read(course, RES)
    assert re.search(r'id="b-nuances".*?<details class="fold">', poro, re.S)
    assert re.search(r'id="b-tables".*?<details class="fold">.*?<table', res, re.S)
    assert re.search(r'id="b-deeper".*?<details class="fold">', res, re.S)
    assert "Показать" in res and "Скрыть" in res


def test_step_has_progress_checklist_bottom_bar_sidebar_and_drawer(tmp_path):
    html = _read(_course(tmp_path), RES)
    assert 'id="step-bar"' in html and "Прогресс шага: 0 из 1" in html
    assert 'data-check="read"' in html and 'id="done-banner"' in html
    assert 'data-check="video"' not in html and 'data-check="tasks"' not in html
    assert 'class="step-bar"' in html and ">Назад<" in html and ">Далее<" in html
    assert 'class="path-side"' in html and 'id="menu"' in html and 'id="drawer"' not in html   # шторку пути заменило общее меню
    assert html.count('aria-current="step"') == 1   # сайдбар
    # окно «проверь по книге»: закрытие кнопкой, нативный modal даёт Esc и ловушку фокуса
    assert re.search(r'<dialog id="book".*?aria-label="Закрыть"', html, re.S)


@pytest.mark.parametrize("name", ["index.html", "cards.html", "map.html", "summary.html", "glossary.html", RES])
def test_menu_has_three_groups_with_icons_and_labels_on_every_page(tmp_path, name):
    html = _read(_course(tmp_path, with_tasks=True), name)
    header = html[html.index('<header class="top">'):html.index("</header>")]
    assert 'class="main-nav"' not in html and "counter" not in header                # из шапки убраны пункты навигации и счётчик
    menu = re.search(r'<dialog id="menu".*?</dialog>', html, re.S).group(0)
    assert re.findall(r'<h3 class="menu-group">([^<]+)</h3>', menu) == ["Курс", "Повторение", "Настройки"]
    labels = re.findall(r'<a href="[a-z]+\.html"[^>]*>(?:<svg.*?</svg>)<span>([^<]+)</span>', menu, re.S)
    assert [l for l in labels if l != "Лист опечаток"] == ["Путь", "Все задания", "Словарь главы", "Конспект", "Карта связей", "Что ломается в данных", "Прогресс", "Ошибки", "Карточки"]
    for target in ("index", "tasks", "glossary", "summary", "map", "it", "progress", "mistakes", "cards"):
        assert f'href="{target}.html"' in menu
    assert menu.count("<svg") >= 10 and 'aria-current="page"' in menu


# ---------------------------------------------------------------- путь

def test_index_cards_tabs_and_segments(tmp_path):
    html = _read(_course(tmp_path), "index.html")
    assert 'id="resume"' in html and "Начать" in html
    assert 'class="part-tabs"' in html and html.count("data-part=") >= 4   # 2 таба + «Все» + секции
    assert 'data-seg="all"' in html and 'data-seg="repeat"' in html
    assert 'class="st-meta">≈' in html and "Шаг 1 · ≈" not in html           # номер уже в кружке таймлайна: «Шаг N ·» в мете убран
    assert 'class="badge"' not in html          # заданий нет — бейджа «решено» нет
    assert 'id="solved-count"' not in html      # и счётчика ✦ нет


# ---------------------------------------------------------------- задания (разметка)

def test_tasks_fixture_matches_organizers_schema():
    schema = json.loads(TASK_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.validate(json.loads(TASKS.read_text(encoding="utf-8")), schema)


def test_tasks_markup_all_five_types(tmp_path):
    course = _course(tmp_path, with_tasks=True)
    res = _read(course, RES)
    assert 'id="b-quiz"' in res
    assert res.count('class="tnum"') == 3 and 'data-task-chip="mini.t01"' in res
    assert 'type="radio" name="opt-mini.t01"' in res and 'type="checkbox" name="opt-mini.t02"' in res
    assert 'data-type="order"' not in res        # порядок — в шаге про решение
    assert 'class="calc-input"' in res and "безразмерная величина" in res
    assert "Правильный ответ:</strong> Нужны ещё признаки" in res
    assert "Правильный ответ:</strong> Высокое сопротивление; Отрицательная аномалия ПС" in res
    assert "Правильный ответ:</strong> 8 безразмерная величина (±0,1)" in res
    assert 'data-action="reread" data-claim="mini.resistivity_depends_on_fluid#c1"' in res
    assert 'data-action="understood"' in res
    dec = _read(course, "step-mini.reservoir_decision.html")
    assert 'data-type="order"' in dec and 'data-move="up"' in dec and 'data-move="down"' in dec
    assert "Правильный ответ:</strong> Оценить пористость → Сравнить сопротивление с водоносным пластом → Сделать вывод о насыщении" in dec
    poro = _read(course, "step-mini.porosity_basics.html")
    assert poro.count('class="gap"') == 2 and "Правильный ответ:</strong> пор, породы" in poro
    assert 'data-check="tasks"' in res and "Прогресс шага: 0 из 2" in res


def test_tasks_make_counter_badges_and_hub_page(tmp_path):
    course = _course(tmp_path, with_tasks=True)
    idx = _read(course, "index.html")
    assert 'id="solved-count"' in idx and "Решено заданий: 0 из 5" in idx
    assert 'data-badge="mini.resistivity_depends_on_fluid" data-total="3" hidden>решено 0/3' in idx      # бейдж — только после первого ответа
    assert "3 задания" in idx and "1 задание" in idx
    hub = _read(course, "tasks.html")
    assert hub.count("data-task-state=") == 5 and "step-mini.porosity_basics.html#task-mini.t04" in hub
    assert "заданий пока нет" not in hub


def test_stale_tasks_with_unknown_step_or_claim_are_dropped_with_warning(tmp_path, capsys):
    # раньше сборка падала; теперь (живая пересборка после правки слоя) такое задание выбрасывается с предупреждением
    data = json.loads(TASKS.read_text(encoding="utf-8"))
    data["tasks"][0]["step_id"] = "mini.nope"
    data["tasks"][1]["claim_ids"] = ["mini.resistivity_depends_on_fluid#c9"]
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    course = build("mini_test", out_root=_setup(tmp_path / "a", True, bad), pages_dir=tmp_path / "pages")
    rep = json.loads((course / "build_report.json").read_text(encoding="utf-8"))
    stale = {w["task"]: w for w in rep["warnings"] if w["code"] == "task_stale"}
    assert set(stale) == {"mini.t01", "mini.t02"}
    assert "mini.nope" in stale["mini.t01"]["errors"][0] and "c9" in stale["mini.t02"]["errors"][0]
    assert rep["tasks"] == 3 and "WARNING" in capsys.readouterr().err


def test_task_answer_pointing_to_missing_option_is_dropped_with_warning(tmp_path):
    data = json.loads(TASKS.read_text(encoding="utf-8"))
    data["tasks"][0]["answer"] = "zzz"
    bad = tmp_path / "bad_answer.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    course = build("mini_test", out_root=_setup(tmp_path / "c", True, bad), pages_dir=tmp_path / "pages")
    rep = json.loads((course / "build_report.json").read_text(encoding="utf-8"))
    w = [x for x in rep["warnings"] if x["code"] == "task_stale"]
    assert len(w) == 1 and w[0]["task"] == "mini.t01" and "zzz" in w[0]["errors"][0] and rep["tasks"] == 4


def test_rebuild_keeps_tasks_json(tmp_path):
    out = _setup(tmp_path, with_tasks=True)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    assert json.loads((course / "tasks.json").read_text(encoding="utf-8"))["tasks"][0]["id"] == "mini.t01"


# ---------------------------------------------------------------- прогресс и ошибки

def test_progress_and_mistakes_empty_states_without_tasks(tmp_path):
    course = _course(tmp_path)
    prog, mis, tasks = _read(course, "progress.html"), _read(course, "mistakes.html"), _read(course, "tasks.html")
    assert "Заданий в этой главе пока нет" in prog and 'id="mastery-pct"' not in prog
    assert "заданий пока нет" in mis and 'id="mistakes-list"' not in mis
    assert "заданий пока нет" in tasks
    assert "<h1>Мой прогресс</h1>" in prog and "<h1>Мои ошибки</h1>" in mis


def test_progress_and_mistakes_skeleton_with_tasks(tmp_path):
    course = _course(tmp_path, with_tasks=True)
    prog, mis = _read(course, "progress.html"), _read(course, "mistakes.html")
    assert 'id="mastery-pct">0% освоено' in prog
    for tab in ("repeat", "reinforce", "mastered"):
        assert f'data-tab="{tab}"' in prog
    assert "Нужно повторить" in prog and "Закрепить" in prog and "Освоено" in prog
    assert 'id="mistakes-list"' in mis and 'id="restore-understood"' in mis
    meta = course_data(course)["meta"]
    assert [t["id"] for t in meta["tasks"]][:2] == ["mini.t01", "mini.t02"]
    assert "{{" not in json.dumps(meta)          # пропуски gap в метаданных замаскированы


def test_extras_link_to_mistakes_and_it_page(tmp_path):
    course = _course(tmp_path, with_tasks=True)
    assert 'href="mistakes.html"' in _read(course, "index.html")
    it = _read(course, "it.html")
    assert "Что ломается в данных" in it and "Где здесь ИТ-задачи" not in it and "Где ломается в данных" in it
    assert re.search(r'data-by="hypothesis"><dt>Гипотеза</dt>', it)
    assert "Где аналогия перестаёт работать" in it


def test_it_page_empty_state_when_layer_has_no_it_fields(tmp_path):
    layer = Layer.model_validate_json(MINI.read_text(encoding="utf-8"))
    for n in layer.nodes:
        n.data_meaning.from_chapter.text = n.data_meaning.breaks.text = ""
        n.data_meaning.hypotheses = []
        n.it_analogy.text = n.it_analogy.breaks_where = ""
        n.inefficiency_lens = None
    d = tmp_path / "out" / layer.chapter
    d.mkdir(parents=True)
    (d / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    course = build("mini_test", out_root=tmp_path / "out", pages_dir=tmp_path / "pages")
    assert "нет описаний" in _read(course, "it.html")


def test_header_has_logo_search_progress_and_menu_button_and_no_bottom_nav(tmp_path):
    html = _read(_course(tmp_path), "index.html")
    header = html[html.index('<header class="top">'):html.index("</header>")]
    assert header.index("brand-logo") < header.index("crumbs-top") < header.index('id="search-input"') < header.index('id="open-menu"')
    assert "Шаг 1 из" not in header and 'id="step-bar"' not in header and "top-progress" not in header     # «шаг N из M» — в кикере шага
    assert 'aria-label="Поиск"' in header and 'title="Меню"' in header and "Меню</span>" in header
    css = (ASSETS / "course.css").read_text(encoding="utf-8")
    assert "span:has(+ .short)" not in css and ".main-nav" not in css           # нижней навигации из пяти пунктов больше нет
