"""Задача 4: иллюстрации, нарисованные кодом. Без сети: модель, выбирающая формулу для графика, — мок."""
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import jsonschema
import pytest

from contracts.models import Claim, Illustrations, Layer
from pipeline.course.build import build
from pipeline.course.steptext import GenerationFailed, LlmAuthError, LlmError, LlmState
from pipeline.illus import gen, run as R

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"
STYLE_FILE = ROOT / "data/organizers/03_стайлгайд/styleguide.json"
SCHEMA = ROOT / "data/organizers/01_схемы/illustration.schema.json"
RES = "mini.resistivity_depends_on_fluid"
UTF8 = {**os.environ, "PYTHONUTF8": "1"}


def _style() -> gen.Style:
    return gen.Style(json.loads(STYLE_FILE.read_text(encoding="utf-8")))


def _layer() -> Layer:
    return Layer.model_validate_json(MINI.read_text(encoding="utf-8"))


def _node(layer, nid=RES):
    return next(n for n in layer.nodes if n.id == nid)


def _spec(**kw) -> R.CurveSpec:
    base = dict(claim_id=f"{RES}#c2", title="Как параметр насыщения зависит от сопротивления пласта", x_name="rho_oil",
                x_label="Сопротивление нефтенасыщенного пласта", x_unit="Ом·м", y_label="Параметр насыщения", y_unit="",
                x_min=5, x_max=80, constants={"rho_water": 5}, expression="rho_oil / rho_water", curve_key="RES",
                note="Чем выше сопротивление пласта, тем больше параметр насыщения.")
    base.update(kw)
    return R.CurveSpec(**base)


def _xml(svg: str) -> ET.Element:
    return ET.fromstring(svg)


def _all_text(svg: str) -> str:
    return " ".join("".join(t.itertext()) for t in _xml(svg).iter("{http://www.w3.org/2000/svg}text"))


def _colors(svg: str) -> set[str]:
    return {m.upper() for m in re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})"', svg)}


# ---------------------------------------------------------------- схема утверждений

def test_chain_separates_observation_from_inference_and_uses_claim_text():
    node = _node(_layer())
    fig = gen.chain(node, _style(), "Что меняет сопротивление пласта")
    svg = _all_text(fig.svg)
    assert "Наблюдение" in svg and "Вывод" in svg and "Допущение" not in svg
    assert "Нефтенасыщенный пласт имеет сопротивление в несколько раз выше водонасыщенного." in svg.replace("  ", " ")
    assert (fig.frame_class, fig.origin, fig.label) == ("B", "code_from_model", "схема")
    assert fig.claim_ids == [f"{RES}#c1", f"{RES}#c3", f"{RES}#c2"] or set(fig.claim_ids) == {f"{RES}#c1", f"{RES}#c2", f"{RES}#c3"}
    assert fig.svg.count("<title") == 1 and "<desc" in fig.svg and "схема" in svg


def test_chain_shows_assumptions_dashed():
    layer = _layer()
    node = _node(layer)
    node.claims[2].kind = "assumption"
    svg = gen.chain(node, _style(), "Т").svg
    assert "Допущение" in _all_text(svg) and "stroke-dasharray" in svg


def test_wrap_keeps_lines_within_limit_and_marks_cut():
    lines = gen.wrap("слово " * 40, 20, max_lines=3)
    assert len(lines) == 3 and all(len(l) <= 21 for l in lines) and lines[-1].endswith("…")
    assert gen.wrap("короткая строка", 40) == ["короткая строка"]


# ---------------------------------------------------------------- общие правила: цвета, шрифт, метка

