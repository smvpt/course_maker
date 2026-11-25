"""Задача 2: текст шагов для новичка. layer.json → out/<ch>/course/step_text.json (layer.json не меняется).

Модель переписывает поля узла абзацами; каждый абзац привязан к утверждениям узла (claim_ids), по ним курс
ставит точную «стр. N». Всё, что можно проверить кодом, проверяется здесь: ссылки на утверждения, числа,
длина фраз, 2–3 фразы в сути, термины, покрытие блоков, русский язык. Не прошло — модели возвращается список
ошибок; после трёх попыток шаг считается неудавшимся: курс всё равно собирается, а страница шага строится из
полей слоя (запись об отказе — в step_text.json, предупреждение — в build_report.json).

В курсе результат лежит в node.ext["course"] = {"hash", "paragraphs"} (см. build.apply_step_text).
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Literal, Optional

from contracts.models import Base, Layer, Node
from pydantic import BaseModel, Field

BLOCKS = ("main", "why", "how", "practice", "nuances", "misconception", "decision", "data", "analogy", "deeper")
Block = Literal["main", "why", "how", "practice", "nuances", "misconception", "decision", "data", "analogy", "deeper"]
MAX_WORDS = 20
ATTEMPTS = 3
VIEWER_FILE = "data/organizers/04_доменные_заготовки/портреты_зрителя.md"


class Para(BaseModel):
    block: Block
    text: str = Field(min_length=3)
    claim_ids: list[str]
    terms: list[str] = Field(default_factory=list)   # термины из terms_introduced, введённые в этом абзаце ([[…]] в тексте)
    hypothesis: bool = False                          # абзац — гипотеза (только блок data)
    limit: bool = False                               # абзац — граница аналогии (только блок analogy)


class StepTextOut(BaseModel):
    """Ответ модели по одному узлу."""
    paragraphs: list[Para]


class StepTextNode(Base):
    hash: str
    paragraphs: list[Para]


class StepTextFailure(Base):
    hash: str
    errors: list[str]


class StepText(Base):
    chapter: str
    nodes: dict[str, StepTextNode]
    failed: dict[str, StepTextFailure] = Field(default_factory=dict)   # шаги, где текст не удался: курс берёт поля слоя


class GenerationFailed(ValueError):
    """Ответ модели не прошёл проверки за все попытки."""

    def __init__(self, message: str, errors: list[str]):
        super().__init__(message)
        self.errors = errors


class LlmError(RuntimeError):
    """Отказ модели на одном вызове (исчерпаны повторы, оборванный JSON, нет кэша). Причина — в __cause__.
    Деградирует только узел или слот, где это случилось."""


class LlmAuthError(LlmError):
    """Ошибка авторизации (401/403, нет ключа): модель недоступна для всей главы, повторять бессмысленно."""


class LlmState:
    """Состояние модели на время одной сборки (общее для текста шагов и заданий).

    «Недоступна» — после MAX_IN_A_ROW отказов ПОДРЯД или сразу при ошибке авторизации. Ответ модели, даже не прошедший
    проверки, считается ответом и сбрасывает счётчик."""
    MAX_IN_A_ROW = 3

    def __init__(self) -> None:
        self.down: Optional[str] = None
        self.in_a_row = 0
        self.failures = 0
        self.calls = 0

    def success(self) -> None:
        self.calls += 1
        self.in_a_row = 0

    def failure(self, e: LlmError) -> None:
        self.calls += 1
        self.failures += 1
        if isinstance(e, LlmAuthError):
            self.down = str(e)
            return
        self.in_a_row += 1
        if self.in_a_row >= self.MAX_IN_A_ROW:
            self.down = f"{self.MAX_IN_A_ROW} отказа подряд, последний: {e}"


# ---------------------------------------------------------------- разбор текста

MARK_RE = re.compile(r"\[\[(.+?)\]\]")
NUM_RE = re.compile(r"\d+(?:[.,]\d+)?")


def plain(text: str) -> str:
    return MARK_RE.sub(r"\1", text)


def numbers_in(text: str) -> set[str]:
    out = set()
    for m in NUM_RE.findall(text):
        s = m.replace(",", ".")
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        out.add(s)
    return out


def sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?…])\s+", plain(text).strip()) if s]


def words(sentence: str) -> int:
    return len(re.findall(r"[\w'’-]+", sentence))


def cyrillic_share(text: str) -> float:
    letters = re.findall(r"[^\W\d_]", text)
    if len(letters) < 10:
        return 1.0
    return sum(1 for ch in letters if "Ѐ" <= ch <= "ӿ") / len(letters)


def norm(text: str) -> str:
    return text.lower().replace("ё", "е")


# ---------------------------------------------------------------- источник узла

def _t(f) -> str:
    return f.text if f is not None else ""


def source_text(node: Node) -> str:
    """Всё, из чего модель вправе брать слова и числа."""
    lay, dm = node.layers, node.data_meaning
    parts = [node.title, node.title_novice or "", _t(node.why_here), _t(lay.topic), _t(lay.main), _t(lay.mechanism),
             _t(lay.practice), _t(lay.nuances), _t(node.now_practice), _t(dm.from_chapter), _t(dm.breaks),
             node.it_analogy.text, node.it_analogy.breaks_where, *node.terms_introduced, *node.terms_used]
    parts += [d.text for d in lay.deeper] + [h.text for h in dm.hypotheses]
    parts += [c.text + " " + c.quote for c in node.claims]
    if node.misconception:
        parts.append(node.misconception.text)
    if node.decision_on_data:
        d = node.decision_on_data
        parts += [*d.features, d.rule, d.conclusion, d.counterexample or ""]
    for w in node.worked_examples:
        parts += [w.condition, w.result, *w.steps]
    parts += [t.text for t in node.book_tasks]
    return "\n".join(parts)


def _no_ext(obj):
    if isinstance(obj, dict):
        return {k: _no_ext(v) for k, v in obj.items() if k != "ext"}
    if isinstance(obj, list):
        return [_no_ext(v) for v in obj]
    return obj


def node_dict(node: Node) -> dict:
    """Узел без служебных ext (в том числе вложенных): то, что видит модель и что попадает в хэш."""
    return _no_ext(node.model_dump(mode="json", by_alias=True))


def node_hash(node: Node) -> str:
    raw = json.dumps(node_dict(node), ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _has(f) -> bool:
    return f is not None and bool(f.text.strip())


def required_blocks(node: Node) -> set[str]:
    """Блоки, у которых в узле есть исходный текст. Только они и могут быть в ответе."""
    lay, dm = node.layers, node.data_meaning
    text_claims = [c for c in node.claims if c.source_kind not in ("formula", "table")]
    req = {
        "main": _has(lay.main),
        "why": _has(node.why_here),
        "how": _has(lay.mechanism) or bool(text_claims),
        "practice": _has(lay.practice) or _has(node.now_practice),
        "nuances": _has(lay.nuances),
        "misconception": node.misconception is not None and bool(node.misconception.text.strip()),
        "decision": node.decision_on_data is not None,
        "data": _has(dm.from_chapter) or _has(dm.breaks) or any(_has(h) for h in dm.hypotheses),
        "analogy": bool(node.it_analogy.text.strip()),
        "deeper": any(_has(d) for d in lay.deeper),
    }
    return {b for b, on in req.items() if on}


# ---------------------------------------------------------------- проверка ответа модели

def validate_node(node: Node, paras: list[Para]) -> list[str]:
    errors: list[str] = []
    claim_ids = {c.id for c in node.claims}
    src_numbers = numbers_in(source_text(node))
    required = required_blocks(node)
    seen_blocks = {p.block for p in paras}

    for b in sorted(required - seen_blocks):
        errors.append(f"нет абзацев блока «{b}», хотя в узле для него есть текст")
    for b in sorted(seen_blocks - required):
        errors.append(f"блок «{b}» не нужен: в узле нет для него исходного текста (ничего не выдумывай)")

    term_count: dict[str, int] = {}
    for i, p in enumerate(paras, 1):
        tag = f"абзац {i} ({p.block})"
        if not p.claim_ids:
            errors.append(f"{tag}: пустой claim_ids")
        for cid in p.claim_ids:
            if cid not in claim_ids:
                errors.append(f"{tag}: claim_id {cid!r} нет в узле")
        for s in sentences(p.text):
            n = words(s)
            if n > MAX_WORDS:
                errors.append(f"{tag}: фраза из {n} слов (максимум {MAX_WORDS}): «{s}»")
        extra_nums = sorted(numbers_in(plain(p.text)) - src_numbers)
        if extra_nums:
            errors.append(f"{tag}: числа {extra_nums} нет в узле — числа берутся только из узла")
        if cyrillic_share(plain(p.text)) < 0.5:
            errors.append(f"{tag}: текст курса должен быть на русском (цитаты автора сюда не вставляй)")
        marks = MARK_RE.findall(p.text)
        if len(marks) != len(p.terms):
            errors.append(f"{tag}: [[…]] в тексте {len(marks)}, а в terms {len(p.terms)}: выдели ровно те термины, что перечислены в terms")
        for t in p.terms:
            if t not in node.terms_introduced:
                errors.append(f"{tag}: термин {t!r} не из terms_introduced узла")
            term_count[t] = term_count.get(t, 0) + 1
        if p.hypothesis and p.block != "data":
            errors.append(f"{tag}: hypothesis=true допустим только в блоке data")
        if p.limit and p.block != "analogy":
            errors.append(f"{tag}: limit=true допустим только в блоке analogy")

    for t in node.terms_introduced:
        if term_count.get(t, 0) != 1:
            errors.append(f"термин {t!r} должен быть выделен [[…]] и объяснён ровно в одном абзаце (сейчас {term_count.get(t, 0)})")

    main = [s for p in paras if p.block == "main" for s in sentences(p.text)]
    if "main" in required and not 2 <= len(main) <= 3:
        errors.append(f"суть («main») должна быть 2–3 фразы, сейчас {len(main)}")
    if node.data_meaning.hypotheses and any(_has(h) for h in node.data_meaning.hypotheses):
        if not any(p.hypothesis for p in paras if p.block == "data"):
            errors.append("в узле есть гипотезы: в блоке data нужен абзац с hypothesis=true")
    if node.it_analogy.breaks_where.strip() and node.it_analogy.text.strip():
        if sum(1 for p in paras if p.limit) != 1:
            errors.append("аналогия должна иметь ровно один абзац с limit=true — границу, где она перестаёт работать")
    return errors


# ---------------------------------------------------------------- вызов модели

PAUSES = (2, 5, 10)                                   # секунды перед повтором временной ошибки
TRANSIENT_STATUS = {408, 425, 429, 500, 502, 503, 504, 529}
TRANSIENT_NAMES = {"Timeout", "APITimeoutError", "APIConnectionError", "RateLimitError", "ServiceUnavailableError",
                   "InternalServerError", "BadGatewayError", "TimeoutError", "ConnectionError"}
AUTH_NAMES = {"AuthenticationError", "PermissionDeniedError"}


def _pause(seconds: float) -> None:
    time.sleep(seconds)


def classify(e: Exception) -> str:
    """auth | transient | other. llm.py (зона П1) сам не повторяет запросы и типы ошибок litellm не оборачивает."""
    names = {c.__name__ for c in type(e).__mro__}
    status = getattr(e, "status_code", None)
    if status in (401, 403) or names & AUTH_NAMES or "LLM_API_KEY" in str(e):
        return "auth"
    if status in TRANSIENT_STATUS or names & TRANSIENT_NAMES or isinstance(e, (TimeoutError, ConnectionError)):
        return "transient"
    return "other"


def call_llm(**kw):
    from pipeline.llm import complete_json as impl   # точка входа в LLM — только pipeline.llm (CLAUDE.md §2)
    for attempt in range(len(PAUSES) + 1):
        try:
            return impl(**kw)
        except (KeyError, TypeError, FileNotFoundError):
            raise        # нет промпта, не хватает переменной: это наша ошибка, не отказ модели — падаем громко
        except Exception as e:
            kind = classify(e)
            if kind == "auth":
                raise LlmAuthError(f"{type(e).__name__}: {e}") from e
            if kind == "transient" and attempt < len(PAUSES):
                _pause(PAUSES[attempt])
                continue
            raise LlmError(f"{type(e).__name__}: {e}") from e


def complete_json(**kw):
    return call_llm(**kw)


def quote_language(layer: Layer) -> str:
    quotes = " ".join(c.quote for n in layer.nodes for c in n.claims)
    return "ru" if cyrillic_share(quotes) >= 0.5 else "en"


def generate_node(node: Node, language: str, viewer: str) -> list[Para]:
    node_json = json.dumps(node_dict(node), ensure_ascii=False, indent=1)
    feedback = "нет, это первая попытка"
    for _ in range(ATTEMPTS):
        out = complete_json(prompt="course/step_page", schema=StepTextOut, tier="default",
                            vars={"node": node_json, "viewer": viewer, "language": language, "feedback": feedback})
        errors = validate_node(node, out.paragraphs)
        if not errors:
            return out.paragraphs
        feedback = "\n".join(f"- {e}" for e in errors)
    raise GenerationFailed(f"{node.id}: текст шага не прошёл проверку за {ATTEMPTS} попытки:\n{feedback}",
                           [e.removeprefix("- ") for e in feedback.splitlines()])


def read_step_text(path: Path, ch: str) -> Optional[StepText]:
    if not path.exists():
        return None
    st = StepText.model_validate_json(path.read_text(encoding="utf-8"))
    if st.chapter != ch:
        raise ValueError(f"{path}: chapter={st.chapter!r}, а запрошена глава {ch!r}")
    return st


def load_step_text(path: Path, ch: str) -> dict[str, StepTextNode]:
    st = read_step_text(path, ch)
    return st.nodes if st else {}


def ensure_step_text(layer: Layer, course_dir: Path, only: Optional[str] = None,
                     state: Optional[LlmState] = None) -> dict[str, StepTextNode]:
    """Дописывает step_text.json: новые, изменившиеся и ранее неудавшиеся узлы генерируются, остальные берутся из файла.

    Не прошло проверки или модель отказала на этом узле — отказ записывается в failed, остальные шаги продолжаются.
    Модель недоступна (3 отказа подряд или авторизация) — остальные шаги записываются как неудавшиеся без обращений к ней."""
    state = state or LlmState()
    path = course_dir / "step_text.json"
    old = read_step_text(path, layer.chapter)
    ids = {n.id for n in layer.nodes}
    nodes = {k: v for k, v in (old.nodes if old else {}).items() if k in ids}
    failed = {k: v for k, v in (old.failed if old else {}).items() if k in ids}
    viewer = (Path(__file__).resolve().parents[2] / VIEWER_FILE).read_text(encoding="utf-8")
    language = quote_language(layer)
    for n in layer.nodes:
        if only is not None and n.id != only:
            continue
        h = node_hash(n)
        if n.id in nodes and nodes[n.id].hash == h:
            continue
        nodes.pop(n.id, None)
        if state.down is not None:
            failed[n.id] = StepTextFailure(hash=h, errors=[f"модель недоступна: {state.down}"])
            continue
        try:
            nodes[n.id] = StepTextNode(hash=h, paragraphs=generate_node(n, language, viewer))
            failed.pop(n.id, None)
            state.success()
        except GenerationFailed as e:
            failed[n.id] = StepTextFailure(hash=h, errors=e.errors)
            state.success()                                # модель ответила, просто неверно
        except LlmError as e:
            state.failure(e)
            reason = f"модель недоступна: {state.down}" if state.down else f"отказ модели: {e}"
            failed[n.id] = StepTextFailure(hash=h, errors=[reason])
    course_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(StepText(chapter=layer.chapter, nodes=nodes, failed=failed).model_dump_json(by_alias=True, indent=2),
                    encoding="utf-8")
    return nodes
