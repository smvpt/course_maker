"""Третий заход: статусы прогресса, карточки, фильтр главной, подписи, надписи без «слов разработчика», конспект без схем-цепочек."""
import json
import re
from pathlib import Path

from pipeline.course.build import book_parts, build
from pipeline.illus import run as R
from tests.course.test_gen_build import _build, _setup
from tests.course.test_illus import CurveLLM, _setup as _illus_setup, _style
from tests.course.test_robust import _layer, _put

ROOT = Path(__file__).resolve().parents[2]
TPL = ROOT / "pipeline/course/templates"
JS = (ROOT / "pipeline/course/assets/course.js").read_text(encoding="utf-8")
CSS = (ROOT / "pipeline/course/assets/course.css").read_text(encoding="utf-8")
RES = "mini.resistivity_depends_on_fluid"


def _page(tmp_path, name, **kw):
    course = _build(tmp_path, tasks=True, **kw)
    return (course / name).read_text(encoding="utf-8")


# 1. прогресс: четыре статуса, полоса пуста при нуле, нет дублирующей строки
def test_progress_has_four_status_tabs_without_the_duplicate_legend(tmp_path):
    html = _page(tmp_path, "progress.html")
    tabs = re.findall(r'<button type="button" data-tab="([a-z]+)"[^>]*>([^<]+?) <span', html)
    assert [t for t, _ in tabs] == ["new", "repeat", "reinforce", "mastered"]
    assert [l for _, l in tabs] == ["Не начато", "Повторить", "Закрепить", "Освоено"]
    assert 'title="Нужно повторить: есть неверные ответы"' in html and "mastery-legend" not in html and "Нужно повторить: 0" not in html
    assert 'id="mastery-pct">0% освоено' in html


def test_step_status_rules_and_default_tab_in_js():
    body = JS[JS.index("function mastery(stepId)"):JS.index("function needsRepeat")]
    order = [body.index(x) for x in ('return "mastered"', 'return "repeat"', 'return "reinforce"', 'return "new"')]
    assert order == sorted(order)
    assert "st.ok === st.total" in body and "st.bad > 0" in body and "st.ok > 0" in body
    assert 'var KEYS = ["new", "repeat", "reinforce", "mastered"]' in JS
    assert 'show(groups.repeat.length ? "repeat" : KEYS.filter(function (k) { return groups[k].length; })[0])' in JS      # при ошибках — «Повторить»
    assert 'if (bar) bar.style.width' in JS                                      # «не начато» — пустое место полосы


# 2. карточки
def test_cards_show_front_then_reveal_then_know_repeat_with_counter_clockwise_icon():
    t = (TPL / "cards.html.j2").read_text(encoding="utf-8")
    assert "Показать суть" in t and 'icon("arrow-counter-clockwise")' in t and 'icon("arrow-left")' not in t
    assert t.index("Показать суть") < t.index('data-mark="know"')
    assert re.search(r"\.card details:not\(\[open\]\) ~ \.card-btns \{ display: none; \}", CSS)           # кнопки только после раскрытия
    assert "отметки хранятся в этом браузере" not in t.lower().replace("отметки хранятся только", "x")


def test_cards_page_texts_for_a_learner(tmp_path):
    html = _page(tmp_path, "cards.html")
    assert "Отметки хранятся в этом браузере." not in html and re.search(r'<p class="fine">Отметки хранятся только в этом браузере\.</p>', html)
    assert html.index('class="fine"') > html.rindex('class="card-btns"')                           # мелкая сноска внизу


# 3. главная
def test_index_filter_is_hidden_until_something_needs_repeating(tmp_path):
    html = _page(tmp_path, "index.html")
    assert re.search(r'<div class="segment"[^>]*\bhidden>', html) and 'data-seg="repeat"' in html
    assert "seg.hidden = !meta.steps.some(function (s) { return needsRepeat(s.id); })" in JS


def test_index_has_no_duplicate_kicker_and_author_book_go_to_course_json(tmp_path):
    layer = _layer()
    out = _put(tmp_path, layer)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "p")
    html = (course / "index.html").read_text(encoding="utf-8")
    assert 'class="kicker"' not in html and "Демо-курс" not in html and 'id="hero-search-input"' not in html      # hero не дублируется кикером и вторым полем поиска
    info = json.loads((course / "course.json").read_text(encoding="utf-8"))
    assert info["author"] is None and info["book"] is None                                                       # данных нет — хаб напишет только название
    (out / "mini_test/units.json").write_text(json.dumps({"chapter": "mini_test", "source": "x.md", "language": "ru", "domain": "geology",
                                                          "pdf_pages": [1], "units": [], "author": "Барабошкин", "book": "Практическая седиментология"},
                                                         ensure_ascii=False), encoding="utf-8")
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "p")
    info = json.loads((course / "course.json").read_text(encoding="utf-8"))
    assert (info["author"], info["book"]) == ("Барабошкин", "Практическая седиментология")
    assert book_parts(layer, None) == (None, None)
    layer.ext = {"core": {"book": "Только книга"}}
    assert book_parts(layer, None) == (None, "Только книга")                                                       # хаб показывает «автор — книга», только если есть оба
    layer.ext = {"core": {"title": None, "author": "Автор", "book": "Книга"}}
    assert book_parts(layer, None) == ("Автор", "Книга")