def _every_figure():
    style = _style()
    layer = _layer()
    node = _node(layer)
    rows = [["Порода", "A", "B"], ["x1", "1,5", "10"], ["x2", "2,5", "30"], ["x3", "3,0", "20"]]
    claim = node.claims[2]
    xs = [5 + i for i in range(76)]
    node2 = _node(layer, "mini.porosity_basics")
    node2.claims[0].text = "Песчаник пористее плотной глины, а известняк занимает промежуточное место."
    long = "Очень длинное название шага, которое обязательно переносится на несколько строк"
    return [gen.chain(node, style, long),
            gen.Figure("curve", gen.curve(long, "Ось x, которая называется длинно и подробно", "Ом·м", "Ось y с длинной подписью", "", xs,
                                          [x / 5 for x in xs], "none", style.curve("RES"), "н", style),
                       "B", "code_from_model", "симуляция", "", "", None, []),
            gen.crossplot(claim, rows, long, style),
            gen.crossplot(claim, [r[:2] for r in rows], long, style),
            gen.column(node2, style, long)]


def test_every_figure_uses_only_styleguide_colors():
    style = _style()
    for fig in _every_figure():
        assert fig is not None
        assert _colors(fig.svg) <= style.colors(), (fig.kind, _colors(fig.svg) - style.colors())
        assert not re.search(r"rgb\(|rgba\(|#[0-9a-fA-F]{3}\b", fig.svg)


def test_every_figure_carries_the_provenance_label_on_the_image():
    style = _style()
    for fig in _every_figure():
        root = _xml(fig.svg)
        assert fig.label in _all_text(fig.svg) or fig.kind == "curve"
        assert style.prov(fig.label) in fig.svg.upper() or style.prov(fig.label) in fig.svg


def test_text_is_at_least_16px_on_a_390px_phone():
    for fig in _every_figure():
        root = _xml(fig.svg)
        vb = [float(v) for v in root.get("viewBox").split()]
        assert vb[2] == gen.W
        sizes = {float(s) for s in re.findall(r'font-size="([\d.]+)"', fig.svg)}
        assert sizes and min(sizes) * 358 / vb[2] >= 16, (fig.kind, sizes)


def test_figures_are_valid_xml_with_accessible_name():
    for fig in _every_figure():
        root = _xml(fig.svg)
        assert root.get("role") == "img" and root.get("aria-labelledby") == "t d"
        assert fig.svg.startswith('<svg xmlns="http://www.w3.org/2000/svg"')


def test_no_domain_words_in_generator_code():
    code = " ".join(p.read_text(encoding="utf-8") for p in (ROOT / "pipeline/illus").glob("*.py")).lower()
    for word in ("песчан", "нефт", "газ ", "керн", "каротаж", "пласт", "скважин", "известняк", "глин"):
        assert word not in code, word


# ---------------------------------------------------------------- график по формуле

def test_curve_values_are_computed_by_code_not_taken_from_the_model():
    node = _node(_layer())
    errors, xs, ys = R.validate_curve(node, _spec(), _style())
    assert errors == [] and len(xs) == R.POINTS
    assert ys == pytest.approx([x / 5 for x in xs])
    assert "values" not in R.CurveSpec.model_fields and "points" not in R.CurveSpec.model_fields


def _polyline(svg: str) -> list[tuple[float, float]]:
    pts = re.search(r'<polyline points="([^"]+)"', svg).group(1).split()
    return [tuple(map(float, p.split(","))) for p in pts]


def _curve_svg(depth, xs, ys):
    return gen.curve("Т", "Икс", "", "Игрек", "", xs, ys, depth, None, "н", _style())


def test_curve_orientation_and_depth_goes_down():
    xs, ys = [1.0, 2.0, 3.0, 4.0], [10.0, 20.0, 30.0, 40.0]
    p = _polyline(_curve_svg("none", xs, ys))
    assert p[0][0] < p[-1][0] and p[0][1] > p[-1][1]            # обычный график: рост — вверх и вправо
    p = _polyline(_curve_svg("y", xs, ys))                        # результат — глубина: растёт вниз
    assert p[0][0] < p[-1][0] and p[0][1] < p[-1][1]
    p = _polyline(_curve_svg("x", xs, ys))                        # аргумент — глубина: по вертикали, растёт вниз
    assert p[0][1] < p[-1][1] and p[0][0] < p[-1][0]
    assert "глубина растёт вниз" in _all_text(_curve_svg("y", xs, ys))


