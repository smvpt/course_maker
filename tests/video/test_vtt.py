"""Субтитры VTT: полный текст, интервалы из меток речи, честная пометка их точности."""
import re

from pipeline.video.timeline import Word, build_timeline, format_vtt, subtitle_cues

SR = 1000
TS = r"\d\d:\d\d:\d\d\.\d\d\d"


def _tl(*items):
    return build_timeline(list(items), SR, lead_in_s=0.5, tail_s=1.0)


def _check_valid(cues, tl):
    for c in cues:
        assert c.start < c.end
    for a, b in zip(cues, cues[1:]):
        assert a.end <= b.start
    assert cues[0].start >= 0 and cues[-1].end <= tl.total


def test_word_timings_split_long_phrase_into_timed_chunks():
    text = "Первая часть фразы довольно длинная, а вторая часть фразы идёт после запятой."
    toks = re.findall(r"[\w-]+", text)
    words = [Word(0.1 + i * 0.3, 0.1 + i * 0.3 + 0.25, t) for i, t in enumerate(toks)]
    tl = _tl(("p1", 5000, 0.0))
    cues = subtitle_cues(tl, {"p1": (text, words, "word")}, max_chars=42)
    assert len(cues) >= 2
    assert " ".join(c.text for c in cues) == text          # полный текст с пунктуацией
    assert all(len(c.text) <= 42 for c in cues)
    assert all(c.source == "word" for c in cues)
    assert cues[0].start == 0.5 + 0.1                      # начало фразы + метка первого слова
    _check_valid(cues, tl)


def test_sentence_timings_are_not_split_into_words():
    text = "Одна фраза. Вторая фраза в той же реплике."
    events = [Word(0.1, 1.0, "Одна фраза."), Word(1.2, 2.9, "Вторая фраза в той же реплике.")]
    tl = _tl(("p1", 3000, 0.0))
    cues = subtitle_cues(tl, {"p1": (text, events, "sentence")})
    assert [c.text for c in cues] == ["Одна фраза.", "Вторая фраза в той же реплике."]
    assert all(c.source == "sentence" for c in cues)
    _check_valid(cues, tl)


def test_no_timings_gives_one_cue_per_phrase_from_audio_bounds():
    tl = _tl(("p1", 2000, 0.7), ("p2", 1500, 0.0))
    cues = subtitle_cues(tl, {"p1": ("Раз.", [], "audio"), "p2": ("Два.", [], "audio")})
    assert [(c.start, c.end, c.source) for c in cues] == [(0.5, 2.5, "audio"), (3.2, 4.7, "audio")]


def test_unalignable_word_timings_fall_back_to_whole_phrase():
    tl = _tl(("p1", 2000, 0.0))
    words = [Word(0.1, 0.5, "совсем"), Word(0.6, 1.0, "другое")]
    cues = subtitle_cues(tl, {"p1": ("Текст фразы.", words, "word")})
    assert len(cues) == 1 and cues[0].text == "Текст фразы." and cues[0].source == "audio"


def test_cues_are_clamped_to_phrase_audio():
    tl = _tl(("p1", 1000, 0.0))
    words = [Word(0.2, 5.0, "Слово")]                      # метка длиннее звука
    cues = subtitle_cues(tl, {"p1": ("Слово", words, "word")})
    assert cues[0].end == tl.segments[0].end


def test_vtt_format_and_sorted_intervals():
    tl = _tl(("p1", 2000, 0.3), ("p2", 61500, 0.0))
    cues = subtitle_cues(tl, {"p1": ("Раз.", [], "audio"), "p2": ("Два.", [], "audio")})
    vtt = format_vtt(cues, note="тайминги: границы аудио фраз")
    assert vtt.startswith("WEBVTT\n\nNOTE тайминги: границы аудио фраз\n\n")
    stamps = re.findall(rf"({TS}) --> ({TS})", vtt)
    assert stamps == [("00:00:00.500", "00:00:02.500"), ("00:00:02.800", "00:01:04.300")]
    assert vtt.endswith("Два.\n")
