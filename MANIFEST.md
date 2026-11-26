# Манифест конвейера

Команда: course_maker (П1 ядро, П2 проверка, П3 курс, П4 видео)
Тег заморозки: `v1.0-freeze`

Подробно по модулям, с лицензиями: `manifest/core.md`, `manifest/verify.md`, `manifest/course.md`, `manifest/video.md`.

## Модели

Все вызовы LLM идут через `pipeline/llm.py` (litellm), модель задаётся в `.env`. По умолчанию (`config/llm.yaml`) — `anthropic/claude-opus-5-5` на всех уровнях (default, strong, vision). Кэш ответов, закоммиченный при заморозке (`cache/llm/`), получен моделями `gemini/gemini-3.5-flash` и `gemini/gemini-3.5-flash-lite`: каждая запись хранит модель, которая ответила (`model`), и запрошенную (`model_requested`).

| Этап | Модель | Версия | Где работает | Что уходит наружу | Как заменить |
| --- | --- | --- | --- | --- | --- |
| Учебный слой (`structure`) | tier strong | `claude-opus-5-5` по умолчанию | облако провайдера через litellm | текст единиц главы | `LLM_MODEL_STRONG` или `LLM_MODEL` в `.env` |
| Описание рисунков (`ingest`) | tier vision | `claude-opus-5-5` по умолчанию | облако провайдера | сканы страниц с рисунками, подписи | `LLM_MODEL_VISION` или `LLM_MODEL` в `.env` |
| Маршрутизация (`route`) | tier default | `claude-opus-5-5` по умолчанию | облако провайдера | поля узлов учебного слоя | `LLM_MODEL_DEFAULT` или `LLM_MODEL` в `.env` |
| Курс и задания (`course`) | tier default | `claude-opus-5-5` по умолчанию | облако провайдера | текст узла учебного слоя | `LLM_MODEL_DEFAULT` или `LLM_MODEL` в `.env` |
| Модуль проверки (`verify`, `verify.external`) | tier strong, кадры — tier vision | `claude-opus-5-5` по умолчанию | облако провайдера; сверка страниц, цитат, чисел, терминов — локально | страницы главы, элементы пакета проверки, сценарии, PNG-кадры | `LLM_MODEL_STRONG` / `LLM_MODEL_VISION` или `LLM_MODEL` в `.env` |
| Сценарий ролика (`video.spec`) | tier default | `claude-opus-5-5` по умолчанию | облако провайдера | узел учебного слоя (поля, утверждения с цитатами), фразы сценария | `LLM_MODEL_DEFAULT` или `LLM_MODEL` в `.env` |
| Озвучка | edge-tts, голос `ru-RU-DmitryNeural` | edge-tts 7.3.1 | онлайн-синтез Microsoft | только текст фраз сценария | `--voice` у `pipeline.video.build`; `TTS_OFFLINE=1` — только кэш `cache/tts/` |
| Проверка озвучки | faster-whisper small | 1.2.1 | локально | ничего | — |
| Иллюстрации (`illus`) | tier default — только выбор формулы и диапазона | `claude-opus-5-5` по умолчанию | облако провайдера; SVG рисует код | текст узла слоя | `LLM_MODEL_DEFAULT` или `LLM_MODEL` в `.env` |

Генерации изображений и видео нет: иллюстрации и кадры роликов рисует код из данных и расчёта.

Запасные модели при лимитах и перегрузке: `LLM_MODEL_FALLBACK` (и `LLM_MODEL_FALLBACK_<TIER>`) в `.env`. Без ключа: `LLM_OFFLINE=1` — только кэш.

## Инструменты

| Инструмент | Версия | Для чего | Данные наружу |
| --- | --- | --- | --- |
| Python | 3.12 | конвейер | нет |
| litellm | 1.111.0 | единый вызов LLM разных провайдеров | промпт и картинки — выбранному провайдеру |
| pydantic | 2.13.5 | контракты данных | нет |
| jsonschema | 4.26.0 | проверка выходов по схемам организаторов | нет |
| PyYAML, python-dotenv | 6.0.3, 1.2.4 | конфиги, `.env` | нет |
| pypdfium2, Pillow | 5.15.2, 13.0.0 | сканы страниц PDF | нет |
| rapidfuzz | 3.9.7 | сверка цитат со страницами md | нет |
| Jinja2 | 3.1.6 | страницы курса | нет |
| KaTeX | 0.16.22 | формулы в курсе (файлы внутри курса) | нет |
| Phosphor Icons | 2.1.1 | иконки курса | нет |
| Manim Community (+ ManimPango, pycairo, PyAV) | 0.22.1 | кадры роликов | нет |
| NumPy, SciPy | 2.5.5, 1.18.1 | расчёт полей для роликов и графиков | нет |
| lasio | 0.34 | чтение каротажа LAS | нет |
| edge-tts | 7.3.1 | озвучка | текст фраз сценария — Microsoft |
| faster-whisper | 1.2.1 | проверка озвучки | нет |
| FFmpeg / ffprobe | сборка N-127043 (libx264, AAC) | сборка и проверка видео | нет |
| git | системный | журнал ручных правок | нет |
| pytest | 9.2.0 | тесты | нет |

Точные версии всех пакетов — `requirements/*.txt`. Данные: Volve (скв. 15/9-19 A, Equinor и партнёры, для учёбы) — `manifest/video.md`.

## Запуск

Одна команда на главу: `make all MD=<путь к главе.md> [PDF=<путь к PDF>]` (без `make`: `python -m pipeline.run --md <путь> [--pdf <путь>]`). Ключ и модель — в `.env`. Подробно — `docs/run.md`.
