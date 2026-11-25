"""Формы ответов LLM на этапах structure (ВНУТРЕННИЕ, не обмен между модулями).
Поля узла — подмодели contracts.models, чтобы черновик напрямую собирался в Node."""
from typing import Literal, Optional

from pydantic import BaseModel, Field

from contracts.models import (DataMeaning, DecisionOnData, Difficulty, Field_, InefficiencyLens, ItAnalogy, Layers,
                              Link, Misconception, NeedsScan, SourceKind, WorkedExample, BookTask)


class PlanNode(BaseModel):
    slug: str
    title: str
    title_novice: str
    difficulty_primary: Difficulty
    difficulty_secondary: Optional[Difficulty] = None
    threshold: bool
    why_here: str
    unit_ids: list[str]
    prerequisites: list[str] = Field(default_factory=list)
    terms_introduced: list[str] = Field(default_factory=list)


class Uncovered(BaseModel):
    unit_id: str
    reason: str


class Plan(BaseModel):
    nodes: list[PlanNode] = Field(min_length=1)
    uncovered: list[Uncovered] = Field(default_factory=list)


class Assignment(BaseModel):
    unit_id: str
    node: Optional[str] = None      # slug узла
    reason: Optional[str] = None    # если node = null


class Assignments(BaseModel):
    items: list[Assignment]


class ClaimDraft(BaseModel):
    text: str
    kind: Literal["observation", "inference", "assumption"]
    page_pdf: int
    quote: str
    source_kind: SourceKind


class NodeDraft(BaseModel):
    layers: Layers
    claims: list[ClaimDraft] = Field(min_length=1)
    links: list[Link] = Field(default_factory=list)
    misconception: Optional[Misconception] = None
    data_meaning: DataMeaning
    it_analogy: ItAnalogy
    now_practice: Optional[Field_] = None
    inefficiency_lens: Optional[InefficiencyLens] = None
    terms_introduced: list[str] = Field(default_factory=list)
    terms_used: list[str] = Field(default_factory=list)
    needs_scan: list[NeedsScan] = Field(default_factory=list)
    decision_on_data: Optional[DecisionOnData] = None
    worked_examples: list[WorkedExample] = Field(default_factory=list)
    book_tasks: list[BookTask] = Field(default_factory=list)


class QuoteFix(BaseModel):
    found: bool
    quote: Optional[str] = None
    page_pdf: Optional[int] = None
