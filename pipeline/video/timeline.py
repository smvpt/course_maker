"""Таймлайн ролика и субтитры.

Единственный источник времени — число сэмплов каждой фразы после декодирования
озвучки. Из него считаются начало и конец фраз, паузы, общая длительность,
кадры анимации и интервалы VTT.
"""
from __future__ import annotations

import re
import wave
from dataclasses import dataclass
from pathlib import Path

LEAD_IN_S = 0.3   # тишина до первой фразы: плеер не съедает начало
TAIL_S = 1.0      # финальное состояние держится после последней фразы
MAX_CUE_CHARS = 42


@dataclass(frozen=True)
class Word:
    """Метка речи относительно начала аудио фразы, в секундах (слово или предложение)."""
    start: float
    end: float
    text: str


@dataclass(frozen=True)
class Segment:
    phrase_id: str
    start_sample: int
    n_samples: int
    pause_samples: int
    sample_rate: int

    @property
    def start(self) -> float:
        return self.start_sample / self.sample_rate

    @property
    def end(self) -> float:
        """Конец звучания фразы."""
        return (self.start_sample + self.n_samples) / self.sample_rate

    @property
    def hold_end(self) -> float:
        """Конец паузы после фразы."""
        return (self.start_sample + self.n_samples + self.pause_samples) / self.sample_rate

    @property
    def duration(self) -> float:
        return self.n_samples / self.sample_rate


@dataclass(frozen=True)
class Timeline:
    sample_rate: int
    lead_samples: int
    tail_samples: int
    segments: tuple[Segment, ...]

    @property
    def total_samples(self) -> int:
        last = self.segments[-1]
        return last.start_sample + last.n_samples + last.pause_samples + self.tail_samples

    @property
    def total(self) -> float:
        return self.total_samples / self.sample_rate

    @property
    def speech_total(self) -> float:
        return sum(s.duration for s in self.segments)


def build_timeline(items: list[tuple[str, int, float]], sample_rate: int,
                   lead_in_s: float = LEAD_IN_S, tail_s: float = TAIL_S) -> Timeline:
    """items: (phrase_id, число сэмплов звука фразы, пауза после фразы в секундах)."""
    if sample_rate <= 0:
        raise ValueError(f"частота дискретизации должна быть > 0, получено {sample_rate}")
    if not items:
        raise ValueError("таймлайн без фраз")
    if lead_in_s < 0 or tail_s < 0:
        raise ValueError("вступление и хвост не могут быть отрицательными")
    cur = round(lead_in_s * sample_rate)
    segs = []
    for pid, n, pause in items:
        if n <= 0:
            raise ValueError(f"фраза {pid}: пустое аудио ({n} сэмплов)")
        if pause < 0:
            raise ValueError(f"фраза {pid}: отрицательная пауза {pause}")
        p = round(pause * sample_rate)
        segs.append(Segment(pid, cur, n, p, sample_rate))
        cur += n + p
    return Timeline(sample_rate, round(lead_in_s * sample_rate), round(tail_s * sample_rate), tuple(segs))


def assemble_wav(tl: Timeline, pcm: dict[str, bytes], out: Path) -> None:
    """Склеивает моно PCM s16le фраз с тишиной по таймлайну в один WAV."""
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(tl.sample_rate)
        w.writeframes(b"\x00\x00" * tl.lead_samples)
        for s in tl.segments:
            data = pcm[s.phrase_id]
            if len(data) != s.n_samples * 2:
                raise ValueError(f"фраза {s.phrase_id}: PCM {len(data)} байт, ожидалось {s.n_samples * 2}")
            w.writeframes(data)
            w.writeframes(b"\x00\x00" * s.pause_samples)
        w.writeframes(b"\x00\x00" * tl.tail_samples)


# ---------------------------------------------------------------- субтитры

@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    text: str
    source: str   # "word" | "sentence" | "audio" — чем заданы границы


def _word_chunks(text: str, words: list[Word], max_chars: int) -> list[tuple[float, float, str]] | None:
    """Режет фразу на куски ≤max_chars по пословным меткам. None — метки не сопоставились с текстом."""
    tokens = [(m.start(), m.end(), m.group()) for m in re.finditer(r"\S+", text)]
    timed: list[list[float] | None] = [None] * len(tokens)
    cursor = 0
    for w in words:
        pos = text.find(w.text, cursor) if w.text else -1
        if pos < 0:
            return None
        cursor = pos + len(w.text)
        k = next(i for i, (a, b, _) in enumerate(tokens) if a <= pos < b)
        if timed[k] is None:
            timed[k] = [w.start, w.end]
        else:
            timed[k][1] = max(timed[k][1], w.end)
    chunks: list[list[int]] = []
    for i, (_, _, tok) in enumerate(tokens):
        if chunks and len(" ".join(tokens[j][2] for j in chunks[-1] + [i])) <= max_chars:
            chunks[-1].append(i)
        else:
            chunks.append([i])
    out: list[tuple[float, float, str]] = []
    for ch in chunks:
        times = [timed[i] for i in ch if timed[i] is not None]
        chunk_text = " ".join(tokens[i][2] for i in ch)
        if not times:          # только знаки препинания — приклеиваем к предыдущему куску
            if not out:
                return None
            a, b, t = out[-1]
            out[-1] = (a, b, f"{t} {chunk_text}")
            continue
        out.append((times[0][0], times[-1][1], chunk_text))
    return out


def subtitle_cues(tl: Timeline, phrases: dict[str, tuple[str, list[Word], str]],
                  max_chars: int = MAX_CUE_CHARS) -> list[Cue]:
    """phrases: phrase_id → (полный текст, метки речи, вид меток "word"|"sentence"|"audio").

    Пословные метки режут длинную фразу на куски; предложенческие дают по реплике на
    предложение; без меток — одна реплика на фразу по границам её аудио. Метки грубее
    слова никогда не дробятся до слов.
    """
    cues: list[Cue] = []
    for seg in tl.segments:
        text, words, timing = phrases[seg.phrase_id]
        parts: list[tuple[float, float, str]] | None = None
        source = timing
        if timing == "word" and words:
            parts = _word_chunks(text, words, max_chars)
        elif timing == "sentence" and words:
            parts = [(w.start, w.end, w.text) for w in words]
        if parts is None:
            parts, source = [(0.0, seg.duration, text)], "audio"
        for a, b, t in parts:
            start = min(max(seg.start + a, seg.start), seg.end)
            end = min(seg.start + b, seg.end)
            if cues and start < cues[-1].end:
                start = cues[-1].end
            if end > start:
                cues.append(Cue(start, end, t, source))
    return cues


def _ts(t: float) -> str:
    ms = round(t * 1000)
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"


def format_vtt(cues: list[Cue], note: str | None = None) -> str:
    out = ["WEBVTT", ""]
    if note:
        out += [f"NOTE {note}", ""]
    for i, c in enumerate(cues, 1):
        out += [str(i), f"{_ts(c.start)} --> {_ts(c.end)}", c.text, ""]
    return "\n".join(out).rstrip("\n") + "\n"
