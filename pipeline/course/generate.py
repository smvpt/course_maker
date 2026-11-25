"""Генерация текста шагов и заданий перед сборкой курса. Модель вызывается только через pipeline.llm."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from contracts.models import Layer
from pipeline.course import guess as guess_mod, interactive as inter_mod, scheme as scheme_mod
from pipeline.course.pernode import ensure_per_node
from pipeline.course.steptext import LlmState, ensure_step_text, quote_language
from pipeline.course.tasks import ensure_tasks


def resolve_domain(ch_dir: Path, arg: Optional[str]) -> str:
    """Домен главы: аргумент --domain, иначе поле domain из out/<ch>/units.json (его пишет ingest)."""
    if arg:
        return arg
    units = ch_dir / "units.json"
    if not units.exists():
        raise ValueError(f"не знаю домен главы: нет {units}, а --domain не задан")
    domain = json.loads(units.read_text(encoding="utf-8")).get("domain")
    if not domain:
        raise ValueError(f"в {units} нет поля domain, задай --domain")
    return domain


def load_misconceptions(domain: str) -> list[dict]:
    from pipeline.common import domain as domain_pack   # доменный пакет читаем только через pipeline.common.domain (CLAUDE.md §2)
    return domain_pack.load(domain).misconceptions


def run(layer: Layer, ch_dir: Path, course_dir: Path, node: Optional[str], domain: Optional[str],
        extras: bool = False, style: Optional[dict] = None, interactive_plan: Optional[dict[str, str]] = None,
        scheme_plan: Optional[set[str]] = None) -> LlmState:
    """Генерирует текст шагов и задания; с extras — ещё интерактив и вопросы «сначала угадай».
    Возвращает состояние модели (для итога сборки)."""
    os.environ.setdefault("CH", layer.chapter)           # llm.py пишет главу в метрики из этой переменной
    misconceptions = load_misconceptions(resolve_domain(ch_dir, domain))   # входы проверяем до первого вызова модели
    state = LlmState()                                   # одно состояние на текст и задания: авторизация упала — дальше не зовём
    ensure_step_text(layer, course_dir, only=node, state=state)
    ensure_tasks(layer, course_dir, misconceptions, only=node, state=state)
    if extras:
        language = quote_language(layer)
        curves = {k: v["ru"] for k, v in style["curves"].items()}
        plan = interactive_plan or {}
        schemes = scheme_plan or set()                      # узлы без формул: «схема-исследование» из утверждений узла
        rocks = {k: v["ru"] for k, v in style["lithology"].items()}
        ensure_per_node(layer, course_dir / "interactive.json", set(plan) | schemes,
                        lambda n: scheme_mod.make_scheme(n, rocks, language) if n.id in schemes
                        else inter_mod.make_interactive(n, plan[n.id], curves, language), state, only=node)
        ensure_per_node(layer, course_dir / "guesses.json", {n.id for n in layer.nodes if guess_mod.wanted(n)},
                        lambda n: guess_mod.make_guess(n, language), state, only=node)
    return state
