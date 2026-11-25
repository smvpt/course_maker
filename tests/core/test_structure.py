"""structure: units → layer.json + coverage.json. LLM подменён ответами по имени промпта."""
import json

import jsonschema
import pytest

from contracts import models as m
from pipeline.common import io, paths
from pipeline.structure import build, quotes
from pipeline.structure import schemas as s

MINI = paths.ROOT / "fixtures" / "core" / "mini_chapter"
MISC = [{"id": "misc.pressure_sound_speed", "text": "Давление расходится с постоянной скоростью, как звук."}]


def F(t="x"):
    return m.Field_(text=t, by_model=False)


def draft(claims, links=()):
    return s.NodeDraft(
        layers=m.Layers(topic=F(), main=F(), mechanism=F(), practice=F(), nuances=F()),
        claims=claims, links=list(links),
        misconception=m.Misconception(ref="misc.nope", text="неизвестное заблуждение", by_model=False),
        data_meaning=m.DataMeaning(from_chapter=F(), breaks=F(), hypotheses=[]),
        it_analogy=m.ItAnalogy(text="a", breaks_where="b", by_model=False),
        terms_introduced=["пьезопроводность"], terms_used=["фильтрация"],
    )


@pytest.fixture
def fake_llm(monkeypatch):
    calls = []
    p039 = [f"p039.{i:02d}" for i in range(1, 12)]

    def fake(prompt, vars, schema, tier="default", images=None):
        calls.append(prompt)
        if prompt == "core/structure_plan":
            assert "p038.20" in vars["units"] and "Ф — Формализм" in vars["difficulty_types"]
            return s.Plan(nodes=[
                s.PlanNode(slug="Piezo Equation", title="Уравнение пьезопроводности", title_novice="Давление расплывается",
                           difficulty_primary="Ф", difficulty_secondary="М", threshold=True, why_here="основа",
                           unit_ids=["p038.19", "p038.20", "p999.99"], terms_introduced=["пьезопроводность"]),
                s.PlanNode(slug="gallery_erfc", title="Пуск галереи", title_novice="Фронт давления",
                           difficulty_primary="М", threshold=False, why_here="после уравнения",
                           unit_ids=[f"p040.{i:02d}" for i in range(1, 16)], prerequisites=["Piezo Equation"]),
            ], uncovered=[s.Uncovered(unit_id=f"p038.{i:02d}", reason="конец § 3 — вне главы") for i in range(1, 19)])
        if prompt == "core/structure_missing":
            missing = [l.split("|")[0].strip("[ ") for l in vars["units"].splitlines() if l.startswith("[")]
            items = []
            for u in missing:
                if u == "p038.21":
                    items.append(s.Assignment(unit_id=u, node=None, reason="сноска со ссылками на литературу"))
                elif u == "p039.11" and calls.count(prompt) == 1:
                    continue                                    # пропустит в первый раз
                else:
                    items.append(s.Assignment(unit_id=u, node="piezo_equation"))
            return s.Assignments(items=items)
        if prompt == "core/structure_node":
            if "piezo_equation" in vars["node_id"]:
                return draft([
                    s.ClaimDraft(text="совпадает с теплопроводностью", kind="observation", page_pdf=39,
                                 quote="по форме совпадающим с классическим уравнением теплопроводности", source_kind="text"),
                    s.ClaimDraft(text="плоскопараллельное", kind="assumption", page_pdf=39,
                                 quote="толщина пласта много МЕНЬШЕ его горизонтальной   протяженности", source_kind="text"),
                    s.ClaimDraft(text="неверная цитата", kind="observation", page_pdf=39,
                                 quote="этой фразы нет в книге совсем", source_kind="text"),
                ], links=[m.Link(type="refutes_misconception", target="misc.pressure_sound_speed")])
            return draft([
                s.ClaimDraft(text="стационарно", kind="observation", page_pdf=39,   # страница неверная
                             quote="Наиболее интересны случаи, для которых в начальный момент", source_kind="text"),
                s.ClaimDraft(text="выдумка", kind="inference", page_pdf=40, quote="выдуманная цитата модели", source_kind="text"),
            ], links=[m.Link(type="prerequisite", target="piezo_equation"),
                      m.Link(type="prerequisite", target="no_such_node"),
                      m.Link(type="to_data", target="data.pressure_transient")])
        if prompt == "core/quote_fix":
            if "неверная цитата" in vars["claim"]:
                return s.QuoteFix(found=True, page_pdf=39,
                                  quote="Часто в модельных задачах задается мгновенное изменение давления")
            return s.QuoteFix(found=False)
        raise AssertionError(prompt)

    monkeypatch.setattr(build, "complete_json", fake)
    return calls


