"""Выходы конвейера проходят JSON-схемы организаторов (CLAUDE.md §1б).

1. Образец слоя организаторов проходит туда-обратно через модель и остаётся валидным.
2. Минимальные экземпляры каждой модели (необязательные поля не заданы) после
   model_dump_json(by_alias=True) валидны: ловит null там, где схема его не допускает.
3. Все fixtures/core/**/{layer,coverage,routing}.json валидны.
"""
import json
from pathlib import Path

import jsonschema
import pytest

from contracts import models as m

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "data" / "organizers" / "01_схемы"
REVIEW = ROOT / "data" / "organizers" / "02_модуль_проверки"


def schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(obj) -> dict:
    return json.loads(obj.model_dump_json(by_alias=True, indent=2))


def validate(obj, schema_path: Path) -> None:
    jsonschema.validate(dump(obj), schema(schema_path))


F = lambda t="x": m.Field_(text=t, by_model=True)  # noqa: E731


def minimal_node() -> m.Node:
    return m.Node(
        id="ch.node",
        order=1,
        title="t",
        why_here=F(),
        difficulty=m.DifficultyPair(primary="Ф"),
        threshold=False,
        layers=m.Layers(topic=F(), main=F(), mechanism=F(), practice=F(), nuances=F()),
        claims=[m.Claim(id="ch.node#c1", text="t", kind="observation", page_pdf=1,
                        quote="дословная цитата", source_kind="text", by_model=False)],
        links=[m.Link(type="prerequisite", target="ch.other")],
        misconception=m.Misconception(text="t", by_model=True),
        data_meaning=m.DataMeaning(from_chapter=F(), breaks=F(), hypotheses=[F()]),
        it_analogy=m.ItAnalogy(text="t", breaks_where="t", by_model=True),
        now_practice=F(),
        inefficiency_lens=m.InefficiencyLens(inputs="a", manual_steps="b", judgment_points="c",
                                             time="d", typical_errors="e", by_model=True),
        terms_introduced=["t"],
        needs_scan=[m.NeedsScan(page=1, what="рис. 1")],
        decision_on_data=m.DecisionOnData(features=["f"], rule="r", conclusion="c"),
        worked_examples=[m.WorkedExample(page_pdf=1, condition="c", steps=["s"], result="r")],
        book_tasks=[m.BookTask(number="1", page_pdf=1, text="t")],
        pages=[1],
    )


CASES = {
    "layer": (lambda: m.Layer(chapter="ch", source="ch.md", nodes=[minimal_node()]),
              SCHEMAS / "node.schema.json"),
    "coverage": (lambda: m.Coverage(chapter="ch", rows=[
        m.CoverageRow(unit_id="p001.01", kind="paragraph", page_pdf=1, excerpt="e", node_ids=["ch.node"]),
        m.CoverageRow(unit_id="p001.02", kind="heading", page_pdf=1, excerpt="e", node_ids=[], reason="колонтитул"),
    ]), SCHEMAS / "coverage.schema.json"),
    "routing": (lambda: m.Routing(chapter="ch", routes=[m.Route(
        node_id="ch.node", format="шортс",
        video_scores=m.VideoScores(time=2, invisible=1, scale=0, counterintuitive=1, cause_effect=2),
        why="w")]), SCHEMAS / "routing.schema.json"),
    "tasks": (lambda: m.Tasks(chapter="ch", tasks=[m.Task(
        id="t1", type="single", step_id="ch.node", claim_ids=["ch.node#c1"], prompt="p",
        options=[m.TaskOption(id="a", text="a")], answer="a", explanation="e")]),
              SCHEMAS / "task.schema.json"),
    "illustrations": (lambda: m.Illustrations(chapter="ch", illustrations=[m.Illustration(
        id="i1", step_id="ch.node", file="i1.svg", frame_class="A", origin="code_from_data",
        caption="c", alt="a")]), SCHEMAS / "illustration.schema.json"),
    "passport": (lambda: m.Passport(
        video_id="v", node_id="ch.node", node_card={}, script=[m.ScriptLine(t_start=0, t_end=1, text="t")],
        sources=[m.SourceRow(claim_id="ch.node#c1", page_or_dataset="стр. 1")], scene_spec="s.json",
        frames=[m.PassportFrame(t=0, class_="A", label="схема")], exaggerations=[],
        prediction_question="q", transfer_question="q", data_it_bridge="b",
        physics_checklist=[m.ChecklistAnswer(item="pc.x", answer="да")], audio_check={}),
                 SCHEMAS / "passport.schema.json"),
    "review_output": (lambda: m.ReviewOutput(package_id="p", remarks=[m.Remark(
        target="C001", category="other", severity="minor", problem="p", fix="f", page_pdf=None)]),
                      REVIEW / "review_output.schema.json"),
}


@pytest.mark.parametrize("name", CASES)
def test_minimal_instances_pass_schema(name):
    build, path = CASES[name]
    validate(build(), path)


def test_organizers_example_roundtrip():
    raw = schema(SCHEMAS / "example_layer.json")
    jsonschema.validate(raw, schema(SCHEMAS / "node.schema.json"))
    layer = m.Layer.model_validate(raw)
    validate(layer, SCHEMAS / "node.schema.json")


FIXTURE_SCHEMAS = {"layer.json": "node.schema.json", "coverage.json": "coverage.schema.json",
                   "routing.json": "routing.schema.json"}
FIXTURE_MODELS = {"layer.json": m.Layer, "coverage.json": m.Coverage, "routing.json": m.Routing}
FIXTURES = sorted(p for p in (ROOT / "fixtures" / "core").rglob("*.json") if p.name in FIXTURE_SCHEMAS)


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: str(p.relative_to(ROOT)))
def test_core_fixtures_pass_schema(path):
    raw = json.loads(path.read_text(encoding="utf-8"))
    sch = schema(SCHEMAS / FIXTURE_SCHEMAS[path.name])
    jsonschema.validate(raw, sch)
    validate(FIXTURE_MODELS[path.name].model_validate(raw), SCHEMAS / FIXTURE_SCHEMAS[path.name])
