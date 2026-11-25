"""Контракты данных между модулями. Пишет только П1.

ФОРМАТЫ ОРГАНИЗАТОРОВ ОБЯЗАТЕЛЬНЫ (пакет вводных, 01_схемы и 02_модуль_проверки):
имена полей ниже повторяют их JSON-схемы один в один. Поля сверх схемы добавлять
можно («убирать обязательные — нельзя»), поэтому extra="allow".
Свои данные модуля, которых нет в схеме, — в поле `ext` под ключом модуля.

Проверка соответствия: tests/core/test_schemas.py валидирует выходы через jsonschema
по файлам data/organizers/01_схемы/*.schema.json.

Внутренние форматы команды (не из схем организаторов): Unit, ChapterUnits,
Script, SceneSpec, Remark-обёртки — помечены «ВНУТРЕННИЙ».
"""
from __future__ import annotations

from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    ext: dict[str, Any] = Field(default_factory=dict)


Difficulty = Literal["М", "В", "И", "Ф", "П", "Пр", "Н", "Р"]
FrameClass = Literal["A", "B", "C", "D"]
FrameLabel = Literal["реальные данные", "симуляция", "схема"]          # для кадров роликов
IllusLabel = Literal["реальные данные", "симуляция", "схема", "иллюстрация ИИ"]
Severity = Literal["critical", "significant", "minor"]


# =====================================================================
# ВНУТРЕННИЙ: единицы главы (ingest)
# =====================================================================

UnitKind = Literal["paragraph", "figure", "formula", "table", "worked_example", "task", "heading"]


class Unit(Base):
    unit_id: str                 # как в coverage.schema: "p095.03" — 3-я единица на стр. 95
    kind: UnitKind               # те же значения, что в coverage.schema
    page_pdf: int                # метка <!-- page N --> в md
    text: str
    figure_ref: Optional[str] = None
    image_path: Optional[str] = None   # скан страницы для vision


class ChapterUnits(Base):
    chapter: str                 # id главы: только [a-z0-9_.-], напр. "latyshova_gl5_par17-20"
    source: str                  # путь к md
    language: Literal["ru", "en"] = "ru"
    domain: str = "geology"
    pdf_pages: list[int]
    units: list[Unit]


# =====================================================================
# node.schema.json — учебный слой
# =====================================================================

class Field_(Base):
    """$defs/field: текст с пометкой происхождения."""
    text: str
    by_model: bool
    hypothesis: Optional[bool] = None


SourceKind = Literal["text", "formula", "table", "task", "figure_caption", "figure_description_model"]


class Claim(Base):
    id: str                      # "^[a-z0-9_.-]+#c[0-9]+$", напр. "latyshova.mixed_section#c1"
    text: str                    # своими словами
    kind: Literal["observation", "inference", "assumption"]
    page_pdf: int
    page_print: Optional[int] = None
    quote: str = Field(min_length=8)   # дословно из md
    source_kind: SourceKind
    by_model: bool
    needs_scan: Optional[bool] = None


class Link(Base):
    type: Literal["prerequisite", "example_of", "refutes_misconception", "to_data"]
    target: str                  # id узла, misc.* или data.*
    note: Optional[str] = None


class DifficultyPair(Base):
    primary: Difficulty
    secondary: Optional[Difficulty] = None


class Layers(Base):
    topic: Field_
    main: Field_
    mechanism: Field_
    practice: Field_
    nuances: Field_
    deeper: list[Field_] = Field(default_factory=list)


class Misconception(Base):
    ref: Optional[str] = None    # misc.* из domain/<d>/misconceptions.json
    text: str
    by_model: bool


class DataMeaning(Base):
    from_chapter: Field_
    breaks: Field_
    hypotheses: list[Field_] = Field(default_factory=list)


class ItAnalogy(Base):
    text: str
    breaks_where: str
    by_model: bool


class InefficiencyLens(Base):
    inputs: str
    manual_steps: str
    judgment_points: str
    time: str
    typical_errors: str
    by_model: bool


class NeedsScan(Base):
    page: int
    what: str


class DecisionOnData(Base):
    features: list[str]
    rule: str
    conclusion: str
    counterexample: Optional[str] = None


class WorkedExample(Base):
    page_pdf: int
    condition: str
    steps: list[str]
    result: str                  # итог с числами автора
    figure: Optional[str] = None  # «рис. N, стр. M»


class BookTask(Base):
    number: str
    page_pdf: int
    text: str
    figure: Optional[str] = None


