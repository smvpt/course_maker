# Манифест модуля «Видео» (П4)

Окружение проверено 25.11.2026: Windows 11 Home 10.0.26200, виртуальное окружение `.venv` (`py -3.12 -m venv .venv`).

| Инструмент | Версия | Лицензия | Данные наружу |
|---|---|---|---|
| Python | 3.12.10 (64-bit, python.org) | PSF-2.0 | нет |
| Manim Community | 0.22.1 | MIT | нет |
| ManimPango (рендер текста, Pango) | 0.7.1 | MIT | нет |
| pycairo | 1.29.2 | LGPL-2.1-only OR MPL-1.1 | нет |
| PyAV (запись видео Manim) | 19.0.2 | BSD-3-Clause | нет |
| NumPy | 2.5.5 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | нет |
| SciPy (T1: интегральная показательная функция E1, поиск корня) | 1.18.1 | BSD-3-Clause | нет |
| lasio (T2: чтение LAS) | 0.34 | MIT | нет |
| faster-whisper (проверка озвучки) | 1.2.1 (CTranslate2 4.9.1, CPU int8) | MIT | нет: распознавание локальное; аудио никуда не уходит |
| Модель распознавания | Systran/faster-whisper-small (Whisper small, конвертирован для CTranslate2), ~480 МБ | MIT | нет; один раз скачивается с Hugging Face в кэш пользователя (`~/.cache/huggingface`), в репозиторий не кладётся |
| jsonschema (проверка паспорта) | 4.26.0 | MIT | нет |
| Схема оборудования T4 | `assets/video/t4_bop.svg` — условная схема превентора, нарисована P4; фото-референсов в материалах проекта нет | собственная | нет |
| Данные T2: Volve, скв. 15/9-19 A | `fixtures/video/t2_volve/159-19A_LFP.las` (8 810 367 байт, SHA256 92537d18…e7b6), выборка andymcdgeo/spwla_volve, коммит c293edf3, скачан 25.11.2026 | Данные Volve, Equinor ASA и бывшие партнёры по лицензии Volve; для учёбы и исследований, без перепродажи (условия из инструкции организаторов); у репозитория выборки файла лицензии нет | нет; в кадре метка «реальные данные» и атрибуция |
| Данные T2 (отладка) | `fixtures/video/t2_demo/synthetic_well.las` — синтетический LAS P4, условные значения | — | нет; в кадре метка «симуляция» |
| edge-tts | 7.3.1 | LGPL-3.0 | **да**: текст фразы сценария → онлайн-синтез Microsoft Edge (wss://speech.platform.bing.com). Больше ничего не отправляется |
| aiohttp (транспорт edge-tts) | 3.14.5 | Apache-2.0 AND MIT | через edge-tts |
| Голос | ru-RU-DmitryNeural (основной) | условия сервиса Microsoft | см. edge-tts |
| FFmpeg / ffprobe | N-127043-g5a54fcf75e-20260930, win64 GPL-сборка (winget-пакет `yt-dlp.FFmpeg`), libx264, AAC | GPL-3.0 (сборка с libx264) | нет |
| Шрифт | Segoe UI (системный шрифт Windows, задан в стайлгайде) | лицензия Microsoft в составе Windows | нет |
| pydantic / pytest (из ядра) | 2.13.5 / 9.2.0 | MIT / MIT | нет |
| LLM через `pipeline.llm` (ядро П1, модель из `config/llm.yaml`) | см. `manifest/core.md` | условия провайдера | **да**: `video.spec` отправляет провайдеру LLM узел учебного слоя (поля узла, утверждения с цитатами) и утверждённые фразы сценария. Текст главы целиком не отправляется |

Кэш синтеза — `cache/tts/<sha256>.mp3` + `.json`. Ключ: текст + голос + rate + volume + pitch + тип меток. В `.json` записаны версия edge-tts и метки речи. При `TTS_OFFLINE=1` промах кэша — ошибка, без сети.
