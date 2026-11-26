# Запуск с нуля

Всё запускается из корня репозитория. Вход и выход — файлы. Повторный запуск ничего не ломает: ответы модели берутся из `cache/llm/`.

## 1. Установка

Нужны Python 3.12 и, для роликов, FFmpeg/ffprobe с libx264 в `PATH` (`winget install Gyan.FFmpeg` или `apt install ffmpeg`). Без FFmpeg собираются слой, маршрут, проверка и курс, но не ролики.

```
git clone <репозиторий> && cd course_maker
python -m venv .venv
.venv/bin/activate             # Windows: .venv\Scripts\activate
make install                   # = python -m pip install -r requirements.txt
make test                      # все тесты, без сети
make smoke                     # весь путь без ключа на маленькой главе, несколько секунд
```

Без `make` (обычный Windows) каждая цель — одна команда Python, см. раздел 6.

## 2. Ключ и модель — только `.env`

```
cp .env.example .env
```

В `.env` два значения: ключ провайдера и модель в формате litellm `<провайдер>/<модель>`.

```
ANTHROPIC_API_KEY=...                          # или OPENAI_API_KEY / GEMINI_API_KEY, или общий LLM_API_KEY
LLM_MODEL=anthropic/claude-opus-5-5            # для всех этапов сразу
```

- Без `LLM_MODEL` берутся модели из `config/llm.yaml` (по умолчанию `anthropic/claude-opus-5-5` на всех уровнях).
- Отдельно по уровню: `LLM_MODEL_DEFAULT`, `LLM_MODEL_STRONG`, `LLM_MODEL_VISION` (сильнее `LLM_MODEL`).
- Запасные модели: `LLM_MODEL_FALLBACK=<м1>,<м2>`. При дневном лимите или перегрузке основной (429/503/529) запрос уходит следующей. Лимит в минуту и перегрузку код сначала пережидает (до 5 повторов с паузой).
- Свой адрес API (прокси): `LLM_API_BASE`.
- Цены для учёта денег — `config/llm.yaml → prices`. Для модели не из списка — расчёт litellm.

Код, промпты и конфиги для смены модели править не нужно.

## 3. Новая глава — без правки файлов

```
make all MD=<путь к главе.md> [PDF=<путь к PDF>] [PAGES=a-b[,c-d]] [ERRATA=<лист опечаток>] \
         [PREREQ=<карточки-предпосылки.md>] [DOMAIN=geology|drilling|…] [AUTHOR=…] [BOOK=…] [VIDEO=1]
```

- **Страницы** — метки `<!-- page N -->` в md (номер = страница PDF). `PAGES` нужен, только если md содержит больше, чем главу.
- **Id главы** — из имени md: транслит, нижний регистр, `[a-z0-9_.-]`. Свой id: `CH=<id>` вместе с `MD=`.
- **Язык** (ru/en) определяется по тексту. Курс всегда на русском, цитаты — на языке оригинала.
- **PDF** не обязателен. С ним в курсе сканы страниц «Проверь по книге». Без него рисунки описываются по подписям, а узлы получают пометку `needs_scan`.
- **Домен** по умолчанию `geology`. Пакета другого домена нет — запуск падает с понятной ошибкой и командой сборки: `python -m domain.build --domain <имя> --ch <id главы>` (ingest к этому моменту уже прошёл) (см. `docs/check.md`).
- **Автор и книга** для шапки курса: `AUTHOR=`/`BOOK=`. Без них — из имени PDF вида «Автор - Книга - год», иначе в шапке только название главы.
- **`VIDEO=1`** — ещё и ролики для узлов, которым маршрут назначил видео (нужен FFmpeg, озвучка edge-tts уходит в сеть Microsoft).

Порядок этапов: ingest → structure → route → иллюстрации → [ролики] → курс → проверка → курс ещё раз (со статусами проверки). Этап, которому не хватает входа, падает с понятной ошибкой.

Наши обучающие и контрольные главы записаны в `config/chapters.yaml` и запускаются по id: `make all CH=baraboshkin_par1-2`.

## 4. Без ключа — из кэша

```
LLM_OFFLINE=1 make all CH=baraboshkin_par1-2
```

С `LLM_OFFLINE=1` модель не вызывается: ответы берутся из `cache/llm/` (ключ кэша — модель + промпт + переменные). Промах кэша — ошибка с именем промпта, а не заглушка. Кэш в git — только для глав, прогнанных до заморозки, и только для той модели, которой они прогнаны. Новая глава без ключа не соберётся.

Озвучка роликов из кэша: `TTS_OFFLINE=1` (кэш `cache/tts/`).

## 5. Что получится

```
out/<ch>/units.json        единицы главы (ingest)
out/<ch>/layer.json        учебный слой — единственный источник правды
out/<ch>/coverage.json     каждая единица → узел или причина, почему без узла
out/<ch>/routing.json      формат каждого узла (текст / карточки / интерактив / шортс / ролик) и шаблон сцены
out/<ch>/illus/            иллюстрации и illustrations.json
out/<ch>/videos/<узел>/    script.json, scene_spec.json, mp4, vtt, passport.json
out/<ch>/verify/report.json  отчёт проверки (код выхода ≠ 0 при критических ошибках)
out/<ch>/course/index.html   курс главы — открывается двойным кликом, без сервера
out/index.html               главная всех собранных курсов
out/_metrics/llm_calls.jsonl каждый вызов модели: этап, модель, токены, деньги
```

## 6. Пересборка и отдельные этапы

| Что | make | без make |
|---|---|---|
| вся глава | `make all CH=<id>` / `MD=…` | `python -m pipeline.run --ch <id>` / `--md <путь> [--pdf …] [--pages …] [--video]` |
| после правки `layer.json` руками | `make rebuild NODE=<id узла> [CH=<id>]` | `python -m pipeline.run --rebuild <id узла> [--ch <id>]` |
| проверка чужого пакета | `make check PKG=<review_package.json> [OUT=…]` | `python -m pipeline.verify.external --pkg <…> --out <…>` |
| один ролик | `make video CH=<id> NODE=<id> [FORMAT=short\|long]` | `python -m pipeline.video.build --ch <id> --node <id>` |
| быстрый прогон | `make smoke` | `LLM_OFFLINE=1 python -m pipeline.run --smoke` |

`make rebuild` пересобирает ролик узла (если он есть) и затем шаг курса. Ролик и текст шага, изменившиеся по слою, требуют ключа: новых ответов модели в кэше нет. Id главы берётся из `layer.json` по id узла, `CH` нужен, только если узел есть в нескольких главах.

Отдельные этапы ядра: `python -m pipeline.ingest.run`, `pipeline.structure.run`, `pipeline.route.run` с теми же `--ch`/`--md`. Этапы других модулей — `docs/check.md`, `docs/course.md`, `docs/video.md`.
