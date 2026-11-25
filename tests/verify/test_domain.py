import json
import re
import sys
import types
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
GEO = ROOT / "domain/geology"
ORG = ROOT / "data/organizers"
PACK_FILES = ["glossary.md", "misconceptions.json", "physics_checklist.json", "it_bridges.md", "styleguide.json",
              "pronunciation.md", "stress_dictionary.md"]


def test_geology_pack_complete():
    for f in PACK_FILES:
        assert (GEO / f).exists(), f
    assert (GEO / "errata").is_dir()


def test_geology_pack_keeps_organizers_ids():
    misc = json.loads((GEO / "misconceptions.json").read_text(encoding="utf-8"))
    pc = json.loads((GEO / "physics_checklist.json").read_text(encoding="utf-8"))
    org_misc = json.loads((ORG / "04_доменные_заготовки/misconceptions.json").read_text(encoding="utf-8"))
    org_pc = json.loads((ORG / "04_доменные_заготовки/physics_checklist.json").read_text(encoding="utf-8"))
    assert {m["id"] for m in org_misc} <= {m["id"] for m in misc}
    assert {p["id"] for p in org_pc} <= {p["id"] for p in pc}
    assert all(re.fullmatch(r"misc\.[a-z0-9_]+", m["id"]) for m in misc)
    assert len({m["id"] for m in misc}) == len(misc)
    assert json.loads((GEO / "styleguide.json").read_text(encoding="utf-8")) == \
        json.loads((ORG / "03_стайлгайд/styleguide.json").read_text(encoding="utf-8"))


ANSWERS = {
    "verify/domain_glossary": {
        "glossary": [{"term": "превентор", "en": "blowout preventer", "definition": "Устройство герметизации устья.",
                      "western": "BOP"}],
        "pronunciation": [{"written": "ПВО", "spoken": "пэ вэ о", "expansion": "противовыбросовое оборудование"}],
        "stress": [{"word": "превентор", "stressed": "превéнтор"}]},
    "verify/domain_misconceptions": {"items": [{"id": "misc.kick_constant", "text": "Газ не меняет давление."}]},
    "verify/domain_checklist": {"items": [{"id": "pc.depth_down", "group": "Кадры", "item": "Глубина вниз."},
                                          {"id": "pc.hydrostatic", "group": "Скважина", "item": "p = ρgh."}]},
    "verify/domain_it_bridges": {"items": [{"concept": "Глушение скважины", "analogy": "Откат транзакции",
                                            "breaks_where": "Физический процесс с задержкой."}]},
}


@pytest.fixture
def fake_llm(monkeypatch):
    calls = []

    def complete_json(prompt, vars, schema, tier="default", images=None):
        calls.append((prompt, vars))
        return schema.model_validate(ANSWERS[prompt])

    monkeypatch.setitem(sys.modules, "pipeline.llm", types.SimpleNamespace(complete_json=complete_json))
    return calls


def test_build_new_domain(tmp_path, fake_llm):
    from domain import build
    md = ROOT / "fixtures/verify/mini_chapter.md"
    dst = build.build("drilling", tmp_path / "drilling", md=md, pages=[1, 2], base=GEO)
    for f in PACK_FILES:
        assert (dst / f).exists(), f
    assert (dst / "errata").is_dir() and not (dst / "templates").exists()     # templates — зона П4
    assert "превентор" in (dst / "glossary.md").read_text(encoding="utf-8")
    assert "превéнтор" in (dst / "stress_dictionary.md").read_text(encoding="utf-8")
    assert "пэ вэ о" in (dst / "pronunciation.md").read_text(encoding="utf-8")
    assert json.loads((dst / "misconceptions.json").read_text(encoding="utf-8"))[0]["id"] == "misc.kick_constant"
    assert "Откат транзакции" in (dst / "it_bridges.md").read_text(encoding="utf-8")
    log = json.loads((dst / "build_log.json").read_text(encoding="utf-8"))
    assert log["domain"] == "drilling" and log["seconds"] >= 0 and log["llm_calls"] == 4
    # глава уходит в промпт со страницами, а пример — из базового пакета
    prompts = {p: v for p, v in fake_llm}
    assert "<!-- page 2 -->" in prompts["verify/domain_glossary"]["chapter"]
    assert "<!-- page 3 -->" not in prompts["verify/domain_glossary"]["chapter"]
    assert "pc.depth_down" in prompts["verify/domain_checklist"]["example"]


def test_build_refuses_overwrite(tmp_path, fake_llm):
    from domain import build
    (tmp_path / "geology").mkdir()
    with pytest.raises(FileExistsError):
        build.build("geology", tmp_path / "geology", md=ROOT / "fixtures/verify/mini_chapter.md", base=GEO)


def test_build_rejects_bad_ids(tmp_path, monkeypatch):
    from domain import build

    def complete_json(prompt, vars, schema, tier="default", images=None):
        a = dict(ANSWERS[prompt])
        if prompt == "verify/domain_misconceptions":
            a = {"items": [{"id": "kick", "text": "x"}]}
        return schema.model_validate(a)

    monkeypatch.setitem(sys.modules, "pipeline.llm", types.SimpleNamespace(complete_json=complete_json))
    with pytest.raises(Exception):
        build.build("drilling", tmp_path / "d", md=ROOT / "fixtures/verify/mini_chapter.md", base=GEO)


def test_domain_prompt_vars():
    rx = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")
    for name in ("domain_glossary", "domain_misconceptions", "domain_checklist", "domain_it_bridges"):
        text = (ROOT / f"prompts/verify/{name}.md").read_text(encoding="utf-8")
        assert set(rx.findall(text)) == {"domain", "chapter", "example"}, name
