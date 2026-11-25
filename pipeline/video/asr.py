"""Локальная проверка озвучки: faster-whisper → сравнение со сценарием (WER) и рассинхрон слов.

Аудио никуда не отправляется: модель запускается локально (CPU, int8). Модель скачивается
один раз с Hugging Face в кэш пользователя; при отсутствии сети и кэша — понятная ошибка.
"""
from __future__ import annotations

import re
import statistics

import numpy as np

WER_LIMIT = 0.10
SYNC_LIMIT_S = 0.5
DEFAULT_MODEL = "small"


class AsrError(RuntimeError):
    pass


def normalize_words(text: str) -> list[str]:
    """Нижний регистр, ё → е, только буквы и цифры; дефисы и тире делят слова."""
    return re.findall(r"[a-zа-я0-9]+", text.lower().replace("ё", "е"))


def _align(ref: list[str], hyp: list[str]) -> list[tuple[str, int | None, int | None]]:
    """Левенштейн по словам с обратным ходом: (ok|sub|del|ins, индекс в ref, индекс в hyp)."""
    n, m = len(ref), len(hyp)
    d = np.zeros((n + 1, m + 1), dtype=int)
    d[:, 0] = np.arange(n + 1)
    d[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + (ref[i - 1] != hyp[j - 1]))
    ops, i, j = [], n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and d[i, j] == d[i - 1, j - 1] + (ref[i - 1] != hyp[j - 1]):
            ops.append(("ok" if ref[i - 1] == hyp[j - 1] else "sub", i - 1, j - 1))
            i, j = i - 1, j - 1
        elif i > 0 and d[i, j] == d[i - 1, j] + 1:
            ops.append(("del", i - 1, None))
            i -= 1
        else:
            ops.append(("ins", None, j - 1))
            j -= 1
    return ops[::-1]


def wer_report(phrases: list[tuple[str, str]], hyp: list[str]) -> dict:
    """WER сценария (phrase_id, текст) против распознанных слов; ошибки привязаны к фразам."""
    ref, owner = [], []
    for pid, text in phrases:
        w = normalize_words(text)
        ref += w
        owner += [pid] * len(w)
    hyp = [x for h in hyp for x in normalize_words(h)]
    ops = _align(ref, hyp)
    errors, last_pid = [], phrases[0][0] if phrases else None   # вставка до первого слова — к первой фразе
    for kind, i, j in ops:
        if i is not None:
            last_pid = owner[i]
        if kind == "ok":
            continue
        pid = owner[i] if i is not None else last_pid            # вставка — к фразе последнего слова сценария
        errors.append({"type": kind, "phrase_id": pid,
                       "expected": ref[i] if i is not None else None, "heard": hyp[j] if j is not None else None})
    per_phrase = {pid: 0 for pid, _ in phrases}
    for e in errors:
        per_phrase[e["phrase_id"]] += 1
    n = len(ref)
    return {"wer": (len(errors) / n) if n else 0.0, "n_ref": n, "n_hyp": len(hyp),
            "substitutions": sum(e["type"] == "sub" for e in errors),
            "deletions": sum(e["type"] == "del" for e in errors),
            "insertions": sum(e["type"] == "ins" for e in errors),
            "errors": errors, "per_phrase": per_phrase}


