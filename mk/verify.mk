# Цели модуля проверки (П2).
#   make verify CH=<id>                         детерминированная проверка → out/<id>/verify/report.json
#   make scene CH=<id> VIDEO=<video_id> [LLM=1] проверка script.json + scene_spec.json ролика
#   make eval ANSWER=<ответ.json> [KEY=<key>]   счёт по ключу (только ПОСЛЕ прогона!)
#   make journal-report                         минуты ручных правок по главам
.PHONY: verify scene eval journal-report

verify:
	$(call need,CH,id главы)
	$(PY) -m pipeline.verify.run --ch "$(CH)"

scene:
	$(call need,CH,id главы)
	$(call need,VIDEO,id ролика)
	$(PY) -m pipeline.verify.scene --ch "$(CH)" --video "$(VIDEO)" $(if $(LLM),--llm)

eval:
	$(call need,ANSWER,путь к ответу модуля)
	$(PY) -m pipeline.verify.eval --answer "$(ANSWER)" $(if $(KEY),--key "$(KEY)")

journal-report:
	$(PY) -m journal.cli report
