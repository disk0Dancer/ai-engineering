.PHONY: help install test fmt lint demo clean
.DEFAULT_GOAL := help

PYTHON ?= python3
VENV ?= .venv
VENV_PY := $(VENV)/bin/python
VENV_PIP := $(VENV_PY) -m pip

help:
	@echo "Targets: install test fmt lint demo clean"

$(VENV_PY):
	$(PYTHON) -m venv $(VENV)

install: $(VENV_PY)
	$(VENV_PY) -m ensurepip --upgrade
	$(VENV_PIP) install --upgrade pip setuptools wheel
	$(VENV_PIP) install --no-build-isolation -e ".[dev]"
	$(VENV_PY) -m support_agent.cli "refund INV-1001"

test:
	$(VENV_PY) -m pytest -q

fmt:
	$(VENV_PY) -m ruff format .

lint:
	$(VENV_PY) -m ruff check .

demo:
	$(VENV_PY) scripts/demo.py

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
