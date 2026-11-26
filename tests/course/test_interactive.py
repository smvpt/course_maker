"""Задача 5: интерактив вместо ролика, «решение на данных» по шагам, «сначала угадай». Без сети: модель — мок."""
import json
import re
from pathlib import Path

import pytest

from contracts.models import Layer, Route, Routing, VideoScores
from pipeline.course import generate, guess as G, interactive as I, steptext, tasks as T
from pipeline.course.build import build
from pipeline.course.pernode import NodeStore, NotFeasible, ensure_per_node, read_store
from pipeline.course.steptext import GenerationFailed, LlmAuthError, LlmError, LlmState, StepTextOut, node_hash
from test_steptext import _paras
from test_tasks_gen import FakeLLM, MISC

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"
RES, PORO, DEC, HIST = ("mini.resistivity_depends_on_fluid", "mini.porosity_basics", "mini.reservoir_decision", "mini.history_note")
CURVES = {"RES": "сопротивление", "GR": "ГК"}


def _layer() -> Layer:
    return Layer.model_validate_json(MINI.read_text(encoding="utf-8"))


def _node(layer, nid=RES):
    return next(n for n in layer.nodes if n.id == nid)


def _route(nid, fmt, secondary=None, template=None) -> Route:
    return Route(node_id=nid, format=fmt, secondary_format=secondary, video_scores=VideoScores(time=1, invisible=1, scale=1, counterintuitive=1, cause_effect=1),
                 template=template, why="тест")


def _spec(**kw) -> I.InteractiveSpec:
    base = dict(claim_id=f"{RES}#c2", title="Как параметр насыщения зависит от сопротивления пласта", slider_name="rho_oil",
                slider_label="Сопротивление нефтенасыщенного пласта", slider_unit="Ом·м", slider_min=5, slider_max=80,
                x_name="x", x_label="Доля толщины пласта", x_unit="", x_min=0, x_max=1, y_label="Условный параметр насыщения", y_unit="",
                constants={"rho_water": 5}, expression="rho_oil * x / rho_water", curve_key="RES",
                note="Чем выше сопротивление пласта, тем больше параметр насыщения.")
    base.update(kw)
    return I.InteractiveSpec(**base)


def _profile_spec(**kw):
    return _spec(x_name="", x_label="", expression="rho_oil / rho_water", slider_label="Глубина", slider_unit="м", **kw)


# ---------------------------------------------------------------- план и шаблоны

def test_template_follows_route_template_then_difficulty():
    layer = _layer()
    node = _node(layer)                                            # трудность «Ф»
    assert I.template_for(node, None) == "distribution"
    assert I.template_for(node, _route(RES, "шортс", template="T2")) == "profile"
    assert I.template_for(node, _route(RES, "шортс", template="T3")) == "growth"
    assert I.template_for(node, _route(RES, "шортс", template="T4")) == "profile"
    for code, want in {"И": "profile", "Пр": "profile", "Н": "profile", "Р": "growth", "В": "growth", "П": "growth", "М": "distribution"}.items():
        node.difficulty.primary = code
        assert I.template_for(node, None) == want


def test_plan_wants_interactive_only_for_video_routed_nodes_without_a_video():
    layer = _layer()
    routes = {RES: _route(RES, "длинное видео", template="T1"), PORO: _route(PORO, "шортс"), DEC: _route(DEC, "текст", "интерактив"),
              HIST: _route(HIST, "текст")}
    plan, no_data = I.plan(layer.nodes, routes, True, lambda nid: False)
    assert plan == {RES: "distribution"} and no_data == [PORO, DEC]      # у порогового шага и «интерактив»-узла нет формулы
    plan, _ = I.plan(layer.nodes, routes, True, lambda nid: nid == RES)  # ролик есть — интерактив не нужен
    assert plan == {}


def test_plan_without_routing_uses_nodes_with_formulas_and_stays_quiet_about_others():
    layer = _layer()
    plan, no_data = I.plan(layer.nodes, {}, False, lambda nid: False)
    assert plan == {RES: "distribution"} and no_data == []
    plan, no_data = I.plan(layer.nodes, {}, True, lambda nid: False)     # routing есть, но про узлы ничего не говорит
    assert plan == {} and no_data == []


# ---------------------------------------------------------------- значения считает код

def _compute(spec, template, nid=RES):
    return I.validate_and_compute(_node(_layer(), nid), spec, template, set(CURVES))


