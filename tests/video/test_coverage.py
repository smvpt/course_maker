"""video.coverage: покрытие видеоузлов шаблонами. Без LLM (готовые пары собираются подменённым генератором) и без рендера."""
import json
import sys
import types
from pathlib import Path

import pytest

from pipeline.video import coverage, spec

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "fixtures" / "video" / "spec"
CH = "video_spec_fixture"
T1_NODE = CH + ".pressure_t1"


def _answer(name, mutate=None):
    d = json.loads((FIX / name).read_text(encoding="utf-8"))
    if mutate:
        mutate(d)
    return d


def _make_t1_pair(tmp_path, monkeypatch):
    """Готовая пара T1 через существующий video.spec с подменённым LLM."""
    answers = {"video/script": [_answer("llm_script.json", lambda d: [p.update(claim_id=T1_NODE + "#c1")
                                                                       for p in d["phrases"]])],
               "video/scene_spec": [_answer("llm_scene_t1.json")]}
    mod = types.ModuleType("pipeline.llm")
    mod.complete_json = lambda prompt, vars, schema, tier="default", images=None: \
        schema.model_validate(answers[prompt].pop(0))
    monkeypatch.setitem(sys.modules, "pipeline.llm", mod)
    assert spec.main(["--ch", CH, "--node", T1_NODE, "--layer", str(FIX / "layer.json"), "--routing",
                      str(FIX / "routing.json"), "--out-root", str(tmp_path)]) == 0
    monkeypatch.setitem(sys.modules, "pipeline.llm", None)          # дальше LLM недоступен
    return tmp_path / CH / "videos" / f"{T1_NODE}.short"


def _run(tmp_path, routing=FIX / "routing.json", *extra):
    return coverage.main(["--ch", CH, "--layer", str(FIX / "layer.json"), "--routing", str(routing),
                          "--out-root", str(tmp_path), *extra])


def _report(tmp_path):
    return json.loads((tmp_path / CH / "videos" / "coverage.json").read_text(encoding="utf-8"))


def _row(rep, node):
    return next(r for r in rep["nodes"] if r["node_id"] == node)


@pytest.fixture
def no_llm(monkeypatch):
    monkeypatch.setitem(sys.modules, "pipeline.llm", None)


def test_statuses_on_fixture(tmp_path, monkeypatch, capsys):
    _make_t1_pair(tmp_path, monkeypatch)
    assert _run(tmp_path) == 0
    rep = _report(tmp_path)
    assert {r["node_id"] for r in rep["nodes"]} == {CH + ".mixed_section", CH + ".en_quote", T1_NODE,
                                                      CH + ".delta_t3", CH + ".well_t4"}   # text_only — не видео
    t1 = _row(rep, T1_NODE)
    assert t1["status"] == "поддерживается" and t1["pair"] == {"script": True, "scene_spec": True, "checks": "пройдены"}
    assert t1["template_implemented"] and t1["format_supported"] and "уравнение пьезопроводности" in t1["model"].lower()
    assert t1["limitations"]
    t3 = _row(rep, CH + ".delta_t3")
    assert t3["status"] == "спецификация ещё не создана" and t3["template_implemented"]   # шаблон есть, пары нет
    en = _row(rep, CH + ".en_quote")
    assert en["format_ru"] == "шортс" and en["format_source"] == "secondary_format"
    for r in rep["nodes"]:                                          # применимость физики маршрутом не подтверждается
        assert r["physical_applicability"]["status"] == "не проверено"
    assert rep["summary"]["поддерживается"] == 1 and rep["summary"]["спецификация ещё не создана"] == 4
    out = capsys.readouterr().out
    assert "поддерживается: 1" in out and "coverage.json" in out
    assert not (tmp_path / CH / "coverage.json").exists()           # выход P1 не трогается


def test_failed_pair_is_reported_with_reason(tmp_path, monkeypatch):
    d = _make_t1_pair(tmp_path, monkeypatch)
    s = json.loads((d / "script.json").read_text(encoding="utf-8"))
    s["phrases"][0]["claim_id"] = "other.chapter#c1"
    (d / "script.json").write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
    assert _run(tmp_path) == 0
    r = _row(_report(tmp_path), T1_NODE)
    assert r["status"] == "спецификация не прошла проверку" and r["pair"]["checks"] == "не пройдены"
    assert any("other.chapter#c1" in x for x in r["reasons"])


