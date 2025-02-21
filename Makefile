build:
	@uv build

tox:
	@uv tool run tox

coverage:
	@uv run pytest -rxXs --cov=src --cov-report=term-missing --cov-fail-under=100

test:
	@uv run pytest

.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -hE '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Catch-all rule to allow additional arguments in make commands
%:
	@:
