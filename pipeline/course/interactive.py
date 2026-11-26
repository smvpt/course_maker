"""Задача 5: интерактив вместо ролика. Слайдер → график, значения которого посчитал код.

Шаблонов три, по типу трудности узла (ТЗ; их же использует маршрутизация, T1–T3):
  distribution  слайдер времени → распределение (давление и т. п.): график по оси x, слайдер меняет момент (формализм)
  profile       слайдер глубины → кривая: профиль по глубине, глубина вниз, маркер на выбранной глубине (интерпретация)
  growth        слайдер времени → рост тела или слоёв: значение и столбец растут вместе со слайдером (облик, развитие)
  dependence    общий: один слайдер (любая переменная формулы) → значение и кривая y(x); для формул с одной переменной,
                запасной шаблон, если формула не годится для основного (например, нужны две переменные, а она одна)
Модель выбирает только формулу узла, переменные из узла и диапазоны. Значения считает Python (тот же safe_eval, что в
расчётах заданий и графиках иллюстраций) на сетке положений слайдера и кладёт в interactive.json: JS ничего не вычисляет.

Интерактив нужен узлам, которым маршрутизация дала видео (или «интерактив»), но ролика нет. Без routing.json —
узлам с формулой. Нет формулы — интерактива нет, предупреждение interactive_no_data, сборка не падает.
"""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Callable, Optional

from contracts.models import Node
from pipeline.course.pernode import NotFeasible
from pipeline.course.steptext import (ATTEMPTS, GenerationFailed, call_llm, cyrillic_share, node_dict, numbers_in, sentences,
                                      source_text)
from pipeline.course.tasks import _fmt_number, safe_eval
from pydantic import BaseModel, Field

VIDEO_FORMATS = {"шортс", "длинное видео"}
INTERACTIVE_FORMAT = "интерактив"
ROUTE_TEMPLATE = {"T1": "distribution", "T2": "profile", "T3": "growth", "T4": "profile"}
DIFFICULTY_TEMPLATE = {"Ф": "distribution", "М": "distribution", "И": "profile", "Пр": "profile", "Н": "profile",
                       "Р": "growth", "В": "growth", "П": "growth"}
TEMPLATE_HINT = {
    "distribution": "слайдер — момент времени; график — распределение величины по оси x в этот момент "
                    "(например давление по расстоянию). Нужны две переменные: слайдер и ось x.",
    "profile": "слайдер — глубина; график — профиль величины по глубине, глубина растёт вниз. Нужна одна переменная (глубина).",
    "growth": "слайдер — время; график и столбец показывают, как величина растёт со временем. Нужна одна переменная (время).",
    "dependence": "слайдер — любая переменная формулы (подпиши её по смыслу); график — кривая результата от этой переменной, маркер на "
                  "выбранном значении. Нужна одна переменная, остальные величины формулы — константы из узла.",
}
SLIDER_STEPS = {"distribution": 41, "profile": 121, "growth": 81, "dependence": 121}
GENERAL = "dependence"
X_POINTS = 60


class InteractiveSpec(BaseModel):
    feasible: bool = True               # false — по узлу построить нельзя; остальные поля тогда не нужны
    claim_id: str = ""                  # утверждение-формула, по которой считаем
    title: str = ""
    slider_name: str = ""               # переменная слайдера в expression (латиница)
    slider_label: str = ""
    slider_unit: str = ""
    slider_min: float = 0.0
    slider_max: float = 1.0
    x_name: str = ""                    # только distribution: переменная оси x
    x_label: str = ""
    x_unit: str = ""
    x_min: float = 0.0
    x_max: float = 1.0
    y_label: str = ""
    y_unit: str = ""
    constants: dict[str, float] = Field(default_factory=dict)   # имя → число ИЗ УЗЛА
    expression: str = ""
    curve_key: Optional[str] = None
    note: str = ""


def complete_json(**kw):
    return call_llm(**kw)


def template_for(node: Node, route) -> str:
    if route is not None and route.template in ROUTE_TEMPLATE:
        return ROUTE_TEMPLATE[route.template]
    return DIFFICULTY_TEMPLATE.get(node.difficulty.primary, "distribution")


