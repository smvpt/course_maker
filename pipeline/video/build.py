"""Сборка ролика: Script + SceneSpec → озвучка → сцена Manim → MP4 + VTT.

    python -m pipeline.video.build --ch <id> --node <node_id> \
        --script <script.json> --scene-spec <scene_spec.json> [--draft]

Выходы — out/<ch>/videos/<video_id>/: <video_id>.mp4, <video_id>.vtt, script.json,
scene_spec.json, timeline.json, build_report.json, _work/ (промежуточные файлы).
Генерация Script/SceneSpec из layer.json (video.spec) — задача 2, здесь не делается.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from pipeline.video import media
from pipeline.video.inputs import ID_RE, VideoInputError, load_inputs
from pipeline.video.layout import FRAME_H, FRAME_W, Layout, LayoutError
from pipeline.video.media import ToolError
from pipeline.video.timeline import build_timeline, format_vtt, subtitle_cues, assemble_wav
from pipeline.video.tts import DEFAULT_VOICE, TtsError, TtsParams, synthesize

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_STYLEGUIDE = ROOT / "data" / "organizers" / "03_стайлгайд" / "styleguide.json"
SAMPLE_RATE = 24000          # родная частота edge-tts (audio-24khz-48kbitrate-mono-mp3)
RES = {"short": {"final": (1080, 1920, 30), "draft": (540, 960, 15)}}
TEMPLATES = {"hello"}
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
        return {"background": sg["background"], "text": sg["text"], "muted": sg["muted"],
                "provenance": sg["provenance"], "font": sg["fonts"]["ui"],
                "min_caption_px": sg["fonts"]["min_caption_px_at_1080"], "safe_zone": sg["safe_zone"]}
    except FileNotFoundError as e:
        raise VideoInputError(f"стайлгайд не найден: {path}") from e
    except (KeyError, json.JSONDecodeError) as e:
        raise VideoInputError(f"стайлгайд {path} без нужного поля или не JSON: {e}") from e


def _check_font(font: str) -> None:
    import manimpango
    if font not in manimpango.list_fonts():
        raise ToolError(f"шрифт стайлгайда «{font}» не установлен в системе — кириллица не отрисуется как задано")


def _render(plan: dict, work: Path, w: int, h: int, fps: int, background: str) -> Path:
    from manim import tempconfig
    from pipeline.video.scene_hello import HelloScene
    cfg = {"pixel_width": w, "pixel_height": h, "frame_rate": fps, "frame_height": FRAME_H,
           "frame_width": FRAME_W, "media_dir": str(work / "manim"), "disable_caching": True,
           "background_color": background, "progress_bar": "none", "verbosity": "WARNING",
           "output_file": "scene", "preview": False}
    with tempconfig(cfg):
        scene = HelloScene()
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


def build(ch: str, node: str, script_path: Path, spec_path: Path, draft: bool, fmt: str | None,
          voice: str, styleguide: Path, out_root: Path, cache_dir: Path) -> dict:
    if not ID_RE.match(ch):
        raise VideoInputError(f"--ch «{ch}» — допустимы только [a-z0-9_.-]")
    media.require("ffmpeg"), media.require("ffprobe")
    script, spec = load_inputs(script_path, spec_path, node_id=node)
    fmt = fmt or script.format
    if fmt not in RES:
        raise VideoInputError(f"формат {fmt}: пока собирается только short (9:16)")
    if spec.template not in TEMPLATES:
        raise VideoInputError(f"шаблон сцены «{spec.template}» не реализован; есть: {sorted(TEMPLATES)}")
    if not isinstance(spec.params.get("title"), str) or not spec.params["title"].strip():
        raise VideoInputError("SceneSpec.params.title обязателен для шаблона hello")
    sg = _styleguide(styleguide)
    _check_font(sg["font"])
    layout = Layout(sg["safe_zone"], sg["min_caption_px"])
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
             "on_screen": p.on_screen, "label": shot_of[p.id].label,
             "label_color": sg["provenance"][shot_of[p.id].label]}
            for s, p in zip(tl.segments, script.phrases)]
    plan = {"layout": layout, "colors": {"text": sg["text"], "muted": sg["muted"]}, "font": sg["font"],
            "fps": fps, "segments": segs, "total": tl.total, "speech_total": tl.speech_total,
            "title": spec.params["title"]}
    scene_mp4 = _render(plan, work, w, h, fps, sg["background"])

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
              "subtitle_timing": kinds, "cues": len(cues), "mp4": str(mp4), "vtt": str(vtt), "probe": check}
    (out / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "build_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "script.json").write_text(script.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    (out / "scene_spec.json").write_text(spec.model_dump_json(by_alias=True, indent=2), encoding="utf-8")
    return report


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
    ap.add_argument("--out-root", type=Path, default=ROOT / "out")
    ap.add_argument("--cache-dir", type=Path, default=ROOT / "cache" / "tts")
    a = ap.parse_args(argv)
    try:
        if a.script is None or a.scene_spec is None:
            raise VideoInputError("нужны --script и --scene-spec: генерация их из layer.json (video.spec) "
                                  "ещё не реализована")
        r = build(a.ch, a.node, a.script, a.scene_spec, a.draft, a.format, a.voice,
                  a.styleguide, a.out_root, a.cache_dir)
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
