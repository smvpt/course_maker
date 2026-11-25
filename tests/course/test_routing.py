"""routing.json с неизвестным шаблоном, форматом или битым содержимым: предупреждение и запись в отчёт, а не молчание и не падение."""
import json
from pathlib import Path

import pytest

from contracts.models import Layer
from pipeline.course import interactive as I
from pipeline.course.build import build, load_routes

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "fixtures/course/mini_layer.json"
RES, PORO = "mini.resistivity_depends_on_fluid", "mini.porosity_basics"
SCORES = {"time": 1, "invisible": 1, "scale": 1, "counterintuitive": 1, "cause_effect": 1}


def _route(nid, fmt="длинное видео", **kw):
    return {"node_id": nid, "format": fmt, "video_scores": SCORES, "why": "тест", **kw}


def _write(tmp_path, routes=None, raw=None) -> Path:
    layer = Layer.model_validate_json(MINI.read_text(encoding="utf-8"))
    d = tmp_path / "out" / layer.chapter
    d.mkdir(parents=True)
    (d / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    (d / "routing.json").write_text(raw if raw is not None else json.dumps({"chapter": "mini_test", "routes": routes}, ensure_ascii=False), encoding="utf-8")
    return tmp_path / "out"


def _build(tmp_path, **kw):
    out = _write(tmp_path, **kw)
    return build("mini_test", out_root=out, pages_dir=tmp_path / "pages")


def _codes(course, prefix="routing_"):
    rep = json.loads((course / "build_report.json").read_text(encoding="utf-8"))
    return [w for w in rep["warnings"] if w["code"].startswith(prefix)]


def test_valid_routing_gives_no_warnings(tmp_path, capsys):
    course = _build(tmp_path, routes=[_route(RES, template="T2"), _route(PORO, "текст", secondary_format="карточки")])
    assert _codes(course) == [] and "WARNING" not in capsys.readouterr().err


def test_unknown_template_warns_and_is_ignored(tmp_path, capsys):
    path = _write(tmp_path, routes=[_route(RES, template="T9"), _route(PORO, template="T4")])
    routes, problems, usable = load_routes(path / "mini_test/routing.json")
    assert usable and routes[RES].template is None and routes[PORO].template == "T4"      # шаблон не из T1–T4 отброшен, маршрут остался
    assert [p["code"] for p in problems] == ["routing_unknown_template"] and problems[0]["node"] == RES and "T9" in problems[0]["message"]
    course = build("mini_test", out_root=path, pages_dir=tmp_path / "pages")
    w = _codes(course)
    assert [x["code"] for x in w] == ["routing_unknown_template"] and "WARNING" in capsys.readouterr().err
    plan, _ = I.plan(Layer.model_validate_json(MINI.read_text(encoding="utf-8")).nodes, routes, True, lambda nid: False)
    assert plan[RES] == "distribution"                                                    # шаблон выбран по типу трудности узла (Ф)


def test_unknown_format_skips_the_route_with_warning(tmp_path):
    path = _write(tmp_path, routes=[_route(RES, "комикс"), _route(PORO, "шортс")])
    routes, problems, usable = load_routes(path / "mini_test/routing.json")
    assert usable and set(routes) == {PORO}
    assert problems[0]["code"] == "routing_unknown_format" and problems[0]["node"] == RES and "комикс" in problems[0]["message"]
    assert [x["code"] for x in _codes(build("mini_test", out_root=path, pages_dir=tmp_path / "pages"))] == ["routing_unknown_format"]


def test_unknown_secondary_format_is_dropped_with_warning(tmp_path):
    path = _write(tmp_path, routes=[_route(RES, "шортс", secondary_format="подкаст")])
    routes, problems, _ = load_routes(path / "mini_test/routing.json")
    assert routes[RES].format == "шортс" and routes[RES].secondary_format is None
    assert problems[0]["code"] == "routing_unknown_format" and "подкаст" in problems[0]["message"]


def test_route_missing_required_fields_is_skipped_with_warning(tmp_path):
    path = _write(tmp_path, routes=[{"node_id": RES, "format": "шортс"}, _route(PORO)])
    routes, problems, _ = load_routes(path / "mini_test/routing.json")
    assert set(routes) == {PORO} and problems[0]["code"] == "routing_invalid_route" and problems[0]["node"] == RES


def test_unreadable_routing_is_treated_as_missing_with_warning(tmp_path, capsys):
    out = _write(tmp_path, raw="{ это не json")
    routes, problems, usable = load_routes(out / "mini_test/routing.json")
    assert routes == {} and not usable and problems[0]["code"] == "routing_unreadable"
    course = build("mini_test", out_root=out, pages_dir=tmp_path / "pages")
    assert [x["code"] for x in _codes(course)] == ["routing_unreadable"] and "WARNING" in capsys.readouterr().err


def test_routes_not_a_list_is_a_warning_not_a_crash(tmp_path):
    out = _write(tmp_path, raw=json.dumps({"chapter": "mini_test", "routes": "нет"}))
    routes, problems, usable = load_routes(out / "mini_test/routing.json")
    assert routes == {} and problems[0]["code"] == "routing_unreadable"


def test_missing_routing_is_normal_and_quiet(tmp_path, capsys):
    layer = Layer.model_validate_json(MINI.read_text(encoding="utf-8"))
    d = tmp_path / "out" / layer.chapter
    d.mkdir(parents=True)
    (d / "layer.json").write_text(layer.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    course = build("mini_test", out_root=tmp_path / "out", pages_dir=tmp_path / "pages")
    assert _codes(course) == [] and "routing" not in capsys.readouterr().err
