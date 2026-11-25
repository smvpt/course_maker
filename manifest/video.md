# Манифест модуля «Видео» (П4)

Окружение проверено 25.11.2026: Windows 11 Home 10.0.26200, виртуальное окружение `.venv` (`py -3.12 -m venv .venv`).

| Инструмент | Версия | Лицензия | Данные наружу |
|---|---|---|---|
| Python | 3.12.10 (64-bit, python.org) | PSF-2.0 | нет |
| Manim Community | 0.22.1 | MIT | нет |
| ManimPango (рендер текста, Pango) | 0.7.1 | MIT | нет |
| pycairo | 1.29.2 | LGPL-2.1-only OR MPL-1.1 | нет |
| PyAV (запись видео Manim) | 19.0.2 | BSD-3-Clause | нет |
| edge-tts | 7.3.1 | LGPL-3.0 | **да**: текст фразы сценария → онлайн-синтез Microsoft Edge (wss://speech.platform.bing.com). Больше ничего не отправляется |
| aiohttp (транспорт edge-tts) | 3.14.5 | Apache-2.0 AND MIT | через edge-tts |
| Голос | ru-RU-DmitryNeural (основной) | условия сервиса Microsoft | см. edge-tts |
| FFmpeg / ffprobe | N-127043-g5a54fcf75e-20260930, win64 GPL-сборка (winget-пакет `yt-dlp.FFmpeg`), libx264, AAC | GPL-3.0 (сборка с libx264) | нет |
| Шрифт | Segoe UI (системный шрифт Windows, задан в стайлгайде) | лицензия Microsoft в составе Windows | нет |
| pydantic / pytest (из ядра) | 2.14.4 / 9.2.0 | MIT / MIT | нет |

Кэш синтеза — `cache/tts/<sha256>.mp3` + `.json`. Ключ: текст + голос + rate + volume + pitch + тип меток. В `.json` записаны версия edge-tts и метки речи. При `TTS_OFFLINE=1` промах кэша — ошибка, без сети.
