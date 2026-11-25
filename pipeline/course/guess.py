"""Фишка «Сначала угадай»: если у узла есть заблуждение, шаг открывается вопросом «как думаешь: это верно?».

Модель пишет две формулировки: ложную (заблуждение узла) и верную (утверждение узла) и пояснения к каждой. Код проверяет
(слова заблуждения в ложной, слова утверждений в верной, числа только из узла, фразы короткие, русский язык) и сам решает,
какую из двух показать: по хэшу id узла, чтобы правильный ответ не был всегда «неверно». Данные — out/<ch>/course/guesses.json.
Те же проверки и деградация, что у заданий; в обязательные ≥15 заданий не входит. Не вышло — шаг открывается как обычно.
"""
from __future__ import annotations

import hashlib
import json
import re

from contracts.models import Node
from pipeline.course.steptext import (ATTEMPTS, GenerationFailed, call_llm, cyrillic_share, node_dict, norm, numbers_in,
                                      sentences, source_text, words)
from pydantic import BaseModel, Field

MAX_STATEMENT_WORDS = 25
MAX_EXPLAIN_WORDS = 30


class GuessSpec(BaseModel):
    false_statement: str = ""           # утверждение, в котором повторено заблуждение узла (оно неверно)
    true_statement: str = ""            # верное утверждение по утверждениям узла
    explain_false: str = ""             # одна фраза: почему ложное утверждение неверно
    explain_true: str = ""              # одна фраза: почему верное утверждение верно
    claim_ids: list[str] = Field(default_factory=list)


def complete_json(**kw):
    return call_llm(**kw)


def wanted(node: Node) -> bool:
    return node.misconception is not None and bool(node.misconception.text.strip())


def show_true(node_id: str) -> bool:
    """Какое утверждение показываем: решает код, детерминированно по id узла."""
    return int(hashlib.sha256(node_id.encode("utf-8")).hexdigest(), 16) % 2 == 0


def stems(text: str) -> set[str]:
    return {norm(w)[:5] for w in re.findall(r"[^\W\d_]{5,}", text)}


def validate_guess(node: Node, spec: GuessSpec) -> list[str]:
    errors: list[str] = []
    src_numbers = numbers_in(source_text(node))
    ids = {c.id for c in node.claims}
    if not spec.claim_ids:
        errors.append("пустой claim_ids")
    for cid in spec.claim_ids:
        if cid not in ids:
            errors.append(f"claim_id {cid!r} нет в узле")
    texts = [("false_statement", spec.false_statement, MAX_STATEMENT_WORDS), ("true_statement", spec.true_statement, MAX_STATEMENT_WORDS),
             ("explain_false", spec.explain_false, MAX_EXPLAIN_WORDS), ("explain_true", spec.explain_true, MAX_EXPLAIN_WORDS)]
    for field, text, limit in texts:
        if not text.strip():
            errors.append(f"пустое поле {field}")
            continue
        if cyrillic_share(text) < 0.5:
            errors.append(f"{field}: текст курса должен быть на русском")
        if len(sentences(text)) != 1 or words(text) > limit:
            errors.append(f"{field}: одна фраза до {limit} слов")
        if "?" in text and field.endswith("statement"):
            errors.append(f"{field}: это должно быть утверждение, а не вопрос")
        extra = sorted(numbers_in(text) - src_numbers)
        if extra:
            errors.append(f"{field}: чисел {extra} нет в узле")
    if norm(spec.false_statement.strip()) == norm(spec.true_statement.strip()):
        errors.append("ложное и верное утверждения должны различаться")
    m = stems(node.misconception.text)
    need = 2 if len(m) >= 4 else 1
    if len(stems(spec.false_statement) & m) < need:
        errors.append("false_statement должно повторять заблуждение узла (в нём должны быть его слова)")
    cited = " ".join(c.text + " " + c.quote for c in node.claims if c.id in spec.claim_ids)
    c = stems(cited)
    if c and len(stems(spec.true_statement) & c) < (2 if len(c) >= 4 else 1):
        errors.append("true_statement должно опираться на указанные утверждения (в нём должны быть их слова)")
    return errors


def make_guess(node: Node, language: str) -> dict:
    feedback = "нет, это первая попытка"
    for _ in range(ATTEMPTS):
        spec = complete_json(prompt="course/guess", schema=GuessSpec, tier="default",
                             vars={"node": json.dumps(node_dict(node), ensure_ascii=False, indent=1), "language": language,
                                   "feedback": feedback})
        errors = validate_guess(node, spec)
        if not errors:
            truth = show_true(node.id)
            pages = sorted({c.page_pdf for c in node.claims if c.id in spec.claim_ids})
            return {"statement": (spec.true_statement if truth else spec.false_statement).strip(), "truth": truth,
                    "explanation": (spec.explain_true if truth else spec.explain_false).strip(),
                    "claim_ids": spec.claim_ids, "pages": pages,
                    "other_statement": (spec.false_statement if truth else spec.true_statement).strip()}
        feedback = "\n".join(f"- {e}" for e in errors)
    raise GenerationFailed(f"{node.id}: вопрос «сначала угадай» не прошёл проверку за {ATTEMPTS} попытки:\n{feedback}",
                           [e.removeprefix("- ") for e in feedback.splitlines()])
