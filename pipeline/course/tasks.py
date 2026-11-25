"""Задача 3: задания курса. layer.json → out/<ch>/course/tasks.json (модель Tasks, схема организаторов task.schema.json).

Что делает модель: придумывает формулировки и варианты по узлу, неверные варианты строит на заблуждениях.
Что делает код: распределяет типы и виды заданий по главе (≥15, все 5 типов, хотя бы одно kind=data), проверяет
каждое задание, перемешивает варианты, ЗАДАЁТ ID, а ответ в calc ВЫЧИСЛЯЕТ (Python, безопасный разбор выражения):
модель даёт только переменные из узла и выражение по формуле главы, числа в ответе от неё не берутся.
Не прошло проверку — модели возвращается список ошибок только по этому заданию; после трёх попыток задание
выбрасывается (запись в tasks.json → ext.course.dropped, предупреждение в build_report.json), курс собирается с тем,
что есть. Меньше 15 заданий или невозможный тип — тоже предупреждение, не ошибка.
"""
from __future__ import annotations

import ast
import json
import math
import random
import sys
from pathlib import Path
from typing import Literal, Optional

from contracts.models import Layer, Node, Task, TaskOption, Tasks
from pipeline.course.steptext import (LlmError, LlmState, call_llm, cyrillic_share, node_dict, node_hash, norm, numbers_in, sentences, source_text,
                                      words, VIEWER_FILE, quote_language)
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[2]
ROTATION = ("single", "multiple", "gap", "order", "calc")
KINDS = ("recall", "understanding", "transfer", "data")
MIN_TASKS = 15
CAP_PER_NODE = 8
ATTEMPTS = 3
LETTERS = "abcdefgh"
FUNCS = {"sqrt": math.sqrt, "log": math.log, "ln": math.log, "log10": math.log10, "exp": math.exp}
SMALL_CONSTANTS = {"1", "2", "3", "4", "5", "10", "100"}   # безразмерные множители формул; остальные числа — только из узла


class LlmOption(BaseModel):
    text: str
    correct: bool = False                    # single/multiple. Для order порядок — это порядок в списке
    misconception: Optional[str] = None      # только у неверных вариантов: id заблуждения


class LlmCalc(BaseModel):
    variables: dict[str, float]              # имя → число ИЗ УЗЛА (из условия задачи)
    expression: str                          # выражение по формуле главы, только + - * / ** скобки sqrt log log10 exp
    unit: str = ""


class LlmTask(BaseModel):
    type: Literal["single", "multiple", "order", "gap", "calc"]
    kind: Literal["recall", "understanding", "transfer", "data"]
    claim_ids: list[str]
    prompt: str
    options: list[LlmOption] = Field(default_factory=list)
    gap_answers: list[str] = Field(default_factory=list)
    calc: Optional[LlmCalc] = None
    explanation: str


class LlmTasks(BaseModel):
    tasks: list[LlmTask]


# ---------------------------------------------------------------- план главы

def calc_capable(node: Node) -> bool:
    if any(c.source_kind == "formula" for c in node.claims):
        return True
    return any(len(numbers_in(w.condition)) >= 2 for w in node.worked_examples)


def _data_capable(node: Node) -> bool:
    dm = node.data_meaning
    return node.decision_on_data is not None or bool(dm.from_chapter.text.strip() or dm.breaks.text.strip())


def plan(nodes: list[Node]) -> dict[str, list[dict]]:
    """node_id → [{"type", "kind"}]. Зависит только от слоя: на одной главе план всегда один.
    Мало узлов — заданий получится меньше MIN_TASKS: это предупреждение check_chapter, а не ошибка."""
    n = len(nodes)
    per = min(CAP_PER_NODE, max(1, math.ceil(MIN_TASKS / n)))
    out: dict[str, list[dict]] = {}
    counter = 0
    for node in nodes:
        slots = []
        for _ in range(per):
            t = ROTATION[counter % len(ROTATION)]
            counter += 1
            while t == "calc" and not calc_capable(node):      # расчёт — только там, где есть формула или числа
                t = ROTATION[counter % len(ROTATION)]
                counter += 1
            slots.append({"type": t, "kind": KINDS[(counter - 1) % len(KINDS)]})
        out[node.id] = slots
    capable = [n for n in nodes if calc_capable(n)]
    if capable and not any(s["type"] == "calc" for ss in out.values() for s in ss):
        out[capable[0].id][-1]["type"] = "calc"
    # хотя бы одно задание «на данных»: у узла с решением на данных, иначе у узла со смыслом для данных
    if not any(s["kind"] == "data" for ss in out.values() for s in ss):
        host = next((n for n in nodes if n.decision_on_data is not None), None) or next((n for n in nodes if _data_capable(n)), None)
        if host is not None:
            out[host.id][0]["kind"] = "data"
    for n in nodes:                                           # узлу с решением на данных — своё задание на данных
        if n.decision_on_data is not None and not any(s["kind"] == "data" for s in out[n.id]):
            out[n.id][0]["kind"] = "data"
    return out


