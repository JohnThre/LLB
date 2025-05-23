# LLB (爱学伴) - Local AI-Driven Sexual Health Education
# Makefile for build automation and project management

.PHONY: help install setup clean test lint format build run dev deploy docs

# Default target
help:
	@echo "LLB (爱学伴) - Build Automation"
	@echo "================================"
	@echo ""
	@echo "Available targets:"
	@echo "  help          Show this help message"
	@echo "  install       Install all dependencies"
	@echo "  setup         Complete project setup"
	@echo "  clean         Clean build artifacts and cache"
	@echo "  test          Run all tests"
	@echo "  lint          Run code linting"
	@echo "  format        Format code"
	@echo "  build         Build the application"
	@echo "  run           Run the application"
	@echo "  dev           Start development servers"
	@echo "  deploy        Deploy the application"
	@echo "  docs          Generate documentation"
	@echo ""

# Variables
PYTHON := python3.11
PIP := pip
NODE := node
NPM := npm
YARN := yarn
BACKEND_DIR := backend
FRONTEND_DIR := frontend
AI_DIR := ai
VENV_DIR := llb-env

# Installation targets
install: install-backend install-frontend install-ai
	@echo "✅ All dependencies installed successfully"

install-backend:
	@echo "📦 Installing backend dependencies..."
	cd $(BACKEND_DIR) && \
	$(PYTHON) -m venv $(VENV_DIR) && \
	source $(VENV_DIR)/bin/activate && \
	$(PIP) install --upgrade pip && \
	$(PIP) install -r requirements.txt

install-frontend:
	@echo "📦 Installing frontend dependencies..."
	cd $(FRONTEND_DIR) && $(YARN) install

install-ai:
	@echo "📦 Installing AI dependencies..."
	cd $(AI_DIR) && \
	source ../$(BACKEND_DIR)/$(VENV_DIR)/bin/activate && \
	$(PIP) install -r requirements.txt

# Setup targets
setup: install setup-env setup-models setup-dirs
	@echo "✅ Project setup completed successfully"

setup-env:
	@echo "🔧 Setting up environment..."
	cp .env.example .env || echo "⚠️  .env.example not found, skipping"
	cd $(BACKEND_DIR) && cp .env.example .env || echo "⚠️  Backend .env.example not found"
	cd $(FRONTEND_DIR) && cp .env.example .env || echo "⚠️  Frontend .env.example not found"

setup-models:
	@echo "🤖 Setting up AI models..."
	cd $(AI_DIR) && \
	source ../$(BACKEND_DIR)/$(VENV_DIR)/bin/activate && \
	$(PYTHON) scripts/download_models.py || echo "⚠️  Model download script not found"

setup-dirs:
	@echo "📁 Creating necessary directories..."
	mkdir -p $(BACKEND_DIR)/logs
	mkdir -p $(BACKEND_DIR)/uploads
	mkdir -p $(BACKEND_DIR)/static
	mkdir -p $(AI_DIR)/cache
	mkdir -p $(AI_DIR)/temp
	mkdir -p docs/generated

# Cleaning targets
clean: clean-backend clean-frontend clean-ai clean-logs
	@echo "✅ Cleanup completed"

clean-backend:
	@echo "🧹 Cleaning backend..."
	cd $(BACKEND_DIR) && \
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
	find . -name "*.pyc" -delete 2>/dev/null || true && \
	rm -rf .pytest_cache 2>/dev/null || true

clean-frontend:
	@echo "🧹 Cleaning frontend..."
	cd $(FRONTEND_DIR) && \
	rm -rf node_modules/.cache 2>/dev/null || true && \
	rm -rf build 2>/dev/null || true && \
	rm -rf dist 2>/dev/null || true

