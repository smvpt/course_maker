"""Интерактив без формул: схема-исследование из утверждений узла. Без сети: модель — мок."""
import json
import re
from pathlib import Path

import pytest

from contracts.models import Layer
from pipeline.course import generate, scheme as S
from pipeline.course.build import build
from pipeline.course.pernode import NotFeasible, read_store
from pipeline.course.steptext import GenerationFailed
from tests.course.test_interactive import _models, _out, _route, _layer as _mini, PORO, RES

ROOT = Path(__file__).resolve().parents[2]
STYLE = json.loads((ROOT / "data/organizers/03_стайлгайд/styleguide.json").read_text(encoding="utf-8"))
ROCKS = {k: v["ru"] for k, v in STYLE["lithology"].items()}
TEXTS = ["Открытые поры соединены между собой и пропускают флюид.", "Закрытые поры изолированы и флюид не пропускают.",
         "Эффективная пористость учитывает только открытые поры."]


def _layer() -> Layer:
    """Мини-глава, где у узла пористости 4 текстовых утверждения и нет формул."""
    layer = _mini()
    node = next(n for n in layer.nodes if n.id == PORO)
    base = node.claims[0]
    for i, t in enumerate(TEXTS, 2):
        node.claims.append(base.model_copy(update={"id": f"{PORO}#c{i}", "text": t, "quote": t.lower(), "page_pdf": 10 + i}))
    return layer


def _spec(**kw) -> S.SchemeSpec:
    base = dict(title="Какие бывают поры", note="Нажми на часть, чтобы узнать, чем она отличается.", layout="chain", parts=[
        S.SchemePart(label="Открытые поры", description="Соединены между собой и пропускают флюид.", claim_id=f"{PORO}#c2"),
        S.SchemePart(label="Закрытые поры", description="Изолированы, поэтому флюид через них не идёт.", claim_id=f"{PORO}#c3"),
        S.SchemePart(label="Эффективная пористость", description="Считается только по сообщающимся пустотам.", claim_id=f"{PORO}#c4")])
    base.update(kw)
    return S.SchemeSpec(**base)


def _errors(spec, layer=None):
    layer = layer or _layer()
    return S.validate_scheme(next(n for n in layer.nodes if n.id == PORO), spec, set(ROCKS))[0]


def _mut(i, **kw):
    spec = _spec()
    spec.parts[i] = spec.parts[i].model_copy(update=kw)
    return spec


def test_valid_scheme_passes_and_data_has_pages_and_claims():
    errors, data = S.validate_scheme(next(n for n in _layer().nodes if n.id == PORO), _spec(), set(ROCKS))
    assert errors == [] and data["template"] == "scheme" and data["layout"] == "chain"
    assert [(p["claim_id"], p["page"]) for p in data["parts"]] == [(f"{PORO}#c{i}", 10 + i) for i in (2, 3, 4)]


@pytest.mark.parametrize("spec, needle", [
    (_spec(parts=_spec().parts[:2]), "от 3 до 7"),
    (_spec(parts=_spec().parts * 3), "от 3 до 7"),
    (_mut(0, label="Закрытые поры"), "уже есть"),
    (_mut(0, label="Пористые зоны с очень длинным названием из многих слов"), "длиннее 6 слов"),
    (_mut(0, label="Квантовая гравитация"), "нет в узле"),
    (_mut(0, description="Открытые поры соединены между собой."), "подсказкой"),
    (_mut(0, description="Занимают 99 процентов объёма."), "числа ['99']"),
    (_mut(0, claim_id=f"{PORO}#c77"), "нет в узле"),
    (_mut(0, claim_id=f"{PORO}#c1", description=f"Первая. Вторая. Третья."), "не больше 2 фраз"),
    (_mut(0, description="Only English words here for the description."), "на русском"),
    (_mut(0, rock="sand"), "layout=layers"),
    (_spec(title="  "), "пустое поле title"),
    (_spec(note="Раз. Два."), "одна фраза"),
])
def test_invalid_schemes_are_rejected_with_a_reason(spec, needle):
    assert any(needle in e for e in _errors(spec)), _errors(spec)


def test_layers_with_rocks_from_styleguide_and_unknown_rock_rejected():
    spec = _spec(layout="layers")
    spec.parts[0] = spec.parts[0].model_copy(update={"rock": "sand"})
    assert _errors(spec) == []
    spec.parts[1] = spec.parts[1].model_copy(update={"rock": "granite"})
    assert any("granite" in e for e in _errors(spec))


def test_formula_or_table_claim_cannot_support_a_part():
    layer = _layer()
    node = next(n for n in layer.nodes if n.id == PORO)
    node.claims[1] = node.claims[1].model_copy(update={"source_kind": "formula"})
    assert any("не формула" in e for e in _errors(_spec(), layer))


def test_make_scheme_feeds_errors_back_then_succeeds(monkeypatch):
    node = next(n for n in _layer().nodes if n.id == PORO)
    calls = []
    monkeypatch.setattr(S, "complete_json", lambda **kw: calls.append(kw) or (_mut(0, label="Квантовая гравитация") if len(calls) == 1 else _spec()))
    out = S.make_scheme(node, ROCKS, "ru")
    assert out["data"]["template"] == "scheme" and len(calls) == 2
    assert calls[0]["vars"]["feedback"].startswith("нет") and "нет в узле" in calls[1]["vars"]["feedback"]
    assert json.loads(calls[0]["vars"]["rocks"])[0]["key"] in ROCKS


