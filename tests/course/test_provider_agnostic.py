"""Курс не привязан к провайдеру: нет параметров конкретной модели, а ответы моделей в разных «манерах» разбираются."""
import json
import re
from pathlib import Path

import pytest

from pipeline import llm
from pipeline.course import guess as G, interactive as I, tasks as T
from pipeline.course.steptext import StepTextOut

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = [StepTextOut, T.LlmTasks, T.AnswerPicks, I.InteractiveSpec, G.GuessSpec]


def test_course_code_and_prompts_name_no_provider_and_pass_no_model_params():
    banned = re.compile(r"gemini|openai|anthropic|claude(?!.md)|reasoning_effort|response_format|response_schema|max_tokens|temperature",
                        re.I)
    offenders = []
    for folder in ("pipeline/course", "pipeline/illus", "prompts/course"):
        for f in (ROOT / folder).rglob("*"):
            if f.suffix in (".py", ".md", ".j2") and "katex" not in f.parts:
                for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                    if banned.search(line):
                        offenders.append(f"{f.relative_to(ROOT)}:{i}: {line.strip()[:80]}")
    assert offenders == []


def test_course_schemas_have_no_provider_specific_keywords():
    """Схема уходит в промпт текстом (pipeline.llm), но на случай провайдера со строгой схемой: без oneOf/allOf/patternProperties."""
    for model in [s for s in SCHEMAS if s is not None]:
        blob = json.dumps(model.model_json_schema())
        assert not re.search(r'"(oneOf|allOf|patternProperties|not|if|then)"', blob), model.__name__


REPLIES = {
    "голый JSON": '{"picks": [{"n": 1, "answer": ["a"], "claim_id": "c#c1", "evidence": "фраза"}]}',
    "в ```json-ограждении": '```json\n{"picks": [{"n": 1, "answer": ["a"], "claim_id": "c#c1", "evidence": "фраза"}]}\n```',
    "в ограждении без языка": '```\n{"picks": [{"n": 1, "answer": ["a"], "claim_id": "c#c1", "evidence": "фраза"}]}\n```',
    "текст до JSON": 'Вот ответ на задание:\n{"picks": [{"n": 1, "answer": ["a"], "claim_id": "c#c1", "evidence": "фраза"}]}',
    "текст до и после JSON": 'Конечно!\n{"picks": [{"n": 1, "answer": ["a"], "claim_id": "c#c1", "evidence": "фраза"}]}\nНадеюсь, это поможет.',
    "ограждение с текстом вокруг": 'Результат:\n```json\n{"picks": [{"n": 1, "answer": ["a"], "claim_id": "c#c1", "evidence": "фраза {в скобках}"}]}\n```\nГотово.',
}


@pytest.mark.parametrize("name", REPLIES)
def test_reply_styles_of_different_models_parse_into_course_schemas(name):
    parsed = T.AnswerPicks.model_validate(llm._extract_json(REPLIES[name]))
    assert parsed.picks[0].answer == ["a"] and parsed.picks[0].claim_id == "c#c1"


def test_nested_course_schema_parses_from_fenced_reply_with_prose():
    reply = ('Вот текст шага.\n```json\n{"paragraphs": [{"block": "main", "text": "Суть.", "claim_ids": ["x#c1"], "terms": [], '
             '"hypothesis": false, "limit": false}]}\n```\nКонец.')
    out = StepTextOut.model_validate(llm._extract_json(reply))
    assert out.paragraphs[0].block == "main" and out.paragraphs[0].claim_ids == ["x#c1"]
