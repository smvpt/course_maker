"""Проверки кодом того, что вернула модель: сценарий и спецификация сцены против узла слоя.

Возвращают список проблем (пустой — всё в порядке); тексты проблем уходят модели как
замечания для повторной попытки и пользователю в ошибке.
"""
from __future__ import annotations

import math
import re

from contracts.models import Node, SceneSpec, Script, SourceRow
from pipeline.video.inputs import ID_RE, shot_link_problems

MAX_WORDS = 18
MAX_ON_SCREEN_WORDS = 8
ESTIMATE_WPM = 130                       # середина допустимых 110–150 слов/мин
DURATION_S = {"short": (40, 75), "long": (90, 180)}
PREDICTION_PAUSE_S = (1.0, 1.5)
ORDER = [("hook", "problem"), ("problem", "solution"), ("solution", "naming"),
         ("data", "decision"), ("decision", "transfer")]
REQUIRED_BEATS = ("hook", "problem", "solution", "naming", "prediction", "data", "decision", "transfer")
# класс кадра → допустимые метки. «реальные данные» не допускаются: датасеты к роликам ещё не подключены.
ALLOWED_LABELS = {"A": {"симуляция"}, "B": {"симуляция", "схема"}, "D": {"схема"}}

WORD_RE = re.compile(r"[^\W_]+(?:-[^\W_]+)*")
NUM_RE = re.compile(r"\d+(?:[.,]\d+)?")
FORMULA_RE = re.compile(r"[=Ͱ-Ͽ√∑∫^]")


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def estimate_duration(script: Script) -> float:
    """Оценка ДО синтеза: слова при ESTIMATE_WPM + паузы. Не замер."""
    words = sum(count_words(p.text) for p in script.phrases)
    return round(words / ESTIMATE_WPM * 60 + sum(max(p.pause_after_s, 0) for p in script.phrases), 1)


def check_script(script: Script, node: Node, fmt: str) -> list[str]:
    problems: list[str] = []
    ph = script.phrases
    if not ph:
        return ["в сценарии нет фраз"]
    claims = {c.id: c for c in node.claims}
    claim_ids = set(claims)
    ids = [p.id for p in ph]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        problems.append(f"id фраз повторяются: {dup}")

    for p in ph:
        tag = f"фраза {p.id}"
        if not ID_RE.match(p.id):
            problems.append(f"{tag}: id только из [a-z0-9_.-]")
        if not p.text.strip():
            problems.append(f"{tag}: пустой текст")
        n = count_words(p.text)
        if n > MAX_WORDS:
            problems.append(f"{tag}: {n} слов, допустимо не больше {MAX_WORDS}")
        if re.search(r"\d", p.text):
            problems.append(f"{tag}: в речи цифры — числа и единицы нужно писать словами")
        if p.claim_id is None:
            problems.append(f"{tag}: нет claim_id — каждая фраза опирается на утверждение узла")
        elif p.claim_id not in claim_ids:
            problems.append(f"{tag}: claim_id {p.claim_id} не принадлежит узлу {node.id}; "
                            f"допустимы {sorted(claim_ids)}")
        if p.pause_after_s < 0:
            problems.append(f"{tag}: отрицательная пауза {p.pause_after_s}")
        if p.on_screen is not None:
            k = count_words(p.on_screen)
            if k > MAX_ON_SCREEN_WORDS:
                problems.append(f"{tag}: подпись on_screen из {k} слов, допустимо не больше {MAX_ON_SCREEN_WORDS}")
            if FORMULA_RE.search(p.on_screen):
                problems.append(f"{tag}: подпись on_screen без формул, «=» и греческих букв")
            # число на экране подтверждается только текстом и цитатой связанного утверждения,
            # не id, ссылками, номерами страниц и прочими метаданными узла
            claim = claims.get(p.claim_id)
            source_numbers = set(NUM_RE.findall(claim.text + "\n" + claim.quote)) if claim else set()
            for num in NUM_RE.findall(p.on_screen):
                if num not in source_numbers:
                    problems.append(f"{tag}: число {num} в подписи не подтверждено текстом и цитатой "
                                    f"утверждения {p.claim_id}")
        if p.is_analogy and "аналог" not in p.text.lower():
            problems.append(f"{tag}: аналогия должна быть названа аналогией прямо в тексте")

    beats = [p.beat for p in ph]
    if beats[0] != "hook":
        problems.append("первая фраза должна быть hook — вопрос или парадокс в первые 3 секунды")
    first = {}
    for i, b in enumerate(beats):
        first.setdefault(b, i)
    for b in REQUIRED_BEATS:
        if b not in first:
            problems.append(f"нет фразы с beat {b}")
    for a, b in ORDER:
        if a in first and b in first and first[a] > first[b]:
            problems.append(f"порядок нарушен: {a} должен идти раньше {b}")
    if "transfer" in first and any(b not in ("transfer", "final") for b in beats[first["transfer"]:]):
        problems.append("после вопроса на перенос (transfer) допустимы только фразы final")
    for i, p in enumerate(ph):
        if p.beat == "prediction":
            lo, hi = PREDICTION_PAUSE_S
            if not lo <= p.pause_after_s <= hi:
                problems.append(f"фраза {p.id}: пауза после предсказания {p.pause_after_s} с, нужно {lo}–{hi} с")
            if not p.text.rstrip().endswith("?"):
                problems.append(f"фраза {p.id}: предсказание — вопрос, должно кончаться «?»")
            if i == len(ph) - 1:
                problems.append(f"фраза {p.id}: после предсказания нужен ответ")
        if p.beat == "transfer" and not p.text.rstrip().endswith("?"):
            problems.append(f"фраза {p.id}: вопрос на перенос должен кончаться «?»")

    for field in ("prediction_question", "transfer_question", "data_it_bridge"):
        if not getattr(script, field).strip():
            problems.append(f"пустое поле {field}")

    lo, hi = DURATION_S[fmt]
    est = estimate_duration(script)
    if not lo <= est <= hi:
        problems.append(f"оценочная длительность {est} с вне {lo}–{hi} с для формата {fmt} "
                        f"(оценка: {ESTIMATE_WPM} слов/мин + паузы)")
    return problems


