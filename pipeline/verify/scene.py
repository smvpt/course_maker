"""Проверка сценария (Script) и спецификации сцены (SceneSpec) до рендера.

check_scene   — детерминированно: обязательные пункты честности ТЗ, привязка фраз к утверждениям,
                числа из исходных единиц, подписи, заблуждения из доменного пакета.
check_physics — LLM по чек-листу физики доменного пакета → ответы ChecklistAnswer (для паспорта П4)
                и замечания по пунктам с ответом «нет».

python -m pipeline.verify.scene --ch <id> --video <video_id> [--llm]
    → out/<id>/verify/scene_<video_id>.json (ReviewOutput + ext.verify.physics_checklist)
"""
import argparse
import json
import re
import sys
from pathlib import Path

from pydantic import BaseModel
from rapidfuzz import fuzz

from contracts.models import ChecklistAnswer, ChapterUnits, Layer, Remark, ReviewOutput, SceneSpec, Script
from pipeline.verify.numbers import extract_numbers, missing_numbers
from pipeline.verify.pages import normalize
from pipeline.verify.remarks import SEV_ORDER, one_per_target

ROOT = Path(__file__).resolve().parents[2]

GENERATED = re.compile(r"сгенерир|генеративн|нейросет|\bии\b|\bai\b|midjourney|stable diffusion|dall-?e|"
                       r"\bsora\b|runway|kling", re.I)
FORMULA = re.compile(r"[Ͱ-Ͽ=√∑∫^²³⁻]")
MAX_PHRASE_WORDS = 18
MAX_SCREEN_WORDS = 8
PAUSE_MIN_S = 1.0
MISC_THRESHOLD = 85


class PhysicsAnswers(BaseModel):
    """Обёртка ответа LLM: список ответов по пунктам чек-листа."""
    answers: list[ChecklistAnswer]


def _domain_json(domain, name):
    p = ROOT / "domain" / domain / name
    if not p.exists():
        raise FileNotFoundError(f"в доменном пакете нет {p}")
    return json.loads(p.read_text(encoding="utf-8"))


def load_misconceptions(domain):
    return _domain_json(domain, "misconceptions.json")


def _r(target, severity, problem, fix, category="other"):
    return Remark(target=target, category=category, severity=severity, problem=problem, fix=fix,
                  page_pdf=None, quote=None)


def _has_number(text):
    return bool(extract_numbers(text))


def _check_honesty(spec):
    v = spec.video_id
    out = []
    shots = {s.id: s for s in spec.shots}
    if not spec.true_scale_shot_id:
        out.append(_r(v, "critical", "нет кадра в истинном масштабе (true_scale_shot_id)",
                      "добавить кадр без вертикального преувеличения и указать его id", "frame_error"))
    elif spec.true_scale_shot_id not in shots:
        out.append(_r(v, "critical", f"true_scale_shot_id {spec.true_scale_shot_id} не найден среди кадров",
                      "указать id существующего кадра в истинном масштабе", "frame_error"))
    elif "масштаб" in (shots[spec.true_scale_shot_id].plaque or "").lower():
        out.append(_r(f"{v}.{spec.true_scale_shot_id}", "significant",
                      "кадр в истинном масштабе несёт плашку «не в масштабе»",
                      "убрать плашку или выбрать другой кадр в истинном масштабе", "frame_error"))
    for e in spec.exaggerations:
        if not _has_number(e):
            out.append(_r(v, "critical", f"преувеличение не названо числом: «{e}»",
                          "указать, что и во сколько раз увеличено: «поры увеличены в 10 000 раз»", "frame_error"))
    if spec.exaggerations and not any(s.plaque for s in spec.shots):
        out.append(_r(v, "critical", "преувеличения есть, но ни на одном кадре нет плашки «не в масштабе»",
                      "поставить плашку с тем, что и во сколько увеличено", "frame_error"))
    for s in spec.shots:
        t = f"{v}.{s.id}"
        if s.plaque and "масштаб" in s.plaque.lower() and not _has_number(s.plaque):
            out.append(_r(t, "significant", f"плашка без числа: «{s.plaque}»",
                          "в плашке назвать, что и во сколько увеличено", "frame_error"))
        if s.frame_class in ("A", "B") and GENERATED.search(f"{s.shows} {s.plaque or ''}"):
            out.append(_r(t, "critical", f"кадр класса {s.frame_class} описан как сгенерированный: «{s.shows}»",
                          "кадры A и B — только кодом из данных или расчёта", "frame_error"))
        if s.frame_class == "A" and s.label == "схема":
            out.append(_r(t, "significant", "кадр класса A (данные) помечен «схема»",
                          "метка по тому, как сделан кадр: «реальные данные» или «симуляция»", "frame_error"))
    return out