def plan(nodes: list[Node], routes: dict, has_routing: bool, has_video: Callable[[str], bool]) -> tuple[dict[str, str], list[str]]:
    """({id узла: шаблон} для узлов, которым нужен интерактив и есть формула, [id узлов, которым нужен, но формулы нет])."""
    todo: dict[str, str] = {}
    no_data: list[str] = []
    for n in nodes:
        if has_video(n.id):
            continue
        route = routes.get(n.id)
        formulas = any(c.source_kind == "formula" for c in n.claims)
        if route is not None:
            wants = bool({route.format, route.secondary_format} & (VIDEO_FORMATS | {INTERACTIVE_FORMAT}))
        else:
            wants = not has_routing and formulas
        if not wants:
            continue
        if formulas:
            todo[n.id] = template_for(n, route)
        else:
            no_data.append(n.id)
    return todo, no_data


def _round(v: float) -> float:
    return float(f"{v:.6g}")


def validate_and_compute(node: Node, spec: InteractiveSpec, template: str, curve_keys: set[str]) -> tuple[list[str], dict]:
    errors: list[str] = []
    formulas = {c.id for c in node.claims if c.source_kind == "formula"}
    src_numbers = numbers_in(source_text(node))
    ident = r"[A-Za-z_][A-Za-z0-9_]*"
    if spec.claim_id not in formulas:
        errors.append(f"claim_id {spec.claim_id!r} — не утверждение-формула этого узла (формулы: {sorted(formulas)})")
    names = [("slider_name", spec.slider_name)] + ([("x_name", spec.x_name)] if template == "distribution" else [])
    for field, name in names:
        if not re.fullmatch(ident, name):
            errors.append(f"{field} {name!r} должно быть именем на латинице")
    if template == "distribution" and spec.x_name == spec.slider_name:
        errors.append("x_name и slider_name должны различаться")
    if {spec.slider_name, spec.x_name} & set(spec.constants):
        errors.append("переменные слайдера и оси не должны повторяться в constants")
    ranges = [("slider", spec.slider_min, spec.slider_max)] + ([("x", spec.x_min, spec.x_max)] if template == "distribution" else [])
    for label, lo, hi in ranges:
        if not (math.isfinite(lo) and math.isfinite(hi) and lo < hi):
            errors.append(f"нужно {label}_min < {label}_max (конечные числа)")
    for name, v in spec.constants.items():
        if _fmt_number(v) not in src_numbers:
            errors.append(f"значения {name}={v} нет в узле: константы берутся только из узла")
    required = ["title", "slider_label", "y_label", "note"] + (["x_label"] if template == "distribution" else [])
    for field in required:
        text = getattr(spec, field)
        if not text.strip():
            errors.append(f"пустое поле {field}")
        elif cyrillic_share(text) < 0.5:
            errors.append(f"{field}: текст курса должен быть на русском")
    if len(sentences(spec.note)) > 1:
        errors.append("note — одна фраза")
    if spec.curve_key is not None and spec.curve_key not in curve_keys:
        errors.append(f"curve_key {spec.curve_key!r} нет в styleguide.curves (поставь null)")
    if errors:
        return errors, {}

    n = SLIDER_STEPS[template]
    slider = [spec.slider_min + (spec.slider_max - spec.slider_min) * i / (n - 1) for i in range(n)]

    def f(**vars_):
        return safe_eval(spec.expression, {**spec.constants, **vars_}, src_numbers)

    try:
        if template == "distribution":
            xs = [spec.x_min + (spec.x_max - spec.x_min) * i / (X_POINTS - 1) for i in range(X_POINTS)]
            series = [[_round(f(**{spec.slider_name: t, spec.x_name: x})) for x in xs] for t in slider]
            flat = [v for row in series for v in row]
        else:
            xs = []
            series = [_round(f(**{spec.slider_name: t})) for t in slider]
            flat = series
    except ValueError as e:
        return [f"{e}"], {}
    if max(flat) - min(flat) <= 1e-9 * max(1.0, abs(max(flat))):
        return ["график — горизонтальная линия: выбери диапазон, где значение меняется"], {}
    if template == "distribution" and all(row == series[0] for row in series):
        return ["значение не зависит от слайдера: выбери выражение, где слайдер действительно влияет"], {}
    claim = next(c for c in node.claims if c.id == spec.claim_id)
    return [], {
        "template": template, "claim_id": spec.claim_id, "page": claim.page_pdf, "title": spec.title.strip(), "note": spec.note.strip(),
        "curve_key": spec.curve_key,
        "slider": {"label": spec.slider_label.strip(), "unit": spec.slider_unit.strip(), "values": [_round(v) for v in slider]},
        "x": {"label": spec.x_label.strip(), "unit": spec.x_unit.strip(), "values": [_round(v) for v in xs]} if xs else None,
        "y": {"label": spec.y_label.strip(), "unit": spec.y_unit.strip(), "min": min(flat), "max": max(flat)},
        "series": series}


