"""Генерация текста шагов и заданий перед сборкой курса. Модель вызывается только через pipeline.llm."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from contracts.models import Layer
from pipeline.course.steptext import ensure_step_text
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


def run(layer: Layer, ch_dir: Path, course_dir: Path, node: Optional[str], domain: Optional[str]) -> None:
    os.environ.setdefault("CH", layer.chapter)           # llm.py пишет главу в метрики из этой переменной
    ensure_step_text(layer, course_dir, only=node)
    ensure_tasks(layer, course_dir, load_misconceptions(resolve_domain(ch_dir, domain)), only=node)
