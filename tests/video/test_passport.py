"""Паспорт ролика: сборка через Passport, честный чек-лист, проверка по схеме организаторов. Без сети."""
import json
from pathlib import Path

import pytest

from contracts.models import SceneSpec, Script
from pipeline.video.passport import (STATUS_AUTO, STATUS_NA, STATUS_UNCHECKED, PassportError, assemble,
                                     audio_check_skipped, checklist_answers, load_checklist, plaques_have_number,
                                     strip_disallowed_nulls, write_passport)
from pipeline.video.templates import load_template_config

ROOT = Path(__file__).resolve().parents[2]
VOLVE = ROOT / "fixtures" / "video" / "t2_volve"
SCHEMA = json.loads((ROOT / "data" / "organizers" / "01_схемы" / "passport.schema.json").read_text(encoding="utf-8"))
ITEMS = load_checklist(ROOT / "data" / "organizers" / "04_доменные_заготовки" / "physics_checklist.json")
T2 = load_template_config(ROOT / "domain" / "geology" / "templates", "T2")


def _inputs():
    script = Script.model_validate_json((VOLVE / "script.json").read_text(encoding="utf-8"))
    spec = SceneSpec.model_validate_json((VOLVE / "scene_spec.json").read_text(encoding="utf-8"))
    return script, spec


def test_checklist_is_honest():
    auto = {"one_state_variable": (True, "тест"), "plaques_have_number": (False, "у s2 нет числа")}
    ans = {a.item: a for a in checklist_answers(ITEMS, T2["physics_checklist"], auto)}
    assert set(ans) == {i["id"] for i in ITEMS}                                  # все 24 пункта
    assert ans["pc.curve_sync"].answer == "да" and ans["pc.curve_sync"].status == STATUS_AUTO
    assert ans["pc.exaggeration_named"].answer == "нет" and "s2" in ans["pc.exaggeration_named"].note
    assert ans["pc.layers_order"].answer == "н/п" and ans["pc.layers_order"].status == STATUS_NA
    # автопроверка, которая не выполнялась, и пункт без автопроверки — «не проверено», не «н/п» и не «да»
    for key in ("pc.depth_down", "pc.tool_mechanism", "pc.plausible_numbers"):
        a = ans[key]
        assert a.status == STATUS_UNCHECKED and a.answer == "нет" and "не проверено" in a.note
    assert all(a.answer != "н/п" for a in ans.values() if a.status != STATUS_NA)


def test_template_without_checklist_config_leaves_everything_unchecked():
    ans = checklist_answers(ITEMS, None, {"one_state_variable": (True, "тест")})
    assert {a.status for a in ans} == {STATUS_UNCHECKED}


def test_plaques_have_number():
    _, spec = _inputs()
    assert plaques_have_number(spec)[0] is True
    spec.shots[1].plaque = "не в масштабе: ствол шире"
    ok, note = plaques_have_number(spec)
    assert ok is False and "s2" in note


def test_strip_only_disallowed_nulls():
    data = {"script": [{"t_start": 0, "t_end": 1, "text": "x", "claim_id": None, "on_screen": None,
                        "is_analogy": None}], "sources": [{"claim_id": "a", "page_or_dataset": "b", "quote": None}]}
    out = strip_disallowed_nulls(data, SCHEMA)
    assert out["script"][0] == {"t_start": 0, "t_end": 1, "text": "x", "claim_id": None}   # claim_id: null допустим
    assert out["sources"][0] == {"claim_id": "a", "page_or_dataset": "b"}


def _passport(audio_check=None):
    script, spec = _inputs()
    segs = [{"phrase_id": p.id, "start": 1.0 + i, "end": 1.8 + i} for i, p in enumerate(script.phrases)]
    frames = [{"t": 1.4, "shot_id": "s1", "file": "frames/s1.png"}, {"t": 9.0, "shot_id": "s5", "file": "frames/s5.png"}]
    checklist = checklist_answers(ITEMS, T2["physics_checklist"], {})
    return assemble(script=script, spec=spec, segments=segs, frames=frames,
                    node_card={"node_id": spec.node_id, "status": "нет учебного слоя"},
                    sources=[{"claim_id": f"{spec.video_id}#data", "page_or_dataset": "Volve, 159-19A_LFP.las"}],
                    checklist=checklist, audio_check=audio_check or audio_check_skipped("тест"),
                    scene_spec_path="out/x/videos/t2_volve_16x9/scene_spec.json",
                    panels=T2["display"]["schema_panels"])