class Node(Base):
    id: str                      # "^[a-z0-9_.-]+$": "<префикс главы>.<slug>", устойчивый
    order: int = Field(ge=1)
    title: str
    why_here: Field_
    difficulty: DifficultyPair
    threshold: bool
    layers: Layers
    claims: list[Claim] = Field(min_length=1)
    links: list[Link]
    misconception: Optional[Misconception] = None
    data_meaning: DataMeaning
    it_analogy: ItAnalogy
    now_practice: Optional[Field_] = None
    inefficiency_lens: Optional[InefficiencyLens] = None
    terms_introduced: list[str]
    terms_used: list[str] = Field(default_factory=list)
    needs_scan: list[NeedsScan] = Field(default_factory=list)
    decision_on_data: Optional[DecisionOnData] = None
    worked_examples: list[WorkedExample] = Field(default_factory=list)
    book_tasks: list[BookTask] = Field(default_factory=list)
    pages: list[int]
    # Сверх схемы (разрешено): заголовок для новичка 3–7 слов, единицы главы узла
    title_novice: Optional[str] = None
    unit_ids: list[str] = Field(default_factory=list)


class Layer(Base):
    chapter: str
    source: str
    pdf_pages: list[str] = Field(default_factory=list)
    generated_by: Optional[str] = None
    nodes: list[Node] = Field(min_length=1)


# =====================================================================
# coverage.schema.json — таблица покрытия (JSON, не CSV)
# =====================================================================

class CoverageRow(Base):
    unit_id: str
    kind: UnitKind
    page_pdf: int
    excerpt: str                 # 5–15 слов начала единицы
    node_ids: list[str]
    reason: Optional[str] = None  # обязательна, если node_ids пуст; «непоказуемо» — не причина


class Coverage(Base):
    chapter: str
    rows: list[CoverageRow]


# =====================================================================
# routing.schema.json
# =====================================================================

FormatRu = Literal["шортс", "длинное видео", "интерактив", "практикум на данных", "карточки", "текст"]


class VideoScores(Base):
    """Каждый критерий 0–2."""
    time: int = Field(ge=0, le=2)
    invisible: int = Field(ge=0, le=2)
    scale: int = Field(ge=0, le=2)
    counterintuitive: int = Field(ge=0, le=2)
    cause_effect: int = Field(ge=0, le=2)


class Route(Base):
    node_id: str
    format: FormatRu
    secondary_format: Optional[FormatRu] = None
    video_scores: VideoScores
    hook_short: Optional[bool] = None
    template: Optional[str] = None   # "T1".."T4"
    why: str


class Routing(Base):
    chapter: str
    routes: list[Route]


# =====================================================================
# task.schema.json — задания курса
# =====================================================================

class TaskOption(Base):
    id: str
    text: str
    misconception: Optional[str] = None   # misc.* для неверного варианта


class Task(Base):
    id: str
    type: Literal["single", "multiple", "order", "gap", "calc"]
    step_id: str                 # шаг курса = node.id
    claim_ids: list[str] = Field(min_length=1)
    prompt: str                  # для gap — пропуски {{1}}, {{2}}
    options: list[TaskOption] = Field(default_factory=list)
    answer: Union[str, float, int, list]  # single: id; multiple/order: список id; gap: список слов; calc: число
    tolerance: Optional[float] = None
    unit: Optional[str] = None
    explanation: str             # одна фраза
    kind: Optional[Literal["recall", "understanding", "transfer", "data"]] = None


class Tasks(Base):
    chapter: str
    tasks: list[Task]


# =====================================================================
# illustration.schema.json
# =====================================================================

class Illustration(Base):
    id: str
    step_id: str
    node_id: Optional[str] = None
    file: str
    frame_class: FrameClass
    origin: Literal["code_from_data", "code_from_model", "photo", "redrawn_from_book", "ai_generated"]
    label: Optional[IllusLabel] = None   # ai_generated → класс C/D, label «иллюстрация ИИ», prompt обязателен
    caption: str
    alt: str
    source: Optional[str] = None
    claim_ids: list[str] = Field(default_factory=list)
    prompt: Optional[str] = None


class Illustrations(Base):
    chapter: str
    illustrations: list[Illustration]


# =====================================================================
# passport.schema.json — паспорт ролика
# =====================================================================

class ScriptLine(Base):
    t_start: float
    t_end: float
    text: str
    claim_id: Optional[str] = None
    is_analogy: Optional[bool] = None
    on_screen: Optional[str] = None


class SourceRow(Base):
    claim_id: str
    page_or_dataset: str
    quote: Optional[str] = None


class PassportFrame(Base):
    t: float
    class_: FrameClass = Field(alias="class")
    label: FrameLabel


class ChecklistAnswer(Base):
    item: str                    # pc.* из physics_checklist.json
    answer: Literal["да", "нет", "н/п"]
    note: Optional[str] = None


