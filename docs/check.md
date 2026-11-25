# Модуль проверки, доменный пакет, журнал (П2)

## Проверка своей главы — без LLM
```
python -m pipeline.verify.run --ch <id>        # или make verify CH=<id>
```
Нужны `out/<id>/units.json`, `layer.json`, `coverage.json`; если есть — `course/tasks.json` и `videos/*/script.json` (+ `scene_spec.json`).
Выход: `out/<id>/verify/report.json` (формат `review_output.schema.json`, одно замечание на цель) и `trust.json` (паспорт доверия). Код выхода 1, если есть `critical`.

Что проверяется:
- цитата утверждения на своей странице (`quotes.py`, порог 88): нет в главе → `critical`, другая страница → `significant`, в `fix` верная страница;
- каждое число текста узла, заданий и сценария есть в исходных единицах узла (`numbers.py`: «0,25», «5–20», «10⁻²», «5·10³», «15 %», числа словами);
- термин из `terms_introduced` не встречается в узлах раньше (`terms.py`, с окончаниями);
- сценарий и спецификация сцены — см. ниже.

П1 вызывает `pipeline.verify.quotes.check_quote(chapter_id, page, quote)` в цикле структурирования (md — из `units.json`).

## Сценарий и сцена ролика (для П4 до рендера)
```
python -m pipeline.verify.scene --ch <id> --video <video_id> [--llm]   # make scene CH=… VIDEO=… [LLM=1]
```
Без LLM: кадр в истинном масштабе, преувеличения названы числом, плашки, класс и метка кадра, нет генерации в A/B, `claim_id` у фраз, числа из главы, пауза на предсказание, вопрос на перенос, «исторический прибор», подписи ≤ 8 слов без формул, фразы-заблуждения из доменного пакета.
С `--llm`: ответы на каждый пункт `physics_checklist.json` (готовы для `passport.physics_checklist`) в `out/<id>/verify/scene_<video>.json`.
Из кода: `pipeline.verify.scene.check_scene(spec, script, claim_ids, sources, domain)`, `check_physics(spec, script, domain)`.

## Внешний пакет (тест)
```
python -m pipeline.verify.external --pkg <package.json> --out <ответ.json> [--team <имя>] [--workers 4]
# или make check PKG=<package.json> [OUT=…]
```
Глава — `chapter_file` рядом с пакетом. Каждая цель — отдельный вызов критика (`prompts/verify/critic.md`, кадры — `critic_frame.md` с картинкой). Замечание к утверждению или фразе выдаётся только с цитатой, которую `quotes.py` нашёл в главе; иначе цель попадает в `ext.verify.unproven` (не ложная тревога).

Счёт по ключу — ТОЛЬКО после прогона:
```
python -m pipeline.verify.eval --answer <ответ.json>     # make eval ANSWER=…
```

## Доменный пакет
`domain/geology/` — по `05_шаблоны/domain_pack_template.md`; `templates/` ведёт П4.
Новый домен (сдвиг):
```
python -m domain.build --domain drilling --ch <id главы после ingest>
python -m domain.build --domain drilling --md <глава.md> --pages a-b
```
Время сборки и счётчики — `domain/<домен>/build_log.json`. Существующий пакет не перезаписывается без `--force`.

## Журнал ручных правок
Любая правка результата после прогона — только так (коммит файлов + строка журнала с хэшем коммита):
```
python -m journal.cli add --ch <id> --min <минуты> --what "что изменено" --files <путь> [...] --reason "почему" [--people N] [--run-no N]
python -m journal.cli add-mentor --ch <id> --min <минуты> --what "слот ментора"
python -m journal.cli report                               # make journal-report
```
Файлы: `journal/manual_edits.csv` (колонки организаторов + `commit`), `journal/mentor_minutes.csv`.
