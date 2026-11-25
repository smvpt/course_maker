# Цели модуля «Курс» (П3). Корневой Makefile делает include mk/*.mk.
PY ?= python

.PHONY: course test-course
course:  ## make course CH=<id> [NODE=<node_id>]
	$(PY) -m pipeline.course.build --ch $(CH) $(if $(NODE),--node $(NODE),)

test-course:
	$(PY) -m pytest tests/course -q