class Passport(Base):
    video_id: str
    node_id: str
    node_card: dict[str, Any]
    script: list[ScriptLine]
    sources: list[SourceRow]
    scene_spec: str              # путь к scene_spec.json
    frames: list[PassportFrame]
    exaggerations: list[str]
    prediction_question: str
    transfer_question: str
    data_it_bridge: str
    physics_checklist: list[ChecklistAnswer]
    audio_check: dict[str, Any]  # темп, LUFS, рассинхрон, WER, «проверить на слух»


# =====================================================================
# ВНУТРЕННИЙ: сценарий и спецификация сцены до рендера (П4)
# =====================================================================

Beat = Literal["hook", "problem", "solution", "naming", "prediction", "data", "decision", "transfer", "final"]


class Phrase(Base):
    id: str
    text: str                    # для уха: ≤15–18 слов, числа словами
    on_screen: Optional[str] = None  # ≤7–8 слов, без формул
    beat: Beat
    claim_id: Optional[str] = None
    is_analogy: bool = False
    pause_after_s: float = 0.0   # 1–1,5 с перед ответом на предсказание


class Script(Base):
    video_id: str
    node_id: str
    format: Literal["short", "long"]   # шортс 9:16 / разбор 16:9
    phrases: list[Phrase]
    prediction_question: str
    transfer_question: str
    data_it_bridge: str


class Shot(Base):
    id: str
    phrase_ids: list[str]
    frame_class: FrameClass
    label: FrameLabel
    shows: str
    plaque: Optional[str] = None  # «не в масштабе: …»


class SceneSpec(Base):
    video_id: str
    node_id: str
    template: str
    params: dict[str, Any]
    objects: list[str]
    invariants: list[str]
    assumptions: list[str]
    exaggerations: list[str] = Field(default_factory=list)
    shots: list[Shot]
    true_scale_shot_id: Optional[str] = None
    convention: str = "русская школа ГИС"
    data_sources: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    historical_objects: list[str] = Field(default_factory=list)


# =====================================================================
# 02_модуль_проверки: review_package / review_output
# =====================================================================

class ReviewItem(Base):
    id: str                      # "^[A-Z][A-Z0-9_.-]*$": C001, A01, L01.03, S01
    type: Literal["claim", "analogy", "script_line", "scene_fact"]
    node_id: Optional[str] = None
    text: str
    kind: Optional[Literal["observation", "inference", "assumption"]] = None
    page_pdf: Optional[int] = None
    quote: Optional[str] = None
    breaks_where: Optional[str] = None
    video_id: Optional[str] = None
    t_start: Optional[float] = None
    t_end: Optional[float] = None
    claim_ref: Optional[str] = None
    on_screen: Optional[str] = None
    spec_path: Optional[str] = None


class ReviewScene(Base):
    video_id: str
    spec: dict[str, Any]


class ReviewFrame(Base):
    id: str                      # F01…
    video_id: str
    file: str
    t: float
    frame_class: FrameClass
    label: FrameLabel
    shows: str
    plaque: Optional[str] = None


class ReviewPackage(Base):
    package_id: str
    chapter: str
    chapter_file: str
    language: Optional[str] = None
    items: list[ReviewItem]
    scenes: list[ReviewScene]
    frames: list[ReviewFrame]


Category = Literal["overgeneralization", "sign_flip", "measured_vs_inferred", "lost_condition",
                   "missing_caveat", "wrong_scaling", "wrong_mechanism", "outdated_as_current",
                   "analogy_without_limit", "frame_error", "other"]


class Remark(Base):
    target: str                  # id элемента или кадра; одно замечание на цель
    category: Category
    severity: Severity
    problem: str
    fix: str
    page_pdf: Optional[int]
    quote: Optional[str] = None


class ReviewOutput(Base):
    package_id: str
    team: Optional[str] = None
    remarks: list[Remark]


# =====================================================================
# 05_шаблоны: журнал правок и метрики (CSV, строки — эти модели)
# =====================================================================

class ManualEdit(Base):
    """Строка manual_edits.csv."""
    time: str                    # ISO: 2026-11-26T10:15
    chapter: str
    file: str
    what_changed: str
    person_minutes: int
    people: int
    run_no: int
    reason: str


class MetricsRow(Base):
    """Строка metrics.csv: одна на главу и этап (layer, routing, course, video, review)."""
    chapter: str
    stage: Literal["layer", "routing", "course", "video", "review"]
    nodes: int
    llm_tokens_in: int
    llm_tokens_out: int
    money_usd: float
    person_minutes: int
    mentor_minutes: int
    video_seconds: float
    manual_share: float


MANUAL_EDITS_HEADER = ["time", "chapter", "file", "what_changed", "person_minutes", "people", "run_no", "reason"]
METRICS_HEADER = ["chapter", "stage", "nodes", "llm_tokens_in", "llm_tokens_out", "money_usd",
                  "person_minutes", "mentor_minutes", "video_seconds", "manual_share"]
