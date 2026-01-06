# Makefile for Paper Collector
# Provides convenient shortcuts for common development tasks

.PHONY: help install test lint format clean run

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies with Poetry
	poetry install

test:  ## Run tests with pytest
	poetry run pytest -v

test-cov:  ## Run tests with coverage report
	poetry run pytest --cov=src --cov-report=html --cov-report=term

lint:  ## Run linting checks
	poetry run ruff check src/ tests/
	poetry run mypy src/

format:  ## Format code with Black
	poetry run black src/ tests/ examples/

format-check:  ## Check code formatting without making changes
	poetry run black --check src/ tests/ examples/

clean:  ## Clean up generated files
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run-example:  ## Run the basic usage example
	poetry run python examples/basic_usage.py

ingest:  ## Ingest a PDF (usage: make ingest PDF=path/to/file.pdf)
	poetry run python -m src.main ingest $(PDF)

version:  ## Show version information
	poetry run python -m src.main version

all: format lint test  ## Run format, lint, and test