clean-ai:
	@echo "🧹 Cleaning AI cache..."
	cd $(AI_DIR) && \
	rm -rf temp/* 2>/dev/null || true && \
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

clean-logs:
	@echo "🧹 Cleaning logs..."
	rm -rf $(BACKEND_DIR)/logs/*.log 2>/dev/null || true

# Testing targets
test: test-backend test-frontend
	@echo "✅ All tests completed"

test-backend:
	@echo "🧪 Running backend tests..."
	cd $(BACKEND_DIR) && \
	source $(VENV_DIR)/bin/activate && \
	pytest tests/ -v --cov=app --cov-report=html

test-frontend:
	@echo "🧪 Running frontend tests..."
	cd $(FRONTEND_DIR) && $(YARN) test --run --coverage

test-ai:
	@echo "🧪 Running AI tests..."
	cd $(AI_DIR) && \
	source ../$(BACKEND_DIR)/$(VENV_DIR)/bin/activate && \
	pytest tests/ -v

# Code quality targets
lint: lint-backend lint-frontend
	@echo "✅ Linting completed"

lint-backend:
	@echo "🔍 Linting backend code..."
	cd $(BACKEND_DIR) && \
	source $(VENV_DIR)/bin/activate && \
	flake8 app/ --max-line-length=80 && \
	mypy app/ --ignore-missing-imports

lint-frontend:
	@echo "🔍 Linting frontend code..."
	cd $(FRONTEND_DIR) && $(YARN) lint

format: format-backend format-frontend
	@echo "✅ Code formatting completed"

format-backend:
	@echo "🎨 Formatting backend code..."
	cd $(BACKEND_DIR) && \
	source $(VENV_DIR)/bin/activate && \
	black app/ --line-length=80 && \
	isort app/

format-frontend:
	@echo "🎨 Formatting frontend code..."
	cd $(FRONTEND_DIR) && $(YARN) format

# Build targets
build: build-backend build-frontend
	@echo "✅ Build completed"

build-backend:
	@echo "🏗️  Building backend..."
	cd $(BACKEND_DIR) && \
	source $(VENV_DIR)/bin/activate && \
	$(PYTHON) -m compileall app/

build-frontend:
	@echo "🏗️  Building frontend..."
	cd $(FRONTEND_DIR) && $(YARN) build

# Run targets
run: run-backend

run-backend:
	@echo "🚀 Starting backend server..."
	cd $(BACKEND_DIR) && \
	source $(VENV_DIR)/bin/activate && \
	uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

run-frontend:
	@echo "🚀 Starting frontend development server..."
	cd $(FRONTEND_DIR) && $(YARN) start

# Development targets
dev:
	@echo "🚀 Starting development environment..."
	@echo "Starting backend server in background..."
	cd $(BACKEND_DIR) && \
	source $(VENV_DIR)/bin/activate && \
	uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload &
	@echo "Starting frontend development server..."
	cd $(FRONTEND_DIR) && $(YARN) start

dev-backend:
	@echo "🚀 Starting backend in development mode..."
	cd $(BACKEND_DIR) && \
	source $(VENV_DIR)/bin/activate && \
	LLB_ENVIRONMENT=development uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

dev-frontend:
	@echo "🚀 Starting frontend in development mode..."
	cd $(FRONTEND_DIR) && $(YARN) start

# Deployment targets
deploy: deploy-local

deploy-local:
	@echo "🚀 Deploying locally..."
	$(MAKE) build
	@echo "✅ Local deployment completed"

deploy-prod:
	@echo "🚀 Deploying to production..."
	$(MAKE) build
	@echo "⚠️  Production deployment not implemented yet"

# Documentation targets
docs: docs-api docs-user
	@echo "✅ Documentation generated"

docs-api:
	@echo "📚 Generating API documentation..."
	cd $(BACKEND_DIR) && \
	source $(VENV_DIR)/bin/activate && \
	$(PYTHON) -c "import app.main; print('API docs available at /docs')"

docs-user:
	@echo "📚 Generating user documentation..."
	@echo "User documentation available in docs/ directory"

# Utility targets
check-deps:
	@echo "🔍 Checking dependencies..."
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "❌ Python 3.11 not found"; exit 1; }
	@command -v $(NODE) >/dev/null 2>&1 || { echo "❌ Node.js not found"; exit 1; }
	@command -v $(YARN) >/dev/null 2>&1 || { echo "❌ Yarn not found"; exit 1; }
	@echo "✅ All required dependencies found"

status:
	@echo "📊 Project Status"
	@echo "=================="
	@echo "Backend: $(shell cd $(BACKEND_DIR) && source $(VENV_DIR)/bin/activate && python --version 2>/dev/null || echo 'Not installed')"
	@echo "Frontend: $(shell cd $(FRONTEND_DIR) && node --version 2>/dev/null || echo 'Not installed')"
	@echo "AI Models: $(shell ls $(AI_DIR)/models/ 2>/dev/null | wc -l || echo '0') models found"

logs:
	@echo "📋 Recent logs:"
	@tail -n 20 $(BACKEND_DIR)/logs/*.log 2>/dev/null || echo "No logs found"

# Docker targets
docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-up:
	@echo "🐳 Starting Docker containers..."
	docker-compose up -d

docker-down:
	@echo "🐳 Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "🐳 Docker container logs:"
	docker-compose logs -f 