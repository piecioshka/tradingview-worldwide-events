PYTHON  ?= python3
SCRIPT  := scripts/generate-events.py
PINE    := worldwide-events.pine

.PHONY: validate generate

validate:
	$(PYTHON) -m py_compile $(SCRIPT)
	@test -f $(PINE) || (echo "Missing: $(PINE)" && exit 1)
	@ls data/events-*.md >/dev/null
	@echo "OK"

generate: validate
	$(PYTHON) $(SCRIPT)
