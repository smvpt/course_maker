# Корневой Makefile (П1). Цели модулей — в mk/<модуль>.mk, подключаются ниже.
#
#   make install                         зависимости всех модулей
#   make test                            все тесты, без сети
#   make smoke                           быстрый прогон без ключа (LLM_OFFLINE=1)
#   make all CH=<id>                     глава из config/chapters.yaml
#   make all MD=<глава.md> [PDF=…] [PAGES=a-b] [ERRATA=…] [PREREQ=…] [DOMAIN=…] [VIDEO=1]
#                                        любая глава без правки файлов
#   make rebuild NODE=<id> [CH=<id>]     пересборка шага и ролика после правки layer.json
#   make check PKG=<review_package.json> [OUT=<путь>]
#   make video CH=<id> NODE=<id> [FORMAT=short|long]

PY ?= $(shell command -v python3 >/dev/null 2>&1 && echo python3 || echo python)
export PYTHONUTF8 := 1

CHAPTER_ARGS = $(if $(CH),--ch "$(CH)") $(if $(MD),--md "$(MD)") $(if $(PDF),--pdf "$(PDF)") \
	$(if $(PAGES),--pages "$(PAGES)") $(if $(ERRATA),--errata "$(ERRATA)") \
	$(if $(PREREQ),--prereq "$(PREREQ)") $(if $(DOMAIN),--domain "$(DOMAIN)")

need = @test -n "$($(1))" || { echo "нужно задать $(1)=… ($(2))" >&2; exit 2; }

.PHONY: install test smoke all rebuild check video

install:
	$(PY) -m pip install -r requirements.txt

test:
	$(PY) -m pytest -q tests

# Временно (до задачи 4 П1): проверка фикстур по схемам организаторов.
# Затем — весь путь на fixtures/core/mini_chapter с LLM_OFFLINE=1.
smoke:
	LLM_OFFLINE=1 $(PY) -m pytest -q tests/core/test_schemas.py

all:
	@test -n "$(CH)$(MD)" || { echo "нужно CH=<id из config/chapters.yaml> или MD=<путь к md главы>" >&2; exit 2; }
	$(PY) -m pipeline.run $(CHAPTER_ARGS) $(if $(VIDEO),--video)

rebuild:
	$(call need,NODE,id узла из layer.json)
	$(PY) -m pipeline.run rebuild --node "$(NODE)" $(if $(CH),--ch "$(CH)")

check:
	$(call need,PKG,путь к review_package.json)
	$(PY) -m pipeline.verify.external --pkg "$(PKG)" --out "$(or $(OUT),out/_check/review_output.json)"

video:
	$(call need,CH,id главы)
	$(call need,NODE,id узла)
	$(PY) -m pipeline.video.build --ch "$(CH)" --node "$(NODE)" $(if $(FORMAT),--format $(FORMAT))

-include mk/*.mk
