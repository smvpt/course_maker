import copy
import json
from pathlib import Path

import jsonschema

from contracts.models import ChapterUnits, Coverage, Layer, Script, Tasks
from pipeline.verify import run as vrun
from pipeline.verify.terms import check_terms

ROOT = Path(__file__).resolve().parents[2]
MD = ROOT / "fixtures/verify/mini_chapter.md"
ORG_NODE = json.loads((ROOT / "fixtures/core/example_layer_organizers.json").read_text(encoding="utf-8"))["nodes"][0]
SCHEMA = json.loads((ROOT / "data/organizers/02_модуль_проверки/review_output.schema.json").read_text(encoding="utf-8"))

Q1 = "Пористость песчаника обычно составляет 15–25 %"
Q2 = "Глинистость снижает проницаемость коллектора"
Q3 = "При глинистости выше 30 % пласт перестает быть коллектором"


def _node(nid, order, claims, main="Текст узла.", terms=(), unit_ids=(), pages=(1,)):
    n = copy.deepcopy(ORG_NODE)
    n.update(id=nid, order=order, title=f"Узел {nid}", terms_introduced=list(terms),
             unit_ids=list(unit_ids), pages=list(pages))
    n["layers"]["main"]["text"] = main
    n["claims"] = [dict(id=f"{nid}#c{i + 1}", text="Пересказ.", kind="observation", page_pdf=p,
                        quote=q, source_kind="text", by_model=False) for i, (p, q) in enumerate(claims)]
    return n


def _units(ch):
    return ChapterUnits(chapter=ch, source=str(MD), pdf_pages=[1, 2, 3], units=[
        dict(unit_id="p001.01", kind="paragraph", page_pdf=1,
             text="Пористость песчаника обычно составляет 15–25 %. Количественная интерпретация требует "
                  "привлечения геологических сведений о характере разреза."),
        dict(unit_id="p002.01", kind="paragraph", page_pdf=2,
             text="Глинистость снижает проницаемость коллектора. При глинистости выше 30 % пласт "
                  "перестает быть коллектором."),
    ])