# ---------------------------------------------------------------- расчёт кодом

class _ToFloat(ast.NodeTransformer):
    def visit_Constant(self, node: ast.Constant) -> ast.Constant:
        return ast.copy_location(ast.Constant(float(node.value)), node)


def safe_eval(expression: str, variables: dict[str, float], allowed_numbers: set[str]) -> float:
    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError as e:
        raise ValueError(f"выражение {expression!r} не разобрать: {e.msg}")
    used: set[str] = set()

    def check(n: ast.AST) -> None:
        if isinstance(n, ast.Expression):
            check(n.body)
        elif isinstance(n, ast.BinOp) and isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
            check(n.left)
            check(n.right)
        elif isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            check(n.operand)
        elif isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
            if numbers_in(repr(n.value)) - allowed_numbers - SMALL_CONSTANTS:
                raise ValueError(f"в выражении число {n.value}: его нет в узле (допустимы только числа узла и {sorted(SMALL_CONSTANTS, key=int)})")
        elif isinstance(n, ast.Name) and n.id in variables:
            used.add(n.id)
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in FUNCS and not n.keywords:
            for a in n.args:
                check(a)
        else:
            raise ValueError(f"в выражении {expression!r} недопустима часть {ast.dump(n)[:50]}")

    check(tree)
    unused = sorted(set(variables) - used)
    if unused:
        raise ValueError(f"переменные {unused} не используются в выражении {expression!r}")
    # Всё считаем во float: целая степень вроде 10**10**10 иначе вычисляется бесконечно, а у float это быстрый OverflowError.
    tree = ast.fix_missing_locations(_ToFloat().visit(tree))
    env = {**FUNCS, **{k: float(v) for k, v in variables.items()}}
    try:
        value = float(eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, env))   # noqa: S307 — дерево проверено выше
    except (ZeroDivisionError, ValueError, OverflowError, TypeError) as e:     # TypeError: комплексный результат
        raise ValueError(f"выражение {expression!r} не вычисляется: {e}")
    if not math.isfinite(value):
        raise ValueError(f"выражение {expression!r} даёт не число")
    return value


def _fmt_number(v: float) -> str:
    return numbers_in(f"{v:.10f}").pop()


# ---------------------------------------------------------------- проверка одного задания

def _check_text_russian(tag: str, text: str, errors: list[str]) -> None:
    if cyrillic_share(text) < 0.5:
        errors.append(f"{tag}: текст курса должен быть на русском")