def _try_template(node: Node, template: str, curve_keys: dict[str, str], language: str, formulas: list[dict]) -> dict:
    feedback = "нет, это первая попытка"
    for _ in range(ATTEMPTS):
        spec = complete_json(prompt="course/interactive", schema=InteractiveSpec, tier="default",
                             vars={"node": json.dumps(node_dict(node), ensure_ascii=False, indent=1),
                                   "formulas": json.dumps(formulas, ensure_ascii=False, indent=1),
                                   "template": f"{template}: {TEMPLATE_HINT[template]}",
                                   "curves": json.dumps([{"key": k, "name": v} for k, v in curve_keys.items()], ensure_ascii=False),
                                   "language": language, "feedback": feedback})
        if not spec.feasible:
            raise NotFeasible(f"модель ответила, что по формулам и числам узла шаблон {template} построить нельзя")
        errors, data = validate_and_compute(node, spec, template, set(curve_keys))
        if not errors:
            return {"spec": spec.model_dump(), "data": data}
        feedback = "\n".join(f"- {e}" for e in errors)
    raise GenerationFailed(f"{node.id}: интерактив ({template}) не прошёл проверку за {ATTEMPTS} попытки:\n{feedback}",
                           [e.removeprefix("- ") for e in feedback.splitlines()])


def make_interactive(node: Node, template: str, curve_keys: dict[str, str], language: str) -> dict:
    """Спецификация от модели → проверка → значения от кода. Возвращает {"spec", "data"} для interactive.json.
    Если модель ответила, что основной шаблон по формулам узла не построить, пробуем общий «один слайдер → кривая»."""
    formulas = [{"claim_id": c.id, "text": c.text, "formula": c.quote, "page": c.page_pdf}
                for c in node.claims if c.source_kind == "formula"]
    chain = [template] + ([GENERAL] if template != GENERAL else [])
    reasons: list[str] = []
    for t in chain:
        try:
            return _try_template(node, t, curve_keys, language, formulas)
        except NotFeasible as e:
            reasons.append(str(e))
    raise NotFeasible("; ".join(reasons))


def table_rows(data: dict, count: int = 9) -> tuple[list[str], list[list[str]]]:
    """Статическая таблица значений (для скринридеров и для случая без JS): те же числа, что у слайдера."""
    vals = data["slider"]["values"]
    idx = sorted({round(i * (len(vals) - 1) / (count - 1)) for i in range(count)})
    s, y = data["slider"], data["y"]
    head = [f"{s['label']}, {s['unit']}" if s["unit"] else s["label"]]
    if data["template"] == "distribution":
        mid = len(data["x"]["values"]) // 2
        x = data["x"]
        head.append(f"{y['label']} при {x['label'].lower()} = {_ru(x['values'][mid])}" + (f" {x['unit']}" if x["unit"] else ""))
        return head, [[_ru(vals[i]), _ru(data["series"][i][mid])] for i in idx]
    head.append(f"{y['label']}, {y['unit']}" if y["unit"] else y["label"])
    return head, [[_ru(vals[i]), _ru(data["series"][i])] for i in idx]


def _ru(v: float) -> str:
    s = str(int(v)) if v == int(v) and abs(v) < 1e7 else f"{v:.4g}"
    return s.replace(".", ",")
