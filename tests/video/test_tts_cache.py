"""Кэш edge-tts: ключ = текст + голос + параметры синтеза; сеть в тестах подменена."""
import pytest

from pipeline.video import tts
from pipeline.video.tts import TtsError, TtsParams, synthesize

P = TtsParams(voice="ru-RU-DmitryNeural")
EVENTS = [{"type": "WordBoundary", "offset": 1_000_000, "duration": 3_000_000, "text": "Проверка"}]


@pytest.fixture
def fake_net(monkeypatch):
    calls = []

    def fetch(text, params):
        calls.append((text, params))
        return b"ID3fake-mp3", list(EVENTS)

    monkeypatch.setattr(tts, "_fetch", fetch)
    monkeypatch.delenv("TTS_OFFLINE", raising=False)
    return calls


def test_second_call_is_served_from_cache(tmp_path, fake_net):
    a = synthesize("Проверка", P, tmp_path)
    b = synthesize("Проверка", P, tmp_path)
    assert len(fake_net) == 1
    assert (a.cached, b.cached) == (False, True)
    assert a.mp3_path == b.mp3_path and b.mp3_path.read_bytes() == b"ID3fake-mp3"
    assert b.timing == "word"
    assert b.words[0].start == pytest.approx(0.1) and b.words[0].end == pytest.approx(0.4)


@pytest.mark.parametrize("other", [
    ("Проверка!", P),
    ("Проверка", TtsParams(voice="ru-RU-SvetlanaNeural")),
    ("Проверка", TtsParams(voice="ru-RU-DmitryNeural", rate="+10%")),
    ("Проверка", TtsParams(voice="ru-RU-DmitryNeural", pitch="-5Hz")),
    ("Проверка", TtsParams(voice="ru-RU-DmitryNeural", volume="+5%")),
    ("Проверка", TtsParams(voice="ru-RU-DmitryNeural", boundary="SentenceBoundary")),
])
def test_any_change_of_text_or_params_is_a_miss(tmp_path, fake_net, other):
    synthesize("Проверка", P, tmp_path)
    r = synthesize(other[0], other[1], tmp_path)
    assert not r.cached and len(fake_net) == 2


def test_offline_miss_is_a_clear_error(tmp_path, fake_net, monkeypatch):
    monkeypatch.setenv("TTS_OFFLINE", "1")
    with pytest.raises(TtsError, match="TTS_OFFLINE"):
        synthesize("Проверка", P, tmp_path)
    assert fake_net == []


def test_offline_hit_works(tmp_path, fake_net, monkeypatch):
    synthesize("Проверка", P, tmp_path)
    monkeypatch.setenv("TTS_OFFLINE", "1")
    assert synthesize("Проверка", P, tmp_path).cached


def test_half_written_entry_is_resynthesized(tmp_path, fake_net):
    r = synthesize("Проверка", P, tmp_path)
    r.mp3_path.with_suffix(".json").unlink()          # обрыв между записью mp3 и метаданных
    assert not synthesize("Проверка", P, tmp_path).cached
    assert len(fake_net) == 2


def test_empty_audio_from_service_is_an_error(tmp_path, monkeypatch):
    monkeypatch.setattr(tts, "_fetch", lambda text, params: (b"", []))
    monkeypatch.delenv("TTS_OFFLINE", raising=False)
    with pytest.raises(TtsError, match="пуст"):
        synthesize("Проверка", P, tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_unavailable_service_is_a_clear_error(tmp_path, monkeypatch):
    def down(text, params):
        raise TtsError("edge-tts недоступен: нет соединения")
    monkeypatch.setattr(tts, "_fetch", down)
    monkeypatch.delenv("TTS_OFFLINE", raising=False)
    with pytest.raises(TtsError, match="недоступен"):
        synthesize("Проверка", P, tmp_path)


def test_sentence_events_are_marked_as_sentence_timing(tmp_path, monkeypatch):
    ev = [{"type": "SentenceBoundary", "offset": 0, "duration": 10_000_000, "text": "Фраза."}]
    monkeypatch.setattr(tts, "_fetch", lambda text, params: (b"x", ev))
    monkeypatch.delenv("TTS_OFFLINE", raising=False)
    r = synthesize("Фраза.", TtsParams(voice="v", boundary="SentenceBoundary"), tmp_path)
    assert r.timing == "sentence" and r.words[0].end == pytest.approx(1.0)


def test_no_events_means_audio_timing(tmp_path, monkeypatch):
    monkeypatch.setattr(tts, "_fetch", lambda text, params: (b"x", []))
    monkeypatch.delenv("TTS_OFFLINE", raising=False)
    assert synthesize("Фраза.", P, tmp_path).timing == "audio"