@pytest.mark.parametrize("mutate, needle", [
    (dict(constants={"rho_water": 41}), "rho_water=41"),
    (dict(claim_id="mini.porosity_basics#c1"), "не утверждение-формула"),
    (dict(x_name="плотность"), "латинице"),
    (dict(x_min=80, x_max=5), "x_min < x_max"),
    (dict(expression="rho_water / (rho_oil - rho_oil)"), "не вычисляется"),
    (dict(expression="rho_water * rho_oil ** rho_oil ** rho_oil"), "не вычисляется"),
    (dict(expression="rho_oil / rho_water * 37"), "нет в узле"),
    (dict(expression="rho_water * rho_oil / rho_oil"), "горизонтальная линия"),
    (dict(curve_key="ЧУЖАЯ"), "styleguide.curves"),
    (dict(title="How resistivity changes with saturation parameter"), "на русском"),
    (dict(note="Раз. И два."), "одна фраза"),
])
def test_curve_spec_is_checked_by_code(mutate, needle):
    errors, _, _ = R.validate_curve(_node(_layer()), _spec(**mutate), _style())
    assert errors and needle in " ".join(errors), errors


def test_generate_curve_feeds_errors_back_and_gives_up_loudly(monkeypatch):
    calls = []

    def bad(**kw):
        calls.append(kw)
        return _spec(constants={"rho_water": 41})
    monkeypatch.setattr(R, "complete_json", bad)
    with pytest.raises(GenerationFailed, match="rho_water=41"):
        R.generate_curve(_node(_layer()), _style(), "ru")
    assert len(calls) == 3 and "rho_water=41" in calls[1]["vars"]["feedback"]
    assert set(calls[0]["vars"]) == {"node", "formulas", "curves", "language", "feedback"}


