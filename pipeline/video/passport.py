"""Паспорт ролика (passport.schema.json организаторов) из фактических входов и результатов сборки.

Честность проверок:
- пункт чек-листа, который код проверил, — «да»/«нет» со статусом «проверено автоматически» и пояснением;
- пункт, который шаблон не изображает (по его конфигурации), — «н/п» со статусом «не применимо» и причиной;
- всё остальное — статус «не проверено». Схема разрешает в answer только «да», «нет», «н/п»: «да» было бы
  выдуманной проверкой, «н/п» — подменой, поэтому стоит «нет» = «не подтверждено», и это сказано в note.
Перед записью паспорт проверяется по JSON-схеме; поля None, которым схема не разрешает null, опускаются.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from contracts.models import ChecklistAnswer, Passport, PassportFrame, SceneSpec, Script, ScriptLine, SourceRow

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "data" / "organizers" / "01_схемы" / "passport.schema.json"
DEFAULT_CHECKLIST = ROOT / "data" / "organizers" / "04_доменные_заготовки" / "physics_checklist.json"
STATUS_AUTO = "проверено автоматически"
STATUS_NA = "не применимо"
STATUS_UNCHECKED = "не проверено"
UNCHECKED_NOTE = ("не проверено: нужен просмотр ментором. «нет» стоит потому, что схема не допускает значения "
                  "«не проверено»; это не найденная ошибка")


class PassportError(RuntimeError):
    pass


def load_checklist(path: Path) -> list[dict]:
    path = Path(path)
    if not path.is_file():
        raise PassportError(f"нет чек-листа физической корректности: {path}")
    items = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(items, list) or not all(isinstance(i, dict) and "id" in i and "item" in i for i in items):
        raise PassportError(f"чек-лист {path}: ожидается список {{id, item}}")
    return items


def checklist_answers(items: list[dict], pc_cfg: dict | None, auto: dict[str, tuple[bool, str]]
                      ) -> list[ChecklistAnswer]:
    """pc_cfg — раздел physics_checklist конфигурации шаблона; auto — результаты автопроверок по имени."""
    out = []
    na = (pc_cfg or {}).get("not_applicable", {})
    checks = (pc_cfg or {}).get("auto", {})
    for it in items:
        pid = it["id"]
        if pid in na:
            out.append(ChecklistAnswer(item=pid, answer="н/п", note=na[pid], status=STATUS_NA, text=it["item"]))
        elif pid in checks and checks[pid] in auto and auto[checks[pid]][0] is None:
            # автопроверка покрыла пункт лишь частично — пункт целиком не подтверждён
            out.append(ChecklistAnswer(item=pid, answer="нет", status=STATUS_UNCHECKED, check=checks[pid],
                                       note=f"{auto[checks[pid]][1]}. " + UNCHECKED_NOTE, text=it["item"]))
        elif pid in checks and checks[pid] in auto:
            ok, note = auto[checks[pid]]
            out.append(ChecklistAnswer(item=pid, answer="да" if ok else "нет", note=note, status=STATUS_AUTO,
                                       check=checks[pid], text=it["item"]))
        else:
            note = UNCHECKED_NOTE if pid not in checks else \
                f"не проверено: автопроверка {checks[pid]} не выполнялась. " + UNCHECKED_NOTE.split(": ", 1)[1]
            out.append(ChecklistAnswer(item=pid, answer="нет", note=note, status=STATUS_UNCHECKED, text=it["item"]))
    return out


def plaques_have_number(spec: SceneSpec) -> tuple[bool, str]:
    """Проверка по спецификации: у каждой плашки и каждого преувеличения есть число; при преувеличениях
    есть кадр истинного масштаба без плашки."""
    bad = [s.id for s in spec.shots if s.plaque and not re.search(r"\d", s.plaque)]
    bad += [f"exaggerations[{i}]" for i, e in enumerate(spec.exaggerations) if not re.search(r"\d", e)]
    if bad:
        return False, f"без числа: {bad}"
    if spec.exaggerations or any(s.plaque for s in spec.shots):
        ts = next((s for s in spec.shots if s.id == spec.true_scale_shot_id), None)
        if ts is None or ts.plaque:
            return False, "нет кадра истинного масштаба без плашки"
        return True, f"все плашки и преувеличения с числом; кадр истинного масштаба — {ts.id}"
    return True, "преувеличений нет"


def audio_check_skipped(reason: str) -> dict:
    """Распознавание не выполнялось: всё, что от него зависит, — «не проверено» без выдуманных чисел."""
    st = {"status": STATUS_UNCHECKED, "reason": reason}
    return {"asr": dict(st), "sync": dict(st), "terms": dict(st),
            "stress": {**st, "to_listen": []}, "listened_by_human": False}


def strip_disallowed_nulls(data, schema: dict):
    """Убирает ключи со значением None там, где схема не допускает null (обязательные nullable остаются)."""
    if isinstance(data, list):
        items = schema.get("items", {})
        return [strip_disallowed_nulls(x, items) for x in data]
    if not isinstance(data, dict):
        return data
    props = schema.get("properties", {})
    out = {}
    for k, v in data.items():
        ps = props.get(k, {})
        if v is None and ps:
            t = ps.get("type")
            types = t if isinstance(t, list) else [t] if t else []
            allows_null = "null" in types or any(x.get("type") == "null" for x in ps.get("anyOf", []))
            if not allows_null:
                continue
        out[k] = strip_disallowed_nulls(v, ps) if isinstance(v, (dict, list)) else v
    return out


def validate(data: dict, schema: dict) -> list[str]:
    from jsonschema import Draft202012Validator
    return [f"{'/'.join(str(p) for p in e.absolute_path) or '(корень)'}: {e.message}"
            for e in Draft202012Validator(schema).iter_errors(data)]


def assemble(*, script: Script, spec: SceneSpec, segments: list[dict], frames: list[dict], node_card: dict,
             sources: list[dict], checklist: list[ChecklistAnswer], audio_check: dict, scene_spec_path: str,
             panels: dict | None = None) -> Passport:
    """segments — фактические интервалы звучания фраз в ролике; frames — сохранённые кадры (t, shot_id, file)."""
    seg = {s["phrase_id"]: s for s in segments}
    shot = {s.id: s for s in spec.shots}
    lines = [ScriptLine(t_start=round(seg[p.id]["start"], 3), t_end=round(seg[p.id]["end"], 3), text=p.text,
                        claim_id=p.claim_id, is_analogy=p.is_analogy, on_screen=p.on_screen,
                        phrase_id=p.id, beat=p.beat, pause_after_s=p.pause_after_s)
             for p in script.phrases]
    pframes = [PassportFrame(t=round(f["t"], 3), **{"class": shot[f["shot_id"]].frame_class},
                             label=shot[f["shot_id"]].label,
                             ext={"shot_id": f["shot_id"], "file": f["file"], **({"panels": panels} if panels else {})})
               for f in frames]
    return Passport(
        video_id=script.video_id, node_id=script.node_id, node_card=node_card, script=lines,
        sources=[SourceRow(**s) for s in sources], scene_spec=scene_spec_path, frames=pframes,
        exaggerations=list(spec.exaggerations), prediction_question=script.prediction_question,
        transfer_question=script.transfer_question, data_it_bridge=script.data_it_bridge,
        physics_checklist=checklist, audio_check=audio_check)


def write_passport(passport: Passport, path: Path, schema: dict) -> dict:
    """Сериализация by_alias=True, проверка по схеме организаторов; при ошибке файл не пишется."""
    data = strip_disallowed_nulls(json.loads(passport.model_dump_json(by_alias=True)), schema)
    problems = validate(data, schema)
    if problems:
        raise PassportError("паспорт не проходит passport.schema.json:\n- " + "\n- ".join(problems))
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return data
