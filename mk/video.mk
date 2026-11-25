# Цели модуля «Видео» (П4). Подключается корневым Makefile через include mk/*.mk.
PYTHON ?= python

.PHONY: video-node video-test video-hello video-hello-final

# Цель `make video CH=… NODE=… [FORMAT=…]` — в корневом Makefile (П1); она вызывает тот же pipeline.video.build.
# Здесь — то же с черновиком и набором данных для T2:
#   make video-node CH=<id главы> NODE=<id узла> [DRAFT=1] [DATASET=<dataset.json>] [FORMAT=short|long]
# Пара script.json/scene_spec.json берётся из out/<CH>/videos/<NODE>.<fmt>/ или генерируется video.spec.
video-node:
	$(if $(CH),,$(error нужен CH=<id главы>))
	$(if $(NODE),,$(error нужен NODE=<id узла>))
	$(PYTHON) -m pipeline.video.build --ch $(CH) --node $(NODE) $(if $(DRAFT),--draft) \
		$(if $(DATASET),--dataset $(DATASET)) $(if $(FORMAT),--format $(FORMAT))

video-test:
	$(PYTHON) -m pytest tests/video -q

# hello-ролик 9:16 на тестовом входе: черновик 540×960 и финал 1080×1920
video-hello:
	$(PYTHON) -m pipeline.video.build --ch video_hello --node video_hello.pipeline_check \
		--script fixtures/video/hello/script.json --scene-spec fixtures/video/hello/scene_spec.json --draft

video-hello-final:
	$(PYTHON) -m pipeline.video.build --ch video_hello --node video_hello.pipeline_check \
		--script fixtures/video/hello/script.json --scene-spec fixtures/video/hello/scene_spec.json