def test_prompt_variables_match_what_code_passes():
    text = (ROOT / "prompts/course/illus_curve.md").read_text(encoding="utf-8")
    assert set(re.findall(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}", text)) == {"node", "formulas", "curves", "language", "feedback"}


# ---------------------------------------------------------------- график по таблице

def test_crossplot_two_numeric_columns_is_a_scatter_from_book_data():
    claim = _node(_layer()).claims[2]
    rows = [["Порода", "Пористость, %", "Проницаемость"], ["a", "10,5", "100"], ["b", "20", "300"], ["c", "−5", "50"]]
    fig = gen.crossplot(claim, rows, "Т", _style())
    assert fig.svg.count("<circle") == 3 and (fig.frame_class, fig.origin, fig.label) == ("A", "code_from_data", "реальные данные")
    assert fig.source == f"таблица книги, стр. {claim.page_pdf}" and fig.claim_ids == [claim.id]
    assert "Пористость, %" in _all_text(fig.svg) and "Проницаемость" in _all_text(fig.svg)


def test_crossplot_single_numeric_column_is_bars():
    claim = _node(_layer()).claims[2]
    fig = gen.crossplot(claim, [["Порода", "Граница"], ["a", "3,5"], ["b", "2,8"], ["c", "1,9"]], "Т", _style())
    assert fig.svg.count("<circle") == 0 and "3,5" in _all_text(fig.svg) and "1,9" in _all_text(fig.svg)


def test_crossplot_rejects_non_numeric_or_tiny_tables():
    claim = _node(_layer()).claims[2]
    assert gen.crossplot(claim, [["a", "b"], ["x", "много"], ["y", "мало"], ["z", "средне"]], "Т", _style()) is None
    assert gen.crossplot(claim, [["a", "b"], ["x", "1"], ["y", "2"]], "Т", _style()) is None


def test_to_float_handles_russian_notation():
    assert gen.to_float("3,5") == 3.5 and gen.to_float("−12") == -12 and gen.to_float("> 40") == 40 and gen.to_float("15 %") == 15
    assert gen.to_float("нет") is None and gen.to_float("") is None


# ---------------------------------------------------------------- колонка слоёв

def _layers_node(text):
    layer = _layer()
    node = _node(layer, "mini.porosity_basics")
    node.claims[0].text = text
    return node


def test_column_lists_only_mentioned_layers_in_order_and_says_not_to_scale():
    style = _style()
    fig = gen.column(_layers_node("В разрезе глины перекрывают песчаники, а ниже лежит известняк."), style, "Колонка")
    names = re.findall(r"(глина|песчаник|известняк)", _all_text(fig.svg).replace("глубина", ""))
    assert names[:3] == ["глина", "песчаник", "известняк"]
    assert "не в масштабе" in _all_text(fig.svg) and "условные" in fig.caption
    colors = {v["color"].upper() for k, v in style.raw["lithology"].items() if k in ("shale", "sand", "limestone")}
    assert colors <= _colors(fig.svg)
    assert (fig.frame_class, fig.label) == ("B", "схема")


def test_column_needs_two_layers():
    assert gen.column(_layers_node("Здесь упомянут только песчаник."), _style(), "К") is None
    assert gen.column(_layers_node("Здесь нет ни одной породы."), _style(), "К") is None


# ---------------------------------------------------------------- глава целиком

class CurveLLM:
    def __init__(self, reply=None, error=None):
        self.reply, self.error, self.calls = reply or _spec(), error, 0

    def __call__(self, **kw):
        self.calls += 1
        if self.error:
            raise self.error
        return self.reply


def _setup(tmp_path, layer=None) -> Path:
    layer = layer or _layer()
    d = tmp_path / "out" / layer.chapter
    d.mkdir(parents=True)
    (d / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    return tmp_path / "out"


def test_run_writes_valid_illustrations_for_every_step_and_part(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(R, "complete_json", CurveLLM())
    out = _setup(tmp_path)
    res = R.run("mini_test", out, _style())
    data = json.loads((out / "mini_test/illus/illustrations.json").read_text(encoding="utf-8"))
    jsonschema.validate(data, json.loads(SCHEMA.read_text(encoding="utf-8")))
    layer = _layer()
    by_step = {}
    for il in res.illustrations:
        by_step.setdefault(il.step_id, []).append(il)
        assert (out / "mini_test" / il.file).exists() and il.file == f"illus/{il.node_id}.{il.ext['kind']}.svg"
        assert il.frame_class in ("A", "B") and il.label in ("схема", "симуляция", "реальные данные") and il.alt and il.caption
        assert il.claim_ids and all(c in {cl.id for n in layer.nodes if n.id == il.step_id for cl in n.claims} for c in il.claim_ids)
        assert il.origin != "ai_generated" and il.prompt is None
    assert set(by_step) == {n.id for n in layer.nodes}                       # не меньше одной на шаг
    parts = {}
    for n in layer.nodes:
        parts.setdefault(n.ext["core"]["part"], []).extend(by_step[n.id])
    assert all(any(i.frame_class in ("A", "B") for i in ils) for ils in parts.values())   # A/B на каждую часть
    assert len({i.id for i in res.illustrations}) == len(res.illustrations)
    assert {i.ext["kind"] for i in by_step[RES]} == {"chain", "curve"}
    assert Illustrations.model_validate(data).illustrations[0].ext["kind"]


def test_single_claim_node_without_special_generator_gets_fallback_chain_with_warning(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(R, "complete_json", CurveLLM())
    res = R.run("mini_test", _setup(tmp_path), _style())
    w = [x for x in res.ext["illus"]["warnings"] if x["code"] == "illus_fallback"]
    assert {x["node"] for x in w} == {"mini.porosity_basics", "mini.reservoir_decision", "mini.history_note"}
    assert "WARNING" in capsys.readouterr().err
    assert [i.ext["kind"] for i in res.illustrations if i.step_id == "mini.porosity_basics"] == ["chain"]


def test_curve_failures_do_not_fail_the_run(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "complete_json", CurveLLM(error=LlmError("обрыв")))
    res = R.run("mini_test", _setup(tmp_path), _style())
    w = [x for x in res.ext["illus"]["warnings"] if x["code"] == "illus_curve_failed"]
    assert len(w) == 1 and "обрыв" in w[0]["message"]
    assert {i.ext["kind"] for i in res.illustrations if i.step_id == RES} == {"chain"}


def test_invalid_curve_spec_three_times_is_a_warning(tmp_path, monkeypatch):
    llm = CurveLLM(reply=_spec(constants={"rho_water": 41}))
    monkeypatch.setattr(R, "complete_json", llm)
    res = R.run("mini_test", _setup(tmp_path), _style())
    w = [x for x in res.ext["illus"]["warnings"] if x["code"] == "illus_curve_failed"]
    assert llm.calls == 3 and "rho_water=41" in w[0]["errors"][0]


def test_model_says_formula_is_not_plottable_is_quiet(tmp_path, monkeypatch):
    monkeypatch.setattr(R, "complete_json", CurveLLM(reply=R.CurveSpec(feasible=False)))
    res = R.run("mini_test", _setup(tmp_path), _style())
    assert not [x for x in res.ext["illus"]["warnings"] if x["code"] == "illus_curve_failed"]
    assert {i.ext["kind"] for i in res.illustrations if i.step_id == RES} == {"chain"}


def test_auth_failure_stops_calling_the_model_for_other_nodes(tmp_path, monkeypatch):
    layer = _layer()
    other = _node(layer, "mini.porosity_basics")
    other.claims.append(Claim(id="mini.porosity_basics#c2", text="Формула пористости.", kind="inference", page_pdf=10,
                              quote="m = V_п / V", source_kind="formula", by_model=False))
    llm = CurveLLM(error=LlmAuthError("нет ключа"))
    monkeypatch.setattr(R, "complete_json", llm)
    res = R.run("mini_test", _setup(tmp_path, layer), _style())
    assert llm.calls == 1
    msgs = [x["message"] for x in res.ext["illus"]["warnings"] if x["code"] == "illus_curve_failed"]
    assert len(msgs) == 2 and "модель недоступна" in msgs[1]


def test_no_llm_skips_curves_without_warnings_about_them(tmp_path):
    res = R.run("mini_test", _setup(tmp_path), _style(), use_llm=False)
    assert {i.ext["kind"] for i in res.illustrations if i.step_id == RES} == {"chain"}
    assert not [x for x in res.ext["illus"]["warnings"] if x["code"] == "illus_curve_failed"]


def test_rerun_removes_files_that_are_no_longer_listed(tmp_path, monkeypatch):
    out = _setup(tmp_path)
    monkeypatch.setattr(R, "complete_json", CurveLLM())
    R.run("mini_test", out, _style())
    curve_file = out / f"mini_test/illus/{RES}.curve.svg"
    assert curve_file.exists()
    R.run("mini_test", out, _style(), use_llm=False)
    assert not curve_file.exists() and (out / f"mini_test/illus/{RES}.chain.svg").exists()


def test_table_and_layer_column_are_used_when_present(tmp_path):
    layer = _layer()
    node = _node(layer)
    node.claims[2].quote = "| Порода | Граница |\n|---|---|\n| песчаник | 3,5 |\n| алевролит | 2,8 |\n| глина | 1,9 |"
    node2 = _node(layer, "mini.porosity_basics")
    node2.claims[0].text = "Песчаник пористее глины."
    res = R.run("mini_test", _setup(tmp_path, layer), _style(), use_llm=False)
    kinds = {n: {i.ext["kind"] for i in res.illustrations if i.step_id == n} for n in (RES, "mini.porosity_basics")}
    assert kinds[RES] == {"chain", "crossplot"} and kinds["mini.porosity_basics"] == {"column"}


def test_missing_or_mismatched_layer_fails_loudly(tmp_path):
    with pytest.raises(FileNotFoundError, match="layer.json"):
        R.run("nope", tmp_path / "out", _style())
    out = _setup(tmp_path)
    (out / "other").mkdir()
    (out / "other/layer.json").write_text((out / "mini_test/layer.json").read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(ValueError, match="mini_test"):
        R.run("other", out, _style())


def test_style_without_required_section_fails_loudly():
    raw = json.loads(STYLE_FILE.read_text(encoding="utf-8"))
    del raw["provenance"]
    with pytest.raises(ValueError, match="provenance"):
        gen.Style(raw)


# ---------------------------------------------------------------- встраивание в курс

def test_course_shows_illustrations_with_label_source_and_alt(tmp_path, monkeypatch):
    out = _setup(tmp_path)
    monkeypatch.setattr(R, "complete_json", CurveLLM())
    res = R.run("mini_test", out, _style())
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    html = (course / f"step-{RES}.html").read_text(encoding="utf-8")
    assert 'id="b-illus"' in html and html.count("<figure") == 2
    assert f'src="assets/illus/{RES}.curve.svg"' in html and f'src="assets/illus/{RES}.chain.svg"' in html
    assert (course / f"assets/illus/{RES}.curve.svg").exists()
    assert re.search(r'<img src="assets/illus/[^"]+" alt="[^"]{20,}"', html)
    assert '<span class="prov">симуляция</span>' in html and "формула главы, стр. 11" in html
    for n in _layer().nodes:                                               # на каждом шаге есть иллюстрация
        assert "<figure" in (course / f"step-{n.id}.html").read_text(encoding="utf-8")
    rep = json.loads((course / "build_report.json").read_text(encoding="utf-8"))
    assert [w["code"] for w in rep["warnings"] if w["code"].startswith("illus_")] == ["illus_fallback"] * 3


def test_course_fails_loudly_if_listed_illustration_file_is_missing(tmp_path, monkeypatch):
    out = _setup(tmp_path)
    R.run("mini_test", out, _style(), use_llm=False)
    (out / f"mini_test/illus/{RES}.chain.svg").unlink()
    with pytest.raises(FileNotFoundError, match="chain.svg"):
        build("mini_test", out_root=out, pages_dir=tmp_path / "pages")


def test_cli_builds_illustrations(tmp_path):
    out = _setup(tmp_path)
    r = subprocess.run([sys.executable, "-m", "pipeline.illus.run", "--ch", "mini_test", "--out", str(out), "--styleguide", str(STYLE_FILE),
                        "--no-llm"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=UTF8)
    assert r.returncode == 0, r.stderr
    assert "иллюстрации: 4" in r.stdout and (out / "mini_test/illus/illustrations.json").exists()
    r = subprocess.run([sys.executable, "-m", "pipeline.illus.run", "--ch", "nope", "--out", str(tmp_path), "--styleguide", str(STYLE_FILE)],
                       cwd=ROOT, capture_output=True, text=True, encoding="utf-8", env=UTF8)
    assert r.returncode != 0 and "layer.json" in r.stderr


def _text_boxes(svg: str):
    """(x, baseline y, строка, размер) для каждой надписи."""
    return [(float(t.get("x")), float(t.get("y")), "".join(t.itertext()), float(t.get("font-size")))
            for t in _xml(svg).iter("{http://www.w3.org/2000/svg}text")]


def test_wrapped_lines_are_spaced_by_exactly_one_line_height():
    style = _style()
    cv = gen.Canvas(style, "Т", "")
    end = cv.block(16, 16, "очень длинный заголовок который точно не поместится в одну строку на этом рисунке " * 2, 368, style.text, bold=True)
    ys = [y for _, y, _, _ in _text_boxes(cv.finish("схема"))][:-1]          # без метки происхождения
    assert len(ys) >= 3 and all(round(b - a) == gen.LH for a, b in zip(ys, ys[1:])), ys
    assert round(end - 16) == len(ys) * gen.LH


def test_no_two_texts_overlap_in_any_figure():
    for fig in _every_figure():
        boxes = [b for b in _text_boxes(fig.svg) if b[2].strip()]
        for i, (x1, y1, s1, f1) in enumerate(boxes):
            for x2, y2, s2, f2 in boxes[i + 1:]:
                same_row_gap = abs(y1 - y2)
                w1, w2 = len(s1) * f1 * 0.5, len(s2) * f2 * 0.5
                horizontally = x1 < x2 + w2 and x2 < x1 + w1
                assert not (horizontally and same_row_gap < gen.LH * 0.7), (fig.kind, s1, s2)


def test_numbers_are_formatted_for_readers():
    assert gen.fmt(1000) == "1000" and gen.fmt(450) == "450" and gen.fmt(3.5) == "3,5" and gen.fmt(0.0015) == "0,0015"
    assert gen.fmt(2500000) == "2500000" and gen.fmt(1.5e9) == "1,5·10^9"
