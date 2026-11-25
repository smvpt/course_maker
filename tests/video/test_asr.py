"""Проверка озвучки без сети и без модели: нормализация, WER с разбором ошибок, рассинхрон слов."""
import pytest

from pipeline.video.asr import normalize_words, sync_report, wer_report


def test_normalize():
    assert normalize_words("Ёлка — гамма-каротаж, УЭС: 0,15!") == ["елка", "гамма", "каротаж", "уэс", "0", "15"]


def test_perfect_match():
    r = wer_report([("p1", "Прибор идёт вниз."), ("p2", "Кривые растут.")], ["прибор", "идет", "вниз", "кривые", "растут"])
    assert r["wer"] == 0 and r["errors"] == [] and r["n_ref"] == 5


def test_errors_are_attributed_to_phrases():
    phrases = [("p1", "Прибор идёт вниз."), ("p2", "Кривые растут вместе с глубиной.")]
    hyp = ["прибор", "идет", "вниз", "кривая", "растут", "с", "глубиной", "ну"]
    r = wer_report(phrases, hyp)
    kinds = sorted((e["type"], e["phrase_id"]) for e in r["errors"])
    assert kinds == [("del", "p2"), ("ins", "p2"), ("sub", "p2")]
    sub = next(e for e in r["errors"] if e["type"] == "sub")
    assert (sub["expected"], sub["heard"]) == ("кривые", "кривая")
    assert r["wer"] == pytest.approx(3 / 8)
    assert r["per_phrase"] == {"p1": 0, "p2": 3}


def test_insertion_before_first_word_belongs_to_first_phrase():
    r = wer_report([("p1", "раз два")], ["эээ", "раз", "два"])
    assert r["errors"] == [{"type": "ins", "phrase_id": "p1", "expected": None, "heard": "эээ"}]


def test_empty_hypothesis_is_total_error():
    r = wer_report([("p1", "раз два три")], [])
    assert r["wer"] == 1.0 and len(r["errors"]) == 3


def test_sync_offsets_from_matched_words():
    tts = [(1.00, 1.30, "Прибор"), (1.40, 1.70, "идёт"), (1.80, 2.10, "вниз")]
    asr = [(1.05, 1.35, "прибор"), (1.50, 1.80, "идет"), (2.60, 2.90, "вверх")]
    r = sync_report(tts, asr, limit_s=0.5)
    assert r["matched_words"] == 2
    assert r["max_abs_s"] == pytest.approx(0.10) and r["median_abs_s"] == pytest.approx(0.075)
    assert r["ok"] is True


def test_sync_fails_over_limit_and_without_matches():
    r = sync_report([(1.0, 1.3, "раз")], [(1.7, 2.0, "раз")], limit_s=0.5)     # сдвинуты обе границы
    assert r["ok"] is False and r["max_abs_s"] == pytest.approx(0.7)
    r = sync_report([(1.0, 1.3, "раз")], [(1.0, 1.3, "два")], limit_s=0.5)
    assert r["ok"] is None and r["matched_words"] == 0 and r["status"] == "не проверено"


def test_one_boundary_off_is_not_a_confirmed_success():
    # регрессия: начало сдвинуто на 0,8 с, конец совпал — это не «успех», а неопределённость меток
    r = sync_report([(1.0, 2.0, "раз")], [(1.8, 2.1, "раз")], limit_s=0.5)
    assert r["ok"] is None and r["status"] == "не проверено"
    assert r["uncertain_words"] == [{"word": "раз", "tts_start": 1.0, "start_diff": 0.8, "end_diff": 0.1}]
    assert r["boundary_exceptions"] == []


def test_start_snapped_into_preceding_silence_is_a_justified_exception():
    # первое слово сегмента: начало распознано в тишине после предыдущего слова (29,0), конец совпал
    tts = [(28.6, 29.0, "одинаковая"), (30.35, 30.55, "как")]
    asr = [(28.62, 29.02, "одинаковая", True), (29.04, 30.50, "как", True)]
    r = sync_report(tts, asr, limit_s=0.5)
    assert r["ok"] is True and r["status"] == "проверено автоматически"
    exc = r["boundary_exceptions"]
    assert len(exc) == 1 and exc[0]["word"] == "как" and "тишин" in exc[0]["reason"]
    assert r["uncertain_words"] == []


@pytest.mark.parametrize("asr_word", [
    (29.04, 30.50, "как", False),        # не первое слово сегмента — исключение не применяется
    (28.30, 30.50, "как", True),         # начало легло на предыдущее слово, а не в тишину
    (30.95, 30.55, "как", True),         # начало позже, а не раньше
])
def test_exception_conditions_are_strict(asr_word):
    tts = [(28.6, 29.0, "одинаковая"), (30.35, 30.55, "как")]
    r = sync_report(tts, [(28.62, 29.02, "одинаковая", True), asr_word], limit_s=0.5)
    assert r["ok"] is None and r["boundary_exceptions"] == []


def test_both_boundaries_shifted_is_a_desync():
    r = sync_report([(1.0, 2.0, "раз")], [(1.8, 2.8, "раз", True)], limit_s=0.5)
    assert r["ok"] is False and r["status"] == "проверено автоматически" and r["desynced_words"]