def test_single_part_has_no_part_heading_but_several_parts_keep_theirs(tmp_path):
    layer = _layer()
    for n in layer.nodes:
        n.ext.get("core", {}).pop("part", None)
    one = (build("mini_test", out_root=_put(tmp_path / "a", layer), pages_dir=tmp_path / "p") / "index.html").read_text(encoding="utf-8")
    assert "<h2>Глава</h2>" not in one
    many = _page(tmp_path / "b", "index.html")
    assert len(re.findall(r'<section class="part" data-part=[^>]*>\s*<h2>', many)) >= 2


# 5, 6, 7, 11. подписи и понятные единицы
def test_by_badges_only_with_the_switch_and_settings_in_the_menu(tmp_path):
    html = _page(tmp_path, f"step-{RES}.html")
    header = html[html.index('<header class="top">'):html.index("</header>")]
    assert "toggle-by" not in header and "toggle-theme" not in header and "counter" not in header      # из шапки убраны ✦, автор/модель, тема
    menu = re.search(r'<dialog id="menu".*?</dialog>', html, re.S).group(0)
    assert [m for m in re.findall(r'data-theme-set="([a-z]+)"', menu)] == ["system", "light", "dark"]
    assert "Показать, что из книги, а что пересказ" in menu and 'role="switch"' in menu and 'id="by-help"' in menu
    assert 'title="Решено заданий: 0 из' in menu and 'id="solved-count"' in menu                    # счётчик решённых — в меню
    assert re.search(r'id="toggle-by"[^>]*data-by-switch', html) and html.count("data-by-switch") == 3     # меню, карточка справа, строка под шапкой
    assert re.search(r"body:not\(\.show-by\) \.by-author, body:not\(\.show-by\) \.by-model \{ display: none; \}", CSS)
    assert "by-hypothesis" not in re.search(r"body:not\(\.show-by\)[^{]*\{", CSS).group(0)              # «гипотеза» видна всегда


def test_step_labels_key_concept_and_progress_in_plain_units(tmp_path):
    html = _page(tmp_path, f"step-{RES}.html")
    assert "пороговое понятие" not in html and "Прочитано" not in html.split('class="step-aside"')[1].split("</aside>")[0]
    assert "Задания: 0 из 3" in html.split('class="step-aside"')[1]
    assert "Прогресс шага: 0 из" in html                                                           # для скринридера остаётся в #step-progress-text
    assert '"Задания: " + okTasks' in JS and "Прочитано" not in JS.split("step-progress-side")[1][:400]
    assert "step-strip" not in html and "step-strip" not in CSS and "step-strip" not in JS


def test_key_concept_is_a_small_star_with_a_hint_not_a_pill(tmp_path):
    layer = _layer()
    for n in layer.nodes:
        n.threshold = True
    out = _put(tmp_path, layer)
    html = (build("mini_test", out_root=out, pages_dir=tmp_path / "p") / f"step-{RES}.html").read_text(encoding="utf-8")
    assert re.search(r'<span class="key-concept" title="Ключевое понятие: без него следующие шаги будут непонятны" tabindex="0">(?:<svg.*?</svg>)<span class="sr">ключевое понятие</span></span>', html, re.S)
    assert "threshold" not in html and "пороговое" not in html and "threshold" not in CSS


# 10. без текстов «от разработчика»
def test_tasks_page_text_is_for_the_learner(tmp_path):
    html = _page(tmp_path, "tasks.html")
    assert "Отвечайте по шагам — после ответа будет разбор и ссылка на страницу книги." in html
    assert "Состояние — «верно», «неверно»" not in html


# 12. конспект без схем-цепочек
def test_summary_skips_chain_schemes_but_keeps_charts_and_columns(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "complete_json", CurveLLM())
    layer = _layer()
    out = _illus_setup(tmp_path, layer)
    res = R.run("mini_test", out, _style())
    kinds = {il.ext["kind"] for il in res.illustrations}
    assert "chain" in kinds and len(kinds) > 1
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "p")
    summary = (course / "summary.html").read_text(encoding="utf-8")
    assert ".chain.svg" not in summary
    for il in res.illustrations:
        if il.ext["kind"] != "chain":
            assert Path(il.file).name in summary or sum(1 for x in res.illustrations if x.node_id == il.node_id and x.ext["kind"] != "chain") > 2
    assert any(".chain.svg" in (course / f"step-{n.id}.html").read_text(encoding="utf-8") for n in layer.nodes)     # на страницах шагов цепочки остаются