def test_assembled_passport_passes_organizers_schema(tmp_path):
    p = _passport()
    data = write_passport(p, tmp_path / "passport.json", SCHEMA)
    saved = json.loads((tmp_path / "passport.json").read_text(encoding="utf-8"))
    assert saved == data
    assert saved["frames"][0] == {"t": 1.4, "class": "A", "label": "реальные данные",
                                  "ext": {"shot_id": "s1", "file": "frames/s1.png",
                                          "panels": {"ствол и прибор": "схема"}}}
    assert saved["script"][0]["t_start"] == 1.0 and saved["script"][0]["claim_id"] is None
    assert saved["exaggerations"] == ["ствол и прибор шире в 20 раз"]
    assert saved["audio_check"]["asr"]["status"] == STATUS_UNCHECKED
    assert "wer" not in saved["audio_check"]["asr"]                               # не выдумываем результат


def test_schema_violation_is_an_error(tmp_path):
    p = _passport()
    p.frames[0].label = "иллюстрация ИИ"          # обходим pydantic: так в паспорт не должно попасть
    with pytest.raises(PassportError, match="label"):
        write_passport(p, tmp_path / "passport.json", SCHEMA)
    assert not (tmp_path / "passport.json").exists()


def test_skipped_audio_check_marks_everything_unverified():
    a = audio_check_skipped("флаг --skip-asr")
    assert a["asr"]["status"] == STATUS_UNCHECKED and "--skip-asr" in a["asr"]["reason"]
    assert a["sync"]["status"] == STATUS_UNCHECKED and a["stress"]["status"] == STATUS_UNCHECKED
    assert a["listened_by_human"] is False


# ---------------------------------------------------------------- проверка озвучки в сборке (без сети и модели)

from pipeline.video import asr, build, media  # noqa: E402

PROBE = {"integrated_lufs": -16.0, "true_peak_dbtp": -1.5, "trailing_silence_s": 1.7,
         "checks": {"lufs_within_1lu_of_-16": True, "true_peak_le_-1dbtp": True, "last_phrase_inside": True}}


def _timeline(script):
    out, t = [], 0.5
    for p in script.phrases:
        words = []
        for w in asr.normalize_words(p.text):
            words.append({"start_s": round(t, 3), "end_s": round(t + 0.3, 3), "text": w})
            t += 0.4
        out.append({"phrase_id": p.id, "timing": "word", "words": words})
        t += 0.5
    return {"phrases": out}


def _fake_asr(monkeypatch, script, drop=0, shift=0.0):
    tl = _timeline(script)
    words = [{"start": w["start_s"] + shift, "end": w["end_s"] + shift, "word": w["text"], "probability": 0.9}
             for ph in tl["phrases"] for w in ph["words"]]
    words = words[drop:]
    monkeypatch.setattr(media, "decode_pcm", lambda src, sr: b"\x00\x00" * 160)
    monkeypatch.setattr(asr, "transcribe", lambda audio, model: {
        "engine": "faster-whisper", "version": "тест", "model": model, "language": "ru", "text": "", "words": words})
    return tl


def test_audio_check_passes_on_matching_recognition(tmp_path, monkeypatch):
    script, _ = _inputs()
    tl = _fake_asr(monkeypatch, script)
    audio, ok, problem = build._audio_check(tmp_path / "x.mp4", script, tl, PROBE, 140.0, "v", False, "small",
                                            None, tmp_path)
    assert ok is True and problem is None
    assert audio["asr"]["wer"] == 0 and audio["sync"]["ok"] and audio["sync"]["max_abs_s"] == 0
    assert audio["terms"]["status"] == STATUS_UNCHECKED                         # нет --layer — нет списка терминов
    assert audio["stress"]["status"] == STATUS_UNCHECKED and audio["listened_by_human"] is False
    assert audio["sync"]["frame_vs_voice"]["status"] == STATUS_UNCHECKED
    assert (tmp_path / "asr_report.json").is_file()


def test_audio_check_fails_on_high_wer(tmp_path, monkeypatch):
    script, _ = _inputs()
    tl = _fake_asr(monkeypatch, script, drop=30)                                # треть слов «не услышана»
    audio, ok, problem = build._audio_check(tmp_path / "x.mp4", script, tl, PROBE, 140.0, "v", False, "small",
                                            None, tmp_path)
    assert ok is False and "WER" in problem and audio["asr"]["wer"] > 0.1
    assert audio["asr"]["errors"][0]["type"] == "del" and audio["asr"]["errors"][0]["phrase_id"] == "p1"
    assert set(audio["stress"]["to_listen"]) >= {audio["asr"]["errors"][0]["expected"]}


