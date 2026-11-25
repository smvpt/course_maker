import json
import sys
import types
from pathlib import Path

import jsonschema
import pytest

from pipeline.verify import external

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((ROOT / "data/organizers/02_модуль_проверки/review_output.schema.json").read_text(encoding="utf-8"))
PKG_SCHEMA = json.loads((ROOT / "data/organizers/02_модуль_проверки/review_package.schema.json")
                        .read_text(encoding="utf-8"))
MD = ROOT / "fixtures/verify/mini_chapter.md"

Q1 = "Пористость песчаника обычно составляет 15–25 %"
Q3 = "При глинистости выше 30 % пласт перестает быть коллектором"


def _pkg(tmp_path):
    (tmp_path / "mini_chapter.md").write_text(MD.read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "frames").mkdir()
    (tmp_path / "frames/F01.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    pkg = {
        "package_id": "mini_pkg", "chapter": "mini", "chapter_file": "mini_chapter.md", "language": "ru",
        "items": [
            {"id": "C001", "type": "claim", "node_id": "mini.por", "text": "Пористость песчаника 15–25 %.",
             "kind": "observation", "page_pdf": 1, "quote": Q1},
            {"id": "C002", "type": "claim", "node_id": "mini.clay", "text": "Глина не влияет на коллектор.",
             "kind": "observation", "page_pdf": 2, "quote": Q3},
            {"id": "C003", "type": "claim", "node_id": "mini.clay", "text": "Коллектор при любой глинистости.",
             "kind": "observation", "page_pdf": 2, "quote": Q3},
            {"id": "A01", "type": "analogy", "node_id": "mini.clay", "text": "Порог как в классификаторе.",
             "breaks_where": "Нигде не ломается."},
            {"id": "L01", "type": "script_line", "node_id": "mini.clay", "text": "Выше 30 % глины коллектора нет.",
             "video_id": "v1", "t_start": 0.0, "t_end": 3.0, "claim_ref": "C002"},
            {"id": "S01", "type": "scene_fact", "node_id": "mini.clay", "text": "Глубина растёт вверх.",
             "video_id": "v1", "spec_path": "params.depth_axis"},
        ],
        "scenes": [{"video_id": "v1", "spec": {"video_id": "v1", "node_id": "mini.clay",
                                               "params": {"depth_axis": "up"}}}],
        "frames": [{"id": "F01", "video_id": "v1", "file": "frames/F01.png", "t": 1.0, "frame_class": "B",
                    "label": "симуляция", "shows": "разрез, газ под нефтью", "plaque": None}],
    }
    jsonschema.validate(pkg, PKG_SCHEMA)
    p = tmp_path / "package.json"
    p.write_text(json.dumps(pkg, ensure_ascii=False), encoding="utf-8")
    return p


SUPPORTED = {"verdict": "supported"}
VERDICTS = {
    "C001": SUPPORTED,
    # противоречит, цитата найдена на стр. 2 → замечание
    "C002": {"verdict": "contradicted", "category": "sign_flip", "severity": "critical",
             "problem": "глина как раз снижает проницаемость", "fix": "Глинистость снижает проницаемость.",
             "page_pdf": 2, "quote": "Глинистость снижает проницаемость коллектора"},
    # противоречит, но цитата выдумана → без доказательства, замечания нет
    "C003": {"verdict": "contradicted", "category": "overgeneralization", "severity": "significant",
             "problem": "x", "fix": "y", "page_pdf": 2, "quote": "При любой глинистости пласт остаётся коллектором всегда"},
    # аналогия: цитата не обязательна, страница — из утверждений узла
    "A01": {"verdict": "contradicted", "category": "analogy_without_limit", "severity": "minor",
            "problem": "граница не названа", "fix": "назвать, где ломается", "page_pdf": 7, "quote": None},
    # фраза ссылается на C002; противоречия нет
    "L01": SUPPORTED,
    "S01": {"verdict": "contradicted", "category": "frame_error", "severity": "critical",
            "problem": "глубина вверх", "fix": "глубина растёт вниз", "page_pdf": 2, "quote": None},
    "F01": {"verdict": "contradicted", "category": "frame_error", "severity": "critical",
            "problem": "газ под нефтью", "fix": "газ над нефтью", "page_pdf": 2, "quote": None},
}


@pytest.fixture
def fake_llm(monkeypatch):
    calls = []

    def complete_json(prompt, vars, schema, tier="default", images=None):
        target = json.loads(vars["item"])["id"]
        calls.append(dict(prompt=prompt, target=target, tier=tier, images=images, vars=vars))
        return schema.model_validate(VERDICTS[target])

    monkeypatch.setitem(sys.modules, "pipeline.llm", types.SimpleNamespace(complete_json=complete_json))
    return calls


def test_external_review(tmp_path, fake_llm):
    out = tmp_path / "answer.json"
    review = external.review(_pkg(tmp_path), out, team="t", workers=2)
    saved = json.loads(out.read_text(encoding="utf-8"))
    jsonschema.validate(saved, SCHEMA)
    by = {r["target"]: r for r in saved["remarks"]}

    assert set(by) == {"C002", "A01", "S01", "F01"}
    assert by["C002"]["page_pdf"] == 2 and by["C002"]["category"] == "sign_flip"
    assert by["A01"]["page_pdf"] == 2            # стр. 7 нет среди утверждений узла → страница узла
    assert by["F01"]["page_pdf"] == 2
    assert all(r["fix"].strip() for r in saved["remarks"])
    assert saved["package_id"] == "mini_pkg" and saved["team"] == "t"
    assert [r["target"] for r in saved["remarks"]] == ["C002", "A01", "S01", "F01"]   # порядок пакета
    assert review.ext["verify"]["unproven"] == ["C003"]

    calls = {c["target"]: c for c in fake_llm}
    assert set(calls) == {"C001", "C002", "C003", "A01", "L01", "S01", "F01"}
    assert calls["F01"]["tier"] == "vision" and calls["F01"]["images"][0].name == "F01.png"
    assert calls["C002"]["tier"] == "strong" and "<!-- page 2 -->" in calls["C002"]["vars"]["context"]
    assert Q3[:20] in calls["L01"]["vars"]["related"]                   # фраза видит своё утверждение
    assert "depth_axis" in calls["S01"]["vars"]["related"]               # факт сцены видит спецификацию


def test_external_bad_package_fails(tmp_path):
    p = tmp_path / "package.json"
    p.write_text(json.dumps({"package_id": "x"}), encoding="utf-8")
    with pytest.raises(Exception):
        external.review(p, tmp_path / "a.json")


def test_verdict_contradicted_requires_fix():
    from pipeline.verify.critic import Verdict
    with pytest.raises(Exception):
        Verdict.model_validate({"verdict": "contradicted", "category": "other", "severity": "minor",
                                "problem": "p", "fix": " "})


def test_prompt_vars_match_code():
    import re
    rx = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")
    code_vars = {"item_type", "item", "context", "related", "checklist"}
    for name in ("critic", "critic_frame"):
        text = (ROOT / f"prompts/verify/{name}.md").read_text(encoding="utf-8")
        assert set(rx.findall(text)) == code_vars, name
    text = (ROOT / "prompts/verify/scene_physics.md").read_text(encoding="utf-8")
    assert set(rx.findall(text)) == {"checklist", "scene_spec", "script"}