def validate_task(node: Node, t: LlmTask, planned: dict, misc_ids: set[str], tag: str) -> list[str]:
    errors: list[str] = []
    src = source_text(node)
    src_numbers = numbers_in(src)
    claim_ids = {c.id for c in node.claims}
    if t.type != planned["type"] or t.kind != planned["kind"]:
        errors.append(f"{tag}: нужен type={planned['type']}, kind={planned['kind']}, а пришло type={t.type}, kind={t.kind}")
    if not t.claim_ids:
        errors.append(f"{tag}: пустой claim_ids")
    for cid in t.claim_ids:
        if cid not in claim_ids:
            errors.append(f"{tag}: claim_id {cid!r} нет в узле")
    _check_text_russian(tag, t.prompt, errors)
    _check_text_russian(tag + " (пояснение)", t.explanation, errors)
    if len(sentences(t.explanation)) != 1 or words(t.explanation) > 30:
        errors.append(f"{tag}: пояснение должно быть одной фразой до 30 слов")
    texts = [norm(o.text.strip()) for o in t.options]
    if len(set(texts)) != len(texts) or any(not x for x in texts):
        errors.append(f"{tag}: тексты вариантов должны быть непустыми и разными")
    for o in t.options:
        _check_text_russian(tag + " (вариант)", o.text, errors)
        if o.misconception is not None and (o.correct or t.type == "order"):
            errors.append(f"{tag}: misconception допустим только у неверных вариантов single/multiple")
        if o.misconception is not None and o.misconception not in misc_ids:
            errors.append(f"{tag}: заблуждения {o.misconception!r} нет в списке (используй id из списка или null)")

    n_opts, n_correct = len(t.options), sum(1 for o in t.options if o.correct)
    if t.type == "single":
        if not 3 <= n_opts <= 4 or n_correct != 1:
            errors.append(f"{tag}: single — 3–4 варианта и ровно один верный (сейчас {n_opts} и {n_correct})")
    elif t.type == "multiple":
        if not 4 <= n_opts <= 5 or not 2 <= n_correct <= n_opts - 1:
            errors.append(f"{tag}: multiple — 4–5 вариантов, верных от 2 и хотя бы один неверный (сейчас {n_opts} и {n_correct})")
    elif t.type == "order":
        if not 3 <= n_opts <= 5:
            errors.append(f"{tag}: order — 3–5 элементов в правильном порядке (сейчас {n_opts})")
    else:
        if t.options:
            errors.append(f"{tag}: у {t.type} поле options должно быть пустым")

    if t.type == "gap":
        k = len(t.gap_answers)
        if k == 0 or any(f"{{{{{i}}}}}" not in t.prompt for i in range(1, k + 1)) or t.prompt.count("{{") != k:
            errors.append(f"{tag}: gap — в prompt пропуски {{{{1}}}}…{{{{{k}}}}} подряд, по числу gap_answers (сейчас gap_answers={k})")
        for a in t.gap_answers:
            if not a.strip() or len(a.split()) > 2 or norm(a.strip()) not in norm(src):
                errors.append(f"{tag}: слово пропуска {a!r} не найдено в тексте узла в такой форме (ответ должен быть в тексте шага; не больше 2 слов)")
    elif t.gap_answers:
        errors.append(f"{tag}: gap_answers только у gap")

    if t.type == "calc":
        if t.calc is None:
            errors.append(f"{tag}: у calc нужно поле calc")
        else:
            prompt_numbers = numbers_in(t.prompt)
            for name, v in t.calc.variables.items():
                nv = {_fmt_number(v)}
                if not nv <= src_numbers:
                    errors.append(f"{tag}: значения {name}={v} нет в узле")
                if not nv <= prompt_numbers:
                    errors.append(f"{tag}: значения {name}={v} нет в условии (prompt): все числа расчёта должны быть в условии")
            try:
                safe_eval(t.calc.expression, t.calc.variables, src_numbers)
            except ValueError as e:
                errors.append(f"{tag}: {e}")
            extra = prompt_numbers - src_numbers
            if extra:
                errors.append(f"{tag}: числа {sorted(extra)} из условия нет в узле")
    elif t.calc is not None:
        errors.append(f"{tag}: поле calc только у calc")
    return errors


def validate_node_tasks(node: Node, tasks: list[LlmTask], planned: list[dict], misc_ids: set[str]) -> list[str]:
    if len(tasks) != len(planned):
        return [f"нужно ровно {len(planned)} заданий в заданном порядке типов, пришло {len(tasks)}"]
    errors: list[str] = []
    for i, (t, p) in enumerate(zip(tasks, planned), 1):
        errors += validate_task(node, t, p, misc_ids, f"задание {i}")
    ref = node.misconception.ref if node.misconception else None
    choice = [t for t in tasks if t.type in ("single", "multiple")]
    if ref and choice and not any(o.misconception == ref for t in choice for o in t.options):
        errors.append(f"в узле есть заблуждение {ref!r}: хотя бы один неверный вариант в single/multiple должен строиться на нём (misconception={ref!r})")
    return errors


# ---------------------------------------------------------------- сборка Task

def _rng(task_id: str) -> random.Random:
    return random.Random(task_id)