def check_scene(spec: SceneSpec, script: Script, real_data_ok: bool = False) -> list[str]:
    """real_data_ok — набор данных ролика подтверждён как реальный: тогда классу A можно «реальные данные»."""
    problems = shot_link_problems(script, spec)
    allowed_labels = {**ALLOWED_LABELS, "A": ALLOWED_LABELS["A"] | ({"реальные данные"} if real_data_ok else set())}
    flat = [pid for s in spec.shots for pid in s.phrase_ids]
    order = [p.id for p in script.phrases]
    if sorted(flat) == sorted(order) and flat != order:
        problems.append("кадры должны идти в порядке фраз: phrase_ids кадров подряд = порядок сценария")
    if not spec.shots:
        problems.append("нет кадров")
    for s in spec.shots:
        allowed = allowed_labels.get(s.frame_class)
        if allowed is None:
            problems.append(f"кадр {s.id}: класс {s.frame_class} не используется (нет фото-источников)")
        elif s.label not in allowed:
            problems.append(f"кадр {s.id}: класс {s.frame_class} с меткой «{s.label}» недопустим, "
                            f"можно {sorted(allowed)}; «реальные данные» — только при подключённом датасете")
        if s.plaque is not None:
            if not s.plaque.lower().startswith("не в масштабе"):
                problems.append(f"кадр {s.id}: плашка должна начинаться с «не в масштабе»")
            elif not re.search(r"\d", s.plaque):
                problems.append(f"кадр {s.id}: в плашке нет числа — что и во сколько раз увеличено")
    for e in spec.exaggerations:
        if not re.search(r"\d", e):
            problems.append(f"преувеличение без числа: «{e}»")
    plaques = [s.id for s in spec.shots if s.plaque]
    if plaques and not spec.exaggerations:
        problems.append(f"у кадров {plaques} есть плашка, но exaggerations пуст")
    ids = {s.id: s for s in spec.shots}
    if spec.true_scale_shot_id is not None:
        shot = ids.get(spec.true_scale_shot_id)
        if shot is None:
            problems.append(f"true_scale_shot_id {spec.true_scale_shot_id} — нет такого кадра")
        elif shot.plaque:
            problems.append(f"кадр истинного масштаба {shot.id} не может иметь плашку «не в масштабе»")
    elif spec.exaggerations or plaques:
        problems.append("есть преувеличения, но не задан true_scale_shot_id — кадр в истинном масштабе")
    for field in ("objects", "invariants", "assumptions"):
        if not [x for x in getattr(spec, field) if x.strip()]:
            problems.append(f"пустое поле {field}")
    if not spec.params:
        problems.append("пустые params шаблона")
    return problems