# ---------------------------------------------------------------- термины: каждое употребление

from pipeline.video.asr import term_report  # noqa: E402


def test_each_term_occurrence_is_checked_by_alignment():
    phrases = [("p1", "Кавернограмма показывает диаметр."), ("p2", "Снова смотрим кавернограмма и ГК.")]
    hyp = ["кавернограмма", "показывает", "диаметр", "снова", "смотрим", "коверного", "и", "гк"]
    r = term_report(phrases, hyp, ["кавернограмма", "ГК"])
    assert r["terms_in_script"] == ["кавернограмма", "ГК"]
    occ = [(o["term"], o["phrase_id"], o["ok"]) for o in r["occurrences"]]
    assert occ == [("кавернограмма", "p1", True), ("кавернограмма", "p2", False), ("ГК", "p2", True)]
    bad = next(o for o in r["occurrences"] if not o["ok"])
    assert bad["heard"] == ["коверного"]
    assert r["not_recognized"] == ["кавернограмма"] and r["ok"] is False      # одно верное не скрывает ошибку


def test_multiword_term_needs_every_word():
    r = term_report([("p1", "гамма каротаж и гамма каротаж")], ["гамма", "каротаж", "и", "гамма", "карта"],
                    ["гамма-каротаж"])
    assert [o["ok"] for o in r["occurrences"]] == [True, False] and r["ok"] is False


def test_terms_absent_from_script_are_not_checked():
    r = term_report([("p1", "раз два")], ["раз", "два"], ["кавернограмма"])
    assert r["terms_in_script"] == [] and r["occurrences"] == [] and r["ok"] is True


# ---------------------------------------------------------------- составной термин: слова подряд

def test_insertion_inside_multiword_term_is_an_error():
    r = term_report([("p1", "Смотрим нейтронная пористость в пласте.")],
                    ["смотрим", "нейтронная", "плотность", "и", "пористость", "в", "пласте"],
                    ["нейтронная пористость"])
    o = r["occurrences"][0]
    assert o["ok"] is False and r["ok"] is False
    assert o["heard"] == ["нейтронная", "плотность", "и", "пористость"]         # весь фрагмент, со вставками


@pytest.mark.parametrize("hyp", [
    ["ну", "нейтронная", "пористость", "в", "пласте"],                          # вставка перед термином
    ["нейтронная", "пористость", "вот", "в", "пласте"],                         # вставка после термина
    ["ну", "нейтронная", "пористость", "вот", "в", "пласте"],                   # и до, и после
])
def test_insertion_around_term_does_not_spoil_it(hyp):
    r = term_report([("p1", "нейтронная пористость в пласте")], hyp, ["нейтронная пористость"])
    o = r["occurrences"][0]
    assert o["ok"] is True and o["heard"] == ["нейтронная", "пористость"]


def test_deleted_word_inside_term_keeps_heard_fragment():
    r = term_report([("p1", "нейтронная пористость пласта")], ["нейтронная", "пласта"], ["нейтронная пористость"])
    o = r["occurrences"][0]
    assert o["ok"] is False and o["heard"] == ["нейтронная"]


def test_hyphenated_tts_word_compares_only_known_boundaries():
    # edge-tts даёт «гамма-каротаж» одной меткой; внутренняя граница неизвестна и не сравнивается
    tts = [(1.0, 2.0, "гамма-каротаж")]
    asr = [(1.0, 1.45, "гамма", True), (1.5, 2.0, "каротаж", False)]
    r = sync_report(tts, asr, limit_s=0.5)
    assert r["ok"] is True and r["uncertain_words"] == [] and r["matched_words"] == 2


def test_hyphenated_word_shift_is_still_detected():
    tts = [(1.0, 2.0, "гамма-каротаж")]
    asr = [(1.8, 2.3, "гамма", True), (2.35, 2.8, "каротаж", False)]          # всё слово сдвинуто на 0,8 с
    r = sync_report(tts, asr, limit_s=0.5)
    assert r["ok"] is None and len(r["uncertain_words"]) == 2                  # по одной известной границе на часть


def test_single_known_boundary_over_limit_is_not_success():
    r = sync_report([(1.0, 2.0, "гамма-каротаж")], [(1.0, 1.45, "гамма", True), (1.5, 2.7, "каротаж", False)],
                    limit_s=0.5)
    assert r["ok"] is None and r["uncertain_words"][0]["word"] == "каротаж"


def test_no_measurable_boundaries_is_unverified_without_numbers():
    # регрессия: у совпавшего слова нет ни одной известной границы — раньше StatisticsError
    r = sync_report([(1.0, 3.0, "альфа-бета-гамма")], [(1.6, 2.0, "бета")], limit_s=0.5)
    assert r["ok"] is None and r["status"] == "не проверено"
    assert r["matched_words"] == 1 and r["unmeasured_words"] == 1
    assert r.get("max_abs_s") is None and r.get("median_abs_s") is None and r.get("p95_abs_s") is None