def test_distribution_series_are_computed_by_code_on_the_slider_grid():
    errors, d = _compute(_spec(), "distribution")
    assert errors == [] and len(d["slider"]["values"]) == 41 and len(d["x"]["values"]) == 60 and len(d["series"]) == 41
    for i in (0, 17, 40):
        for j in (0, 30, 59):
            assert d["series"][i][j] == pytest.approx(d["slider"]["values"][i] * d["x"]["values"][j] / 5, rel=1e-5)
    flat = [v for row in d["series"] for v in row]
    assert d["y"]["min"] == min(flat) and d["y"]["max"] == max(flat) and d["page"] == 11 and d["x"]["unit"] == ""


def test_profile_and_growth_series():
    for template, n in (("profile", 121), ("growth", 81)):
        errors, d = _compute(_profile_spec(), template)
        assert errors == [] and len(d["series"]) == n and d["series"] == [pytest.approx(v / 5, rel=1e-5) for v in d["slider"]["values"]]
        assert d["x"] is None and d["template"] == template


def test_model_cannot_supply_values():
    assert not {"series", "values", "points", "data"} & set(I.InteractiveSpec.model_fields)


@pytest.mark.parametrize("template, mutate, needle", [
    ("distribution", dict(constants={"rho_water": 41}), "rho_water=41"),
    ("distribution", dict(claim_id=f"{PORO}#c1"), "не утверждение-формула"),
    ("distribution", dict(x_name="rho_oil"), "должны различаться"),
    ("distribution", dict(x_name="икс"), "латинице"),
    ("distribution", dict(slider_min=80, slider_max=5), "slider_min < slider_max"),
    ("distribution", dict(x_label=""), "пустое поле x_label"),
    ("distribution", dict(expression="rho_oil * x"), "не используются"),
    ("distribution", dict(expression="rho_water * rho_oil / rho_oil + x - x"), "горизонтальная линия"),
    ("distribution", dict(expression="rho_oil ** rho_oil ** rho_oil * x / rho_water"), "не вычисляется"),
    ("distribution", dict(expression="rho_oil * x / rho_water * 37"), "нет в узле"),
    ("distribution", dict(curve_key="ЧУЖАЯ"), "styleguide.curves"),
    ("distribution", dict(title="How the saturation parameter depends on formation resistivity"), "на русском"),
    ("distribution", dict(note="Раз. И два."), "одна фраза"),
])
def test_interactive_spec_is_checked_by_code(template, mutate, needle):
    errors, d = _compute(_spec(**mutate), template)
    assert errors and needle in " ".join(errors) and d == {}, errors


def test_distribution_must_depend_on_the_slider():
    errors, _ = _compute(_spec(expression="rho_water * x + rho_oil * 0 + rho_oil / rho_oil"), "distribution")
    assert errors            # слайдер не меняет картинку (или выражение недопустимо) — в любом случае не принимается


# ---------------------------------------------------------------- вызов модели

def test_make_interactive_returns_spec_and_data_and_passes_the_template(monkeypatch):
    calls = []
    monkeypatch.setattr(I, "complete_json", lambda **kw: calls.append(kw) or _spec())
    out = I.make_interactive(_node(_layer()), "distribution", CURVES, "ru")
    assert out["data"]["series"] and out["spec"]["expression"] == "rho_oil * x / rho_water"
    assert "distribution" in calls[0]["vars"]["template"] and set(calls[0]["vars"]) == {"node", "formulas", "template", "curves", "language", "feedback"}
    assert calls[0]["prompt"] == "course/interactive" and calls[0]["schema"] is I.InteractiveSpec


def test_make_interactive_not_feasible_and_invalid(monkeypatch):
    monkeypatch.setattr(I, "complete_json", lambda **kw: I.InteractiveSpec(feasible=False))
    with pytest.raises(NotFeasible):
        I.make_interactive(_node(_layer()), "profile", CURVES, "ru")
    calls = []
    monkeypatch.setattr(I, "complete_json", lambda **kw: calls.append(kw) or _spec(constants={"rho_water": 41}))
    with pytest.raises(GenerationFailed, match="rho_water=41"):
        I.make_interactive(_node(_layer()), "distribution", CURVES, "ru")
    assert len(calls) == 3 and "rho_water=41" in calls[1]["vars"]["feedback"]


