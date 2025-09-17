# GTR-Bench Makefile

.PHONY: help install test lint format clean docs

help:  ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install dependencies and package
	pip install -r requirements.txt
	pip install -e .

install-dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:  ## Run tests
	pytest

test-unit:  ## Run unit tests only
	pytest tests/unit/

test-integration:  ## Run integration tests only
	pytest tests/integration/

lint:  ## Run linting
	flake8 src/ tests/
	mypy src/

format:  ## Format code
	black src/ tests/
	isort src/ tests/

format-check:  ## Check code formatting
	black --check src/ tests/
	isort --check-only src/ tests/

docs:  ## Build documentation
	cd docs && make html

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build package
	python setup.py sdist bdist_wheel

evaluate:  ## Run benchmark evaluation
	python scripts/evaluation/run_benchmark.py

setup-data:  ## Setup sample data
	mkdir -p data/{raw,processed,annotations,splits,samples}
	mkdir -p experiments/{runs,logs,checkpoints}
	mkdir -p results/{outputs,analysis,reports,leaderboard}