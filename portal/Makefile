# OWASP Zombies on Fire - Tabletop Exercise Portal
# Makefile for common operations (macOS/Linux)

.PHONY: help install install-dev run dev test clean docker-build docker-run docker-stop docker-logs setup-env

# Default target
help:
	@echo "╔═══════════════════════════════════════════════════════════╗"
	@echo "║    OWASP Zombies on Fire - Makefile Commands              ║"
	@echo "╚═══════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install        Install dependencies in virtual environment"
	@echo "  make install-dev    Install with development dependencies"
	@echo "  make setup-env      Create .env file from template"
	@echo ""
	@echo "Run Commands:"
	@echo "  make run            Run the application (production mode)"
	@echo "  make dev            Run the application (development mode with reload)"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-build   Build Docker image"
	@echo "  make docker-run     Run application in Docker"
	@echo "  make docker-stop    Stop Docker containers"
	@echo "  make docker-logs    View Docker container logs"
	@echo "  make docker-prod    Run with production Docker Compose"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make test           Run tests"
	@echo "  make clean          Remove virtual environment and cache files"
	@echo "  make lint           Run linting (if configured)"
	@echo ""

# Python and venv settings
PYTHON := python3
VENV := venv
VENV_BIN := $(VENV)/bin
PIP := $(VENV_BIN)/pip
PYTHON_VENV := $(VENV_BIN)/python

# Create virtual environment and install dependencies
install: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo ""
	@echo "✓ Installation complete!"
	@echo "  Activate venv: source $(VENV)/bin/activate"
	@echo "  Run app: make run"

# Create virtual environment with dev dependencies
install-dev: $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-asyncio httpx black isort flake8
	@echo ""
	@echo "✓ Development installation complete!"

# Create virtual environment
$(VENV):
	$(PYTHON) -m venv $(VENV)
	@echo "✓ Virtual environment created"

# Setup environment file
setup-env:
	@if [ -f .env ]; then \
		echo "⚠ .env file already exists"; \
	else \
		cp .env.example .env; \
		SECRET_KEY=$$($(PYTHON) -c "import secrets; print(secrets.token_urlsafe(32))"); \
		if [ "$$(uname)" = "Darwin" ]; then \
			sed -i '' "s/your-super-secret-key-change-this-in-production/$$SECRET_KEY/" .env; \
		else \
			sed -i "s/your-super-secret-key-change-this-in-production/$$SECRET_KEY/" .env; \
		fi; \
		echo "✓ .env file created with generated secret key"; \
		echo "⚠ Remember to configure your LLM API keys in .env"; \
	fi
	@mkdir -p uploads generated_pdfs
	@echo "✓ Required directories created"

# Run application (production mode)
run: $(VENV)
	$(PYTHON_VENV) -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run application (development mode with auto-reload)
dev: $(VENV)
	$(PYTHON_VENV) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run tests
test: $(VENV)
	$(PYTHON_VENV) -m pytest tests/ -v

# Docker build
docker-build:
	docker build -t zombies-on-fire:latest .

# Docker run (development)
docker-run:
	docker-compose up -d
	@echo ""
	@echo "✓ Container started"
	@echo "  View logs: make docker-logs"
	@echo "  Stop: make docker-stop"

# Docker run (production)
docker-prod:
	docker-compose -f docker-compose.prod.yml up -d
	@echo ""
	@echo "✓ Production containers started"

# Docker stop
docker-stop:
	docker-compose down
	@echo "✓ Containers stopped"

# Docker logs
docker-logs:
	docker-compose logs -f

# Clean up
clean:
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf app/__pycache__
	rm -rf app/**/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleaned up"

# Lint (if tools installed)
lint: $(VENV)
	-$(VENV_BIN)/black --check app/
	-$(VENV_BIN)/isort --check-only app/
	-$(VENV_BIN)/flake8 app/

# Format code
format: $(VENV)
	$(VENV_BIN)/black app/
	$(VENV_BIN)/isort app/
	@echo "✓ Code formatted"
