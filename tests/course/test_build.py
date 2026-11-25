import json
import re
import shutil
from pathlib import Path

import pytest
from PIL import Image

from contracts.models import Layer
from pipeline.course.build import build

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"
ORG = ROOT / "fixtures/core/example_layer_organizers.json"
STYLE = ROOT / "data/organizers/03_стайлгайд/styleguide.json"


def _setup(tmp_path: Path, src: Path) -> tuple[str, Path]:
    layer = Layer.model_validate_json(src.read_text(encoding="utf-8"))
    ch_dir = tmp_path / "out" / layer.chapter
    ch_dir.mkdir(parents=True)
    shutil.copy(src, ch_dir / "layer.json")
    return layer.chapter, tmp_path / "out"


def _build(tmp_path, src=MINI, **kw):
    ch, out = _setup(tmp_path, src)
    kw.setdefault("pages_dir", tmp_path / "pages")
    course = build(ch, out_root=out, **kw)
    return ch, course


def _step_data(html: str) -> dict:
    m = re.search(r'<script type="application/json" id="step-data">(.*?)</script>', html, re.S)
    assert m, "нет встроенных данных шага"
    return json.loads(m.group(1))


def _all_html(course: Path) -> dict[str, str]:
    return {p.name: p.read_text(encoding="utf-8") for p in course.glob("*.html")}


@pytest.mark.parametrize("src", [ORG, MINI])
def test_builds_offline_site(tmp_path, src):
    ch, course = _build(tmp_path, src)
    layer = Layer.model_validate_json(src.read_text(encoding="utf-8"))
    pages = _all_html(course)
    assert "index.html" in pages and "cards.html" in pages and "summary.html" in pages and "map.html" in pages
    for n in layer.nodes:
        assert f"step-{n.id}.html" in pages
    for name, html in pages.items():
        # без CDN и сети: ни одного внешнего src/href, никаких fetch
        assert not re.search(r'(src|href)\s*=\s*"(https?:)?//', html), name
        assert "fetch(" not in html, name
        # все локальные ссылки ведут на существующие файлы
        for ref in re.findall(r'(?:src|href)="([^"#:]+)(?:#[^"]*)?"', html):
            assert (course / ref).exists(), f"{name}: битая ссылка {ref}"
    assert "fetch(" not in (course / "assets/course.js").read_text(encoding="utf-8")


def test_index_follows_graph_order(tmp_path):
    _, course = _build(tmp_path)
    html = (course / "index.html").read_text(encoding="utf-8")
    hrefs = re.findall(r'href="step-([^"]+)\.html"', html)
    order = list(dict.fromkeys(hrefs))
    assert order == ["mini.porosity_basics", "mini.history_note",
                     "mini.resistivity_depends_on_fluid", "mini.reservoir_decision"]
    assert "Часть 1. Основы" in html and "Часть 2. Насыщение" in html
    assert re.search(r"≈\s*\d+\s*мин", html)


def test_prev_next_follow_order(tmp_path):
    _, course = _build(tmp_path)
    html = (course / "step-mini.history_note.html").read_text(encoding="utf-8")
    assert 'rel="prev" href="step-mini.porosity_basics.html"' in html
    assert 'rel="next" href="step-mini.resistivity_depends_on_fluid.html"' in html


def test_every_claim_has_page_and_quote(tmp_path):
    _, course = _build(tmp_path)
    layer = Layer.model_validate_json(MINI.read_text(encoding="utf-8"))
    for n in layer.nodes:
        html = (course / f"step-{n.id}.html").read_text(encoding="utf-8")
        data = _step_data(html)
        for c in n.claims:
            assert data["claims"][c.id]["quote"] == c.quote
            assert data["claims"][c.id]["page"] == c.page_pdf
            assert f'data-claim="{c.id}"' in html
            assert f"стр. {c.page_pdf}" in html


def test_every_paragraph_has_page_ref(tmp_path):
    _, course = _build(tmp_path)
    html = (course / "step-mini.resistivity_depends_on_fluid.html").read_text(encoding="utf-8")
    paras = re.findall(r'<div class="para"[^>]*>(.*?)</div><!--/para-->', html, re.S)
    assert len(paras) >= 8
    for p in paras:
        assert "стр. " in p, p[:120]


def test_empty_blocks_hidden(tmp_path):
    _, course = _build(tmp_path)
    poro = (course / "step-mini.porosity_basics.html").read_text(encoding="utf-8")
    hist = (course / "step-mini.history_note.html").read_text(encoding="utf-8")
    assert 'id="b-nuances"' in poro
    assert 'id="b-nuances"' not in hist
    assert 'id="b-misconception"' not in hist
    assert 'id="b-examples"' not in hist
    assert 'id="b-formulas"' not in hist
    assert 'id="b-tables"' not in hist
    # пустые строки в полях не превращаются в пустые абзацы
    assert not re.search(r'<p[^>]*>\s*</p>', hist)


def test_author_model_hypothesis_marks(tmp_path):
    _, course = _build(tmp_path)
    poro = (course / "step-mini.porosity_basics.html").read_text(encoding="utf-8")
    res = (course / "step-mini.resistivity_depends_on_fluid.html").read_text(encoding="utf-8")
    assert re.search(r'data-by="author"[^>]*>[^<]*Пористость — доля пустот', poro)
    assert re.search(r'data-by="model"[^>]*>[^<]*Нефть почти не проводит', res)
    assert re.search(r'data-by="hypothesis"[^>]*>[^<]*Признак «сопротивление', res)
    assert 'class="quote" data-by="author"' in res
    assert 'id="toggle-by"' in res


