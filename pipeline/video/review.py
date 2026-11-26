"""Записать подтверждение прослушанной фразы, сохранив автоматические замечания.

python -m pipeline.video.review --video-dir <готовый каталог> --review <human_review.json>
Это запись частичного просмотра, а не повторная проверка звука или одобрение всего ролика.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from contracts.models import Passport
from pipeline.video.passport import ROOT, SCHEMA_PATH, write_passport


def attach(passport: Passport, timeline: dict, review: dict, cache_dir: Path) -> Passport:
    phrase = next((p for p in timeline['phrases'] if p['phrase_id'] == review.get('phrase_id')), None)
    if phrase is None or phrase.get('tts_key') != review.get('tts_key'):
        raise ValueError('Прослушанная фраза не совпадает с ключом TTS в таймлайне ролика')
    for key in ('reviewer', 'reviewed_on', 'scope', 'term', 'question', 'answer'):
        if not isinstance(review.get(key), str) or not review[key].strip():
            raise ValueError(f'В отзыве нет {key}')
    if not isinstance(review.get('accepted'), bool):
        raise ValueError('accepted должен быть явно указан как true или false')
    audio = cache_dir / (phrase['tts_key'] + '.mp3')
    if hashlib.sha256(audio.read_bytes()).hexdigest() != review.get('audio_sha256'):
        raise ValueError('Хэш прослушанного аудио не совпадает с записью TTS')
    result = passport.model_copy(deep=True)
    reviews = result.audio_check.setdefault('human_phrase_reviews', [])
    entry = {**review, 'coverage': 'только указанная фраза и термин', 'automatic_results_overridden': False}
    if entry not in reviews:
        reviews.append(entry)
    # Не изменяем asr/terms/sync, listened_by_human или одобрение ментора.
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--video-dir', type=Path, required=True)
    ap.add_argument('--review', type=Path, required=True)
    ap.add_argument('--cache-dir', type=Path, default=ROOT / 'cache/tts')
    a = ap.parse_args(argv)
    try:
        passport = Passport.model_validate_json((a.video_dir/'passport.json').read_text(encoding='utf-8'))
        timeline = json.loads((a.video_dir/'timeline.json').read_text(encoding='utf-8'))
        review = json.loads(a.review.read_text(encoding='utf-8'))
        updated = attach(passport, timeline, review, a.cache_dir)
        schema = json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
        write_passport(updated, a.video_dir/'passport.json', schema)
    except (ValueError, OSError, KeyError) as e:
        print(f'ОШИБКА записи просмотра: {e}')
        return 2
    print('Записан просмотр отдельной фразы; автоматические результаты не изменены.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