def build_task(node: Node, t: LlmTask, task_id: str) -> Task:
    rng = _rng(task_id)
    common = dict(id=task_id, type=t.type, step_id=node.id, claim_ids=t.claim_ids, prompt=t.prompt.strip(),
                  explanation=t.explanation.strip(), kind=t.kind)
    if t.type in ("single", "multiple"):
        opts = list(t.options)
        rng.shuffle(opts)
        options = [TaskOption(id=LETTERS[i], text=o.text.strip(), misconception=None if o.correct else o.misconception)
                   for i, o in enumerate(opts)]
        right = [options[i].id for i, o in enumerate(opts) if o.correct]
        return Task(**common, options=options, answer=right[0] if t.type == "single" else right)
    if t.type == "order":
        items = [TaskOption(id=f"o{i + 1}", text=o.text.strip()) for i, o in enumerate(t.options)]
        shown = list(items)
        for _ in range(50):
            rng.shuffle(shown)
            if [x.id for x in shown] != [x.id for x in items]:
                break
        else:
            shown = items[1:] + items[:1]
        return Task(**common, options=shown, answer=[x.id for x in items])
    if t.type == "gap":
        return Task(**common, options=[], answer=[a.strip() for a in t.gap_answers])
    value = round(safe_eval(t.calc.expression, t.calc.variables, numbers_in(source_text(node))), 6)
    return Task(**common, options=[], answer=value, tolerance=max(round(abs(value) * 0.01, 6), 1e-6),
                unit=t.calc.unit.strip() or None)


# ---------------------------------------------------------------- вызов модели

def complete_json(**kw):
    return call_llm(**kw)


def generate_node_tasks(node: Node, planned: list[dict], misconceptions: list[dict], language: str, viewer: str
                        ) -> tuple[list[Task], list[dict], list[dict], Optional[LlmError]]:
    """Задания узла. Возвращает (прошедшие проверку, выброшенные, предупреждения узла, отказ модели или None).

    Проверка идёт по каждому заданию отдельно: на следующую попытку модели возвращаются только слоты, которые не
    прошли, с их ошибками. После ATTEMPTS попыток оставшиеся слоты выбрасываются. Отказ модели (LlmError) обрывает
    попытки этого узла: уже принятые задания остаются, остальные слоты выбрасываются с причиной; сам отказ
    возвращается четвёртым значением, чтобы ensure_tasks учёл его в состоянии модели."""
    misc_ids = {m["id"] for m in misconceptions}
    catalogue = list(misconceptions)
    if node.misconception and node.misconception.ref and node.misconception.ref not in misc_ids:
        catalogue.append({"id": node.misconception.ref, "text": node.misconception.text})
        misc_ids.add(node.misconception.ref)
    done: dict[int, LlmTask] = {}
    errors: dict[int, list[str]] = {}
    pending = list(range(len(planned)))
    feedback = "нет, это первая попытка"
    failure: Optional[LlmError] = None
    for _ in range(ATTEMPTS):
        requested = [planned[i] for i in pending]
        try:
            out = complete_json(prompt="course/tasks", schema=LlmTasks, tier="default",
                                vars={"node": json.dumps(node_dict(node), ensure_ascii=False, indent=1),
                                      "requested": json.dumps(requested, ensure_ascii=False),
                                      "misconceptions": json.dumps(catalogue, ensure_ascii=False, indent=1),
                                      "viewer": viewer, "language": language, "feedback": feedback})
        except LlmError as e:
            failure = e
            for slot in pending:
                errors[slot] = [f"отказ модели: {e}"]
            break
        still: list[int] = []
        for pos, slot in enumerate(pending):
            if pos >= len(out.tasks):
                errors[slot] = ["модель не вернула это задание"]
                still.append(slot)
                continue
            errs = validate_task(node, out.tasks[pos], planned[slot], misc_ids, f"задание {slot + 1}")
            if errs:
                errors[slot] = errs
                still.append(slot)
            else:
                done[slot] = out.tasks[pos]
                errors.pop(slot, None)
        pending = still
        if not pending:
            break
        feedback = "\n".join(f"- {e}" for slot in pending for e in errors[slot])
    tasks = [build_task(node, done[i], f"{node.id}.t{i + 1}") for i in sorted(done)]
    dropped = [{"node": node.id, "slot": i + 1, "type": planned[i]["type"], "errors": errors[i]} for i in pending]
    warnings: list[dict] = []
    ref = node.misconception.ref if node.misconception else None
    choice = [t for t in done.values() if t.type in ("single", "multiple")]
    if ref and choice and not any(o.misconception == ref for t in choice for o in t.options):
        warnings.append({"code": "misconception_unused", "node": node.id, "ref": ref,
                         "message": f"шаг {node.id}: ни один неверный вариант не построен на заблуждении {ref}"})
    return tasks, dropped, warnings, failure


# ---------------------------------------------------------------- глава целиком

