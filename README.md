# course_maker — конвейер «глава книги → курс»

Глава книги (md с метками `<!-- page N -->`) → учебный слой → маршрутизация форматов → демо-курс (шаги, задания, карточки, иллюстрации) и ролики.
Курс открывается локально из файла, без сервера и логина.

Подробная инструкция запуска — **[docs/run.md](docs/run.md)**. Порядок работы на новой главе, проверки и ручные правки — **[docs/playbook.md](docs/playbook.md)**. Модели, инструменты и что уходит наружу — **[MANIFEST.md](MANIFEST.md)**.

## Быстрый старт

Нужны Python 3.12 и, для роликов и полного `pytest`, FFmpeg/ffprobe в `PATH` (`winget install Gyan.FFmpeg` / `apt install ffmpeg`).

**bash (Linux, macOS, Git Bash):**
```
python -m pip install -r requirements.txt
python -m pytest -q tests                      # без FFmpeg в PATH падает 1 тест видео
LLM_OFFLINE=1 python -m pipeline.run --smoke   # весь путь без ключа на маленькой главе, секунды
LLM_OFFLINE=1 LLM_MODEL=gemini/gemini-3.5-flash python -m pipeline.run --ch baraboshkin_par1-2
```

**PowerShell (Windows):**
```
python -m pip install -r requirements.txt
$env:LLM_OFFLINE="1"; python -m pipeline.run --smoke
$env:LLM_OFFLINE="1"; $env:LLM_MODEL="gemini/gemini-3.5-flash"; python -m pipeline.run --ch baraboshkin_par1-2
```
Переменные `$env:` остаются до конца сессии PowerShell: перед запуском с ключом — `Remove-Item Env:LLM_OFFLINE, Env:LLM_MODEL`.

Последняя команда собирает главу Барабошкина «Дельты» без ключа, из закоммиченного кэша ответов `cache/llm/`. Кэш получен моделью `gemini/gemini-3.5-flash`, поэтому её имя обязательно: с другой моделью — промах кэша и понятная ошибка. В кэше только ответы ядра (слой, маршрут), поэтому тексты шагов курса без ключа собираются из полей слоя.
Открыть курс: `out/baraboshkin_par1-2/course/index.html` (двойной клик), все собранные курсы — `out/index.html`.

С `make` (Linux, macOS, Git Bash с make) те же действия: `make install`, `make test`, `make smoke`, `make all CH=<id>`.

## Новая глава — без правки файлов

1. `.env` из `.env.example`: ключ провайдера и модель в формате litellm, например
   `ANTHROPIC_API_KEY=…` и `LLM_MODEL=anthropic/claude-opus-5-5` (или `GEMINI_API_KEY` / `OPENAI_API_KEY`). Несколько ключей одного провайдера — `LLM_API_KEYS=к1,к2`.
2. `python -m pipeline.run --md <глава.md> [--pdf <глава.pdf>] [--domain <домен>]`
   (`make all MD=<глава.md> [PDF=…] [DOMAIN=…]`).
   Id главы — из имени файла, язык — по тексту, страницы — из меток в md.
3. Глава из другого домена: если пакета `domain/<домен>/` нет, запуск остановится и подскажет команду сборки пакета `python -m domain.build --domain <домен> --ch <id>` (см. [docs/check.md](docs/check.md)).

Все параметры — [docs/run.md](docs/run.md), раздел 3.

## Пересборка после правки факта в слое

1. Поменять число или формулировку в `out/<id>/layer.json` (поле `claims[].text` нужного узла).
2. `python -m pipeline.run --rebuild <id узла>` (`make rebuild NODE=<id узла>`) — пересобирает ролик узла, если он есть, и страницу шага.
3. Открыть `out/<id>/course/step-<id узла>.html`: на странице новое число, цитата автора рядом — как в книге.

## Где что лежит

| Что | Где |
| --- | --- |
| Инструкция запуска | [docs/run.md](docs/run.md) |
| Плейбук: новая глава, проверки, ручные правки через журнал | [docs/playbook.md](docs/playbook.md) |
| Перечень моделей и как их заменить | [MANIFEST.md](MANIFEST.md), [docs/run.md](docs/run.md) раздел 2 |
| Промпты | `prompts/core/`, `prompts/verify/`, `prompts/course/`, `prompts/video/` |
| Доменный пакет геологии | `domain/geology/` |
| Модуль проверки внешнего пакета | `python -m pipeline.verify.external --pkg <review_package.json> --out <ответ.json>`, [docs/check.md](docs/check.md) |
| Курс | [docs/course.md](docs/course.md) |
| Ролики | [docs/video.md](docs/video.md); готовые ролики с паспортами — `out/latyshova_gl5_par17-20/videos/`, `out/basniev_gl23-24/videos/` |
| Учебный слой, покрытие, маршрут (Барабошкин, настоящий прогон) | `fixtures/core/live_baraboshkin_par1-2/` |
| Метрики | `metrics.csv` (шаблон организаторов); по каждой главе — `out/<id>/metrics.csv` |
| Журнал ручных правок | `journal/manual_edits.csv` |
| Кэш ответов модели и озвучки | `cache/llm/`, `cache/tts/` |

Тег замороженной версии — `v1.0-freeze`.