def test_prompt_variables_match_what_code_passes():
    for name, want in (("interactive", {"node", "formulas", "template", "curves", "language", "feedback"}),
                       ("guess", {"node", "language", "feedback"})):
        text = (ROOT / f"prompts/course/{name}.md").read_text(encoding="utf-8")
        assert set(re.findall(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}", text)) == want, name


def test_table_rows_repeat_the_same_numbers_as_the_slider():
    errors, d = _compute(_spec(), "distribution")
    head, rows = I.table_rows(d)
    assert len(rows) == 9 and "Сопротивление нефтенасыщенного пласта, Ом·м" == head[0] and "при доля толщины пласта" in head[1]
    assert rows[0][0] == "5" and rows[-1][0] == "80"
    errors, d = _compute(_profile_spec(), "profile")
    head, rows = I.table_rows(d)
    assert head == ["Глубина, м", "Условный параметр насыщения"] and rows[-1] == ["80", "16"]


# ---------------------------------------------------------------- хранилище по узлам

def _store_run(layer, tmp_path, make, wanted, state=None, only=None):
    return ensure_per_node(layer, tmp_path / "store.json", wanted, make, state or LlmState(), only)


def test_store_keeps_fresh_entries_and_regenerates_changed_and_failed(tmp_path):
    layer = _layer()
    calls = []

    def make(n):
        calls.append(n.id)
        if n.id == PORO:
            raise GenerationFailed("x", ["не вышло"])
        return {"v": n.id}
    st = _store_run(layer, tmp_path, make, {RES, PORO})
    assert set(st.nodes) == {RES} and st.failed[PORO].errors == ["не вышло"] and calls == [RES, PORO]
    calls.clear()
    _store_run(layer, tmp_path, make, {RES, PORO})
    assert calls == [PORO]                                         # свежий не трогаем, неудавшийся пробуем снова
    _node(layer).layers.main.text = "другой текст"
    calls.clear()
    _store_run(layer, tmp_path, make, {RES, PORO})
    assert calls == [RES, PORO]
    assert read_store(tmp_path / "store.json", "mini_test").nodes[RES].hash == node_hash(_node(layer))


def test_store_marks_not_feasible_and_model_failures_per_node_and_stops_on_auth(tmp_path):
    layer = _layer()
    seq = iter([NotFeasible("нельзя"), LlmError("обрыв"), {"ok": 1}])

    def make(n):
        r = next(seq)
        if isinstance(r, Exception):
            raise r
        return r
    state = LlmState()
    st = _store_run(layer, tmp_path, make, {RES, PORO, DEC}, state)
    assert st.failed[RES].errors == ["нельзя"] and st.failed[PORO].errors[0].startswith("отказ модели") and DEC in st.nodes
    assert state.down is None
    auth = LlmState()
    calls = []

    def make2(n):
        calls.append(n.id)
        raise LlmAuthError("нет ключа")
    st = _store_run(layer, tmp_path / "x", make2, {RES, PORO, DEC}, auth)
    assert calls == [RES] and all(f.errors[0].startswith("модель недоступна") for f in st.failed.values())


# ---------------------------------------------------------------- «сначала угадай»

def _gspec(**kw) -> G.GuessSpec:
    base = dict(false_statement="Высокое сопротивление пласта всегда означает, что в нём нефть.",
                true_statement="Нефтенасыщенный пласт имеет сопротивление в несколько раз выше водонасыщенного.",
                explain_false="Высокое сопротивление даёт не только нефть, но и плотная порода.",
                explain_true="Нефть почти не проводит ток, а вода проводит хорошо.", claim_ids=[f"{RES}#c1"])
    base.update(kw)
    return G.GuessSpec(**base)


def test_guess_is_wanted_only_when_node_has_a_misconception():
    layer = _layer()
    assert [n.id for n in layer.nodes if G.wanted(n)] == [RES]


@pytest.mark.parametrize("mutate, needle", [
    (dict(false_statement="Пласт бывает разным."), "заблуждение узла"),
    (dict(true_statement="Совсем другая мысль про всё на свете."), "опираться на указанные утверждения"),
    (dict(false_statement="Высокое сопротивление пласта всегда означает нефть в 7 раз."), "чисел ['7']"),
    (dict(true_statement="Нефтенасыщенный пласт имеет сопротивление в несколько раз выше водонасыщенного?"), "не вопрос"),
    (dict(false_statement=" ".join(["слово"] * 30) + "."), "до 25 слов"),
    (dict(explain_false="Это так. И вот почему."), "одна фраза"),
    (dict(claim_ids=[]), "пустой claim_ids"),
    (dict(claim_ids=["mini.nope#c1"]), "нет в узле"),
    (dict(true_statement="High resistivity of the oil-bearing formation exceeds water one"), "на русском"),
])
def test_guess_is_checked_by_code(mutate, needle):
    errors = G.validate_guess(_node(_layer()), _gspec(**mutate))
    assert errors and needle in " ".join(errors), errors


def test_guess_statements_must_differ():
    same = "Нефтенасыщенный пласт имеет сопротивление выше водонасыщенного, высокое сопротивление всегда означает нефть."
    assert any("различаться" in e for e in G.validate_guess(_node(_layer()), _gspec(false_statement=same, true_statement=same)))


def test_code_decides_which_statement_is_shown_and_it_is_not_always_the_same():
    shown = {G.show_true(f"mini.node{i}") for i in range(20)}
    assert shown == {True, False}
    assert G.show_true(RES) == G.show_true(RES)
    for truth, key in ((True, "true_statement"), (False, "false_statement")):
        node = _node(_layer())
        spec = _gspec()
        import pipeline.course.guess as g
        orig = g.show_true
        g.show_true = lambda _id, t=truth: t
        try:
            g.complete_json = lambda **kw: spec
            out = g.make_guess(node, "ru")
        finally:
            g.show_true = orig
        assert out["truth"] is truth and out["statement"] == getattr(spec, key) and out["explanation"] == getattr(spec, "explain_true" if truth else "explain_false")
        assert out["pages"] == [11] and out["other_statement"] == (spec.false_statement if truth else spec.true_statement)


def test_make_guess_feeds_errors_back_and_fails_after_three(monkeypatch):
    calls = []
    monkeypatch.setattr(G, "complete_json", lambda **kw: calls.append(kw) or _gspec(claim_ids=[]))
    with pytest.raises(GenerationFailed, match="claim_ids"):
        G.make_guess(_node(_layer()), "ru")
    assert len(calls) == 3 and "claim_ids" in calls[1]["vars"]["feedback"] and set(calls[0]["vars"]) == {"node", "language", "feedback"}


# ---------------------------------------------------------------- сборка курса

def _out(tmp_path, layer=None, routes=None) -> Path:
    layer = layer or _layer()
    d = tmp_path / "out" / layer.chapter
    d.mkdir(parents=True)
    (d / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    (d / "units.json").write_text(json.dumps({"domain": "geology"}), encoding="utf-8")
    if routes is not None:
        (d / "routing.json").write_text(Routing(chapter=layer.chapter, routes=routes).model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    return tmp_path / "out"


def _models(monkeypatch, layer=None, inter=None, guess=None):
    layer = layer or _layer()
    monkeypatch.setattr(steptext, "complete_json", lambda **kw: StepTextOut(paragraphs=_paras(json.loads(kw["vars"]["node"])["id"])))
    monkeypatch.setattr(T, "complete_json", FakeLLM(layer))
    inter_calls, guess_calls = [], []

    def fake_inter(**kw):
        inter_calls.append(kw)
        r = inter if inter is not None else _spec()
        if isinstance(r, Exception):
            raise r
        return r

    def fake_guess(**kw):
        guess_calls.append(kw)
        r = guess if guess is not None else _gspec()
        if isinstance(r, Exception):
            raise r
        return r
    monkeypatch.setattr(I, "complete_json", fake_inter)
    monkeypatch.setattr(G, "complete_json", fake_guess)
    monkeypatch.setattr(generate, "load_misconceptions", lambda d: MISC)
    return inter_calls, guess_calls


def _course(tmp_path, monkeypatch, routes=None, extras=True, layer=None, **models):
    layer = layer or _layer()
    out = _out(tmp_path, layer, routes)
    calls = _models(monkeypatch, layer, **models)
    return build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True, extras=extras), calls


def _html(course, nid):
    return (course / f"step-{nid}.html").read_text(encoding="utf-8")


def _report(course):
    return json.loads((course / "build_report.json").read_text(encoding="utf-8"))


def test_interactive_block_for_a_video_routed_step_without_a_video(tmp_path, monkeypatch):
    routes = [_route(RES, "длинное видео", template="T2"), _route(PORO, "текст")]
    course, (inter_calls, _) = _course(tmp_path, monkeypatch, routes, inter=_profile_spec())
    html = _html(course, RES)
    assert 'id="b-interactive"' in html and 'data-template="profile"' in html and '<input type="range" id="inter-slider" min="0" max="120" step="1"' in html
    assert '<span class="prov-chip">симуляция</span>' in html and "Значения рассчитаны кодом по формуле главы" in html
    data = json.loads(re.search(r'id="inter-data">(.*?)</script>', html, re.S).group(1))
    assert data["template"] == "profile" and len(data["series"]) == 121 and data["palette"]["badge"].startswith("#")
    assert data["palette"]["color"] == "#F1C40F" and data["slider"]["label"] == "Глубина"          # цвет кривой «сопротивление» из styleguide
    assert re.search(r"<table>.*?<th scope=\"col\">Глубина, м</th>", html, re.S)                   # те же числа таблицей
    assert 'id="b-media"' not in html                                                              # вместо ролика
    assert 'id="b-interactive"' not in _html(course, PORO) and len(inter_calls) == 1
    rep = _report(course)
    assert rep["interactive_steps"] == 1
    assert (course / "interactive.json").exists()


def test_without_routing_template_follows_the_difficulty_type(tmp_path, monkeypatch):
    course, _ = _course(tmp_path, monkeypatch)                     # трудность «Ф» → распределение
    html = _html(course, RES)
    assert 'data-template="distribution"' in html
    data = json.loads(re.search(r'id="inter-data">(.*?)</script>', html, re.S).group(1))
    assert len(data["series"]) == 41 and len(data["series"][0]) == 60 and data["x"]["label"] == "Доля толщины пласта"
    assert not [w for w in _report(course)["warnings"] if w["code"].startswith("interactive")]


def test_step_without_formula_gets_a_warning_and_no_interactive(tmp_path, monkeypatch, capsys):
    course, _ = _course(tmp_path, monkeypatch, [_route(RES, "шортс"), _route(PORO, "длинное видео")])
    rep = _report(course)
    w = [x for x in rep["warnings"] if x["code"] == "interactive_no_data"]
    assert [x["node"] for x in w] == [PORO] and "WARNING" in capsys.readouterr().err
    assert 'id="b-interactive"' not in _html(course, PORO)


def test_video_with_subtitles_beats_interactive(tmp_path, monkeypatch):
    layer = _layer()
    out = _out(tmp_path, layer, [_route(RES, "длинное видео")])
    vdir = out / "mini_test/videos" / RES
    vdir.mkdir(parents=True)
    (vdir / "clip.mp4").write_bytes(b"\x00\x00\x00\x18ftypmp42")
    (vdir / "clip.vtt").write_text("WEBVTT\n\n00:00.000 --> 00:02.000\nПривет\n", encoding="utf-8")
    inter_calls, _ = _models(monkeypatch, layer)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True, extras=True)
    html = _html(course, RES)
    assert '<video controls' in html and 'src="media/%s/clip.mp4"' % RES in html
    assert re.search(r'<track kind="subtitles" srclang="ru" label="[^"]+" data-cues="cues-main" default>', html)         # реплики встроены: <track src> с file:// не грузится
    assert json.loads(re.search(r'id="cues-main">(.*?)</script>', html, re.S).group(1)) == [{"s": 0.0, "e": 2.0, "t": "Привет"}]
    assert (course / f"media/{RES}/clip.vtt").exists() and (course / f"media/{RES}/clip.mp4").exists()
    assert 'id="b-interactive"' not in html and inter_calls == []


def test_pending_block_shows_passport_link_or_nothing(tmp_path, monkeypatch):
    layer = _layer()
    routes = [_route(PORO, "шортс"), _route(DEC, "длинное видео")]          # у обоих нет формулы: интерактива нет
    out = _out(tmp_path, layer, routes)
    pdir = out / "mini_test/videos" / PORO
    pdir.mkdir(parents=True)
    (pdir / "passport.json").write_text("{}", encoding="utf-8")
    _models(monkeypatch, layer)
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True, extras=True)
    with_passport, without = _html(course, PORO), _html(course, DEC)
    assert 'id="b-media"' in with_passport and f'href="media/{PORO}/passport.json"' in with_passport and "паспорте ролика" in with_passport
    assert 'id="b-media"' not in without and "не собран" not in without