def test_make_scheme_not_feasible_and_gives_up_after_three_attempts(monkeypatch):
    node = next(n for n in _layer().nodes if n.id == PORO)
    monkeypatch.setattr(S, "complete_json", lambda **kw: S.SchemeSpec(feasible=False))
    with pytest.raises(NotFeasible, match="модель ответила"):
        S.make_scheme(node, ROCKS, "ru")
    calls = []
    monkeypatch.setattr(S, "complete_json", lambda **kw: calls.append(1) or _mut(0, claim_id="нет"))
    with pytest.raises(GenerationFailed):
        S.make_scheme(node, ROCKS, "ru")
    assert len(calls) == 3


def test_prompt_variables_match_what_code_passes():
    text = (ROOT / "prompts/course/scheme.md").read_text(encoding="utf-8")
    assert set(re.findall(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}", text)) == {"node", "rocks", "language", "feedback"}


# ---------------------------------------------------------------- сборка курса

def _course(tmp_path, monkeypatch, scheme=None, routes=None):
    layer = _layer()
    out = _out(tmp_path, layer, routes if routes is not None else [_route(PORO, "шортс")])
    _models(monkeypatch, layer)
    monkeypatch.setattr(generate, "load_misconceptions", lambda domain: [])
    monkeypatch.setattr(S, "complete_json", lambda **kw: scheme or _spec())
    return build("mini_test", out_root=out, pages_dir=tmp_path / "pages", generate=True, extras=True), layer


def test_video_node_without_formula_gets_scheme_interactive_on_the_step_page(tmp_path, monkeypatch):
    course, _ = _course(tmp_path, monkeypatch)
    html = (course / f"step-{PORO}.html").read_text(encoding="utf-8")
    assert 'id="b-interactive"' in html and 'data-template="scheme"' in html and '<span class="prov-chip">схема</span>' in html
    assert html.count('class="scheme-part"') == 3 and "Открытые поры" in html
    assert 'data-mode="quiz"' in html and 'id="scheme-detail" aria-live="polite"' in html
    data = json.loads(re.search(r'id="inter-data">(.*?)</script>', html, re.S).group(1))
    assert data["template"] == "scheme" and all(p["claim_id"] in html for p in data["parts"])
    rep = json.loads((course / "build_report.json").read_text(encoding="utf-8"))
    assert rep["interactive_steps"] >= 1 and not [w for w in rep["warnings"] if w["code"] == "interactive_no_data" and w["node"] == PORO]
    assert read_store(course / "interactive.json", "mini_test").nodes[PORO].data["data"]["template"] == "scheme"


def test_layers_scheme_paints_bands_with_styleguide_lithology(tmp_path, monkeypatch):
    spec = _spec(layout="layers")
    spec.parts[0] = spec.parts[0].model_copy(update={"rock": "sand"})
    course, _ = _course(tmp_path, monkeypatch, scheme=spec)
    html = (course / f"step-{PORO}.html").read_text(encoding="utf-8")
    assert 'data-layout="layers"' in html and f'--part-bg: {STYLE["lithology"]["sand"]["color"]}' in html and "--part-fg:" in html


def test_scheme_not_feasible_keeps_the_old_warning_and_no_block(tmp_path, monkeypatch):
    course, _ = _course(tmp_path, monkeypatch, scheme=S.SchemeSpec(feasible=False))
    rep = json.loads((course / "build_report.json").read_text(encoding="utf-8"))
    w = [x for x in rep["warnings"] if x["code"] == "interactive_no_data" and x["node"] == PORO]
    assert len(w) == 1
    assert 'id="b-interactive"' not in (course / f"step-{PORO}.html").read_text(encoding="utf-8")


def test_without_the_model_the_warning_stays_and_a_stored_scheme_is_reused(tmp_path, monkeypatch):
    course, layer = _course(tmp_path, monkeypatch)
    again = build("mini_test", out_root=tmp_path / "out", pages_dir=tmp_path / "pages")        # без generate: берём interactive.json
    assert 'data-template="scheme"' in (again / f"step-{PORO}.html").read_text(encoding="utf-8")
    fresh = tmp_path / "second"
    out = _out(fresh, layer, [_route(PORO, "шортс")])
    c2 = build("mini_test", out_root=out, pages_dir=fresh / "pages")
    rep = json.loads((c2 / "build_report.json").read_text(encoding="utf-8"))
    assert [x["node"] for x in rep["warnings"] if x["code"] == "interactive_no_data"] == [PORO]


def test_scheme_js_and_css_have_modes_keyboard_and_book_link():
    js = (ROOT / "pipeline/course/assets/course.js").read_text(encoding="utf-8")
    for needle in ("function initScheme", "Проверь по книге", '"btn-small pg"', "startQuiz", "Какая это часть схемы", "role", "next.focus()"):
        assert needle in js
    css = (ROOT / "pipeline/course/assets/course.css").read_text(encoding="utf-8")
    assert re.search(r"\.scheme-part \{[^}]*min-height: 48px", css) and "data-layout=\"layers\"" in css
    tpl = (ROOT / "pipeline/course/templates/step.html.j2").read_text(encoding="utf-8")
    assert tpl.count('<button type="button" class="scheme-part"') == 1                 # настоящие кнопки: Tab, Enter, пробел


def test_prompt_demands_a_distinguishing_feature_in_every_description():
    text = (ROOT / "prompts/course/scheme.md").read_text(encoding="utf-8")
    assert "отличает ЭТУ часть" in text and "feasible=false" in text.split("3. Названия")[1]


def test_label_words_may_be_inflected_but_must_still_come_from_the_node():
    assert _errors(_mut(0, label="Открытая пора")) == []                     # в узле «Открытые поры»: другая форма — не повод отказывать
    assert _errors(_mut(0, label="Закрытых порах")) == []
    assert any("нет в узле" in e for e in _errors(_mut(0, label="Квантовых зон")))
