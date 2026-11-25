"""Озвучка фраз через edge-tts с кэшем в cache/tts/.

Наружу (в сервис Microsoft) уходит только текст фразы. Ключ кэша — хэш текста,
голоса и всех параметров синтеза. TTS_OFFLINE=1: промах кэша — ошибка, сети нет.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from pipeline.video.timeline import Word

DEFAULT_VOICE = "ru-RU-DmitryNeural"
TICKS_PER_S = 10_000_000   # смещения edge-tts — в единицах по 100 нс
RETRY_DELAYS_S = (2, 5, 10, 20)   # сервис периодами рвёт соединение без аудио (NoAudioReceived)


class TtsError(RuntimeError):
    pass


@dataclass(frozen=True)
class TtsParams:
    voice: str = DEFAULT_VOICE
    rate: str = "+0%"
    volume: str = "+0%"
    pitch: str = "+0Hz"
    boundary: str = "WordBoundary"


@dataclass(frozen=True)
class TtsResult:
    mp3_path: Path
    events: list[dict]
    cached: bool
    key: str

    @property
    def timing(self) -> str:
        kinds = {e["type"] for e in self.events}
        if kinds == {"WordBoundary"}:
            return "word"
        if kinds == {"SentenceBoundary"}:
            return "sentence"
        return "audio"

    @property
    def words(self) -> list[Word]:
        return [Word(e["offset"] / TICKS_PER_S, (e["offset"] + e["duration"]) / TICKS_PER_S, e["text"])
                for e in self.events]


def cache_key(text: str, params: TtsParams) -> str:
    payload = json.dumps({"engine": "edge-tts", "text": text, **asdict(params)},
                         ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _fetch(text: str, params: TtsParams) -> tuple[bytes, list[dict]]:
    """Один синтез через сеть с повторами. Единственное место, где есть сеть."""
    import aiohttp
    import edge_tts

    async def run() -> tuple[bytes, list[dict]]:
        com = edge_tts.Communicate(text, params.voice, rate=params.rate, volume=params.volume,
                                   pitch=params.pitch, boundary=params.boundary)
        audio, events = bytearray(), []
        async for ch in com.stream():
            if ch["type"] == "audio":
                audio += ch["data"]
            elif ch["type"] in ("WordBoundary", "SentenceBoundary"):
                events.append({k: ch[k] for k in ("type", "offset", "duration", "text")})
        return bytes(audio), events

    last: Exception | None = None
    for delay in (0, *RETRY_DELAYS_S):
        time.sleep(delay)
        try:
            return asyncio.run(run())
        except (edge_tts.exceptions.EdgeTTSException, aiohttp.ClientError,
                asyncio.TimeoutError, OSError) as e:
            last = e
    raise TtsError(f"edge-tts недоступен после {len(RETRY_DELAYS_S) + 1} попыток за "
                   f"{sum(RETRY_DELAYS_S)} с (голос {params.voice}): "
                   f"{type(last).__name__}: {last}. Проверьте сеть и повторите позже; голос можно сменить "
                   f"для всей серии через --voice. Фраза: «{text[:60]}»") from last


def synthesize(text: str, params: TtsParams, cache_dir: Path) -> TtsResult:
    key = cache_key(text, params)
    mp3, meta = cache_dir / f"{key}.mp3", cache_dir / f"{key}.json"
    if mp3.is_file() and meta.is_file() and mp3.stat().st_size > 0:
        data = json.loads(meta.read_text(encoding="utf-8"))
        if data.get("key") == key:
            return TtsResult(mp3, data["events"], True, key)
    if os.environ.get("TTS_OFFLINE") == "1":
        raise TtsError(f"TTS_OFFLINE=1, а фразы нет в кэше {cache_dir} (ключ {key}, голос {params.voice}): "
                       f"«{text[:60]}»")
    audio, events = _fetch(text, params)
    if not audio:
        raise TtsError(f"edge-tts вернул пустое аудио (голос {params.voice}): «{text[:60]}»")
    cache_dir.mkdir(parents=True, exist_ok=True)
    tmp = mp3.with_suffix(".mp3.tmp")
    tmp.write_bytes(audio)
    os.replace(tmp, mp3)
    import edge_tts
    record = {"key": key, "text": text, "params": asdict(params),
              "edge_tts_version": edge_tts.__version__, "events": events}
    tmp = meta.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, meta)   # метаданные пишутся последними: их наличие = запись целая
    return TtsResult(mp3, events, False, key)
