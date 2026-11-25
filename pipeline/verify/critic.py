"""LLM-критик: одна цель (утверждение, аналогия, фраза, факт сцены, кадр) против страниц главы.

Замечание выдаётся только с доказательством: для утверждений и фраз — цитата, которую
quotes.py находит в главе; для аналогий, фактов сцены и кадров — страница утверждения узла.
Неожиданное, но подтверждённое главой не трогаем: ложная тревога стоит баллов.
"""
import json
from typing import Literal, Optional

from pydantic import BaseModel, model_validator

from contracts.models import Category, Remark, Severity
from pipeline.verify.quotes import check_quote_md

NEEDS_QUOTE = {"claim", "script_line"}


class Verdict(BaseModel):
    """Ответ LLM по одной цели."""
    verdict: Literal["supported", "contradicted", "not_in_source"]
    category: Optional[Category] = None
    severity: Optional[Severity] = None
    problem: str = ""
    fix: str = ""
    page_pdf: Optional[int] = None
    quote: Optional[str] = None

    @model_validator(mode="after")
    def _complete(self):
        if self.verdict == "contradicted":
            miss = [f for f in ("category", "severity") if getattr(self, f) is None]
            miss += [f for f in ("problem", "fix") if not getattr(self, f).strip()]
            if miss:
                raise ValueError(f"verdict=contradicted требует полей {miss}")
        return self


def page_context(pages, page_nums):
    """Сырые страницы главы с метками, по возрастанию."""
    return "\n".join(f"<!-- page {n} -->\n{pages[n].strip()}" for n in sorted(set(page_nums)) if n in pages)


def ask(item_type, item, context, related, checklist="—", image=None):
    from pipeline.llm import complete_json
    vars = {"item_type": item_type,
            "item": json.dumps(item, ensure_ascii=False, indent=1),
            "context": context,
            "related": related,
            "checklist": checklist}
    if image is not None:
        return complete_json(prompt="verify/critic_frame", vars=vars, schema=Verdict, tier="vision", images=[image])
    return complete_json(prompt="verify/critic", vars=vars, schema=Verdict, tier="strong")


def to_remark(target, item_type, v, md, default_page, allowed_pages):
    """Verdict → Remark или (None, причина). Без доказательства замечание не выдаём."""
    if v.verdict != "contradicted":
        return None, v.verdict
    page, quote = None, None
    if v.quote:
        r = check_quote_md(md, v.page_pdf if v.page_pdf is not None else default_page, v.quote)
        if r.status != "not_found":
            page, quote = r.page, v.quote
    if page is None:
        if item_type in NEEDS_QUOTE:
            return None, "unproven"
        page = v.page_pdf if v.page_pdf in allowed_pages else default_page
    return Remark(target=target, category=v.category, severity=v.severity, problem=v.problem.strip(),
                  fix=v.fix.strip(), page_pdf=page, quote=quote), "contradicted"
