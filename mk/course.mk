# Цели модуля «Курс» (П3). Корневой Makefile делает include mk/*.mk.
PY ?= python

.PHONY: course illus test-course
course:  ## make course CH=<id> [NODE=<node_id>] [NO_LLM=1] [DOMAIN=<домен>]
	$(PY) -m pipeline.course.build --ch "$(CH)" $(if $(NODE),--node "$(NODE)") $(if $(NO_LLM),--no-llm) $(if $(DOMAIN),--domain "$(DOMAIN)")

illus:  ## make illus CH=<id> [NO_LLM=1] [DOMAIN=<домен>]
	$(PY) -m pipeline.illus.run --ch "$(CH)" $(if $(NO_LLM),--no-llm) $(if $(DOMAIN),--domain "$(DOMAIN)")

test-course:
	$(PY) -m pytest tests/course -q
