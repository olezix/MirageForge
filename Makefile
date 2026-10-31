# MirageForge Makefile
# Standard development commands

.PHONY: help setup install install-dev test test-cov lint lint-fix format type-check demo run server clean docker docker-build docker-up docker-down check docs

PYTHON := python3
PIP := pip
PYTEST := pytest
RUFF := ruff
MYPY := mypy

help: ## Show this help message
	@echo "MirageForge Development Commands"
	@echo "================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Setup project and install all dependencies
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e ".[dev]"
	@echo "✓ Setup complete. Run 'make test' to verify installation."

install: ## Install production dependencies only
	$(PIP) install -e .

install-dev: ## Install development dependencies
	$(PIP) install -e ".[dev]"

install-ml: ## Install optional ML dependencies (CLIP, torch)
	$(PIP) install -e ".[ml]"

test: ## Run tests without network or GPU
	$(PYTEST) -v tests/

test-cov: ## Run tests with coverage report
	$(PYTEST) -v --cov=mirageforge --cov-report=html --cov-report=term-missing tests/

test-unit: ## Run unit tests only
	$(PYTEST) -v tests/unit/

test-integration: ## Run integration tests only
	$(PYTEST) -v tests/integration/

test-e2e: ## Run end-to-end tests only
	$(PYTEST) -v tests/e2e/

lint: ## Run linters (ruff and mypy)
	$(RUFF) check .
	$(MYPY) src/mirageforge

lint-fix: ## Auto-fix linting issues
	$(RUFF) check --fix .
	$(RUFF) format .

format: ## Format code with ruff
	$(RUFF) format .
	$(RUFF) check --fix .

type-check: ## Run type checking with mypy
	$(MYPY) src/mirageforge

demo: ## Run demo pipeline (generates artifacts)
	$(PYTHON) -m mirageforge.cli demo --out artifacts/demo --seed 42 --rounds 3 --candidates 200 --top 12

run: ## Run development server
	$(PYTHON) -m mirageforge.cli run-server --host 0.0.0.0 --port 8000

server: ## Run server with uvicorn directly
	uvicorn mirageforge.web.app:app --host 0.0.0.0 --port 8000 --reload

init-db: ## Initialize database
	$(PYTHON) -m mirageforge.cli init-db

export: ## Export study data (requires ADMIN_TOKEN)
	$(PYTHON) -m mirageforge.cli export --study-id 1 --format csv --out artifacts/export

analyze: ## Analyze study data
	$(PYTHON) -m mirageforge.cli analyze --study-id 1 --out artifacts/analysis

clean: ## Remove generated files and caches
	rm -rf artifacts/*
	rm -rf data/*.db
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete

docker-build: ## Build Docker image
	docker build -t mirageforge:latest .

docker-up: ## Start services with docker-compose
	docker-compose up -d

docker-down: ## Stop docker-compose services
	docker-compose down

docker: ## Build and run with docker-compose
	docker-compose up --build

check: ## Run all checks (lint + test + demo smoke test)
	@echo "Running lint..."
	$(MAKE) lint
	@echo "Running tests..."
	$(MAKE) test
	@echo "Running demo smoke test..."
	$(PYTHON) -m mirageforge.cli demo --out artifacts/demo-smoke --seed 999 --rounds 1 --candidates 50 --top 6
	@echo "✓ All checks passed"

docs: ## Generate documentation (placeholder)
	@echo "Documentation is in docs/ directory"
	@echo "Open README.md to get started"

ci: ## Run CI checks locally (same as GitHub Actions)
	$(MAKE) check

# Development shortcuts
dev: setup init-db run ## Setup, init DB, and run server

rebuild: clean setup test ## Clean, setup, and test

.PHONY: help
