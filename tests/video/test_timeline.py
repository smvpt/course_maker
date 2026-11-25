"""Таймлайн ролика строится из фактического числа сэмплов каждой фразы и пауз."""
import wave

import pytest

from pipeline.video.timeline import assemble_wav, build_timeline

SR = 24000


def test_phrases_follow_each_other_with_pauses():
    tl = build_timeline([("p1", SR * 2, 0.5), ("p2", SR * 3, 0.0), ("p3", SR // 2, 1.0)],
                        SR, lead_in_s=0.25, tail_s=1.0)
    s1, s2, s3 = tl.segments
    assert (s1.start, s1.end, s1.hold_end) == (0.25, 2.25, 2.75)
    assert (s2.start, s2.end, s2.hold_end) == (2.75, 5.75, 5.75)
    assert (s3.start, s3.end, s3.hold_end) == (5.75, 6.25, 7.25)
    assert tl.total == 8.25                       # пауза после последней + хвост
    assert tl.speech_total == 5.5


def test_last_phrase_is_never_at_the_very_end():
    tl = build_timeline([("p1", SR, 0.0)], SR, lead_in_s=0.0, tail_s=0.5)
    assert tl.total - tl.segments[-1].end == 0.5


def test_durations_come_from_samples_not_rounded_seconds():
    tl = build_timeline([("p1", 12345, 0.0), ("p2", 777, 0.0)], SR, lead_in_s=0.0, tail_s=0.0)
    assert tl.segments[1].start_sample == 12345
    assert tl.total_samples == 12345 + 777
    assert tl.segments[0].duration == pytest.approx(12345 / SR)


@pytest.mark.parametrize("items", [[], [("p1", 0, 0.0)], [("p1", 100, -0.1)]])
def test_bad_timeline_input_fails(items):
    with pytest.raises(ValueError):
        build_timeline(items, SR)


def test_assembled_wav_has_exact_layout(tmp_path):
    tl = build_timeline([("a", 100, 0.01), ("b", 50, 0.0)], 1000, lead_in_s=0.005, tail_s=0.02)
    pcm = {"a": b"\x01\x00" * 100, "b": b"\x02\x00" * 50}
    out = tmp_path / "speech.wav"
    assemble_wav(tl, pcm, out)
    with wave.open(str(out)) as w:
        assert (w.getframerate(), w.getnchannels(), w.getsampwidth()) == (1000, 1, 2)
        frames = w.readframes(w.getnframes())
    assert len(frames) == tl.total_samples * 2
    samples = [int.from_bytes(frames[i:i + 2], "little", signed=True) for i in range(0, len(frames), 2)]
    assert samples[:5] == [0] * 5                 # вступление
    assert samples[5:105] == [1] * 100            # фраза a
    assert samples[105:115] == [0] * 10           # пауза после a
    assert samples[115:165] == [2] * 50           # фраза b
    assert samples[165:] == [0] * 20              # хвост


def test_assemble_rejects_pcm_of_wrong_length(tmp_path):
    tl = build_timeline([("a", 100, 0.0)], 1000)
    with pytest.raises(ValueError, match="a"):
        assemble_wav(tl, {"a": b"\x00\x00" * 99}, tmp_path / "x.wav")
