# Цели модуля «Видео» (П4). Подключается корневым Makefile через include mk/*.mk.
PYTHON ?= python

.PHONY: video-test video-hello video-hello-final

video-test:
	$(PYTHON) -m pytest tests/video -q

# hello-ролик 9:16 на тестовом входе: черновик 540×960 и финал 1080×1920
video-hello:
	$(PYTHON) -m pipeline.video.build --ch video_hello --node video_hello.pipeline_check \
		--script fixtures/video/hello/script.json --scene-spec fixtures/video/hello/scene_spec.json --draft

video-hello-final:
	$(PYTHON) -m pipeline.video.build --ch video_hello --node video_hello.pipeline_check \
		--script fixtures/video/hello/script.json --scene-spec fixtures/video/hello/scene_spec.json
