# Цели модуля «Видео» (П4). Подключается корневым Makefile через include mk/*.mk.
PYTHON ?= python

.PHONY: video-specs video-node video-coverage video-test video-hello video-hello-final

# Цель `make video CH=… NODE=… [FORMAT=…]` — в корневом Makefile (П1); она вызывает тот же pipeline.video.build.
# Здесь — то же с черновиком и набором данных для T2:
#   make video-node CH=<id главы> NODE=<id узла> [DRAFT=1] [DATASET=<dataset.json>] [FORMAT=short|long]
# Пара script.json/scene_spec.json берётся из out/<CH>/videos/<NODE>.<fmt>/ или генерируется video.spec.
video-node:
	$(if $(CH),,$(error нужен CH=<id главы>))
	$(if $(NODE),,$(error нужен NODE=<id узла>))
	$(PYTHON) -m pipeline.video.build --ch $(CH) --node $(NODE) $(if $(DRAFT),--draft) \
		$(if $(DATASET),--dataset $(DATASET)) $(if $(FORMAT),--format $(FORMAT))

# Спецификации (script.json + scene_spec.json) всех видеоузлов главы, без рендера: out/<CH>/videos/spec_report.json
#   make video-specs CH=<id главы> [DATASET=<dataset.json>] [DOMAIN=geology]
video-specs:
	$(if $(CH),,$(error нужен CH=<id главы>))
	$(PYTHON) -m pipeline.video.spec --ch $(CH) --all $(if $(DATASET),--dataset $(DATASET)) $(if $(DOMAIN),--domain $(DOMAIN))

# Отчёт покрытия видеоузлов шаблонами (без LLM и рендера): out/<CH>/videos/coverage.json
#   make video-coverage CH=<id главы> [DOMAIN=geology]
video-coverage:
	$(if $(CH),,$(error нужен CH=<id главы>))
	$(PYTHON) -m pipeline.video.coverage --ch $(CH) $(if $(DOMAIN),--domain $(DOMAIN))

video-test:
	$(PYTHON) -m pytest tests/video -q

# hello-ролик 9:16 на тестовом входе: черновик 540×960 и финал 1080×1920
video-hello:
	$(PYTHON) -m pipeline.video.build --ch video_hello --node video_hello.pipeline_check \
		--script fixtures/video/hello/script.json --scene-spec fixtures/video/hello/scene_spec.json --draft

video-hello-final:
	$(PYTHON) -m pipeline.video.build --ch video_hello --node video_hello.pipeline_check \
		--script fixtures/video/hello/script.json --scene-spec fixtures/video/hello/scene_spec.json