def check_chapter(layer: Layer, tasks: list[Task], emit: bool = True) -> list[dict]:
    """Требования главы (≥15, все 5 типов, хотя бы одно kind=data). Нарушения — предупреждения, не ошибки."""
    warnings: list[dict] = []

    def warn(code: str, message: str, **extra) -> None:
        warnings.append({"code": code, "message": message, **extra})
        if emit:
            print(f"WARNING: {message}", file=sys.stderr)

    if len(tasks) < MIN_TASKS:
        warn("few_tasks", f"заданий {len(tasks)}, нужно не меньше {MIN_TASKS}", count=len(tasks))
    if tasks and not any(t.kind == "data" for t in tasks):
        warn("no_data_task", "нет ни одного задания kind=data")
    types = {t.type for t in tasks}
    missing = [t for t in ROTATION if t not in types]
    if "calc" in missing and not any(calc_capable(n) for n in layer.nodes):
        warn("calc_not_possible", "в главе нет формул и чисел для расчёта: заданий calc нет")
        missing.remove("calc")
    if missing and tasks:
        warn("missing_task_type", f"нет заданий типов: {', '.join(missing)}", types=missing)
    return warnings


def load_tasks(path: Path, ch: str) -> Optional[Tasks]:
    if not path.exists():
        return None
    t = Tasks.model_validate_json(path.read_text(encoding="utf-8"))
    if t.chapter != ch:
        raise ValueError(f"{path}: chapter={t.chapter!r}, а запрошена глава {ch!r}")
    return t


def ensure_tasks(layer: Layer, course_dir: Path, misconceptions: list[dict], only: Optional[str] = None,
                 state: Optional[LlmState] = None) -> Tasks:
    """Дописывает tasks.json: узлы без заданий, изменившиеся (по хэшу) и с ранее выброшенными заданиями генерируются
    заново, остальные берутся из файла. Отказ модели деградирует только слоты своего узла. Модель недоступна
    (3 отказа подряд или авторизация) — слоты остальных узлов выбрасываются без обращений к ней."""
    state = state or LlmState()
    path = course_dir / "tasks.json"
    old = load_tasks(path, layer.chapter)
    oc = old.ext.get("course", {}) if old else {}
    old_hashes = oc.get("hashes", {})
    retry = {d["node"] for d in oc.get("dropped", [])}
    viewer = (ROOT / VIEWER_FILE).read_text(encoding="utf-8")
    language = quote_language(layer)
    planned = plan(layer.nodes)
    by_node: dict[str, list[Task]] = {n.id: [t for t in (old.tasks if old else []) if t.step_id == n.id] for n in layer.nodes}
    hashes = {n.id: old_hashes[n.id] for n in layer.nodes if n.id in old_hashes and (by_node[n.id] or n.id in retry)}
    dropped = [d for d in oc.get("dropped", []) if d["node"] in by_node]
    node_warnings = [w for w in oc.get("node_warnings", []) if w["node"] in by_node]
    generated_all = True
    for n in layer.nodes:
        if only is not None and n.id != only:
            generated_all = generated_all and bool(hashes.get(n.id))
            continue
        h = node_hash(n)
        if hashes.get(n.id) == h and n.id not in retry:
            continue
        dropped = [d for d in dropped if d["node"] != n.id]
        node_warnings = [w for w in node_warnings if w["node"] != n.id]
        if state.down is None:
            by_node[n.id], new_dropped, new_warnings, failure = generate_node_tasks(n, planned[n.id], misconceptions, language, viewer)
            if failure is not None:
                state.failure(failure)
            else:
                state.success()
        else:
            by_node[n.id] = []
            new_dropped = [{"node": n.id, "slot": i + 1, "type": s["type"], "errors": [f"модель недоступна: {state.down}"]}
                           for i, s in enumerate(planned[n.id])]
            new_warnings = []
        dropped += new_dropped
        node_warnings += new_warnings
        hashes[n.id] = h
    tasks = [t for n in layer.nodes for t in by_node[n.id]]
    # если модель недоступна, «мало заданий» и т. п. — следствие простоя: оно уже описано как model_unavailable
    warnings = check_chapter(layer, tasks, emit=False) if (only is None or generated_all) and state.down is None else []
    result = Tasks(chapter=layer.chapter, tasks=tasks,
                   ext={"course": {"hashes": hashes, "warnings": warnings, "dropped": dropped, "node_warnings": node_warnings}})
    course_dir.mkdir(parents=True, exist_ok=True)
    path.write_text(result.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    return result
