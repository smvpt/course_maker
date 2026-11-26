"""metrics: llm_calls.jsonl + журнал правок → out/<ch>/metrics.csv по шаблону организаторов."""
import csv
import json

from contracts import models as m
from pipeline.common import metrics, paths

TEMPLATE = paths.ORGANIZERS / "05_шаблоны" / "metrics.csv"


def test_metrics_rows_by_stage(tmp_path, monkeypatch):
    monkeypatch.setenv("OUT_DIR", str(tmp_path))
    (tmp_path / "_metrics").mkdir()
    calls = [
        {"chapter": "ch", "prompt": "core/structure_node", "cache_hit": False, "tokens_in": 100, "tokens_out": 10, "money_usd": 0.5},
        {"chapter": "ch", "prompt": "core/structure_node", "cache_hit": True, "tokens_in": 100, "tokens_out": 10, "money_usd": 0.5},
        {"chapter": "ch", "prompt": "core/route", "cache_hit": False, "tokens_in": 7, "tokens_out": 3, "money_usd": None},
        {"chapter": "other", "prompt": "course/step_page", "cache_hit": False, "tokens_in": 1, "tokens_out": 1, "money_usd": 1},
    ]
    (tmp_path / "_metrics" / "llm_calls.jsonl").write_text("\n".join(json.dumps(c) for c in calls), encoding="utf-8")
    journal = tmp_path / "j.csv"
    journal.write_text("time,chapter,file,what_changed,person_minutes,people,run_no,reason,commit\n"
                       "t,ch,out/ch/layer.json,x,4,1,1,r,abc\n", encoding="utf-8")
    monkeypatch.setattr(metrics, "JOURNAL", journal)
    (tmp_path / "ch").mkdir()
    layer = json.loads((paths.ROOT / "fixtures/core/live_baraboshkin_par1-2/layer.json").read_text(encoding="utf-8"))
    (tmp_path / "ch" / "layer.json").write_text(json.dumps(layer), encoding="utf-8")

    rows = {r.stage: r for r in metrics.build("ch")}
    assert list(rows) == ["layer", "routing", "course", "video", "review"]
    assert rows["layer"].llm_tokens_in == 100 and rows["layer"].money_usd == 0.5      # попадание в кэш не считается
    assert rows["layer"].person_minutes == 4 and rows["layer"].nodes == 6
    assert rows["routing"].llm_tokens_out == 3 and rows["routing"].money_usd == 0.0
    assert rows["course"].llm_tokens_in == 0

    out = metrics.write("ch")
    with open(out, encoding="utf-8") as f, open(TEMPLATE, encoding="utf-8") as t:
        assert next(csv.reader(f)) == next(csv.reader(t))
    with open(out, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            m.MetricsRow.model_validate(r)