def _check_links(spec, script):
    v = spec.video_id
    out = []
    phrase_ids = {p.id for p in script.phrases}
    covered = set()
    for s in spec.shots:
        unknown = [p for p in s.phrase_ids if p not in phrase_ids]
        covered.update(s.phrase_ids)
        if unknown:
            out.append(_r(f"{v}.{s.id}", "significant", f"кадр ссылается на фразы {unknown}, их нет в сценарии",
                          "phrase_ids — id фраз сценария"))
    for p in script.phrases:
        if p.id not in covered:
            out.append(_r(f"{v}.{p.id}", "minor", "фраза не привязана ни к одному кадру",
                          "добавить id фразы в phrase_ids кадра"))
    if spec.node_id != script.node_id:
        out.append(_r(v, "significant", f"сцена про узел {spec.node_id}, сценарий — про {script.node_id}",
                      "одна пара script + scene_spec на узел"))
    if spec.historical_objects:
        marks = [p.on_screen or "" for p in script.phrases] + [s.plaque or "" for s in spec.shots]
        if not any("историческ" in m.lower() for m in marks):
            out.append(_r(v, "significant",
                          f"устаревшее оборудование {spec.historical_objects} без пометки «исторический прибор»",
                          "подпись «исторический прибор» на кадре и фраза «как это делается сейчас»",
                          "outdated_as_current"))
    return out


def check_script(script, claim_ids, sources, misconceptions=()):
    """Фразы сценария: claim_id, числа из исходных единиц узла, подписи, вопросы, пауза, заблуждения."""
    v = script.video_id
    out = []
    if not script.prediction_question.strip():
        out.append(_r(v, "significant", "нет вопроса-предсказания", "добавить prediction_question"))
    if not script.transfer_question.strip():
        out.append(_r(v, "significant", "нет вопроса на перенос", "добавить transfer_question в конце"))
    preds = [p for p in script.phrases if p.beat == "prediction"]
    if not preds:
        out.append(_r(v, "significant", "нет фразы-предсказания (beat prediction) с паузой",
                      f"фраза-вопрос с паузой {PAUSE_MIN_S}–1,5 с перед ответом"))
    for p in script.phrases:
        t = f"{v}.{p.id}"
        if p.claim_id is None and not p.is_analogy:
            out.append(_r(t, "significant", "у фразы нет claim_id", "привязать фразу к утверждению слоя"))
        elif p.claim_id is not None and p.claim_id not in claim_ids:
            out.append(_r(t, "significant", f"claim_id {p.claim_id} нет в слое",
                          "ссылаться на существующее утверждение"))
        miss = missing_numbers(p.text + " \n" + (p.on_screen or ""), sources)
        if miss:
            out.append(_r(t, "significant", f"чисел {', '.join(f'{x:g}' for x in miss)} нет в исходных единицах узла",
                          "брать числа только из главы"))
        if re.search(r"\d", p.text):
            out.append(_r(t, "minor", "в тексте для озвучки числа цифрами", "в закадре числа словами"))
        if len(p.text.split()) > MAX_PHRASE_WORDS:
            out.append(_r(t, "minor", f"фраза длиннее {MAX_PHRASE_WORDS} слов", "разбить фразу"))
        if p.on_screen:
            if len(p.on_screen.split()) > MAX_SCREEN_WORDS:
                out.append(_r(t, "minor", f"подпись длиннее {MAX_SCREEN_WORDS} слов", "сократить подпись"))
            if FORMULA.search(p.on_screen):
                out.append(_r(t, "minor", "формула или греческая буква в подписи",
                              "формулы — в интерактив курса, не в подпись"))
        if p.beat == "prediction" and p.pause_after_s < PAUSE_MIN_S:
            out.append(_r(t, "significant", f"пауза после предсказания {p.pause_after_s} с",
                          f"pause_after_s от {PAUSE_MIN_S} до 1,5 с"))
        q = normalize(p.text)
        for m in misconceptions:
            mt = normalize(m["text"])
            if q and mt and fuzz.partial_ratio(mt, q) >= MISC_THRESHOLD and len(q) >= 0.6 * len(mt):
                out.append(_r(t, "significant", f"фраза повторяет заблуждение {m['id']}: «{m['text']}»",
                              "показать заблуждение как опровергаемое или переформулировать"))
    return out


