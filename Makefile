.PHONY: help install lint format test jupyter neo4j-up neo4j-down generate-data verify clean

help:
	@echo "Graph Masterclass — Available Commands"
	@echo "======================================="
	@echo "make install           Install dependencies"
	@echo "make lint              Run ruff linter"
	@echo "make format            Format code with ruff"
	@echo "make test              Run pytest suite"
	@echo "make jupyter           Start JupyterLab"
	@echo "make generate-data     Generate all synthetic datasets"
	@echo "make neo4j-up          Start Neo4j container"
	@echo "make neo4j-down        Stop Neo4j container"
	@echo "make neo4j-logs        Tail Neo4j logs"
	@echo "make verify            Run lint and test"
	@echo "make clean             Clean generated files"

install:
	@echo "Installing dependencies..."
	python -m pip install --upgrade pip
	pip install -r requirements.txt

lint:
	@echo "Running linter..."
	ruff check src tests

format:
	@echo "Formatting code..."
	ruff format src tests

test:
	@echo "Running tests..."
	pytest -v

jupyter:
	@echo "Starting JupyterLab..."
	jupyter lab

generate-data:
	@echo "Generating synthetic datasets..."
	python -m src.data_generation.support_escalation
	python -m src.data_generation.approval_handoffs
	python -m src.data_generation.hidden_experts
	python -m src.data_generation.document_policy
	python -m src.data_generation.supplier_risk
	python -m src.data_generation.finance_reporting
	python -m src.data_generation.project_margin
	python -m src.data_generation.it_incidents
	python -m src.data_generation.compliance_controls
	python -m src.data_generation.sales_accounts
	python -m src.data_generation.product_feedback
	python -m src.data_generation.portfolio_benchmark

neo4j-up:
	@echo "Starting Neo4j container..."
	docker compose up -d neo4j
	@echo "Waiting for Neo4j to be ready..."
	@sleep 10
	@echo "Neo4j Browser: http://localhost:7474"
	@echo "Bolt endpoint: bolt://localhost:7687"

neo4j-down:
	@echo "Stopping Neo4j container..."
	docker compose down

neo4j-logs:
	@echo "Tailing Neo4j logs..."
	docker compose logs -f neo4j

neo4j-clean:
	@echo "Removing Neo4j volumes..."
	docker compose down -v

verify: lint test
	@echo "✓ All checks passed"

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleanup complete"