def test_build_layer_and_coverage(fake_llm):
    cu = io.load(m.ChapterUnits, MINI / "units.json")
    md = (MINI / "chapter.md").read_text(encoding="utf-8")
    ctx = build.Context(difficulty_types="Ф — Формализм и модель", viewers="цифровики",
                        example_node="{}", misconceptions=MISC, known_terms="нет")
    layer, cov = build.build(cu, md, ctx)

    sch = lambda n: json.loads((paths.SCHEMAS / n).read_text(encoding="utf-8"))  # noqa: E731
    jsonschema.validate(json.loads(layer.model_dump_json(by_alias=True)), sch("node.schema.json"))
    jsonschema.validate(json.loads(cov.model_dump_json(by_alias=True)), sch("coverage.schema.json"))

    n1, n2 = layer.nodes
    assert n1.id == "barenblatt_mini.piezo_equation" and n2.id == "barenblatt_mini.gallery_erfc"
    assert [n.order for n in layer.nodes] == [1, 2]
    assert n1.why_here.by_model and n1.layers.main.by_model and n1.it_analogy.by_model   # честная пометка
    assert set(n1.unit_ids) >= {f"p039.{i:02d}" for i in range(1, 12)}                     # дозапрос покрытия, 2 круга
    assert "p999.99" not in n1.unit_ids
    assert n1.pages == [38, 39]

    c = {x.text: x for x in n1.claims}
    assert c["совпадает с теплопроводностью"].by_model is False
    assert c["плоскопараллельное"].ext["core"]["quote_verified"] is True                    # пробелы и регистр не важны
    fixed = c["неверная цитата"]
    assert fixed.quote.startswith("Часто в модельных") and fixed.by_model is False
    assert [x.id for x in n1.claims] == [f"{n1.id}#c{i}" for i in (1, 2, 3)]
    assert n1.misconception.ref is None and n1.ext["core"]["dropped"]                       # неизвестный misc — не молча

    c2 = {x.text: x for x in n2.claims}
    assert c2["стационарно"].page_pdf == 40                                                 # страница поправлена кодом
    bad = c2["выдумка"]
    assert bad.by_model is True and bad.ext["core"]["quote_verified"] is False
    assert [(l.type, l.target) for l in n2.links] == [("prerequisite", n1.id), ("to_data", "data.pressure_transient")]

    rows = {r.unit_id: r for r in cov.rows}
    assert list(rows) == [u.unit_id for u in cu.units]                                      # каждая единица ровно раз
    assert rows["p038.21"].reason.startswith("сноска") and rows["p038.21"].node_ids == []
    assert rows["p038.05"].reason and rows["p040.03"].node_ids == [n2.id]
    assert all(r.node_ids or r.reason for r in cov.rows)
    assert 5 <= len(rows["p040.03"].excerpt.split()) <= 15
    assert fake_llm.count("core/structure_missing") == 2


def test_run_writes_outputs(fake_llm, tmp_path, monkeypatch):
    from pipeline.common import config, domain
    from pipeline.structure import run

    monkeypatch.setenv("OUT_DIR", str(tmp_path))
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "misconceptions.json").write_text(json.dumps(MISC, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(domain, "load", lambda name: domain.Domain(name=name, path=pack))
    spec = config.resolve(md=str(MINI / "chapter.md"), ch="barenblatt_mini")
    (tmp_path / "barenblatt_mini").mkdir()
    (tmp_path / "barenblatt_mini" / "units.json").write_text((MINI / "units.json").read_text(encoding="utf-8"),
                                                             encoding="utf-8")
    ctx = run.context(spec)
    assert "Восемь типов трудности" in ctx.difficulty_types and "нет" in ctx.known_terms
    monkeypatch.setattr(run, "context", lambda spec: build.Context(
        difficulty_types="Ф — Формализм и модель", viewers="", example_node="{}", misconceptions=MISC, known_terms="нет"))
    run.run(spec)
    assert io.load(m.Layer, tmp_path / "barenblatt_mini" / "layer.json").nodes
    assert io.load(m.Coverage, tmp_path / "barenblatt_mini" / "coverage.json").rows


def test_missing_domain_pack_is_loud(tmp_path, monkeypatch):
    from pipeline.common import domain
    monkeypatch.setattr(domain.paths, "DOMAIN", tmp_path)
    domain.load.cache_clear()
    with pytest.raises(FileNotFoundError, match="domain.build"):
        domain.load("drilling")


def test_quote_search():
    pages = {39: "текст  страницы\nс переносом", 40: "другая"}
    assert quotes.find(pages, "ТЕКСТ страницы с переносом", 39) == 39
    assert quotes.find(pages, "другая", 39) == 40          # соседняя страница
    assert quotes.find(pages, "нет", 39) is None
    # разметка md — не текст: **термин** цитируют без звёздочек
    assert quotes.find({30: "Фациальная ассоциация** включает _те_ фации"}, "Фациальная ассоциация включает те фации", 30) == 30
    # цитата через границу страниц: начинается на 40, кончается на 41
    split = {40: "представляющим фацию", 41: "пляжа. Дальше"}
    assert quotes.find(split, "представляющим фацию пляжа.", 40) == 40
    assert quotes.find(split, "фацию пляжа. Дальше", 41) == 40      # начало — на 40
    # склейка единиц ingest: колонтитул между страницами уже убран
    pages_from_units = quotes.unit_pages([m.Unit(unit_id="p040.01", kind="paragraph", page_pdf=40,
                                                 text="фацию пляжа")])
    assert quotes.find(pages_from_units, "фацию пляжа", 40) == 40
