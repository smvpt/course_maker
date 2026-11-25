"""Загрузка и проверка входа видео: Script и SceneSpec из contracts.models."""
from __future__ import annotations

import re
from pathlib import Path

from pydantic import BaseModel, ValidationError

from contracts.models import SceneSpec, Script

MAX_ON_SCREEN_WORDS = 8
ID_RE = re.compile(r"^[a-z0-9_.-]+$")


class VideoInputError(ValueError):
    pass


def _load(path: Path, model: type[BaseModel]) -> BaseModel:
    path = Path(path)
    if not path.is_file():
        raise VideoInputError(f"{model.__name__}: файл не найден: {path}")
    try:
        return model.model_validate_json(path.read_text(encoding="utf-8"))
    except ValidationError as e:
        raise VideoInputError(f"{path} не проходит контракт {model.__name__}:\n{e}") from e


def shot_link_problems(script: Script, spec: SceneSpec) -> list[str]:
    """Каждая фраза ровно в одном кадре, кадр не пуст, ссылки только на существующие фразы, id кадров уникальны."""
    problems: list[str] = []
    ids = [p.id for p in script.phrases]
    shot_ids = [s.id for s in spec.shots]
    dup = sorted({i for i in shot_ids if shot_ids.count(i) > 1})
    if dup:
        problems.append(f"id кадров повторяются: {dup}")
    seen: dict[str, str] = {}
    for shot in spec.shots:
        if not shot.phrase_ids:
            problems.append(f"кадр {shot.id}: пустой phrase_ids — у каждого кадра хотя бы одна фраза")
        for pid in shot.phrase_ids:
            if pid not in ids:
                problems.append(f"кадр {shot.id} ссылается на неизвестную фразу {pid}")
            elif pid in seen:
                problems.append(f"фраза {pid} в двух кадрах: {seen[pid]} и {shot.id}")
            seen[pid] = shot.id
    for pid in ids:
        if pid not in seen:
            problems.append(f"фраза {pid} не входит ни в один кадр SceneSpec.shots")
    return problems


def check_pair(script: Script, spec: SceneSpec, node_id: str | None = None) -> None:
    problems: list[str] = []
    ids = [p.id for p in script.phrases]
    if not ids:
        problems.append("в сценарии нет фраз")
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        problems.append(f"id фраз повторяются: {dup}")
    for p in script.phrases:
        if not p.text.strip():
            problems.append(f"фраза {p.id}: пустой текст")
        if p.pause_after_s < 0:
            problems.append(f"фраза {p.id}: отрицательная пауза {p.pause_after_s}")
        if p.on_screen and len(p.on_screen.split()) > MAX_ON_SCREEN_WORDS:
            problems.append(f"фраза {p.id}: on_screen длиннее {MAX_ON_SCREEN_WORDS} слов")
    if not ID_RE.match(script.video_id):
        problems.append(f"video_id «{script.video_id}» — допустимы только [a-z0-9_.-]")
    if script.video_id != spec.video_id:
        problems.append(f"video_id не совпадает: Script «{script.video_id}», SceneSpec «{spec.video_id}»")
    if script.node_id != spec.node_id:
        problems.append(f"node_id не совпадает: Script «{script.node_id}», SceneSpec «{spec.node_id}»")
    if node_id is not None and script.node_id != node_id:
        problems.append(f"--node {node_id}, а вход сделан для узла {script.node_id}")
    problems += shot_link_problems(script, spec)
    if problems:
        raise VideoInputError("вход видео некорректен:\n- " + "\n- ".join(problems))


def load_inputs(script_path: Path, spec_path: Path, node_id: str | None = None) -> tuple[Script, SceneSpec]:
    script = _load(script_path, Script)
    spec = _load(spec_path, SceneSpec)
    check_pair(script, spec, node_id)
    return script, spec