def test_incomplete_and_corrupt_pairs(tmp_path, monkeypatch):
    d = _make_t1_pair(tmp_path, monkeypatch)
    (d / "scene_spec.json").write_text("{", encoding="utf-8")
    assert _run(tmp_path) == 0
    assert _row(_report(tmp_path), T1_NODE)["status"] == "спецификация не прошла проверку"
    (d / "scene_spec.json").unlink()
    assert _run(tmp_path) == 0
    r = _row(_report(tmp_path), T1_NODE)
    assert r["status"] == "спецификация не прошла проверку" and any("неполная" in x for x in r["reasons"])


def _routing(tmp_path, mutate):
    r = json.loads((FIX / "routing.json").read_text(encoding="utf-8"))
    mutate(r["routes"])
    p = tmp_path / "routing.json"
    p.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    return p


def _set(node, **kw):
    return lambda routes: next(x for x in routes if x["node_id"] == node).update(**kw)


@pytest.mark.parametrize("mutate,status,needle", [
    (_set(T1_NODE, template=None), "нужен новый шаблон", "не указан"),
    (_set(T1_NODE, template="T7"), "нужен новый шаблон", "T7"),
    (_set(T1_NODE, format="длинное видео"), "формат не поддерживается", "long"),
])
def test_template_and_format_states(tmp_path, no_llm, mutate, status, needle):
    assert _run(tmp_path, _routing(tmp_path, mutate)) == 0
    r = _row(_report(tmp_path), T1_NODE)
    assert r["status"] == status and any(needle in x for x in r["reasons"])


def test_domain_without_template_descriptions_needs_new_template(tmp_path, no_llm):
    assert _run(tmp_path, FIX / "routing.json", "--domain", "no_templates_fixture") == 0
    r = _row(_report(tmp_path), T1_NODE)
    assert r["status"] == "нужен новый шаблон" and any("T1.json" in x for x in r["reasons"])


def test_route_problems_unknown_node_and_duplicates(tmp_path, no_llm):
    def mutate(routes):
        dup = dict(next(x for x in routes if x["node_id"] == T1_NODE))
        routes.append(dup)
        routes.append(dict(dup, node_id=CH + ".ghost"))
    assert _run(tmp_path, _routing(tmp_path, mutate)) == 0
    rep = _report(tmp_path)
    t1 = _row(rep, T1_NODE)
    assert t1["status"] == "ошибка маршрута" and any("2 маршрута" in x for x in t1["reasons"])
    ghost = _row(rep, CH + ".ghost")
    assert ghost["status"] == "ошибка маршрута" and any("нет в layer.json" in x for x in ghost["reasons"])


def test_chapter_mismatch_is_an_error(tmp_path, no_llm, capsys):
    assert coverage.main(["--ch", "other_chapter", "--layer", str(FIX / "layer.json"), "--routing",
                          str(FIX / "routing.json"), "--out-root", str(tmp_path)]) == 2
    assert "other_chapter" in capsys.readouterr().err
    assert not (tmp_path / "other_chapter").exists()


def test_missing_inputs_are_an_error(tmp_path, no_llm, capsys):
    assert coverage.main(["--ch", CH, "--out-root", str(tmp_path)]) == 2
    assert "layer.json" in capsys.readouterr().err


def test_damaged_param_sources_in_ready_pair_do_not_stop_the_report(tmp_path, monkeypatch):
    d = _make_t1_pair(tmp_path, monkeypatch)
    spec_d = json.loads((d / "scene_spec.json").read_text(encoding="utf-8"))
    spec_d["ext"]["video"]["param_sources"]["kappa_m2_s"]["numbers"] = 0.5            # число вместо списка
    (d / "scene_spec.json").write_text(json.dumps(spec_d, ensure_ascii=False), encoding="utf-8")
    assert _run(tmp_path) == 0
    rep = _report(tmp_path)
    r = _row(rep, T1_NODE)
    assert r["status"] == "спецификация не прошла проверку" and any("numbers" in x for x in r["reasons"])
    assert len(rep["nodes"]) == 5                                                     # остальные узлы в отчёте


def test_unexpected_check_failure_is_reported_per_node(tmp_path, monkeypatch, no_llm):
    from pipeline.video import build

    def boom(*a, **k):
        raise TypeError("сломанная проверка")
    monkeypatch.setattr(build, "_check_ready_pair", boom)
    d = tmp_path / CH / "videos" / f"{T1_NODE}.short"
    d.mkdir(parents=True)
    (d / "script.json").write_text("{}", encoding="utf-8")
    (d / "scene_spec.json").write_text("{}", encoding="utf-8")
    assert _run(tmp_path) == 0
    rep = _report(tmp_path)
    r = _row(rep, T1_NODE)
    assert r["status"] == "спецификация не прошла проверку"
    assert any("проверка упала" in x and "TypeError" in x for x in r["reasons"])
    assert len(rep["nodes"]) == 5
