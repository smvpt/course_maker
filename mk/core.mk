# Цели ядра (П1): отдельные этапы. Аргументы главы — как у make all (CH= или MD= …).
.PHONY: ingest structure route

ingest:
	@test -n "$(CH)$(MD)" || { echo "нужно CH=… или MD=…" >&2; exit 2; }
	$(PY) -m pipeline.ingest.run $(CHAPTER_ARGS)

structure:
	@test -n "$(CH)$(MD)" || { echo "нужно CH=… или MD=…" >&2; exit 2; }
	$(PY) -m pipeline.structure.run $(CHAPTER_ARGS)

route:
	@test -n "$(CH)$(MD)" || { echo "нужно CH=… или MD=…" >&2; exit 2; }
	$(PY) -m pipeline.route.run $(CHAPTER_ARGS)
