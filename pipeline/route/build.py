"""layer → routing: модель ставит оценки видеоёмкости, формат и обоснование; код держит правила config/route.yaml."""
from __future__ import annotations

import math
import sys
from functools import lru_cache
from typing import Optional

import yaml
from pydantic import BaseModel, Field

from contracts.models import FormatRu, Layer, Node, Route, Routing, VideoScores
from pipeline.common import paths
from pipeline.llm import complete_json


class RouteDraft(BaseModel):
    node_id: str
    format: FormatRu
    secondary_format: Optional[FormatRu] = None
    video_scores: VideoScores
    hook_short: bool = False
    template: Optional[str] = None
    why: str


class RouteDrafts(BaseModel):
    routes: list[RouteDraft] = Field(default_factory=list)


@lru_cache(maxsize=None)
def rules() -> dict:
    return yaml.safe_load((paths.CONFIG / "route.yaml").read_text(encoding="utf-8"))


def node_line(n: Node) -> str:
    sec = f", второй {n.difficulty.secondary}" if n.difficulty.secondary else ""
    return (f"- node_id: {n.id}\n  название: {n.title}\n  тип трудности: {n.difficulty.primary}{sec}"
            f"{'; пороговая идея' if n.threshold else ''}\n  суть: {n.layers.main.text}\n"
            f"  механизм: {n.layers.mechanism.text}\n  утверждений: {len(n.claims)}, примеров автора: "
            f"{len(n.worked_examples)}, задач книги: {len(n.book_tasks)}")


def default_template(primary: str) -> Optional[str]:
    return next((t for t, d in rules()["templates"].items() if primary in d.get("types", [])), None)


def route(layer: Layer, difficulty_types: str) -> Routing:
    cfg = rules()
    templates = "\n".join(f"- {t}: {d['about']} (по умолчанию для типов: {', '.join(d.get('types') or []) or '—'})"
                          for t, d in cfg["templates"].items())
    want = {n.id: n for n in layer.nodes}
    got: dict[str, RouteDraft] = {}
    log = {"foreign_routes": [], "template_fixed": [], "hooks_unset": []}
    for _ in range(2):
        todo = [n for n in layer.nodes if n.id not in got]
        if not todo:
            break
        ans = complete_json("core/route", {
            "difficulty_types": difficulty_types, "templates": templates,
            "hook_share": f"{int(cfg['hook_short_max_share'] * 100)} %",
            "nodes": "\n".join(node_line(n) for n in todo),
        }, schema=RouteDrafts, tier="default")
        for r in ans.routes:
            if r.node_id in want and r.node_id not in got:
                got[r.node_id] = r
            elif r.node_id not in want:
                log["foreign_routes"].append(r.node_id)
    missing = [n.id for n in layer.nodes if n.id not in got]
    if missing:
        raise ValueError(f"узлы без маршрута после дозапроса: {missing}")

    routes = []
    for n in layer.nodes:
        d = got[n.id]
        template = d.template
        if d.format in cfg["template_formats"] or d.secondary_format in cfg["template_formats"]:
            if template not in cfg["templates"]:
                fixed = default_template(n.difficulty.primary)
                log["template_fixed"].append({"node": n.id, "was": template, "now": fixed})
                template = fixed
        else:
            template = None
        r = Route(node_id=n.id, format=d.format, secondary_format=d.secondary_format, video_scores=d.video_scores,
                  hook_short=d.hook_short, template=template, why=d.why)
        r.ext["core"] = {"video_score": sum(d.video_scores.model_dump(exclude={"ext"}).values())}
        routes.append(r)

    # шортсы-крючки — не больше доли роликов; оставляем самые видеоёмкие
    videos = sum(1 for r in routes if r.format in cfg["video_formats"] or r.hook_short)
    allowed = math.floor(cfg["hook_short_max_share"] * videos + 1e-9)
    hooks = sorted((r for r in routes if r.hook_short), key=lambda r: -r.ext["core"]["video_score"])
    for r in hooks[allowed:]:
        r.hook_short = False
        log["hooks_unset"].append(r.node_id)
    if log["hooks_unset"]:
        print(f"[route] сняты пометки шортса-крючка (больше {cfg['hook_short_max_share']:.0%} роликов): "
              f"{log['hooks_unset']}", file=sys.stderr)

    routing = Routing(chapter=layer.chapter, routes=routes)
    routing.ext["core"] = log
    return routing
