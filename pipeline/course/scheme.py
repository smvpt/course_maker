"""Интерактив без формул: «схема-исследование» из утверждений узла.

Нужна узлам, которым маршрутизация дала видео или интерактив, ролика нет и формулы для слайдера нет (у глав без формул
это почти все видео-узлы). Модель выбирает 3–7 частей схемы (зоны, этапы, слои), по каждой — короткое название и описание
из утверждения узла; страница показывает схему кликабельными элементами и режим «проверь себя» (назови часть по описанию).
Ничего сверх узла: названия и числа проверяет код, у каждой части есть утверждение и «стр. N» (окно «Проверь по книге»).
Слои колонки красятся цветами литологии из styleguide, если модель назвала породу из его списка.
"""
from __future__ import annotations

import json
import re
from typing import Literal, Optional

from contracts.models import Node
from pipeline.course.pernode import NotFeasible
from pipeline.course.steptext import (ATTEMPTS, GenerationFailed, call_llm, cyrillic_share, node_dict, norm, numbers_in, sentences,
                                      source_text, words)
from pydantic import BaseModel, Field

TEMPLATE = "scheme"
MIN_PARTS, MAX_PARTS = 3, 7
MAX_LABEL_WORDS, MAX_DESCRIPTION_WORDS = 6, 35


class SchemePart(BaseModel):
    label: str = ""
    description: str = ""
    claim_id: str = ""
    rock: Optional[str] = None            # ключ породы из styleguide.lithology (только для layout=layers), иначе null


class SchemeSpec(BaseModel):
    feasible: bool = True                 # false — из утверждений узла схему не собрать; остальные поля тогда не нужны
    title: str = ""
    note: str = ""
    layout: Literal["chain", "layers"] = "chain"
    parts: list[SchemePart] = Field(default_factory=list)


def complete_json(**kw):
    return call_llm(**kw)


def validate_scheme(node: Node, spec: SchemeSpec, rock_keys: set[str]) -> tuple[list[str], dict]:
    errors: list[str] = []
    claims = {c.id: c for c in node.claims}
    src = norm(source_text(node))
    src_numbers = numbers_in(source_text(node))
    for field in ("title", "note"):
        text = getattr(spec, field)
        if not text.strip():
            errors.append(f"пустое поле {field}")
        elif cyrillic_share(text) < 0.5:
            errors.append(f"{field}: текст курса должен быть на русском")
    if len(sentences(spec.note)) > 1:
        errors.append("note — одна фраза")
    if not MIN_PARTS <= len(spec.parts) <= MAX_PARTS:
        errors.append(f"частей схемы должно быть от {MIN_PARTS} до {MAX_PARTS} (сейчас {len(spec.parts)})")
    seen: set[str] = set()
    for i, p in enumerate(spec.parts, 1):
        tag = f"часть {i}"
        label, desc = p.label.strip(), p.description.strip()
        if not label or not desc:
            errors.append(f"{tag}: нужны и label, и description")
            continue
        if words(label) > MAX_LABEL_WORDS:
            errors.append(f"{tag}: название длиннее {MAX_LABEL_WORDS} слов: «{label}»")
        if norm(label) in seen:
            errors.append(f"{tag}: название «{label}» уже есть — названия частей должны быть разными")
        seen.add(norm(label))
        stems = [t[:max(3, min(5, len(t) - 2))] for t in re.findall(r"[а-яёa-z0-9]{4,}", norm(label))]    # основа короче слова: падежи («части» ≠ «часть»)
        missing = [t for t in stems if t not in src]
        if missing:
            errors.append(f"{tag}: слов из названия «{label}» нет в узле (основы {missing}): названия берутся только из узла")
        for text, what in ((label, "название"), (desc, "описание")):
            if cyrillic_share(text) < 0.5:
                errors.append(f"{tag}: {what} должно быть на русском")
        if len(sentences(desc)) > 2 or words(desc) > MAX_DESCRIPTION_WORDS:
            errors.append(f"{tag}: описание — не больше 2 фраз и {MAX_DESCRIPTION_WORDS} слов")
        if norm(label) in norm(desc):
            errors.append(f"{tag}: описание не должно содержать название «{label}»: в режиме «проверь себя» оно было бы подсказкой")
        extra = sorted(numbers_in(desc) - src_numbers)
        if extra:
            errors.append(f"{tag}: числа {extra} нет в узле")
        if p.claim_id not in claims:
            errors.append(f"{tag}: claim_id {p.claim_id!r} нет в узле")
        elif claims[p.claim_id].source_kind in ("formula", "table"):
            errors.append(f"{tag}: опорой части должно быть текстовое утверждение, а не формула или таблица")
        if p.rock is not None and (spec.layout != "layers" or p.rock not in rock_keys):
            errors.append(f"{tag}: rock {p.rock!r} допустим только при layout=layers и только из списка пород (иначе null)")
    if errors:
        return errors, {}
    return [], {"template": TEMPLATE, "title": spec.title.strip(), "note": spec.note.strip(), "layout": spec.layout,
                "parts": [{"label": p.label.strip(), "description": p.description.strip(), "claim_id": p.claim_id,
                           "page": claims[p.claim_id].page_pdf, "rock": p.rock} for p in spec.parts]}


def make_scheme(node: Node, rocks: dict[str, str], language: str) -> dict:
    """Спецификация от модели → проверка → {"spec", "data"} для interactive.json. NotFeasible — схему не собрать."""
    feedback = "нет, это первая попытка"
    for _ in range(ATTEMPTS):
        spec = complete_json(prompt="course/scheme", schema=SchemeSpec, tier="default",
                             vars={"node": json.dumps(node_dict(node), ensure_ascii=False, indent=1),
                                   "rocks": json.dumps([{"key": k, "name": v} for k, v in rocks.items()], ensure_ascii=False),
                                   "language": language, "feedback": feedback})
        if not spec.feasible:
            raise NotFeasible("модель ответила, что из утверждений узла схему-исследование построить нельзя")
        errors, data = validate_scheme(node, spec, set(rocks))
        if not errors:
            return {"spec": spec.model_dump(), "data": data}
        feedback = "\n".join(f"- {e}" for e in errors)
    raise GenerationFailed(f"{node.id}: схема не прошла проверку за {ATTEMPTS} попытки:\n{feedback}",
                           [e.removeprefix("- ") for e in feedback.splitlines()])