def _write(out, ch, nodes, tasks=None, script=None):
    out.mkdir(parents=True, exist_ok=True)
    cov = Coverage(chapter=ch, rows=[
        dict(unit_id="p001.01", kind="paragraph", page_pdf=1, excerpt="Пористость песчаника", node_ids=[nodes[0]["id"]]),
        dict(unit_id="p002.01", kind="paragraph", page_pdf=2, excerpt="Глинистость", node_ids=[nodes[-1]["id"]]),
        dict(unit_id="p003.01", kind="paragraph", page_pdf=3, excerpt="Характерное время", node_ids=[],
             reason="за рамками главы"),
    ])
    (out / "coverage.json").write_text(cov.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    (out / "units.json").write_text(_units(ch).model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    layer = Layer.model_validate(dict(chapter=ch, source=str(MD), nodes=nodes))
    (out / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    if tasks:
        (out / "course").mkdir(exist_ok=True)
        (out / "course/tasks.json").write_text(Tasks.model_validate(tasks).model_dump_json(by_alias=True),
                                               encoding="utf-8")
    if script:
        d = out / "videos" / script["video_id"]
        d.mkdir(parents=True)
        (d / "script.json").write_text(Script.model_validate(script).model_dump_json(by_alias=True),
                                       encoding="utf-8")


def _clean_nodes():
    return [
        _node("mini.porosity", 1, [(1, Q1)], main="Пористость песчаника 15–25 %.", unit_ids=["p001.01"]),
        _node("mini.clay", 2, [(2, Q2), (2, Q3)], main="Проницаемость падает, выше 30 % — не коллектор.",
              terms=["проницаемость"], unit_ids=["p002.01"], pages=[2]),
    ]


def test_clean_chapter_no_remarks(tmp_path):
    out = tmp_path / "mini"
    _write(out, "mini", _clean_nodes())
    report, code = vrun.run("mini", out, journal_root=tmp_path)
    assert report.remarks == [] and code == 0
    trust = json.loads((out / "verify/trust.json").read_text(encoding="utf-8"))
    assert trust["coverage"] == {"units": 3, "in_nodes": 2, "with_reason": 1, "pct_in_nodes": 66.7,
                                 "pct_accounted": 100.0}
    assert trust["quotes"]["pct"] == 100.0 and trust["numbers"]["pct"] == 100.0
    assert trust["remarks"] == {"critical": 0, "significant": 0, "minor": 0}
    assert trust["manual"]["person_minutes"] == 0
    saved = json.loads((out / "verify/report.json").read_text(encoding="utf-8"))
    jsonschema.validate(saved, SCHEMA)
    assert saved["package_id"] == "mini"


def test_broken_chapter_remarks(tmp_path):
    nodes = [
        # проницаемость упомянута раньше узла, где объяснена; 40 % — из воздуха; цитата со стр. 2 указана как 1
        _node("mini.porosity", 1, [(1, Q1), (1, Q3)],
              main="Пористость 15–25 %, проницаемость важна, примерно 40 % пород.", unit_ids=["p001.01"]),
        # выдуманная цитата
        _node("mini.clay", 2, [(2, "Глинистые коллекторы всегда содержат больше нефти, чем чистые пески")],
              main="Проницаемость падает.", terms=["проницаемость"], unit_ids=["p002.01"], pages=[2]),
    ]
    tasks = dict(chapter="mini", tasks=[dict(id="t1", type="single", step_id="mini.clay",
                                             claim_ids=["mini.clay#c1"], prompt="Глинистость выше 35 % — это?",
                                             options=[dict(id="a", text="коллектор")], answer="a",
                                             explanation="Порог из главы.")])
    script = dict(video_id="v1", node_id="mini.clay", format="short", prediction_question="?",
                  transfer_question="?", data_it_bridge="-", phrases=[
                      dict(id="p1", text="При глинистости выше тридцати процентов коллектора нет.", beat="hook",
                           claim_id="mini.clay#c1"),
                      dict(id="p2", text="А в половине случаев — пятьдесят процентов.", beat="problem",
                           claim_id="mini.clay#c9"),
                  ])
    out = tmp_path / "mini"
    _write(out, "mini", nodes, tasks, script)
    metrics = tmp_path / "_metrics"
    metrics.mkdir()
    (metrics / "llm_calls.jsonl").write_text("\n".join(json.dumps(r) for r in [
        {"chapter": "mini", "cache_hit": False, "money_usd": 0.5, "tokens_in": 100, "tokens_out": 10},
        {"chapter": "mini", "cache_hit": True, "money_usd": 0.5, "tokens_in": 100, "tokens_out": 10},
        {"chapter": "other", "cache_hit": False, "money_usd": 9.0},
    ]), encoding="utf-8")
    report, code = vrun.run("mini", out, journal_root=tmp_path)
    trust = json.loads((out / "verify/trust.json").read_text(encoding="utf-8"))
    assert trust["quotes"] == {"claims": 3, "found": 1, "other_page": 1, "not_found": 1, "pct": 33.3}
    assert trust["numbers"]["found"] < trust["numbers"]["total"]
    assert trust["cost"]["money_usd"] == 0.5 and trust["cost"]["cached"] == 1 and trust["cost"]["llm_calls"] == 2
    assert trust["remarks"]["critical"] == 1
    by = {r.target: r for r in report.remarks}
    jsonschema.validate(json.loads((out / "verify/report.json").read_text(encoding="utf-8")), SCHEMA)

    assert code == 1
    assert by["mini.clay#c1"].severity == "critical"                       # цитаты нет в главе
    assert by["mini.porosity#c2"].page_pdf == 2                             # цитата с другой страницы
    assert "40" in by["mini.porosity"].problem                              # число из воздуха
    assert "проницаемость" in by["mini.porosity"].problem                   # термин раньше определения
    assert "35" in by["t1"].problem                                         # число в задании
    assert "50" in by["v1.p2"].problem and "mini.clay#c9" in by["v1.p2"].problem
    assert "v1.p1" not in by
    assert len(by) == len(report.remarks)                                   # одно замечание на цель
    assert all(r.fix.strip() for r in report.remarks)


def test_missing_layer_fails_loudly(tmp_path):
    import pytest
    with pytest.raises(FileNotFoundError):
        vrun.run("nope", tmp_path / "nope")


def test_terms_inflected_use_before_definition():
    layer = Layer.model_validate(dict(chapter="mini", source="x", nodes=[
        _node("a.one", 1, [(1, Q1)], main="Здесь зависит от проницаемости пласта."),
        _node("a.two", 2, [(2, Q2)], main="Определение.", terms=["проницаемость"]),
        _node("a.three", 3, [(2, Q2)], main="Проницаемостью управляют поры."),
    ]))
    hits = check_terms(layer)
    assert [(h.node_id, h.term, h.defined_in) for h in hits] == [("a.one", "проницаемость", "a.two")]
