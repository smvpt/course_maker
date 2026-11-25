"""Сборка ролика: Script + SceneSpec → озвучка → сцена Manim → MP4 + VTT → паспорт.

    python -m pipeline.video.build --ch <id> --node <node_id> [--draft]
        [--layer <layer.json>] [--routing <routing.json>] [--format short|long] [--dataset <dataset.json>]
    python -m pipeline.video.build --ch <id> --node <node_id> --script <script.json> --scene-spec <scene_spec.json>

Без --script/--scene-spec пара берётся из каталога video.spec (out/<ch>/videos/<node_id>.<fmt>/) после
проверки соответствия узлу, формату, шаблону и набору данных; если пары нет — её генерирует video.spec.

Выходы — out/<ch>/videos/<video_id>/: <video_id>.mp4, <video_id>.vtt, script.json,
scene_spec.json, timeline.json, build_report.json, passport.json (по passport.schema.json),
asr_report.json (распознавание озвучки), frames/, _work/ (промежуточные файлы).
Код выхода: 0 — собрано и проверено; 2 — ошибка входа или инструмента; 3 — ролик и паспорт записаны,
но проверка озвучки не пройдена или не выполнена.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

from pipeline.video import asr, media
from pipeline.video.passport import (DEFAULT_CHECKLIST, SCHEMA_PATH, PassportError, assemble, audio_check_skipped,
                                     checklist_answers, load_checklist, plaques_have_number, write_passport)
from pipeline.video.inputs import ID_RE, VideoInputError, load_inputs
from pipeline.video.layout import FRAME_H, LONG_SAFE_ZONE, REF_LONG, REF_H, REF_W, Layout, LayoutError
from pipeline.video.media import ToolError
from pipeline.video.timeline import build_timeline, format_vtt, subtitle_cues, assemble_wav
from pipeline.video.templates import TEMPLATE_FORMATS, format_problem
from pipeline.video.tts import DEFAULT_VOICE, TtsError, TtsParams, synthesize

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STYLEGUIDE = ROOT / "data" / "organizers" / "03_стайлгайд" / "styleguide.json"
SAMPLE_RATE = 24000          # родная частота edge-tts (audio-24khz-48kbitrate-mono-mp3)
RES = {"short": {"final": (1080, 1920, 30), "draft": (540, 960, 15)},
       "long": {"final": (1920, 1080, 30), "draft": (960, 540, 15)}}
TEMPLATES = TEMPLATE_FORMATS          # шаблон → форматы: общий источник с video.spec
TARGET_WPM = (110, 150)
VTT_NOTES = {
    "word": "тайминги: пословные метки edge-tts (WordBoundary), сдвинуты на начало фразы в таймлайне",
    "sentence": "тайминги: метки предложений edge-tts (SentenceBoundary), не пословные",
    "audio": "тайминги: границы аудио фраз; пословных меток нет",
}


class BuildCheckError(RuntimeError):
    pass


def _styleguide(path: Path) -> dict:
    try:
        sg = json.loads(Path(path).read_text(encoding="utf-8"))
        return {"background": sg["background"], "panel": sg["panel"], "text": sg["text"], "muted": sg["muted"],
                "provenance": sg["provenance"], "raw": sg, "font": sg["fonts"]["ui"],
                "min_caption_px": sg["fonts"]["min_caption_px_at_1080"], "safe_zone": sg["safe_zone"]}
    except FileNotFoundError as e:
        raise VideoInputError(f"стайлгайд не найден: {path}") from e
    except (KeyError, json.JSONDecodeError) as e:
        raise VideoInputError(f"стайлгайд {path} без нужного поля или не JSON: {e}") from e


def _check_font(font: str) -> None:
    import manimpango
    if font not in manimpango.list_fonts():
        raise ToolError(f"шрифт стайлгайда «{font}» не установлен в системе — кириллица не отрисуется как задано")


def _sg_color(sg: dict, dotted: str) -> str:
    v = sg["raw"]
    for k in dotted.split("."):
        if not isinstance(v, dict) or k not in v:
            raise VideoInputError(f"в стайлгайде нет цвета {dotted}")
        v = v[k]
    return v["color"] if isinstance(v, dict) else v


def _prepare_template(spec, script, sg: dict, templates_dir: Path) -> tuple[dict, dict, dict]:
    """Проверка параметров шаблона ДО озвучки и рендера: (данные для сцены, доп. цвета, сведения для отчёта)."""
    if spec.template == "hello":
        if not isinstance(spec.params.get("title"), str) or not spec.params["title"].strip():
            raise VideoInputError("SceneSpec.params.title обязателен для шаблона hello")
        return {"title": spec.params["title"]}, {}, {}
    if spec.template == "T2":
        return _prepare_t2(spec, script, sg, templates_dir)
    from pipeline.video import t1_template
    cfg = t1_template.load_config(templates_dir)
    prep = t1_template.prepare(spec, script, cfg)
    info = {"model": cfg["model"], "influence_radius": cfg["influence_radius"],
            "params": {k: spec.params.get(k, d.get("default")) for k, d in cfg["params"].items()},
            "r_influence_end_m": round(prep["r_influence_end"], 3),
            "well_argument_end": prep["well_argument_end"], "color_max_mpa": prep["color_max"],
            "graph_max_mpa": prep["graph_max"], "config": str(Path(templates_dir) / "T1.json")}
    return {"t1": prep}, {"field": _sg_color(sg, prep["field_color_key"])}, info


def _prepare_t2(spec, script, sg: dict, templates_dir: Path) -> tuple[dict, dict, dict]:
    from pipeline.video import t2_template
    from pipeline.video.templates import load_template_config
    cfg = load_template_config(templates_dir, "T2")
    if cfg is None:
        raise VideoInputError(f"нет описания шаблона T2: {Path(templates_dir) / 'T2.json'}")
    prep = t2_template.prepare(spec, script, cfg)
    disp = cfg["display"]
    colors = {"curve_colors": {cv["mnemonic"]: _sg_color(sg, f"curves.{cv['kind']}") for cv in prep["curves"]},
              "tool": _sg_color(sg, disp["tool_color"]), "mud": _sg_color(sg, disp["mud_color"]),
              "uncertainty": _sg_color(sg, disp["rule_unknown_color"]),
              "rule_true": sg[disp["rule_true_color"]], "schema": sg["provenance"]["схема"]}
    ds = prep["dataset"]
    info = {"model": cfg["model"], "config": str(Path(templates_dir) / "T2.json"),
            "dataset_provenance": ds.provenance, "data_label": ds.label,
            "curves": [{k: cv[k] for k in ("mnemonic", "kind", "unit", "label", "log", "range")} for cv in prep["curves"]],
            "interval_m": [prep["top"], prep["bottom"]], "rule": {k: v for k, v in prep["rule"].items()},
            "rule_counts": {"выполнено": int((prep["rule_state"] == 1).sum()), "не выполнено": int((prep["rule_state"] == 0).sum()),
                            "нет данных": int((prep["rule_state"] == -1).sum())},
            "borehole_exaggeration": prep["exaggeration"]}
    return {"t2": prep, "chain": disp["chain"], "school_label": disp["school_label"]}, colors, info


def _render(scene_cls, plan: dict, work: Path, w: int, h: int, fps: int, background: str) -> Path:
    from manim import tempconfig
    cfg = {"pixel_width": w, "pixel_height": h, "frame_rate": fps, "frame_height": FRAME_H,
           "frame_width": FRAME_H * w / h, "media_dir": str(work / "manim"), "disable_caching": True,
           "background_color": background, "progress_bar": "none", "verbosity": "WARNING",
           "output_file": "scene", "preview": False}
    with tempconfig(cfg):
        scene = scene_cls()
        scene.plan = plan
        scene.render()
        out = Path(scene.renderer.file_writer.movie_file_path)
    if not out.is_file():
        raise ToolError(f"Manim не создал видео сцены: {out}")
    return out


def _verify(mp4: Path, tl, w: int, h: int, fps: int) -> dict:
    info = media.probe(mp4)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    if v is None or a is None:
        raise BuildCheckError(f"в {mp4} нет видео- или аудиодорожки")
    v_dur, a_dur = float(v["duration"]), float(a["duration"])
    loud = media.loudness(mp4)
    tail = media.trailing_silence(mp4, a_dur)
    last_end = tl.segments[-1].end
    checks = {
        "video_h264": v["codec_name"] == "h264",
        "pix_fmt_yuv420p": v["pix_fmt"] == "yuv420p",
        "size": (v["width"], v["height"]) == (w, h),
        "audio_aac": a["codec_name"] == "aac",
        "video_covers_timeline": abs(v_dur - tl.total) <= 1.5 / fps,
        "audio_covers_timeline": a_dur >= tl.total - 0.05,
        "last_phrase_inside": min(v_dur, a_dur) >= last_end + 0.3,
        "trailing_silence_ge_0.3s": tail >= 0.3,
        "lufs_within_1lu_of_-16": abs(loud["integrated_lufs"] - media.TARGET_I) <= 1.0,
        "true_peak_le_-1dbtp": loud["true_peak_dbtp"] <= -1.0,
    }
    result = {"width": v["width"], "height": v["height"], "video_codec": v["codec_name"],
              "pix_fmt": v["pix_fmt"], "video_frames": int(v.get("nb_read_frames") or v.get("nb_frames") or 0),
              "video_duration_s": v_dur, "audio_codec": a["codec_name"], "audio_sample_rate": int(a["sample_rate"]),
              "audio_duration_s": a_dur, "timeline_total_s": tl.total, "last_phrase_end_s": last_end,
              "trailing_silence_s": round(tail, 3), **loud, "checks": checks}
    failed = [k for k, ok in checks.items() if not ok]
    if failed:
        raise BuildCheckError(f"MP4 не прошёл проверки {failed}: {json.dumps(result, ensure_ascii=False)}")
    return result


def _rel(path: Path) -> str:
    path = Path(path).resolve()
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def _node_card(script, node_obj) -> dict:
    if node_obj is None:
        note = (script.ext.get("video") or {}).get("note")
        return {"node_id": script.node_id, "status": "учебный слой не передан (--layer): карточка узла не заполнена",
                **({"note": note} if note else {})}
    n = node_obj
    return {"node_id": n.id, "title": n.title, "title_novice": n.title_novice, "difficulty": n.difficulty.model_dump(),
            "threshold": n.threshold, "main": n.layers.main.text, "pages": n.pages,
            "terms_introduced": n.terms_introduced,
            "claims": [{"id": c.id, "kind": c.kind, "page_pdf": c.page_pdf} for c in n.claims]}


def _auto_checks(spec, tpl_info: dict) -> dict:
    """Автопроверки для чек-листа: по спецификации и по инвариантам шаблона, закреплённым тестами."""
    auto = {"plaques_have_number": plaques_have_number(spec)}
    if spec.template == "T1":
        auto["label_matches_source"] = (True, "t1_template.prepare: все кадры A/B с меткой «симуляция» — кадр считается моделью")
        auto["one_state_variable"] = (True, "по построению: карта и график — одна функция PressureModel.delta_p от одного "
                                            "времени (тест test_field_and_graph_come_from_one_function)")
    if spec.template == "T2":
        prov = tpl_info["dataset_provenance"]
        auto["label_matches_source"] = (True, f"t2_template.prepare: метка кадров «{tpl_info['data_label']}» соответствует "
                                              f"набору ({prov['kind']}; sha256 и скважина сверены); панель ствола — «схема»")
        auto["one_state_variable"] = (True, "по построению: прибор, кривые и колонка решения — одна глубина через "
                                            "depth_frac (тест test_tool_and_curves_share_one_depth)")
        auto["depth_down"] = (True, "по построению: depth_frac 0 — верх, 1 — низ; шкала глубины и единицы кривых "
                                    "подписаны (тест test_tool_and_curves_share_one_depth)")
        auto["objects_fixed_geometry"] = (True, "по построению: ствол и прибор одной формы во всех кадрах; ширина меняется "
                                                "только на кадрах с плашкой «не в масштабе» и в кадре истинного масштаба")
    return auto


def _sources(script, spec, tpl_info: dict) -> list[dict]:
    rows = [dict(r) for r in (spec.ext.get("video") or {}).get("sources", [])]
    if spec.template == "T2":
        p = tpl_info["dataset_provenance"]
        a, b = p["interval_m"]
        uwi = f" ({p['uwi']})" if p.get("uwi") else ""
        rows.append({"claim_id": f"{script.video_id}#data",
                     "page_or_dataset": f"{p['attribution'] or p['source']}; файл {p['file']}; скв. {p['well']}{uwi}; "
                                        f"{a:g}–{b:g} м; sha256 {p['sha256'][:12]}…",
                     "provenance": p})
    return rows


def _audio_check(mp4: Path, script, timeline: dict, probe: dict, wpm: float, voice: str, skip_asr: bool,
                 asr_model: str, node_obj, out: Path) -> tuple[dict, bool | None, str | None]:
    """Измеренный звук + распознавание. Возвращает (audio_check, проверка пройдена?, причина провала)."""
    base = {"voice": voice,
            "tempo": {"wpm": wpm, "target": list(TARGET_WPM), "ok": TARGET_WPM[0] <= wpm <= TARGET_WPM[1],
                      "method": "слова сценария / время от первого до последнего слова фраз по меткам TTS"},
            "loudness": {"integrated_lufs": probe["integrated_lufs"], "true_peak_dbtp": probe["true_peak_dbtp"],
                         "target_lufs": media.TARGET_I, "ok": probe["checks"]["lufs_within_1lu_of_-16"],
                         "no_clipping": probe["checks"]["true_peak_le_-1dbtp"]},
            "trailing_silence_s": probe["trailing_silence_s"], "last_phrase_inside": probe["checks"]["last_phrase_inside"]}
    abbreviations = sorted({w for p in script.phrases for w in re.findall(r"\b[А-ЯЁA-Z]{2,}\b", p.text)})
    tempo_fail = [] if base["tempo"]["ok"] else [f"темп {wpm} слов/мин вне {TARGET_WPM[0]}–{TARGET_WPM[1]}"]

    def unchecked(reason: str) -> tuple[dict, bool | None, str]:
        # известный провал (темп) не прячется за «не проверено»: тогда итог — False
        return ({**base, **audio_check_skipped(reason)}, False if tempo_fail else None,
                "; ".join(tempo_fail + [reason]))

    if skip_asr:
        return unchecked("распознавание пропущено флагом --skip-asr")
    pcm = np.frombuffer(media.decode_pcm(mp4, 16000), dtype=np.int16).astype(np.float32) / 32768.0
    try:
        tr = asr.transcribe(pcm, asr_model)
    except asr.AsrError as e:
        return unchecked(f"распознавание не выполнено: {e}")
    wer = asr.wer_report([(p.id, p.text) for p in script.phrases], [w["word"] for w in tr["words"]])
    tts_words = [(w["start_s"], w["text"]) for ph in timeline["phrases"] if ph["timing"] == "word" for w in ph["words"]]
    sync = asr.sync_report(tts_words, [(w["start"], w["word"]) for w in tr["words"]])
    (out / "asr_report.json").write_text(json.dumps({"transcription": tr, "wer": wer, "sync": sync},
                                                    ensure_ascii=False, indent=2), encoding="utf-8")
    if node_obj is None:
        terms = {"status": "не проверено", "reason": "нет списка терминов узла: учебный слой не передан (--layer)"}
    else:
        terms = {"status": "проверено автоматически",
                 "method": "каждое употребление термина в сценарии — по выравниванию сценария и распознавания",
                 **asr.term_report([(p.id, p.text) for p in script.phrases], [w["word"] for w in tr["words"]],
                                   node_obj.terms_introduced + node_obj.terms_used)}
    disputed = sorted({e["expected"] for e in wer["errors"] if e["expected"]} | set(abbreviations))
    audio = {**base,
             "asr": {"status": "проверено автоматически", "engine": tr["engine"], "version": tr["version"],
                     "model": tr["model"], "language": tr["language"], "wer": round(wer["wer"], 4),
                     "limit": asr.WER_LIMIT, "ok": wer["wer"] <= asr.WER_LIMIT, "n_ref_words": wer["n_ref"],
                     "substitutions": wer["substitutions"], "deletions": wer["deletions"],
                     "insertions": wer["insertions"], "errors": wer["errors"][:60], "per_phrase": wer["per_phrase"],
                     "report": "asr_report.json"},
             "sync": {"status": "проверено автоматически",
                      "method": "начала слов: распознавание готового MP4 против меток слов TTS в таймлайне ролика",
                      **sync,
                      "frame_vs_voice": {"status": "не проверено",
                                         "reason": "смысловое соответствие кадра фразе проверяет человек; подписи и "
                                                   "анимация привязаны к тому же звуковому таймлайну по построению"}},
             "terms": terms,
             "stress": {"status": "не проверено",
                        "reason": "распознавание ударения не проверяет; словаря ударений домена в пакете нет",
                        "to_listen": disputed},
             "listened_by_human": False}
    failed = tempo_fail + [k for k, ok in (("WER", audio["asr"]["ok"]), ("рассинхрон", sync["ok"]),
                                           ("термины", terms.get("ok", True))) if not ok]
    return audio, not failed, ("; ".join(failed) or None)


def build(ch: str, node: str, script_path: Path, spec_path: Path, draft: bool, fmt: str | None,
          voice: str, styleguide: Path, out_root: Path, cache_dir: Path, domain: str = "geology",
          skip_asr: bool = False, asr_model: str = asr.DEFAULT_MODEL, layer_path: Path | None = None,
          checklist_path: Path = DEFAULT_CHECKLIST) -> dict:
    if not ID_RE.match(ch):
        raise VideoInputError(f"--ch «{ch}» — допустимы только [a-z0-9_.-]")
    if not ID_RE.match(domain):
        raise VideoInputError(f"--domain «{domain}» — допустимы только [a-z0-9_.-]")
    media.require("ffmpeg"), media.require("ffprobe")
    script, spec = load_inputs(script_path, spec_path, node_id=node)
    fmt = fmt or script.format
    if fmt not in RES:
        raise VideoInputError(f"формат {fmt} неизвестен; есть {sorted(RES)}")
    if spec.template not in TEMPLATES:
        raise VideoInputError(f"шаблон сцены «{spec.template}» не реализован; есть: {sorted(TEMPLATES)}")
    if format_problem(spec.template, fmt):
        raise VideoInputError(format_problem(spec.template, fmt))
    sg = _styleguide(styleguide)
    tpl_plan, tpl_colors, tpl_info = _prepare_template(spec, script, sg, ROOT / "domain" / domain / "templates")
    try:
        checklist_items = load_checklist(checklist_path)
    except PassportError as e:
        raise VideoInputError(str(e)) from e
    node_obj = None
    if layer_path is not None:
        from contracts.models import Layer
        if not Path(layer_path).is_file():
            raise VideoInputError(f"--layer: файл не найден: {layer_path}")
        layer = Layer.model_validate_json(Path(layer_path).read_text(encoding="utf-8"))
        node_obj = next((n for n in layer.nodes if n.id == script.node_id), None)
        if node_obj is None:
            raise VideoInputError(f"--layer: узла {script.node_id} нет в {layer_path}")
    _check_font(sg["font"])
    layout = (Layout(sg["safe_zone"], sg["min_caption_px"], ref=(REF_W, REF_H)) if fmt == "short"
              else Layout(LONG_SAFE_ZONE, sg["min_caption_px"], ref=REF_LONG))
    w, h, fps = RES[fmt]["draft" if draft else "final"]

    out = out_root / ch / "videos" / script.video_id
    work = out / "_work"
    work.mkdir(parents=True, exist_ok=True)

    # 1. озвучка по фразам (кэш) → PCM → фактическая длительность в сэмплах
    params = TtsParams(voice=voice)
    tts, pcm = {}, {}
    for p in script.phrases:
        tts[p.id] = synthesize(p.text, params, cache_dir)
        pcm[p.id] = media.decode_pcm(tts[p.id].mp3_path, SAMPLE_RATE)
    tl = build_timeline([(p.id, len(pcm[p.id]) // 2, p.pause_after_s) for p in script.phrases], SAMPLE_RATE)
    speech_wav = work / "speech.wav"
    assemble_wav(tl, pcm, speech_wav)

    # 2. субтитры: полный текст из меток речи
    phrases = {p.id: (p.text, tts[p.id].words, tts[p.id].timing) for p in script.phrases}
    cues = subtitle_cues(tl, phrases)
    kinds = sorted({c.source for c in cues})
    vtt = out / f"{script.video_id}.vtt"
    vtt.write_text(format_vtt(cues, note="; ".join(VTT_NOTES[k] for k in kinds)), encoding="utf-8")

    # 3. сцена: границы фраз из таймлайна
    shot_of = {pid: s for s in spec.shots for pid in s.phrase_ids}
    missing = sorted({s.label for s in spec.shots} - set(sg["provenance"]))
    if missing:
        raise VideoInputError(f"в стайлгайде нет цвета метки происхождения для {missing}")
    segs =[{"phrase_id": s.phrase_id, "start": s.start, "end": s.end, "hold_end": s.hold_end,
             "on_screen": p.on_screen, "shot_id": shot_of[p.id].id, "plaque": shot_of[p.id].plaque,
             "label": shot_of[p.id].label, "label_color": sg["provenance"][shot_of[p.id].label]}
            for s, p in zip(tl.segments, script.phrases)]
    plan = {"layout": layout, "font": sg["font"], "fps": fps, "segments": segs, "total": tl.total,
            "speech_total": tl.speech_total, **tpl_plan,
            "colors": {"text": sg["text"], "muted": sg["muted"], "panel": sg["panel"], **tpl_colors}}
    if spec.template == "T2":
        from pipeline.video.scene_t2 import T2Scene as scene_cls
    elif spec.template == "T1":
        from pipeline.video.scene_t1 import T1Scene as scene_cls
    else:
        from pipeline.video.scene_hello import HelloScene as scene_cls
    scene_mp4 = _render(scene_cls, plan, work, w, h, fps, sg["background"])

    # 4. сборка: нормализация −16 LUFS, H.264, длина = длина дорожки
    measured = media.loudnorm_measure(speech_wav)
    mp4 = out / f"{script.video_id}.mp4"
    media.mux(scene_mp4, speech_wav, mp4, tl.total, fps, measured, draft)
    check = _verify(mp4, tl, w, h, fps)

    # 5. отчёт
    # темп: по пословным меткам — от первого до последнего слова фразы (без тишины mp3), иначе по длине аудио
    n_words = sum(len(re.findall(r"\w+", p.text)) for p in script.phrases)
    spoken = sum((tts[s.phrase_id].words[-1].end - tts[s.phrase_id].words[0].start)
                 if tts[s.phrase_id].timing == "word" else s.duration for s in tl.segments)
    wpm = round(n_words / spoken * 60, 1)
    import edge_tts
    import manim
    timeline = {"sample_rate": SAMPLE_RATE, "total_s": tl.total, "speech_total_s": tl.speech_total,
                "phrases": [{"phrase_id": s.phrase_id, "start_s": s.start, "end_s": s.end, "hold_end_s": s.hold_end,
                             "timing": tts[s.phrase_id].timing, "tts_cached": tts[s.phrase_id].cached,
                             "tts_key": tts[s.phrase_id].key,
                             "words": [{"start_s": round(s.start + w_.start, 3), "end_s": round(s.start + w_.end, 3),
                                        "text": w_.text} for w_ in tts[s.phrase_id].words]}
                            for s in tl.segments]}
    report = {"video_id": script.video_id, "node_id": script.node_id, "format": fmt, "draft": draft,
              "resolution": [w, h], "fps": fps, "inputs": {"script": str(script_path), "scene_spec": str(spec_path),
                                                           "styleguide": str(styleguide)},
              "tts": {"engine": "edge-tts", "version": edge_tts.__version__, **params.__dict__},
              "manim": manim.__version__, "ffmpeg": media.version("ffmpeg"),
              "loudnorm_input": measured, "words": n_words, "wpm": wpm,
              "warnings": [] if TARGET_WPM[0] <= wpm <= TARGET_WPM[1] else
              [f"темп {wpm} слов/мин вне {TARGET_WPM[0]}–{TARGET_WPM[1]}"],
              "template": spec.template, "template_info": tpl_info,
              "shots": [{"shot_id": sid, "start_s": round(min(x["start"] for x in segs if x["shot_id"] == sid), 3),
                         "end_s": round(max(x["hold_end"] for x in segs if x["shot_id"] == sid), 3),
                         "plaque": next(x["plaque"] for x in segs if x["shot_id"] == sid),
                         "true_scale": sid == spec.true_scale_shot_id}
                        for sid in dict.fromkeys(x["shot_id"] for x in segs)],
              "subtitle_timing": kinds, "cues": len(cues), "mp4": str(mp4), "vtt": str(vtt), "probe": check}
    # кадры для ревью: середина окна каждого shot и последний кадр (финальное состояние)
    frames_dir = out / "frames"
    if frames_dir.is_dir():
        for f in frames_dir.glob("*.png"):
            f.unlink()
    report["frames"] = []
    for sh in report["shots"]:
        t_mid = round((sh["start_s"] + sh["end_s"]) / 2, 3)
        png = frames_dir / f"{sh['shot_id']}.png"
        media.extract_frame(mp4, t_mid, png)
        report["frames"].append({"shot_id": sh["shot_id"], "t_s": t_mid, "file": str(png)})
    last = frames_dir / "final.png"
    media.extract_frame(mp4, max(tl.total - 1.5 / fps, 0.0), last)
    report["frames"].append({"shot_id": report["shots"][-1]["shot_id"], "t_s": round(tl.total - 1.5 / fps, 3),
                             "file": str(last)})
    # 6. проверка озвучки и паспорт ролика
    audio, audio_ok, audio_problem = _audio_check(mp4, script, timeline, check, wpm, voice, skip_asr, asr_model,
                                                  node_obj, out)
    from pipeline.video.templates import load_template_config
    tcfg = load_template_config(ROOT / "domain" / domain / "templates", spec.template)
    checklist = checklist_answers(checklist_items, (tcfg or {}).get("physics_checklist"), _auto_checks(spec, tpl_info))
    passport = assemble(script=script, spec=spec,
                        segments=[{"phrase_id": s.phrase_id, "start": s.start, "end": s.end} for s in tl.segments],
                        frames=[{"t": f["t_s"], "shot_id": f["shot_id"], "file": _rel(f["file"])} for f in report["frames"]],
                        node_card=_node_card(script, node_obj), sources=_sources(script, spec, tpl_info),
                        checklist=checklist, audio_check=audio, scene_spec_path=_rel(out / "scene_spec.json"),
                        panels=((tcfg or {}).get("display") or {}).get("schema_panels"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        write_passport(passport, out / "passport.json", schema)
    except PassportError as e:
        raise BuildCheckError(str(e)) from e
    report.update({"passport": str(out / "passport.json"), "audio_ok": audio_ok, "audio_problem": audio_problem,
                   "checklist_status": {s: sum(1 for c in checklist if c.status == s)
                                        for s in dict.fromkeys(c.status for c in checklist)}})
    (out / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "build_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "script.json").write_text(script.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    (out / "scene_spec.json").write_text(spec.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    return report


def _same_file(a: Path, b: Path) -> bool:
    return Path(a).resolve() == Path(b).resolve()


def _check_ready_pair(script_path: Path, spec_path: Path, node, route, fmt: str, dataset: Path | None,
                      domain: str) -> None:
    """Готовая пара из каталога video.spec: тот же узел, формат, шаблон и набор данных, плюс все проверки
    генератора относительно текущего узла (spec.pair_problems, без LLM). Битые файлы — ошибка, не перегенерация."""
    from pipeline.video import spec as vspec
    from pipeline.video.t2_template import resolve_dataset_path
    script, spec = load_inputs(script_path, spec_path, node_id=node.id)
    problems = []
    if script.video_id != f"{node.id}.{fmt}":
        problems.append(f"video_id «{script.video_id}», а для узла и формата нужен «{node.id}.{fmt}»")
    if script.format != fmt:
        problems.append(f"формат сценария {script.format}, а маршрут даёт {fmt}")
    if spec.template != route.template:
        problems.append(f"шаблон спецификации {spec.template}, а в маршруте {route.template}")
    ds = spec.params.get("dataset")
    if dataset is not None and (not isinstance(ds, str) or not _same_file(resolve_dataset_path(ds), dataset)):
        problems.append(f"спецификация собрана с набором данных {ds!r}, а передан --dataset {dataset}")
    if not problems:   # содержательные проверки — только для пары, которая вообще относится к этому маршруту
        problems += vspec.pair_problems(script, spec, node, fmt, ROOT / "domain" / domain / "templates")
    if problems:
        raise VideoInputError(f"готовая пара в {script_path.parent} не подходит:\n- " + "\n- ".join(problems)
                              + "\nУдалите её, чтобы сгенерировать заново, или передайте --script и --scene-spec")


def resolve_inputs(ch: str, node: str, script: Path | None, scene_spec: Path | None, layer: Path | None,
                   routing: Path | None, out_root: Path, domain: str, fmt: str | None, dataset: Path | None
                   ) -> tuple[Path, Path, Path | None, str | None]:
    """(script.json, scene_spec.json, layer.json для паспорта, формат) для сборки.

    Явная пара — как есть. Без пары: узел и маршрут из layer.json/routing.json; готовая пара из каталога
    video.spec проверяется и используется; если пары нет — вызывается video.spec (генерация через LLM)."""
    if (script is None) != (scene_spec is None):
        raise VideoInputError("нужны оба файла --script и --scene-spec или ни одного (тогда пара берётся из "
                              "каталога video.spec или генерируется)")
    if script is not None:
        if routing is not None or dataset is not None:
            raise VideoInputError("--routing и --dataset нужны только без --script/--scene-spec (для video.spec)")
        return script, scene_spec, layer, fmt
    from pipeline.video import spec as vspec
    layer, routing = vspec.default_paths(ch, out_root, layer, routing)
    try:
        node_obj, route, route_fmt = vspec.load_route(ch, node, layer, routing, out_root)
    except vspec.SpecError as e:
        raise VideoInputError(str(e)) from e
    if fmt is not None and fmt != route_fmt:
        raise VideoInputError(f"--format {fmt}, а маршрут узла {node} даёт {route_fmt} (шаблон {route.template})")
    out = vspec.output_dir(out_root, ch, node_obj.id, route_fmt)
    sp, cp = out / "script.json", out / "scene_spec.json"
    if sp.exists() and cp.exists():
        _check_ready_pair(sp, cp, node_obj, route, route_fmt, dataset, domain)
    elif sp.exists() or cp.exists():
        raise VideoInputError(f"в {out} только один файл из пары script.json/scene_spec.json — пара неполная; "
                              f"удалите его, чтобы сгенерировать заново")
    else:
        try:
            vspec.run(ch, node, layer, routing, out_root, domain, dataset)
        except vspec.SpecError as e:
            raise VideoInputError(f"генерация сценария и спецификации (video.spec) не удалась: {e}") from e
    return sp, cp, layer, route_fmt


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.video.build", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ch", required=True, help="id главы: каталог out/<ch>/")
    ap.add_argument("--node", required=True, help="id узла; должен совпадать с Script.node_id")
    ap.add_argument("--script", type=Path, help="Script JSON (contracts.models.Script)")
    ap.add_argument("--scene-spec", type=Path, help="SceneSpec JSON (contracts.models.SceneSpec)")
    ap.add_argument("--format", choices=["short", "long"], help="по умолчанию — Script.format")
    ap.add_argument("--draft", action="store_true", help="черновик 540×960, 15 к/с")
    ap.add_argument("--voice", default=DEFAULT_VOICE, help="голос edge-tts (один на всю серию)")
    ap.add_argument("--styleguide", type=Path, default=DEFAULT_STYLEGUIDE)
    ap.add_argument("--domain", default="geology", help="доменный пакет: настройки шаблонов в domain/<домен>/templates/")
    ap.add_argument("--out-root", type=Path, default=ROOT / "out")
    ap.add_argument("--cache-dir", type=Path, default=ROOT / "cache" / "tts")
    ap.add_argument("--skip-asr", action="store_true", help="не распознавать озвучку (в паспорте — «не проверено»)")
    ap.add_argument("--asr-model", default=asr.DEFAULT_MODEL, help="модель faster-whisper (локально)")
    ap.add_argument("--layer", type=Path, help="layer.json (по умолчанию out/<ch>/layer.json без явной пары); "
                                               "карточка узла и термины в паспорте")
    ap.add_argument("--routing", type=Path, help="routing.json (по умолчанию out/<ch>/routing.json; без явной пары)")
    ap.add_argument("--dataset", type=Path, help="описание набора данных для шаблонов с данными (T2), без явной пары")
    ap.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST, help="physics_checklist.json")
    a = ap.parse_args(argv)
    try:
        script_path, spec_path, layer_path, fmt = resolve_inputs(
            a.ch, a.node, a.script, a.scene_spec, a.layer, a.routing, a.out_root, a.domain, a.format, a.dataset)
        r = build(a.ch, a.node, script_path, spec_path, a.draft, fmt, a.voice,
                  a.styleguide, a.out_root, a.cache_dir, a.domain, a.skip_asr, a.asr_model, layer_path, a.checklist)
    except (VideoInputError, TtsError, ToolError, LayoutError, BuildCheckError) as e:
        print(f"ОШИБКА video.build: {e}", file=sys.stderr)
        return 2
    p = r["probe"]
    print(f"MP4: {r['mp4']}\nVTT: {r['vtt']}\n"
          f"{p['width']}x{p['height']} {p['video_codec']} {p['video_duration_s']:.3f} с, "
          f"звук {p['audio_codec']} {p['audio_duration_s']:.3f} с, {p['integrated_lufs']} LUFS, "
          f"пик {p['true_peak_dbtp']} dBTP, темп {r['wpm']} сл/мин, субтитры: {', '.join(r['subtitle_timing'])}")
    for wmsg in r["warnings"]:
        print(f"ПРЕДУПРЕЖДЕНИЕ: {wmsg}")
    print(f"паспорт: {r['passport']} (чек-лист: {r['checklist_status']})")
    if r["audio_ok"] is not True:
        print(f"ОШИБКА проверки озвучки: {r['audio_problem']} — ролик и паспорт записаны, подробности в паспорте "
              f"(audio_check) и asr_report.json", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
