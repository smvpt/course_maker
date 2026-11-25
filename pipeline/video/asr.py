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


SNAP_REASON = ("начало первого слова сегмента распознавание поставило в тишину перед ним (после конца "
               "предыдущего слова по меткам TTS) — звука там нет; конец слова совпал")


def sync_report(tts: list[tuple], asr: list[tuple], limit_s: float = SYNC_LIMIT_S) -> dict:
    """Рассинхрон слов: распознавание готового ролика против меток TTS в таймлайне.

    tts — (начало, конец, слово); asr — (начало, конец, слово[, первое_в_сегменте]).
    По каждому совпавшему слову проверяются обе границы:
      обе в пределах порога — синхронно; обе за порогом — рассинхрон (ok = False);
      одна за порогом — метки неоднозначны: «не проверено» (ok = None), кроме одного обоснованного исключения —
      первое слово сегмента, начало распознано раньше, внутри тишины после предыдущего слова, конец совпал
      (известная особенность меток Whisper). Каждое исключение записывается с обоснованием.
    ok = True — только если все слова синхронны или подпадают под исключение.
    """
    def flat(words, has_first: bool):
        """Слова → нормализованные части. Метка, покрывшая несколько частей («гамма-каротаж»), задаёт только
        начало первой части и конец последней; внутренние границы неизвестны (None) и не сравниваются."""
        out = []
        for item in words:
            t0, t1, w = item[:3]
            first = bool(item[3]) if has_first and len(item) > 3 else False
            parts = normalize_words(w)
            for k, x in enumerate(parts):
                out.append((t0 if k == 0 else None, t1 if k == len(parts) - 1 else None, x, first and k == 0))
        return out

    a, b = flat(tts, False), flat(asr, True)
    ops = _align([x[2] for x in a], [x[2] for x in b])
    pairs = [(i, j) for kind, i, j in ops if kind == "ok"]
    if not pairs:
        return {"matched_words": 0, "ok": None, "status": "не проверено", "limit_s": limit_s,
                "note": "ни одно слово распознавания не совпало со словами сценария — синхрон не измерен"}
    desync, uncertain, exceptions, worst = [], [], [], []
    unmeasured = 0
    for i, j in pairs:
        ds = b[j][0] - a[i][0] if a[i][0] is not None and b[j][0] is not None else None
        de = b[j][1] - a[i][1] if a[i][1] is not None and b[j][1] is not None else None
        if ds is None and de is None:
            unmeasured += 1                       # обе границы внутри составного слова — не измерено
            continue
        rec = {"word": a[i][2], "tts_start": round(a[i][0], 3) if a[i][0] is not None else None,
               "start_diff": round(ds, 3) if ds is not None else None,
               "end_diff": round(de, 3) if de is not None else None}
        s_bad = ds is not None and abs(ds) > limit_s
        e_bad = de is not None and abs(de) > limit_s
        if s_bad and e_bad:
            desync.append(rec)
        elif s_bad or e_bad:
            prev_end = next((a[k][1] for k in range(i - 1, -1, -1) if a[k][1] is not None), 0.0)
            snapped = (b[j][3] and de is not None and not e_bad and s_bad and ds < 0 and b[j][0] >= prev_end - limit_s)
            if snapped:
                exceptions.append({**rec, "reason": SNAP_REASON})
                worst.append(abs(de))
                continue
            uncertain.append(rec)                 # за порогом одна граница (или единственная известная) — не успех
        worst.append(max(abs(x) for x in (ds, de) if x is not None))
    if not worst:                                  # совпавшие слова есть, но ни одной известной границы
        return {"matched_words": len(pairs), "unmeasured_words": unmeasured, "ok": None, "status": "не проверено",
                "limit_s": limit_s, "desynced_words": [], "uncertain_words": [], "boundary_exceptions": [],
                "note": "у совпавших слов нет измеримых границ (только внутренние части составных слов) — "
                        "синхрон не измерен"}
    ok = False if desync else (None if uncertain else True)
    return {"matched_words": len(pairs), "measure": "по слову — обе границы (начало и конец)",
            "median_abs_s": round(statistics.median(worst), 3), "p95_abs_s": round(float(np.percentile(worst, 95)), 3),
            "max_abs_s": round(max(worst), 3), "desynced_words": desync, "uncertain_words": uncertain,
            "boundary_exceptions": exceptions, "unmeasured_words": unmeasured, "limit_s": limit_s, "ok": ok,
            "status": "не проверено" if ok is None else "проверено автоматически"}


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
        for k, w in enumerate(seg.words or []):
            words.append({"start": round(float(w.start), 3), "end": round(float(w.end), 3), "word": w.word.strip(),
                          "probability": round(float(w.probability), 3), "segment_start": k == 0})
    return {"engine": "faster-whisper", "version": faster_whisper.__version__, "model": model_name,
            "language": info.language, "language_probability": round(float(info.language_probability), 3),
            "text": " ".join(t.strip() for t in text), "words": words}
