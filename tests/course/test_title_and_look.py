"""Первое впечатление: название главы, шапка шага, главная (hero, таймлайн), сайдбар. Структура, не пиксели."""
import json
import re
from pathlib import Path

from contracts.models import Layer
from pipeline.course.build import build, chapter_title
from tests.course.test_robust import _layer, _put, _report

ROOT = Path(__file__).resolve().parents[2]
RES, PORO = "mini.resistivity_depends_on_fluid", "mini.porosity_basics"


def _units(out: Path, headings: list[tuple[str, str]], ch="mini_test") -> None:
    units = [{"unit_id": f"p{page:03d}.{i:02d}", "kind": kind, "page_pdf": page, "text": text}
             for i, (kind, text, page) in enumerate(headings, 1)]
    (out / ch / "units.json").write_text(json.dumps({"chapter": ch, "source": "x.md", "language": "ru", "domain": "geology",
                                                      "pdf_pages": [30], "units": units}, ensure_ascii=False), encoding="utf-8")


def _title(tmp_path, ext, headings=None):
    layer = _layer()
    layer.ext = ext
    out = _put(tmp_path, layer)
    if headings is not None:
        _units(out, headings)
    return chapter_title(layer, out / "mini_test"), out


def test_title_order_layer_then_first_heading_then_id(tmp_path):
    h = [("paragraph", "Текст до заголовка.", 30), ("heading", "## 1.2 Дельты [Deltas]", 30), ("heading", "### 1.2.1 Флювиальные дельты", 34)]
    assert _title(tmp_path / "a", {"core": {"title": "Название от ядра"}}, h)[0] == "Название от ядра"
    assert _title(tmp_path / "b", {}, h)[0] == "1.2 Дельты"                 # без #, без английского в скобках, как в книге
    assert _title(tmp_path / "c", {}, [("paragraph", "Только текст.", 30)])[0] == "mini_test"
    assert _title(tmp_path / "d", {})[0] == "mini_test"                    # нет units.json


def test_course_never_shows_raw_id_when_a_heading_exists(tmp_path):
    layer = _layer()
    layer.ext = {}
    out = _put(tmp_path, layer)
    _units(out, [("heading", "# 1.2 Дельты", 30)])
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    html = (course / "index.html").read_text(encoding="utf-8")
    assert re.search(r"<h1>\s*1\.2 Дельты\s*</h1>", html) and "mini_test</h1>" not in html
    assert "<title>1.2 Дельты</title>" in html
    w = [x for x in _report(course)["warnings"] if x["code"] == "no_title"]
    assert len(w) == 1 and "1.2 Дельты" in w[0]["message"]                 # слой названия не дал — об этом по-прежнему предупреждаем


def _built(tmp_path):
    from tests.course.test_gen_build import _build
    course = _build(tmp_path, tasks=True)
    return course, (course / "index.html").read_text(encoding="utf-8"), (course / f"step-{RES}.html").read_text(encoding="utf-8")


def test_step_header_is_a_compact_kicker_with_pages_and_prereq_chips(tmp_path):
    _, _, html = _built(tmp_path)
    start = html.index('<header class="step-head">')
    head = html[start:html.index("</header>", start)]
    assert re.search(r'class="kicker">Шаг \d+ из \d+ · ≈ \d+ мин · стр\. \d+', head)
    assert "В книге:" not in head and 'class="step-bar-top"' not in head
    assert 'id="step-bar"' in html and html.index('id="step-bar"') > html.index("</header>", start)     # полоска вне шапки: прилипает к сайту


def test_sections_nav_is_collapsed_on_mobile_and_hidden_on_desktop():
    css = (ROOT / "pipeline/course/assets/course.css").read_text(encoding="utf-8")
    assert re.search(r"@media \(min-width: 1024px\)[^}]*\{[^@]*\.toc\s*\{\s*display:\s*none", css, re.S)
    tpl = (ROOT / "pipeline/course/templates/step.html.j2").read_text(encoding="utf-8")
    assert '<details open id="toc-details">' in tpl and "Разделы" in tpl and "На этой странице" not in tpl      # на мобильном сворачивает JS


def test_sidebar_is_280px_16px_two_line_titles_with_status_circle():
    css = (ROOT / "pipeline/course/assets/course.css").read_text(encoding="utf-8")
    assert "17.5rem" in css and "-webkit-line-clamp: 2" in css and "line-height: 1.3" in css
    assert re.search(r"\.path-list a\s*\{[^}]*font-size:\s*1rem", css)
    assert re.search(r"li\.done > a \.num::after\s*\{[^}]*content:\s*\"✓\"", css)


def test_home_hero_has_meta_line_start_card_with_ring_and_timeline(tmp_path):
    _, html, _ = _built(tmp_path)
    assert re.search(r'class="meta">\d+ шаг(?:а|ов)? · ≈ \d+ мин · \d+ (задание|задания|заданий)', html)
    assert 'id="resume"' in html and 'class="ring"' in html and 'id="ring-fg"' in html
    assert 'class="steps-list timeline"' in html
    row = html[html.index('class="step-row"'):]
    assert row.count('class="st-meta"') >= 1 and 'class="st-sub"' not in html


def test_main_block_is_a_highlighted_card_and_quotes_have_a_source(tmp_path):
    _, _, html = _built(tmp_path)
    css = (ROOT / "pipeline/course/assets/course.css").read_text(encoding="utf-8")
    assert re.search(r"\.block-main\s*\{[^}]*border-left:\s*4px solid var\(--ui-accent\)", css)
    assert "<cite>" in html and "стр." in html[html.index("<cite>"):html.index("<cite>") + 60]
    assert re.search(r"main\.with-side > \.step\s*\{[^}]*max-width:\s*70ch", css)


def test_look_uses_only_interface_colours_not_legend_colours():
    css = (ROOT / "pipeline/course/assets/course.css").read_text(encoding="utf-8")
    assert not re.search(r"--(rock|fluid|curve|measure|lith)", css)
    assert not re.search(r"#[0-9a-fA-F]{6}\b", css.replace("#000", "").replace("background: #fff", ""))


def test_build_normalises_terms_in_stored_step_text_too(tmp_path):
    """Текст, сгенерированный до правила терминов, при сборке (в том числе --no-llm) приводится к нему: в «Суть» одно выделение."""
    from pipeline.course.steptext import node_hash
    from tests.course.test_gen_build import _setup, TEXT
    out = _setup(tmp_path)
    p = out / "mini_test/course/step_text.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    main = next(x for x in data["nodes"][RES]["paragraphs"] if x["block"] == "main")
    main["text"] = "Это [[параметр насыщения]] и ещё [[чужой термин]], а также **жирное** слово. Вторая фраза."
    main["terms"] = ["параметр насыщения", "чужой термин"]
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    html = (course / f"step-{RES}.html").read_text(encoding="utf-8")
    block = html[html.index('id="b-main"'):html.index("</section>", html.index('id="b-main"'))]
    assert block.count("<dfn>") == 1 and "чужой термин" in block and "<strong>" not in block and "**" not in block