def term_report(phrases: list[tuple[str, str]], hyp: list[str], terms: list[str]) -> dict:
    """Каждое употребление термина в сценарии проверяется по выравниванию сценария и распознавания:
    употребление верно, только если все его слова сопоставлены точно и стоят в распознавании подряд —
    вставка внутри составного термина делает его неверным, вставки до и после — нет.
    Одно верное употребление не скрывает другое. heard — весь распознанный фрагмент, со вставками."""
    ref, owner = [], []
    for pid, text in phrases:
        w = normalize_words(text)
        ref += w
        owner += [pid] * len(w)
    hyp = [x for h in hyp for x in normalize_words(h)]
    match: dict[int, tuple[str, int | None]] = {}       # индекс слова сценария → (ok|sub|del, индекс в hyp)
    for kind, i, j in _align(ref, hyp):
        if i is not None:
            match[i] = (kind, j)
    used, occurrences = [], []
    for term in dict.fromkeys(terms):
        tw = normalize_words(term)
        if not tw:
            continue
        starts = [k for k in range(len(ref) - len(tw) + 1) if ref[k:k + len(tw)] == tw]
        if starts:
            used.append(term)
        for k in starts:
            span = range(k, k + len(tw))
            js = [match[i][1] for i in span if match[i][1] is not None]
            # верно: каждое слово совпало точно И в распознавании они стоят подряд (без вставок внутри термина)
            exact = all(match[i][0] == "ok" for i in span)
            contiguous = len(js) == len(tw) and js == list(range(js[0], js[0] + len(tw)))
            occurrences.append({"term": term, "phrase_id": owner[k], "ok": exact and contiguous,
                                # весь распознанный фрагмент от первого до последнего сопоставленного слова,
                                # включая вставки между ними
                                "heard": hyp[js[0]:js[-1] + 1] if js else []})
    bad = list(dict.fromkeys(o["term"] for o in occurrences if not o["ok"]))
    return {"terms_in_script": used, "occurrences": occurrences, "not_recognized": bad, "ok": not bad}


def sync_report(tts: list[tuple[float, str]], asr: list[tuple[float, str]], limit_s: float = SYNC_LIMIT_S) -> dict:
    """Рассинхрон: для совпавших слов — начало по распознаванию минус начало по меткам TTS (в ролике)."""
    def flat(words):
        out = []
        for t, w in words:
            out += [(t, x) for x in normalize_words(w)]
        return out
    a, b = flat(tts), flat(asr)
    ops = _align([w for _, w in a], [w for _, w in b])
    diffs = [b[j][0] - a[i][0] for kind, i, j in ops if kind == "ok"]
    absd = [abs(x) for x in diffs]
    if not absd:
        return {"matched_words": 0, "ok": False, "limit_s": limit_s,
                "note": "ни одно слово распознавания не совпало со словами сценария"}
    return {"matched_words": len(absd), "median_abs_s": round(statistics.median(absd), 3),
            "p95_abs_s": round(float(np.percentile(absd, 95)), 3), "max_abs_s": round(max(absd), 3),
            "mean_signed_s": round(statistics.mean(diffs), 3), "limit_s": limit_s, "ok": max(absd) <= limit_s}


def transcribe(audio_16k: np.ndarray, model_name: str = DEFAULT_MODEL, language: str = "ru") -> dict:
    """Распознавание моно 16 кГц float32. Возвращает слова с метками и сведения о модели."""
    try:
        import faster_whisper
        from faster_whisper import WhisperModel
    except ModuleNotFoundError as e:
        raise AsrError("faster-whisper не установлен (requirements/video.txt)") from e
    try:
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
    except Exception as e:   # нет сети и нет модели в кэше, повреждённый кэш
        raise AsrError(f"модель faster-whisper «{model_name}» не загружена: {type(e).__name__}: {e}") from e
    segments, info = model.transcribe(audio_16k, language=language, word_timestamps=True, beam_size=5,
                                      vad_filter=False, condition_on_previous_text=False)
    words, text = [], []
    for seg in segments:
        text.append(seg.text)
        for w in seg.words or []:
            words.append({"start": round(float(w.start), 3), "end": round(float(w.end), 3), "word": w.word.strip(),
                          "probability": round(float(w.probability), 3)})
    return {"engine": "faster-whisper", "version": faster_whisper.__version__, "model": model_name,
            "language": info.language, "language_probability": round(float(info.language_probability), 3),
            "text": " ".join(t.strip() for t in text), "words": words}
