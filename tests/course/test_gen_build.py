"""Интеграция задач 2 и 3 в сборку курса: текст шагов, точные страницы, KaTeX, задания, генерация на моках."""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import jsonschema
import pytest

from contracts.models import Layer
from pipeline.course import generate, steptext, tasks as T
from pipeline.course.build import build
from pipeline.course.steptext import StepTextOut, node_hash
from test_steptext import _paras
from test_tasks_gen import FakeLLM, MISC

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"
TEXT = ROOT / "fixtures/course/mini_step_text.json"
TASKS = ROOT / "fixtures/course/mini_tasks.json"
SCHEMA = ROOT / "data/organizers/01_схемы/task.schema.json"
RES = "step-mini.resistivity_depends_on_fluid.html"
UTF8 = {**os.environ, "PYTHONUTF8": "1"}      # как в Makefile П1: вывод по-русски в pipe на Windows


def _layer() -> Layer:
    return Layer.model_validate_json(MINI.read_text(encoding="utf-8"))


def _setup(tmp_path: Path, text=True, tasks=False, mutate=None) -> Path:
    layer = _layer()
    if mutate:
        mutate(layer)
    d = tmp_path / "out" / layer.chapter
    (d / "course").mkdir(parents=True)
    (d / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    if text:
        data = json.loads(TEXT.read_text(encoding="utf-8"))
        original = _layer()
        for n in original.nodes:
            data["nodes"][n.id]["hash"] = node_hash(n)          # хэш — от исходного узла, как при генерации
        (d / "course/step_text.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    if tasks:
        (d / "course/tasks.json").write_text(TASKS.read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path / "out"


def _build(tmp_path, **kw):
    return build("mini_test", out_root=_setup(tmp_path, **kw), pages_dir=tmp_path / "pages")


def _html(course: Path, name: str) -> str:
    return (course / name).read_text(encoding="utf-8")


# ---------------------------------------------------------------- задача 2: текст шагов

def test_paragraph_pages_come_from_its_claims_not_from_all_node_pages(tmp_path):
    html = _html(_build(tmp_path), RES)
    # утверждение c3 лежит на стр. 12, а узел целиком — на стр. 11: чип должен быть именно «стр. 12»
    assert re.search(r'Граничные значения параметра насыщения(?:(?!</p>).)*?data-page="12">стр\. 12</button></p>', html, re.S)
    assert not re.search(r'Граничные значения параметра насыщения(?:(?!</p>).)*?data-page="11"', html, re.S)
    assert re.search(r'Автор приводит оценку(?:(?!</p>).)*?data-page="11">стр\. 11</button></p>', html, re.S)
    assert 'data-claims="mini.resistivity_depends_on_fluid#c3"' in html


def test_generated_text_replaces_layer_fields_and_marks_model_hypothesis_and_limit(tmp_path):
    html = _html(_build(tmp_path), RES)
    assert re.search(r'data-by="model">Нефть почти не проводит ток, а солёная вода проводит хорошо\.', html)
    assert re.search(r'data-by="hypothesis">Возможно, отношение к сопротивлению водоносного соседа', html)
    assert re.search(r'<div class="para limit"[^>]*><p data-by="model">Аналогия перестаёт работать', html)
    assert 'class="by by-hypothesis">гипотеза</span>' in html
    assert 'data-by="author">Нефть почти не проводит' not in html


def test_term_is_highlighted_at_first_mention(tmp_path):
    html = _html(_build(tmp_path), RES)
    assert "<dfn>параметр насыщения</dfn> — отношение сопротивлений" in html
    assert "[[" not in html and "]]" not in html


def test_quotes_moved_to_their_own_foldable_block(tmp_path):
    html = _html(_build(tmp_path), RES)
    assert re.search(r'id="b-quotes".*?<details class="fold">.*?class="quote" data-by="author"', html, re.S)
    how = html[html.index('id="b-how"'):html.index('id="b-quotes"')]
    assert 'class="quote"' not in how
    legacy = _html(_build(tmp_path / "legacy", text=False), RES)
    assert 'id="b-quotes"' not in legacy and 'class="quote"' in legacy


def test_every_generated_paragraph_has_exact_page_chip(tmp_path):
    course = _build(tmp_path)
    for p in course.glob("step-*.html"):
        html = p.read_text(encoding="utf-8")
        for para in re.findall(r'<div class="para(?: limit)?" data-claims="[^"]+">(.*?)</div><!--/para-->', html, re.S):
            assert re.search(r'data-page="\d+">стр\. \d+</button>', para), (p.name, para[:90])


def test_decision_has_no_node_wide_page_chips_when_text_is_generated(tmp_path):
    html = _html(_build(tmp_path), RES)
    src = re.search(r'<p class="src-line">(.*?)</p>', html, re.S).group(1)
    assert "стр." not in src


def test_stale_step_text_warns_and_falls_back_to_layer_fields(tmp_path, capsys):
    def edit(layer):
        next(n for n in layer.nodes if n.id == "mini.porosity_basics").layers.main.text = "Пористость — доля пустот, а не масса."
    course = _build(tmp_path, mutate=edit)
    assert "WARNING" in capsys.readouterr().err
    rep = json.loads(_html(course, "build_report.json"))
    w = [x for x in rep["warnings"] if x["code"] == "stale_step_text"]
    assert w and w[0]["nodes"] == ["mini.porosity_basics"]
    poro = _html(course, "step-mini.porosity_basics.html")
    assert "data-claims=" not in poro and "Пористость — доля пустот, а не масса." in poro   # из полей слоя
    assert "data-claims=" in _html(course, RES)                                              # остальные шаги — из step_text.json
    assert rep["step_text_nodes"] == 3


def test_step_text_with_unknown_claim_fails_loudly(tmp_path):
    out = _setup(tmp_path)
    p = out / "mini_test/course/step_text.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["nodes"]["mini.porosity_basics"]["paragraphs"][0]["claim_ids"] = ["mini.porosity_basics#c9"]
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError, match="c9"):
        build("mini_test", out_root=out, pages_dir=tmp_path / "pages")


def test_layer_json_is_not_modified_by_build(tmp_path):
    out = _setup(tmp_path)
    before = (out / "mini_test/layer.json").read_bytes()
    build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    assert (out / "mini_test/layer.json").read_bytes() == before


# ---------------------------------------------------------------- KaTeX

def test_katex_is_local_and_only_on_pages_with_formulas(tmp_path):
    course = _build(tmp_path)
    res, poro = _html(course, RES), _html(course, "step-mini.porosity_basics.html")
    assert 'href="assets/katex/katex.min.css"' in res and 'src="assets/katex/katex.min.js"' in res
    assert "katex" not in poro
    assert 'data-katex' in res and "<noscript><style>" in res
    assert not re.search(r'(src|href)="(https?:)?//', res)
    css = (course / "assets/katex/katex.min.css").read_text(encoding="utf-8")
    fonts = re.findall(r"url\(([^)]+)\)", css)
    assert fonts and all(f.endswith(".woff2") and (course / "assets/katex" / f).exists() for f in fonts)
    assert (course / "assets/katex/LICENSE").exists()
    assert (course / "assets/katex/katex.min.js").stat().st_size > 100_000


def test_course_js_renders_formulas_with_katex_without_swallowing_failures():
    js = (ROOT / "pipeline/course/assets/course.js").read_text(encoding="utf-8")
    assert "window.katex.render" in js and "throwOnError: false" in js
    assert 'console.error("KaTeX не загружен' in js


# ---------------------------------------------------------------- задача 3: разметка и данные для логики

def test_tasks_data_embedded_for_the_script(tmp_path):
    html = _html(_build(tmp_path, tasks=True), RES)
    data = json.loads(re.search(r'id="tasks-data">(.*?)</script>', html, re.S).group(1))
    assert data["mini.t01"] == {"type": "single", "answer": "b", "tolerance": None}
    assert data["mini.t02"]["answer"] == ["a", "b"]
    assert data["mini.t05"] == {"type": "calc", "answer": 8, "tolerance": 0.1}
    assert 'id="tasks-data"' not in _html(_build(tmp_path / "x"), RES)


def test_tasks_markup_has_everything_the_logic_needs(tmp_path):
    course = _build(tmp_path, tasks=True)
    res, dec = _html(course, RES), _html(course, "step-mini.reservoir_decision.html")
    assert res.count('data-action="check"') == 3 and res.count('class="task-msg"') == 3
    assert res.count('data-action="again"') == 3 and res.count('class="feedback" hidden tabindex="-1"') == 3
    assert 'class="drag-handle"' in dec and dec.count('data-move=') == 6
    js = (ROOT / "pipeline/course/assets/course.js").read_text(encoding="utf-8")
    for needle in ("setPointerCapture", "pointermove", "data-move", 'data-action="again"', "highlightClaim"):
        assert needle in js


def test_reread_prefers_the_paragraph_that_cites_the_claim():
    js = (ROOT / "pipeline/course/assets/course.js").read_text(encoding="utf-8")
    assert '.para[data-claims~="' in js and "document.getElementById(claimAnchor(claimId))" in js


# ---------------------------------------------------------------- генерация на моках, без сети

def _fake_text_llm(monkeypatch):
    def fake(**kw):
        node_id = json.loads(kw["vars"]["node"])["id"]
        return StepTextOut(paragraphs=_paras(node_id))
    monkeypatch.setattr(steptext, "complete_json", fake)


def test_build_with_generate_writes_step_text_and_valid_tasks(tmp_path, monkeypatch, capsys):
    out = _setup(tmp_path, text=False)
    _fake_text_llm(monkeypatch)
    monkeypatch.setattr(T, "complete_json", FakeLLM(_layer()))
    monkeypatch.setattr(generate, "load_misconceptions", lambda domain: MISC)
    (out / "mini_test/units.json").write_text(json.dumps({"domain": "geology"}), encoding="utf-8")
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True)
    assert (course / "step_text.json").exists() and (course / "tasks.json").exists()
    jsonschema.validate(json.loads((course / "tasks.json").read_text(encoding="utf-8")), json.loads(SCHEMA.read_text(encoding="utf-8")))
    html = _html(course, RES)
    assert 'data-claims="' in html and 'id="b-quiz"' in html and 'id="tasks-data"' in html
    assert json.loads(_html(course, "build_report.json"))["tasks"] >= 15
    assert (out / "mini_test/layer.json").exists()


def test_generate_single_node_regenerates_only_that_node(tmp_path, monkeypatch):
    out = _setup(tmp_path, text=False)
    _fake_text_llm(monkeypatch)
    llm = FakeLLM(_layer())
    monkeypatch.setattr(T, "complete_json", llm)
    monkeypatch.setattr(generate, "load_misconceptions", lambda domain: MISC)
    build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True, domain="geology")
    calls_before = len(llm.calls)
    layer_path = out / "mini_test/layer.json"
    layer = Layer.model_validate_json(layer_path.read_text(encoding="utf-8"))
    next(n for n in layer.nodes if n.id == "mini.porosity_basics").layers.main.text = "Пористость — доля пустот в породе."
    layer_path.write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    texts = []
    monkeypatch.setattr(steptext, "complete_json", lambda **kw: (texts.append(json.loads(kw["vars"]["node"])["id"]),
                                                                  StepTextOut(paragraphs=_paras(json.loads(kw["vars"]["node"])["id"])))[1])
    build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True, domain="geology", node="mini.porosity_basics")
    assert texts == ["mini.porosity_basics"] and len(llm.calls) == calls_before + 1