def test_formulas_tables_and_errata(tmp_path):
    _, course = _build(tmp_path)
    res = (course / "step-mini.resistivity_depends_on_fluid.html").read_text(encoding="utf-8")
    assert 'id="b-formulas"' in res
    assert 'class="tex" data-tex="P_н = \\rho_{нп} / \\rho_{вп}"' in res
    assert 'id="b-tables"' in res and "<table" in res
    assert re.search(r'<mark class="ocr-fix"[^>]*title="[^"]*3\.S[^"]*">3,5</mark>', res)
    errata = (course / "errata.html").read_text(encoding="utf-8")
    assert "3.S" in errata and "3,5" in errata and "step-mini.resistivity_depends_on_fluid.html" in errata
    assert 'href="errata.html"' in (course / "index.html").read_text(encoding="utf-8")


def test_no_errata_page_without_fixes(tmp_path):
    _, course = _build(tmp_path, ORG)
    assert not (course / "errata.html").exists()
    assert "errata.html" not in (course / "index.html").read_text(encoding="utf-8")


def test_legend_colors_same_in_both_themes(tmp_path):
    _, course = _build(tmp_path)
    css = (course / "assets/tokens.css").read_text(encoding="utf-8")
    style = json.loads(STYLE.read_text(encoding="utf-8"))
    for key, v in style["lithology"].items():
        decl = f"--lith-{key}: {v['color']};"
        assert css.count(decl) == 1, decl
    for key, v in style["curves"].items():
        assert css.count(f"--curve-{key.lower()}: {v['color']};") == 1
    # легенда объявлена до тематических блоков и в них не переопределяется
    themed = css[css.index("/* theme */"):]
    assert "--lith-" not in themed and "--curve-" not in themed and "--fluid-" not in themed


def test_verify_status(tmp_path):
    ch, out = _setup(tmp_path, MINI)
    (out / ch / "verify").mkdir()
    (out / ch / "verify/report.json").write_text(json.dumps({
        "package_id": ch, "remarks": [{
            "target": "mini.porosity_basics#c1", "category": "lost_condition", "severity": "significant",
            "problem": "потеряно условие", "fix": "добавить условие", "page_pdf": 10, "quote": None}]}),
        encoding="utf-8")
    course = build(ch, out_root=out, pages_dir=tmp_path / "pages")
    poro = _step_data((course / "step-mini.porosity_basics.html").read_text(encoding="utf-8"))
    assert poro["claims"]["mini.porosity_basics#c1"]["verify"] == {
        "status": "remark", "severity": "significant", "problem": "потеряно условие"}
    hist = _step_data((course / "step-mini.history_note.html").read_text(encoding="utf-8"))
    assert hist["claims"]["mini.history_note#c1"]["verify"] == {"status": "ok"}


def test_verify_status_without_report(tmp_path):
    _, course = _build(tmp_path)
    d = _step_data((course / "step-mini.porosity_basics.html").read_text(encoding="utf-8"))
    assert d["claims"]["mini.porosity_basics#c1"]["verify"] == {"status": "not_checked"}


def test_page_scans_compressed_and_missing_marked(tmp_path):
    pages = tmp_path / "pages" / "mini_test"
    pages.mkdir(parents=True)
    # шумная картинка размером со скан страницы — плохо жмётся
    import random
    img = Image.new("RGB", (1240, 1754), "white")
    px = img.load()
    rnd = random.Random(0)
    for y in range(0, 1754, 3):
        for x in range(0, 1240, 3):
            v = rnd.randint(0, 255)
            px[x, y] = (v, v, v)
    img.save(pages / "p10.png")
    _, course = _build(tmp_path)
    d = _step_data((course / "step-mini.porosity_basics.html").read_text(encoding="utf-8"))
    scan = d["pages"]["10"]["scan"]
    assert scan == "assets/pages/p10.jpg"
    assert (course / scan).stat().st_size <= 150_000
    d2 = _step_data((course / "step-mini.resistivity_depends_on_fluid.html").read_text(encoding="utf-8"))
    assert d2["pages"]["11"]["scan"] is None


def test_missing_layer_fails_loudly(tmp_path):
    with pytest.raises(FileNotFoundError, match="layer.json"):
        build("nope", out_root=tmp_path / "out", pages_dir=tmp_path / "pages")


def test_unknown_node_fails_loudly(tmp_path):
    ch, out = _setup(tmp_path, MINI)
    with pytest.raises(ValueError, match="mini.nope"):
        build(ch, out_root=out, node="mini.nope", pages_dir=tmp_path / "pages")


def test_rebuild_single_node(tmp_path):
    ch, out = _setup(tmp_path, MINI)
    course = build(ch, out_root=out, pages_dir=tmp_path / "pages")
    other = course / "step-mini.history_note.html"
    other.write_text("STALE", encoding="utf-8")
    build(ch, out_root=out, node="mini.porosity_basics", pages_dir=tmp_path / "pages")
    assert other.read_text(encoding="utf-8") == "STALE"
    assert "Пористость" in (course / "step-mini.porosity_basics.html").read_text(encoding="utf-8")


def test_map_has_edges(tmp_path):
    _, course = _build(tmp_path)
    html = (course / "map.html").read_text(encoding="utf-8")
    assert "<svg" in html
    assert html.count('class="edge"') == 2
    assert 'href="step-mini.reservoir_decision.html"' in html


def test_text_size_and_print_rules(tmp_path):
    _, course = _build(tmp_path)
    css = (course / "assets/course.css").read_text(encoding="utf-8")
    assert "@media print" in css
    assert "prefers-reduced-motion" in css
    assert "prefers-color-scheme: dark" in (course / "assets/tokens.css").read_text(encoding="utf-8")
    assert not re.search(r"font-size:\s*(1[0-5]|[0-9])px", css)
