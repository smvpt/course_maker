"""route: layer → routing.json. LLM подменён."""
import json

import jsonschema
import pytest

from contracts import models as m
from pipeline.common import io, paths
from pipeline.route import build

MINI = paths.ROOT / "fixtures" / "core" / "mini_chapter"


def scores(*v):
    return m.VideoScores(time=v[0], invisible=v[1], scale=v[2], counterintuitive=v[3], cause_effect=v[4])


def make_layer(n_extra=0):
    layer = io.load(m.Layer, MINI / "layer.json")
    base = layer.nodes[1]
    for i in range(n_extra):
        x = base.model_copy(deep=True)
        x.id, x.order = f"{base.id}_{i}", base.order + i + 1
        layer.nodes.append(x)
    return layer


def test_route_rules(monkeypatch):
    layer = make_layer(n_extra=4)          # 6 узлов
    ids = [n.id for n in layer.nodes]
    calls = []

    def fake(prompt, vars, schema, tier="default", images=None):
        calls.append(vars["nodes"])
        assert "T4" in vars["templates"] and "Ф" in vars["difficulty_types"]
        routes = [
            build.RouteDraft(node_id=ids[0], format="длинное видео", video_scores=scores(2, 2, 1, 2, 2),
                             hook_short=True, template="T9", why="Ф: невидимое во времени"),     # шаблона нет → по типу
            build.RouteDraft(node_id=ids[1], format="текст", video_scores=scores(0, 0, 0, 0, 0),
                             hook_short=False, template="T1", why="справка"),                    # текст → без шаблона
        ] + [build.RouteDraft(node_id=i, format="шортс", video_scores=scores(1, 1, 1, 1, 1), hook_short=True,
                              template="T4", why="крючок") for i in ids[2:5]]
        if len(calls) == 1:
            return build.RouteDrafts(routes=routes + [build.RouteDraft(node_id="чужой", format="текст",
                                                                       video_scores=scores(0, 0, 0, 0, 0), why="x")])
        return build.RouteDrafts(routes=[build.RouteDraft(node_id=ids[5], format="карточки",
                                                          video_scores=scores(0, 0, 0, 0, 1), why="термины")])

    monkeypatch.setattr(build, "complete_json", fake)
    r = build.route(layer, difficulty_types="Ф — Формализм")
    jsonschema.validate(json.loads(r.model_dump_json(by_alias=True)),
                        json.loads((paths.SCHEMAS / "routing.schema.json").read_text(encoding="utf-8")))

    assert [x.node_id for x in r.routes] == ids                        # каждый узел ровно раз, в порядке слоя
    assert len(calls) == 2 and ids[5] in calls[1] and ids[0] not in calls[1]   # дозапрос только пропущенных
    by = {x.node_id: x for x in r.routes}
    assert by[ids[0]].template == "T1"                                 # Ф → T1 по config/route.yaml
    assert by[ids[1]].template is None
    assert by[ids[2]].template == "T4"
    videos = [x for x in r.routes if x.format in ("шортс", "длинное видео")]
    hooks = [x for x in r.routes if x.hook_short]
    assert len(hooks) <= 0.2 * len(videos) + 1e-9                      # не больше 20 % роликов
    assert r.ext["core"]["hooks_unset"]                                # снятые крючки записаны
    assert by[ids[0]].ext["core"]["video_score"] == 9


def test_route_missing_after_retry_is_loud(monkeypatch):
    layer = make_layer()
    monkeypatch.setattr(build, "complete_json", lambda *a, **k: build.RouteDrafts(routes=[]))
    with pytest.raises(ValueError, match="без маршрута"):
        build.route(layer, difficulty_types="")