def check_scene(spec, script, claim_ids, sources, domain="geology"):
    """Все детерминированные замечания к паре script + scene_spec, одно на цель."""
    misc = load_misconceptions(domain) if domain else []
    remarks = _check_honesty(spec) + _check_links(spec, script) + check_script(script, claim_ids, sources, misc)
    return one_per_target(remarks)


def check_physics(spec, script, domain="geology"):
    """LLM отвечает на каждый пункт чек-листа физики; «нет» → замечание frame_error."""
    from pipeline.llm import complete_json
    checklist = _domain_json(domain, "physics_checklist.json")
    res = complete_json(prompt="verify/scene_physics", tier="strong", schema=PhysicsAnswers, vars={
        "checklist": json.dumps(checklist, ensure_ascii=False, indent=1),
        "scene_spec": spec.model_dump_json(by_alias=True, indent=1),
        "script": script.model_dump_json(by_alias=True, indent=1),
    })
    ids = [c["id"] for c in checklist]
    got = [a.item for a in res.answers]
    if sorted(got) != sorted(ids):
        raise ValueError(f"LLM ответила не на все пункты чек-листа: нет {sorted(set(ids) - set(got))}, "
                         f"лишние {sorted(set(got) - set(ids))}")
    items = {c["id"]: c["item"] for c in checklist}
    answers = sorted(res.answers, key=lambda a: ids.index(a.item))
    remarks = [_r(spec.video_id, "significant", f"{a.item}: {a.note or items[a.item]}",
                  f"исправить сцену: {items[a.item]}", "frame_error")
               for a in answers if a.answer == "нет"]
    return answers, one_per_target(remarks)


def node_context(out_dir, node_id):
    """claim_ids слоя и исходные тексты узла (как в verify.run)."""
    from pipeline.verify.pages import load_pages
    from pipeline.verify.quotes import md_from_units
    from pipeline.verify.run import node_sources
    layer = Layer.model_validate_json((out_dir / "layer.json").read_text(encoding="utf-8"))
    units = ChapterUnits.model_validate_json((out_dir / "units.json").read_text(encoding="utf-8"))
    nodes = {n.id: n for n in layer.nodes}
    if node_id not in nodes:
        raise ValueError(f"узла {node_id} нет в слое")
    md_pages = load_pages(md_from_units(out_dir / "units.json"))
    src = node_sources(nodes[node_id], {u.unit_id: u.text for u in units.units}, md_pages)
    return {c.id for n in layer.nodes for c in n.claims}, src, units.domain


def main(argv=None):
    ap = argparse.ArgumentParser(description="Проверка script.json + scene_spec.json ролика")
    ap.add_argument("--ch", required=True)
    ap.add_argument("--video", required=True)
    ap.add_argument("--llm", action="store_true", help="ещё и чек-лист физики через strong-модель")
    a = ap.parse_args(argv)
    out_dir = ROOT / "out" / a.ch
    vdir = out_dir / "videos" / a.video
    for f in ("script.json", "scene_spec.json"):
        if not (vdir / f).exists():
            raise FileNotFoundError(f"{vdir / f} не найден")
    script = Script.model_validate_json((vdir / "script.json").read_text(encoding="utf-8"))
    spec = SceneSpec.model_validate_json((vdir / "scene_spec.json").read_text(encoding="utf-8"))
    claim_ids, src, domain = node_context(out_dir, script.node_id)
    remarks = check_scene(spec, script, claim_ids, src, domain)
    report = ReviewOutput(package_id=f"{a.ch}/{a.video}", team="", remarks=remarks)
    if a.llm:
        answers, prem = check_physics(spec, script, domain)
        report.remarks = one_per_target(remarks + prem)
        report.ext["verify"] = {"physics_checklist": [x.model_dump() for x in answers]}
    dst = out_dir / "verify" / f"scene_{a.video}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(report.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    counts = {s: sum(r.severity == s for r in report.remarks) for s in SEV_ORDER}
    print(f"scene {a.video}: {counts} → {dst.relative_to(ROOT)}")
    return 1 if counts["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