def test_audio_check_fails_on_desync(tmp_path, monkeypatch):
    script, _ = _inputs()
    tl = _fake_asr(monkeypatch, script, shift=0.8)
    _, ok, problem = build._audio_check(tmp_path / "x.mp4", script, tl, PROBE, 140.0, "v", False, "small",
                                        None, tmp_path)
    assert ok is False and "рассинхрон" in problem


def test_audio_check_skipped_and_model_failure_are_not_success(tmp_path, monkeypatch):
    script, _ = _inputs()
    audio, ok, problem = build._audio_check(tmp_path / "x.mp4", script, {}, PROBE, 140.0, "v", True, "small",
                                            None, tmp_path)
    assert ok is None and audio["asr"]["status"] == STATUS_UNCHECKED and "wer" not in audio["asr"]
    assert audio["loudness"]["integrated_lufs"] == -16.0                        # измеренное — остаётся
    monkeypatch.setattr(media, "decode_pcm", lambda src, sr: b"\x00\x00" * 16)

    def no_model(audio, model):
        raise asr.AsrError("нет сети и модели в кэше")
    monkeypatch.setattr(asr, "transcribe", no_model)
    audio, ok, problem = build._audio_check(tmp_path / "x.mp4", script, {}, PROBE, 140.0, "v", False, "small",
                                            None, tmp_path)
    assert ok is None and "нет сети" in audio["asr"]["reason"]


def test_dataset_row_in_sources():
    script, spec = _inputs()
    info = {"dataset_provenance": {"attribution": "Volve", "source": "s", "file": "f.las", "well": "15/9-19",
                                   "uwi": "NO 15/9-19 A", "interval_m": [3790.0, 3875.0], "sha256": "ab" * 32}}
    rows = build._sources(script, spec, info)
    assert rows[-1]["claim_id"] == "t2_volve_16x9#data"
    assert "f.las" in rows[-1]["page_or_dataset"] and "3790–3875 м" in rows[-1]["page_or_dataset"]


# ---------------------------------------------------------------- регрессия: темп входит в итог

def test_bad_tempo_fails_audio_check_even_with_perfect_recognition(tmp_path, monkeypatch):
    script, _ = _inputs()
    tl = _fake_asr(monkeypatch, script)
    audio, ok, problem = build._audio_check(tmp_path / "x.mp4", script, tl, PROBE, 95.0, "v", False, "small",
                                            None, tmp_path)
    assert audio["tempo"]["ok"] is False and audio["asr"]["ok"] and audio["sync"]["ok"]
    assert ok is False and "темп" in problem


def test_bad_tempo_is_a_failure_even_when_asr_is_skipped(tmp_path):
    script, _ = _inputs()
    audio, ok, problem = build._audio_check(tmp_path / "x.mp4", script, {}, PROBE, 170.0, "v", True, "small",
                                            None, tmp_path)
    assert ok is False and "темп" in problem and "--skip-asr" in problem
    assert audio["asr"]["status"] == STATUS_UNCHECKED


def test_terms_checked_per_occurrence_in_build(tmp_path, monkeypatch):
    from contracts.models import Layer
    script, _ = _inputs()
    tl = _fake_asr(monkeypatch, script)
    words = [w for ph in tl["phrases"] for w in ph["words"]]
    i = [k for k, w in enumerate(words) if w["text"] == "сопротивление"]
    assert len(i) >= 2                                                         # термин звучит несколько раз
    heard = [{"start": w["start_s"], "end": w["end_s"], "word": ("сопротивления" if k == i[-1] else w["text"]),
              "probability": 0.9} for k, w in enumerate(words)]
    monkeypatch.setattr(asr, "transcribe", lambda audio, model: {
        "engine": "faster-whisper", "version": "тест", "model": model, "language": "ru", "text": "", "words": heard})
    layer = Layer.model_validate_json((ROOT / "fixtures" / "video" / "spec" / "layer.json").read_text(encoding="utf-8"))
    node = layer.nodes[0].model_copy(update={"terms_introduced": ["сопротивление"], "terms_used": []})
    audio, ok, problem = build._audio_check(tmp_path / "x.mp4", script, tl, PROBE, 140.0, "v", False, "small",
                                            node, tmp_path)
    assert audio["terms"]["not_recognized"] == ["сопротивление"]
    assert [o["ok"] for o in audio["terms"]["occurrences"]].count(False) == 1
    assert ok is False and "термины" in problem
