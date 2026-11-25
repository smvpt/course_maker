"""Иллюстрации курса: layer.json → out/<ch>/illus/*.svg + illustrations.json (схема организаторов illustration.schema.json).

python -m pipeline.illus.run --ch <id> [--domain <имя>] [--styleguide <файл>] [--no-llm]

На каждый шаг (узел) — схема утверждений (класс B) и, если подходит, один специальный рисунок:
  график по формуле главы (B, «симуляция»; модель лишь выбирает формулу, переменные и диапазон, значения считает код),
  график по таблице книги (A, «реальные данные») или условная колонка слоёв (B, «схема»).
Ни один рисунок не генерируется моделью изображений. Не подошёл ни один специальный генератор и в шаге одно утверждение —
схема из утверждений как запасной вариант и предупреждение в illustrations.json (ext.illus.warnings) и в stderr.
Сбой модели при выборе формулы не роняет сборку: шаг остаётся без графика, причина — в предупреждении.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import Literal, Optional

from contracts.models import Illustration, Illustrations, Layer
from pipeline.course.build import parse_md_table
from pipeline.course.steptext import (ATTEMPTS, GenerationFailed, LlmError, LlmState, call_llm, cyrillic_share, node_dict,
                                      numbers_in, quote_language, sentences, source_text)
from pipeline.course.tasks import _fmt_number, safe_eval
from pipeline.illus import gen
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
POINTS = 80


# ---------------------------------------------------------------- график по формуле: спецификация от модели, значения от кода

class CurveSpec(BaseModel):
    feasible: bool = True               # false — формулу по данным узла построить нельзя; остальные поля тогда не нужны
    claim_id: str = ""                  # id утверждения-формулы, по которой строится график
    title: str = ""
    x_name: str = ""                    # имя независимой переменной в expression (латиница)
    x_label: str = ""
    x_unit: str = ""
    y_label: str = ""
    y_unit: str = ""
    x_min: float = 0.0
    x_max: float = 1.0
    constants: dict[str, float] = Field(default_factory=dict)   # имя → число ИЗ УЗЛА
    expression: str = ""                # y как функция x_name и constants
    depth_axis: Literal["none", "x", "y"] = "none"
    curve_key: Optional[str] = None     # ключ кривой из styleguide.curves, если график — кривая из легенды
    note: str = ""                      # одна фраза: что показывает график


def complete_json(**kw):
    return call_llm(**kw)


def validate_curve(node, spec: CurveSpec, style: gen.Style) -> tuple[list[str], list[float], list[float]]:
    errors: list[str] = []
    formulas = {c.id for c in node.claims if c.source_kind == "formula"}
    src_numbers = numbers_in(source_text(node))
    if spec.claim_id not in formulas:
        errors.append(f"claim_id {spec.claim_id!r} — не утверждение-формула этого узла (формулы: {sorted(formulas)})")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", spec.x_name):
        errors.append(f"x_name {spec.x_name!r} должно быть именем на латинице")
    if spec.x_name in spec.constants:
        errors.append("x_name не должно повторяться в constants")
    if not (math.isfinite(spec.x_min) and math.isfinite(spec.x_max) and spec.x_min < spec.x_max):
        errors.append("нужно x_min < x_max (конечные числа)")
    for name, v in spec.constants.items():
        if _fmt_number(v) not in src_numbers:
            errors.append(f"значения {name}={v} нет в узле: константы берутся только из узла")
    for field_name in ("title", "x_label", "y_label", "note"):
        text = getattr(spec, field_name)
        if not text.strip():
            errors.append(f"пустое поле {field_name}")
        elif cyrillic_share(text) < 0.5:
            errors.append(f"{field_name}: текст курса должен быть на русском")
    if len(sentences(spec.note)) > 1:
        errors.append("note — одна фраза")
    if spec.curve_key is not None and style.curve(spec.curve_key) is None:
        errors.append(f"curve_key {spec.curve_key!r} нет в styleguide.curves (поставь null)")
    if errors:
        return errors, [], []
    xs = [spec.x_min + (spec.x_max - spec.x_min) * i / (POINTS - 1) for i in range(POINTS)]
    ys: list[float] = []
    for x in xs:
        try:
            ys.append(safe_eval(spec.expression, {**spec.constants, spec.x_name: x}, src_numbers))
        except ValueError as e:
            return [f"{e} (при {spec.x_name}={x:g})"], [], []
    if max(ys) - min(ys) <= 1e-9 * max(1.0, abs(max(ys))):
        return ["график — горизонтальная линия: выбери диапазон, где значение меняется"], [], []
    return [], xs, ys


def generate_curve(node, style: gen.Style, language: str) -> Optional[tuple[CurveSpec, list[float], list[float]]]:
    """Спецификация графика от модели с проверкой кодом. None — формулу по узлу построить нельзя (модель так и ответила)."""
    formulas = [{"claim_id": c.id, "text": c.text, "formula": c.quote, "page": c.page_pdf}
                for c in node.claims if c.source_kind == "formula"]
    curves = [{"key": k, "name": v["ru"]} for k, v in style.raw["curves"].items()]
    feedback = "нет, это первая попытка"
    for _ in range(ATTEMPTS):
        spec = complete_json(prompt="course/illus_curve", schema=CurveSpec, tier="default",
                             vars={"node": json.dumps(node_dict(node), ensure_ascii=False, indent=1),
                                   "formulas": json.dumps(formulas, ensure_ascii=False, indent=1),
                                   "curves": json.dumps(curves, ensure_ascii=False), "language": language, "feedback": feedback})
        if not spec.feasible:
            return None
        errors, xs, ys = validate_curve(node, spec, style)
        if not errors:
            return spec, xs, ys
        feedback = "\n".join(f"- {e}" for e in errors)
    raise GenerationFailed(f"{node.id}: график по формуле не прошёл проверку за {ATTEMPTS} попытки:\n{feedback}",
                           [e.removeprefix("- ") for e in feedback.splitlines()])


# ---------------------------------------------------------------- рисунки узла

def figures_for_node(node, style: gen.Style, state: LlmState, use_llm: bool, language: str, warnings: list[dict]
                     ) -> list[gen.Figure]:
    def warn(code: str, message: str, **extra) -> None:
        print(f"WARNING: {message}", file=sys.stderr)
        warnings.append({"code": code, "message": message, "node": node.id, **extra})

    title = node.title_novice or node.title
    special: Optional[gen.Figure] = None

    formulas = [c for c in node.claims if c.source_kind == "formula"]
    if formulas and use_llm and state.down is None:
        try:
            made = generate_curve(node, style, language)
            state.success()
            if made:
                spec, xs, ys = made
                claim = next(c for c in node.claims if c.id == spec.claim_id)
                svg = gen.curve(spec.title, spec.x_label, spec.x_unit, spec.y_label, spec.y_unit, xs, ys, spec.depth_axis,
                                style.curve(spec.curve_key), spec.note, style)
                special = gen.Figure(
                    kind="curve", svg=svg, frame_class="B", origin="code_from_model", label="симуляция",
                    caption=f"{spec.note.strip()} Значения рассчитаны кодом по формуле главы, а не измерены.",
                    alt=gen._alt(spec.title, [spec.note, f"по горизонтали: {spec.x_label}", f"по вертикали: {spec.y_label}"]),
                    source=f"формула главы, стр. {claim.page_pdf}", claim_ids=[claim.id], ext={"spec": spec.model_dump()})
        except GenerationFailed as e:
            state.success()                              # модель отвечала, просто неверно
            warn("illus_curve_failed", f"график по формуле шага {node.id} не построен: {e.errors[0]}", errors=e.errors)
        except LlmError as e:
            state.failure(e)
            warn("illus_curve_failed", f"график по формуле шага {node.id} не построен: отказ модели: {e}")
    elif formulas and use_llm:
        warn("illus_curve_failed", f"график по формуле шага {node.id} не построен: модель недоступна: {state.down}")

    if special is None:
        for c in (c for c in node.claims if c.source_kind == "table"):
            rows = parse_md_table(c.quote)
            special = gen.crossplot(c, rows, title, style) if rows else None
            if special:
                break
    if special is None:
        special = gen.column(node, style, title)

    figs: list[gen.Figure] = []
    if len(node.claims) >= 2 or special is None:
        figs.append(gen.chain(node, style, title))
        if special is None and len(node.claims) < 2:
            warn("illus_fallback", f"для шага {node.id} не подошёл ни один специальный генератор, схема из единственного утверждения")
    if special is not None:
        figs.append(special)
    return figs


# ---------------------------------------------------------------- глава

def read_layer(ch_dir: Path) -> Layer:
    path = ch_dir / "layer.json"
    if not path.exists():
        raise FileNotFoundError(f"нет {path}: сначала make structure (П1)")
    return Layer.model_validate_json(path.read_text(encoding="utf-8"))


def run(ch: str, out_root: Path, style: gen.Style, use_llm: bool = True, state: Optional[LlmState] = None) -> Illustrations:
    ch_dir = out_root / ch
    layer = read_layer(ch_dir)
    if layer.chapter != ch:
        raise ValueError(f"{ch_dir / 'layer.json'}: chapter={layer.chapter!r}, а запрошена глава {ch!r}")
    state = state or LlmState()
    language = quote_language(layer)
    illus_dir = ch_dir / "illus"
    illus_dir.mkdir(parents=True, exist_ok=True)
    list_path = illus_dir / "illustrations.json"
    old_files = {il.file for il in Illustrations.model_validate_json(list_path.read_text(encoding="utf-8")).illustrations} \
        if list_path.exists() else set()

    warnings: list[dict] = []
    items: list[Illustration] = []
    for node in layer.nodes:
        for k, fig in enumerate(figures_for_node(node, style, state, use_llm, language, warnings), 1):
            rel = f"illus/{node.id}.{fig.kind}.svg"
            (ch_dir / rel).write_text(fig.svg, encoding="utf-8")
            items.append(Illustration(id=f"{node.id}.il{k}", step_id=node.id, node_id=node.id, file=rel, frame_class=fig.frame_class,
                                      origin=fig.origin, label=fig.label, caption=fig.caption, alt=fig.alt, source=fig.source,
                                      claim_ids=fig.claim_ids, ext={"kind": fig.kind, **fig.ext}))
    for stale in old_files - {i.file for i in items}:         # файлы прошлого запуска, которых больше нет в списке
        (ch_dir / stale).unlink(missing_ok=True)
    result = Illustrations(chapter=ch, illustrations=items, ext={"illus": {"warnings": warnings}})
    list_path.write_text(result.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    return result


def load_style(ch_dir: Path, domain: Optional[str], styleguide: Optional[Path]) -> gen.Style:
    if styleguide:
        return gen.Style(json.loads(Path(styleguide).read_text(encoding="utf-8")))
    from pipeline.course.generate import resolve_domain
    from pipeline.common import domain as domain_pack           # доменный пакет — только через pipeline.common.domain
    return gen.Style(domain_pack.load(resolve_domain(ch_dir, domain)).styleguide)


def main() -> None:
    ap = argparse.ArgumentParser(description="layer.json → out/<ch>/illus/ (SVG, нарисованные кодом)")
    ap.add_argument("--ch", required=True)
    ap.add_argument("--out", type=Path, default=Path(os.environ.get("OUT_DIR") or ROOT / "out"), help="корень out/")
    ap.add_argument("--domain", help="доменный пакет (по умолчанию — из out/<ch>/units.json)")
    ap.add_argument("--styleguide", type=Path, help="styleguide.json вместо стайлгайда доменного пакета")
    ap.add_argument("--no-llm", action="store_true", help="не звать модель: графики по формулам не строятся")
    a = ap.parse_args()
    os.environ.setdefault("CH", a.ch)
    style = load_style(a.out / a.ch, a.domain, a.styleguide)
    res = run(a.ch, a.out, style, use_llm=not a.no_llm)
    kinds: dict[str, int] = {}
    for il in res.illustrations:
        kinds[il.ext["kind"]] = kinds.get(il.ext["kind"], 0) + 1
    print(f"иллюстрации: {len(res.illustrations)} ({', '.join(f'{k}: {v}' for k, v in sorted(kinds.items()))}) → "
          f"{a.out / a.ch / 'illus' / 'illustrations.json'}")


if __name__ == "__main__":
    main()