def test_interactive_failure_leaves_the_passport_link_and_warns(tmp_path, monkeypatch):
    layer = _layer()
    out = _out(tmp_path, layer, [_route(RES, "шортс")])
    pdir = out / "mini_test/videos" / RES
    pdir.mkdir(parents=True)
    (pdir / "passport.json").write_text("{}", encoding="utf-8")
    _models(monkeypatch, layer, inter=_spec(constants={"rho_water": 41}))
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True, extras=True)
    html = _html(course, RES)
    assert 'id="b-interactive"' not in html and f'href="media/{RES}/passport.json"' in html
    assert [w["code"] for w in _report(course)["warnings"] if w["code"] == "interactive_failed"] == ["interactive_failed"]


def test_decision_on_data_is_a_stepper_that_shows_everything_without_js(tmp_path, monkeypatch):
    course, _ = _course(tmp_path, monkeypatch)
    html = _html(course, RES)
    assert '<div class="sig-flow" data-by="model" data-stepper>' in html or re.search(r'<div class="sig-flow"[^>]*data-stepper>', html)
    assert re.search(r'<p class="stepper-ctl" hidden>', html)                       # без JS элементов управления нет, всё видно
    for part in ("Сигнал", "Правило", "Вывод", "Контрпример"):
        assert part in html