def test_resolve_domain(tmp_path):
    assert generate.resolve_domain(tmp_path, "drilling") == "drilling"
    with pytest.raises(ValueError, match="units.json"):
        generate.resolve_domain(tmp_path, None)
    (tmp_path / "units.json").write_text(json.dumps({"domain": "geology"}), encoding="utf-8")
    assert generate.resolve_domain(tmp_path, None) == "geology"
    (tmp_path / "units.json").write_text(json.dumps({}), encoding="utf-8")
    with pytest.raises(ValueError, match="domain"):
        generate.resolve_domain(tmp_path, None)


def test_cli_no_llm_builds_from_existing_files(tmp_path):
    out = _setup(tmp_path, tasks=True)
    r = subprocess.run([sys.executable, "-m", "pipeline.course.build", "--ch", "mini_test", "--out", str(out), "--no-llm",
                        "--pages", str(tmp_path / "pages")], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=UTF8)
    assert r.returncode == 0, r.stderr
    assert (out / "mini_test/course/index.html").exists() and "курс:" in r.stdout


def test_cli_fails_loudly_without_layer(tmp_path):
    r = subprocess.run([sys.executable, "-m", "pipeline.course.build", "--ch", "nope", "--out", str(tmp_path), "--no-llm"],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=UTF8)
    assert r.returncode != 0 and "layer.json" in r.stderr


def test_script_stores_and_restores_the_students_choice():
    js = (ROOT / "pipeline/course/assets/course.js").read_text(encoding="utf-8")
    assert '"answers"' in js and "store.set(K.answers, answers)" in js
    assert "function applyAnswer" in js and "id in answers ? answers[id] : null" in js
    assert "answers     {id задания: ответ ученика}" in js          # контракт описан в начале файла
