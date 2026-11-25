# Архитектура репозитория

```
glava-kurs/                         (приватный репозиторий)
├── CLAUDE.md                       общие правила для всех агентов          — читают все
├── MANIFEST.md                     манифест по шаблону организаторов        — П1 (к заморозке)
├── metrics.csv                     метрики по шаблону организаторов         — П1
├── Makefile                        include mk/*.mk; цели install test smoke all rebuild check video — П1
├── requirements.txt                -r requirements/*.txt                   — П1
├── .env.example  .gitignore                                                — П1
│
├── contracts/models.py             модели по JSON-схемам организаторов      — П1 (только он)
│
├── config/
│   ├── chapters.yaml               главы: id, md, pdf, страницы, язык, домен, errata, prereq_cards — П1
│   └── llm.yaml                    модели по tier, цены                     — П1
│
├── pipeline/
│   ├── llm.py                      единственная точка вызова LLM, кэш, лог  — П1
│   ├── common/                     paths, io, config, domain.load()         — П1
│   ├── ingest/                     md+pdf → out/<ch>/units.json, сканы страниц — П1
│   ├── structure/                  units → layer.json + coverage.json       — П1
│   ├── route/                      layer → routing.json                     — П1
│   ├── verify/                     цитаты, числа, термины, сцены, критик, внешний пакет — П2
│   ├── course/                     layer → сайт курса + tasks.json          — П3
│   ├── illus/                      иллюстрации A/B кодом + illustrations.json — П3
│   └── video/                      script, scene_spec, шаблоны T1–T4, TTS, ffmpeg, passport.json — П4
│
├── prompts/
│   ├── core/                       промпты П1
│   ├── verify/                     промпты П2
│   ├── course/                     промпты П3
│   └── video/                      промпты П4
│
├── domain/                         доменные пакеты (структура организаторов) — П2
│   ├── geology/
│   │   ├── glossary.md  misconceptions.json  physics_checklist.json  it_bridges.md
│   │   ├── styleguide.json  pronunciation.md  stress_dictionary.md
│   │   ├── errata/                 листы опечаток по главам
│   │   └── templates/              параметры шаблонов сцен по типам трудности — П4
│   ├── drilling/                   собирается скриптом на тесте (сдвиг)
│   └── build.py                    сборка пакета для нового домена          — П2
│
├── journal/
│   ├── cli.py                      add / add-mentor / report + git commit   — П2
│   ├── manual_edits.csv            журнал правок (формат организаторов)
│   └── mentor_minutes.csv
│
├── scripts/demo_rebuild.sh         живая пересборка на защите               — П1
├── assets/video/                   SVG оборудования по фото-референсам      — П4
│
├── tests/core/ verify/ course/ video/      тесты каждого модуля, без сети   — владелец модуля
├── fixtures/core/ verify/ course/ video/   маленькие образцы данных         — владелец модуля
│   └── core/example_layer_organizers.json  пример слоя от организаторов
│
├── data/                           ТОЛЬКО ЧТЕНИЕ для всех
│   ├── books/                      6 книг md (с Drive «books md»)
│   ├── pdf/                        6 PDF (с Drive «книги»), переименованы как md
│   ├── analysis/                   6 анализов книг (с Drive «analysis books»)
│   ├── organizers/                 «пакет_вводных» целиком, структура как на Drive
│   │   ├── 01_схемы/               node, coverage, routing, task, illustration, passport .schema.json + example_layer.json
│   │   ├── 02_модуль_проверки/     review_package/output/key схемы, score_review.py, контрольный_пакет/ (key.json НЕ открывать до прогона)
│   │   ├── 03_стайлгайд/           styleguide.json, legend.html
│   │   ├── 04_доменные_заготовки/  misconceptions.json, physics_checklist.json, словарь ударений, портреты зрителя
│   │   ├── 05_шаблоны/             manual_edits.csv, metrics.csv, MANIFEST_template.md, domain_pack_template.md
│   │   └── 06_подача_и_референсы/  подача_доменов_геологии.md, разборы_4_роликов.md
│   └── pages/                      PNG страниц (генерирует ingest, в .gitignore)
│
├── cache/llm/  cache/tts/          кэш вызовов, коммитится при заморозке    — никто руками
├── out/<chapter>/                  результаты конвейера                     — никто руками
│   ├── units.json layer.json coverage.json routing.json          (П1)
│   ├── verify/report.json trust.json                              (П2)
│   ├── illus/illustrations.json + файлы                           (П3)
│   ├── course/index.html … tasks.json                             (П3)
│   └── videos/<video_id>/script.json scene_spec.json *.mp4 *.vtt passport.json frames/ (П4)
│
└── docs/
    ├── tz.md                       ТЗ
    ├── ARCHITECTURE.md             этот файл
    ├── PLAN.md                     последовательность действий
    ├── product.md                  фишки сверх ТЗ
    ├── submission_checklist.md     чек-лист сдачи
    ├── roles/P1.md … P4.md         задачи каждого
    ├── prompts/START_P1.md … P4    стартовые промпты агентам
    ├── run.md  playbook.md         (П1, к заморозке)
    └── check.md course.md video.md (П2, П3, П4)
```

## Поток данных

```
data/books/*.md + data/pdf/*.pdf
   │  ingest (П1)
   ▼
units.json ──structure (П1)──▶ layer.json + coverage.json ──route (П1)──▶ routing.json
                                   │   ▲ verify.quotes/numbers (П2) в цикле
                                   ▼
               ┌───────────────────┼───────────────────────┐
         illus (П3)          course (П3)              video (П4)
     illustrations.json   сайт + tasks.json   script → scene_spec → verify.scene (П2) → TTS → Manim → ffmpeg → passport.json
               └───────────────────┼───────────────────────┘
                                   ▼
                        verify.run (П2) → report.json, trust.json
```

## Что НЕ кладём в git
`.env` (ключ), `data/pages/`, `out/` (кроме финальных курсов и роликов при сдаче — решает П1), видео-референсы с Drive «видео» (01–06.mp4 — П4 держит у себя).
