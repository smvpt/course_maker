## Ядро (П1): ingest, structure, route, llm.py

### Модели

| Этап | Модель | Версия | Где работает | Что уходит наружу | Как заменить |
| --- | --- | --- | --- | --- | --- |
| Учебный слой (structure) | anthropic/claude-opus-5-5 (tier strong) | claude-opus-5-5 | облако Anthropic через litellm | текст единиц главы | `LLM_MODEL_STRONG` или `LLM_MODEL` в `.env` |
| Маршрутизация (route) | anthropic/claude-opus-5-5 (tier default) | claude-opus-5-5 | облако Anthropic через litellm | поля узлов учебного слоя | `LLM_MODEL_DEFAULT` или `LLM_MODEL` в `.env` |
| Описание рисунков (ingest) | anthropic/claude-opus-5-5 (tier vision) | claude-opus-5-5 | облако Anthropic через litellm | сканы страниц с рисунками, подписи | `LLM_MODEL_VISION` или `LLM_MODEL` в `.env` |

Провайдер меняется именем модели (`openai/…`, `gemini/…`) и ключом (`LLM_API_KEY` или стандартная переменная провайдера). Без ключа: `LLM_OFFLINE=1` — только кэш `cache/llm/`.

### Инструменты

| Инструмент | Версия | Лицензия | Для чего | Данные наружу |
| --- | --- | --- | --- | --- |
| Python | 3.11+ | PSF | конвейер | нет |
| pydantic | 2.13.5 | MIT | контракты данных | нет |
| PyYAML | 6.0.3 | MIT | конфиги | нет |
| python-dotenv | 1.2.4 | BSD-3 | чтение `.env` | нет |
| litellm | 1.111.0 | MIT | единый вызов LLM разных провайдеров | текст промпта и картинки — выбранному провайдеру |
| jsonschema | 4.26.0 | MIT | проверка выходов по схемам организаторов | нет |
| pytest | 9.2.0 | MIT | тесты | нет |