def _source_structure_problems(key: str, src) -> list[str]:
    """Структура источника до чтения полей: повреждённый источник — замечание, а не исключение."""
    if not isinstance(src, dict):
        return [f"param_sources.{key}: ожидается объект {{claim_ids, numbers, derivation, factor}}, "
                f"получено {type(src).__name__}"]
    problems = []
    if not isinstance(src.get("claim_ids"), list) or not all(isinstance(x, str) for x in src["claim_ids"]):
        problems.append(f"param_sources.{key}.claim_ids — список строк, получено {src.get('claim_ids')!r}")
    if not isinstance(src.get("numbers"), list) or not all(isinstance(x, str) for x in src["numbers"]):
        problems.append(f"param_sources.{key}.numbers — список строк с числами как в тексте, получено "
                        f"{src.get('numbers')!r}")
    factor = src.get("factor", 1.0)
    if isinstance(factor, bool) or not isinstance(factor, (int, float)) or not math.isfinite(factor) or factor <= 0:
        problems.append(f"param_sources.{key}.factor — конечное число > 0, получено {factor!r}")
    if "derivation" in src and not isinstance(src["derivation"], str):
        problems.append(f"param_sources.{key}.derivation — строка, получено {type(src['derivation']).__name__}")
    return problems


def param_source_problems(spec: SceneSpec, node: Node, cfg: dict) -> list[str]:
    """Каждый физический параметр шаблона — с источником: claim узла, где есть указанные числа.
    Структура источников проверяется до чтения полей; повреждённая — замечание."""
    problems: list[str] = []
    claims = {c.id: c for c in node.claims}
    video = spec.ext.get("video", {})
    if not isinstance(video, dict):
        return [f"ext.video — объект, получено {type(video).__name__}"]
    sources = video.get("param_sources", {})
    if not isinstance(sources, dict):
        return [f"ext.video.param_sources — объект «параметр → источник», получено {type(sources).__name__}"]
    for key, d in cfg["params"].items():
        if key not in spec.params:
            continue
        needs = d.get("kind") == "physical" or (
            d.get("kind") == "rule" and isinstance(spec.params[key], dict) and spec.params[key].get("status") == "из узла")
        if not needs:
            continue
        src = sources.get(key)
        if src is None or src == {}:
            problems.append(f"params.{key}: физический параметр без источника в узле (param_sources.{key}); "
                            f"если числа в узле нет — не включай параметр, а укажи его в missing_params")
            continue
        broken = _source_structure_problems(key, src)
        if broken:
            problems += broken
            continue
        foreign = [c for c in src["claim_ids"] if c not in claims]
        if foreign:
            problems.append(f"params.{key}: claim_id {foreign} не из узла {node.id}")
        own = [c for c in src["claim_ids"] if c in claims]
        if not own or not src["numbers"]:
            problems.append(f"params.{key}: в param_sources нужны claim_ids узла и числа из них")
            continue
        text = "\n".join(f"{claims[c].text}\n{claims[c].quote}" for c in own)
        found = {n.replace(",", ".") for n in NUM_RE.findall(text)}
        missing = [n for n in src["numbers"] if n.replace(",", ".") not in found]
        for n in missing:
            problems.append(f"params.{key}: число {n} не найдено в тексте и цитате {own}")
        value = spec.params[key]
        if len(src["numbers"]) == 1 and not missing:
            # одно число источника: значение = число × factor (пересчёт единиц), иначе источник не подтверждает значение
            factor = src.get("factor", 1.0)
            expected = float(src["numbers"][0].replace(",", ".")) * float(factor)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or \
                    not math.isclose(float(value), expected, rel_tol=1e-6):
                problems.append(f"params.{key} = {value!r}, а источник даёт {src['numbers'][0]} × factor {factor:g} "
                                f"= {expected:g}; укажите factor пересчёта единиц или исправьте значение")
            src["arithmetic_checked"] = True
        elif len(src["numbers"]) > 1:
            src["arithmetic_checked"] = False      # производная величина: арифметику код не проверяет — помечено
    return problems


def source_page(c) -> str:
    return f"стр. {c.page_pdf}" + (f" (печ. {c.page_print})" if c.page_print is not None else "")


def sources_table(script: Script, node: Node, extra_claim_ids=()) -> list[dict]:
    """Таблица «утверждение → страница + цитата» для паспорта — кодом из claims узла: утверждения фраз
    в порядке фраз, затем прочие использованные (элементы схемы, источники параметров)."""
    claims = {c.id: c for c in node.claims}
    rows, seen = [], set()
    for cid in [p.claim_id for p in script.phrases] + list(extra_claim_ids):
        if cid in seen or cid not in claims:
            continue
        seen.add(cid)
        c = claims[cid]
        row = SourceRow(claim_id=c.id, page_or_dataset=source_page(c), quote=c.quote, claim_text=c.text,
                        kind=c.kind, source_kind=c.source_kind, by_model=c.by_model)
        rows.append(row.model_dump(by_alias=True))
    return rows


def source_language(node: Node) -> str:
    """Язык цитат узла: en, если латиницы больше кириллицы."""
    text = " ".join(c.quote for c in node.claims)
    lat = len(re.findall(r"[A-Za-z]", text))
    cyr = len(re.findall(r"[А-Яа-яЁё]", text))
    return "en" if lat > cyr else "ru"