def test_guess_card_opens_the_step_and_has_the_explanation(tmp_path, monkeypatch):
    course, (_, guess_calls) = _course(tmp_path, monkeypatch)
    html = _html(course, RES)
    truth = G.show_true(RES)
    spec = _gspec()
    assert f'<section id="guess" class="guess" aria-labelledby="guess-h" data-truth="{str(truth).lower()}">' in html
    assert (spec.true_statement if truth else spec.false_statement) in html
    assert (spec.explain_true if truth else spec.explain_false) in html
    assert re.search(r'data-answer="true">Верно</button>', html) and re.search(r'data-answer="false">Неверно</button>', html) and 'data-action="skip"' in html
    assert '<div id="step-body">' in html and html.index('id="guess"') < html.index('id="step-body"') < html.index('id="b-main"')
    assert html.index('id="step-body"') < html.index('<footer class="step-foot">')
    assert 'id="guess"' not in _html(course, PORO)                                  # у остальных шагов заблуждения нет
    rep = _report(course)
    assert rep["guess_steps"] == 1 and len(guess_calls) == 1 and rep["tasks"] >= 15  # вопрос в обязательные задания не входит
    assert json.loads((course / "tasks.json").read_text(encoding="utf-8"))["tasks"]


def test_guess_failure_means_the_step_opens_as_usual(tmp_path, monkeypatch):
    course, _ = _course(tmp_path, monkeypatch, guess=_gspec(claim_ids=[]))
    assert 'id="guess"' not in _html(course, RES) and 'id="step-body"' in _html(course, RES)
    assert [w["node"] for w in _report(course)["warnings"] if w["code"] == "guess_failed"] == [RES]


