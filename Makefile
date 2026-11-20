.DEFAULT_GOAL := help

PYTHON ?= python3
VENV_PYTHON := .venv/bin/python
CLI_LANG ?= ru

.PHONY: help setup run test lint format format-check check

help:
	@printf '%s\n' \
		'make help                 Show commands' \
		'make setup                Create .venv and install dev dependencies' \
		'make run [CLI_LANG=en]    Run the converter (default language: ru)' \
		'make test                 Run tests' \
		'make lint                 Run Ruff lint' \
		'make format               Format code with Ruff' \
		'make format-check         Check formatting' \
		'make check                Run tests, lint, format check, and pip check'

setup:
	@test -d .venv || $(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install -r requirements-dev.txt

run:
	$(VENV_PYTHON) index.py --lang "$(CLI_LANG)"

test:
	$(VENV_PYTHON) -m pytest

lint:
	$(VENV_PYTHON) -m ruff check .

format:
	$(VENV_PYTHON) -m ruff format .

format-check:
	$(VENV_PYTHON) -m ruff format --check .

check: test lint format-check
	$(VENV_PYTHON) -m pip check