def test_extras_are_off_in_the_library_default_and_on_in_the_cli(tmp_path, monkeypatch):
    course, (inter_calls, guess_calls) = _course(tmp_path, monkeypatch, extras=False)
    assert inter_calls == [] and guess_calls == [] and not (course / "interactive.json").exists()
    import inspect
    from pipeline.course import build as B
    assert inspect.signature(B.build).parameters["extras"].default is False
    assert "extras=not a.no_llm" in inspect.getsource(B.main)


def test_outage_message_counts_interactive_and_questions(tmp_path, monkeypatch, capsys):
    layer = _layer()
    out = _out(tmp_path, layer)
    monkeypatch.setattr(generate, "load_misconceptions", lambda d: MISC)
    monkeypatch.setattr(steptext, "complete_json", lambda **kw: (_ for _ in ()).throw(LlmAuthError("AuthenticationError: нет ключа")))
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True, extras=True)
    rep = _report(course)
    mu = [w for w in rep["warnings"] if w["code"] == "model_unavailable"]
    assert len(mu) == 1 and "без интерактива и вопросов 2" in mu[0]["message"]
    assert [l for l in capsys.readouterr().err.splitlines() if l.startswith("WARNING")] == ["WARNING: " + mu[0]["message"]]


def test_script_has_slider_guess_and_stepper_logic():
    js = (ROOT / "pipeline/course/assets/course.js").read_text(encoding="utf-8")
    for needle in ("function initInteractive", 'getElementById("inter-slider")', "aria-valuetext", "K.guess", '"skip"',
                   "data-stepper", "[data-stepper-next]"):
        assert needle in js, needle
    assert 'createElementNS("http://www.w3.org/2000/svg", tag)' in js and "SVGNS" not in js     # var ниже вызова initStep был бы undefined
    assert "eval(" not in js and "new Function" not in js                             # JS ничего не вычисляет по формулам


# ---------------------------------------------------------------- общий шаблон «один слайдер → значение и кривая»

def _dep_spec(**kw):
    base = dict(x_name="", x_label="", expression="rho_oil / rho_water", slider_label="Сопротивление нефтенасыщенного пласта", slider_unit="Ом·м")
    base.update(kw)
    return _spec(**base)


def test_dependence_template_for_a_one_variable_formula():
    errors, d = _compute(_dep_spec(), "dependence")
    assert errors == [] and d["template"] == "dependence" and d["x"] is None
    assert len(d["slider"]["values"]) == 121 and d["series"] == [pytest.approx(v / 5, rel=1e-5) for v in d["slider"]["values"]]
    assert d["slider"]["label"] == "Сопротивление нефтенасыщенного пласта" and d["slider"]["unit"] == "Ом·м"
    assert "dependence" in I.TEMPLATE_HINT and "любая переменная" in I.TEMPLATE_HINT["dependence"]


def test_dependence_needs_no_second_variable_but_still_checks_everything_else():
    errors, _ = _compute(_dep_spec(constants={"rho_water": 41}), "dependence")
    assert any("rho_water=41" in e for e in errors)
    errors, _ = _compute(_dep_spec(expression="rho_water * rho_oil ** rho_oil ** rho_oil"), "dependence")
    assert any("не вычисляется" in e for e in errors)
    errors, _ = _compute(_dep_spec(expression="rho_water * rho_oil / rho_oil"), "dependence")
    assert any("горизонтальная линия" in e for e in errors)


def test_primary_template_not_feasible_falls_back_to_dependence_once(monkeypatch):
    calls = []

    def fake(**kw):
        calls.append(kw["vars"]["template"])
        return I.InteractiveSpec(feasible=False) if len(calls) == 1 else _dep_spec()
    monkeypatch.setattr(I, "complete_json", fake)
    out = I.make_interactive(_node(_layer()), "distribution", CURVES, "ru")
    assert out["data"]["template"] == "dependence" and len(calls) == 2
    assert calls[0].startswith("distribution") and calls[1].startswith("dependence")


def test_not_feasible_for_both_templates_stays_not_feasible(monkeypatch):
    calls = []
    monkeypatch.setattr(I, "complete_json", lambda **kw: calls.append(1) or I.InteractiveSpec(feasible=False))
    with pytest.raises(NotFeasible, match="distribution.*dependence|dependence"):
        I.make_interactive(_node(_layer()), "profile", CURVES, "ru")
    assert len(calls) == 2
    calls.clear()
    with pytest.raises(NotFeasible):
        I.make_interactive(_node(_layer()), "dependence", CURVES, "ru")
    assert len(calls) == 1                                          # у самого общего шаблона запасного нет


def test_invalid_spec_does_not_trigger_the_fallback_template(monkeypatch):
    calls = []
    monkeypatch.setattr(I, "complete_json", lambda **kw: calls.append(kw["vars"]["template"]) or _spec(constants={"rho_water": 41}))
    with pytest.raises(GenerationFailed):
        I.make_interactive(_node(_layer()), "distribution", CURVES, "ru")
    assert len(calls) == 3 and all(c.startswith("distribution") for c in calls)


def test_course_page_uses_the_dependence_template_after_fallback(tmp_path, monkeypatch):
    layer = _layer()
    out = _out(tmp_path, layer)
    _models(monkeypatch, layer)
    seq = []
    monkeypatch.setattr(I, "complete_json", lambda **kw: seq.append(1) or (I.InteractiveSpec(feasible=False) if len(seq) == 1 else _dep_spec()))
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True, extras=True)
    html = _html(course, RES)
    assert 'data-template="dependence"' in html and 'id="b-interactive"' in html and 'min="0" max="120"' in html
    assert [w for w in _report(course)["warnings"] if w["code"].startswith("interactive")] == []
