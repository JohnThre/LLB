# LLB (爱学伴) - AI-Powered Sexual Health Education
# Makefile for development, testing, and deployment

.PHONY: help setup clean test dev build deploy

# Default target
.DEFAULT_GOAL := help

# Use bash shell explicitly
SHELL := /bin/bash

# Colors for output
BLUE := \\033[0;34m
GREEN := \\033[0;32m
YELLOW := \\033[1;33m
RED := \\033[0;31m
NC := \\033[0m # No Color

# Project configuration
PROJECT_NAME := LLB (爱学伴)
BACKEND_DIR := backend
FRONTEND_DIR := frontend
AI_DIR := ai
VENV_NAME := llb-env

help: ## Show this help message
	@echo "$(BLUE)$(PROJECT_NAME) - Development Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Setup Commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(setup|install|clean)"
	@echo ""
	@echo "$(GREEN)Development Commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(dev|start|stop|restart)"
	@echo ""
	@echo "$(GREEN)Testing Commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(test|coverage)"
	@echo ""
	@echo "$(GREEN)Build & Deploy Commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(build|deploy|docker)"
	@echo ""
	@echo "$(GREEN)Utility Commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -vE "(setup|install|clean|dev|start|stop|restart|test|coverage|build|deploy|docker)"

# Setup Commands
setup: ## Run the complete project setup with AI providers
	@echo "$(BLUE)Setting up $(PROJECT_NAME) with AI providers...$(NC)"
	chmod +x setup_ai_providers.sh
	./setup_ai_providers.sh

install-deps: ## Install all dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@echo "$(YELLOW)Installing backend dependencies...$(NC)"
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && pip install -r requirements.txt
	@echo "$(YELLOW)Installing frontend dependencies...$(NC)"
	cd $(FRONTEND_DIR) && yarn install

verify-providers: ## Verify AI provider configuration
	@echo "$(BLUE)Verifying AI provider configuration...$(NC)"
	@if [ -f ".env" ]; then \
		echo "$(GREEN)✅ Environment file found$(NC)"; \
		if grep -q "OPENAI_API_KEY=" .env && [ "$$(grep OPENAI_API_KEY= .env | cut -d= -f2)" != "" ]; then \
			echo "$(GREEN)✅ OpenAI API key configured$(NC)"; \
		fi; \
		if grep -q "ANTHROPIC_API_KEY=" .env && [ "$$(grep ANTHROPIC_API_KEY= .env | cut -d= -f2)" != "" ]; then \
			echo "$(GREEN)✅ Claude API key configured$(NC)"; \
		fi; \
		if grep -q "GOOGLE_API_KEY=" .env && [ "$$(grep GOOGLE_API_KEY= .env | cut -d= -f2)" != "" ]; then \
			echo "$(GREEN)✅ Gemini API key configured$(NC)"; \
		fi; \
		if grep -q "OLLAMA_ENABLED=true" .env; then \
			echo "$(GREEN)✅ Ollama enabled$(NC)"; \
			curl -s http://localhost:11434/api/tags >/dev/null && echo "$(GREEN)✅ Ollama running$(NC)" || echo "$(YELLOW)⚠️  Ollama not running$(NC)"; \
		fi; \
	else \
		echo "$(RED)❌ Environment file missing. Run 'make setup' first.$(NC)"; \
	fi

clean: ## Clean build artifacts and caches
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	# Backend cleanup
	find $(BACKEND_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find $(BACKEND_DIR) -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf $(BACKEND_DIR)/htmlcov $(BACKEND_DIR)/.coverage $(BACKEND_DIR)/.pytest_cache
	rm -f $(BACKEND_DIR)/test.db
	# Frontend cleanup
	rm -rf $(FRONTEND_DIR)/node_modules/.cache $(FRONTEND_DIR)/dist $(FRONTEND_DIR)/coverage
	# AI cleanup
	rm -rf $(AI_DIR)/cache $(AI_DIR)/temp
	# General cleanup
	find . -name "*.Zone.Identifier" -type f -delete 2>/dev/null || true
	find . -name ".DS_Store" -type f -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

# Development Commands
dev: ## Start all services in development mode
	@echo "$(BLUE)Starting $(PROJECT_NAME) in development mode...$(NC)"
	@echo "$(YELLOW)Backend will be available at: http://localhost:8000$(NC)"
	@echo "$(YELLOW)Frontend will be available at: http://localhost:3000$(NC)"
	@echo "$(YELLOW)API docs will be available at: http://localhost:8000/docs$(NC)"
	@echo ""
	@echo "$(YELLOW)Press Ctrl+C to stop all services$(NC)"
	@trap 'echo "$(RED)Stopping services...$(NC)"; kill 0' INT; \
	(cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000) & \
	(cd $(FRONTEND_DIR) && yarn dev --host 0.0.0.0 --port 3000) & \
	wait

dev-backend: ## Start only the backend service
	@echo "$(BLUE)Starting backend service...$(NC)"
	@echo "$(YELLOW)Backend API: http://localhost:8000$(NC)"
	@echo "$(YELLOW)API docs: http://localhost:8000/docs$(NC)"
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend: ## Start only the frontend service
	@echo "$(BLUE)Starting frontend service...$(NC)"
	@echo "$(YELLOW)Frontend: http://localhost:3000$(NC)"
	cd $(FRONTEND_DIR) && yarn dev --host 0.0.0.0 --port 3000

stop: ## Stop all running services
	@echo "$(BLUE)Stopping all services...$(NC)"
	-pkill -f "uvicorn app.main:app"
	-pkill -f "yarn dev"
	-pkill -f "vite"
	@echo "$(GREEN)✅ All services stopped$(NC)"

restart: stop dev ## Restart all services

status: ## Check project status
	@echo "$(BLUE)$(PROJECT_NAME) Status$(NC)"
	@echo ""
	@echo "$(YELLOW)System Requirements:$(NC)"
	@python3 --version 2>/dev/null && echo "$(GREEN)✅ Python 3 available$(NC)" || echo "$(RED)❌ Python 3 not found$(NC)"
	@node --version 2>/dev/null && echo "$(GREEN)✅ Node.js available$(NC)" || echo "$(RED)❌ Node.js not found$(NC)"
	@yarn --version 2>/dev/null && echo "$(GREEN)✅ Yarn available$(NC)" || echo "$(RED)❌ Yarn not found$(NC)"
	@echo ""
	@echo "$(YELLOW)Project Structure:$(NC)"
	@[ -d "$(BACKEND_DIR)" ] && echo "$(GREEN)✅ Backend directory$(NC)" || echo "$(RED)❌ Backend directory missing$(NC)"
	@[ -d "$(FRONTEND_DIR)" ] && echo "$(GREEN)✅ Frontend directory$(NC)" || echo "$(RED)❌ Frontend directory missing$(NC)"
	@[ -d "$(AI_DIR)" ] && echo "$(GREEN)✅ AI directory$(NC)" || echo "$(RED)❌ AI directory missing$(NC)"
	@echo ""
	@echo "$(YELLOW)Dependencies:$(NC)"
	@[ -d "$(BACKEND_DIR)/$(VENV_NAME)" ] && echo "$(GREEN)✅ Python virtual environment$(NC)" || echo "$(RED)❌ Python virtual environment missing$(NC)"
	@[ -d "$(FRONTEND_DIR)/node_modules" ] && echo "$(GREEN)✅ Node.js dependencies$(NC)" || echo "$(RED)❌ Node.js dependencies missing$(NC)"
	@echo ""
	@echo "$(YELLOW)AI Providers:$(NC)"
	@[ -f ".env" ] && echo "$(GREEN)✅ Environment configuration$(NC)" || echo "$(RED)❌ Environment configuration missing$(NC)"
	@curl -s http://localhost:11434/api/tags >/dev/null && echo "$(GREEN)✅ Ollama available$(NC)" || echo "$(YELLOW)⚠️  Ollama not running$(NC)"

# Testing Commands
test: ## Run all tests
	@echo "$(BLUE)Running all tests...$(NC)"
	@$(MAKE) test-backend
	@$(MAKE) test-frontend
	@$(MAKE) test-ai

test-backend: ## Run backend tests
	@echo "$(BLUE)Running backend tests...$(NC)"
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && python -m pytest tests/ -v

test-frontend: ## Run frontend tests
	@echo "$(BLUE)Running frontend tests...$(NC)"
	cd $(FRONTEND_DIR) && npx vitest run

test-ai: ## Run AI module tests
	@echo "$(BLUE)Running AI module tests...$(NC)"
	cd $(AI_DIR) && . ../$(BACKEND_DIR)/$(VENV_NAME)/bin/activate && python -m pytest tests/ -v

coverage: ## Generate test coverage reports
	@echo "$(BLUE)Generating coverage reports...$(NC)"
	# Backend coverage
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && python -m pytest --cov=app --cov-report=html --cov-report=term-missing
	# Frontend coverage
	cd $(FRONTEND_DIR) && yarn test --coverage --run
	@echo "$(GREEN)✅ Coverage reports generated$(NC)"
	@echo "$(YELLOW)Backend coverage: $(BACKEND_DIR)/htmlcov/index.html$(NC)"
	@echo "$(YELLOW)Frontend coverage: $(FRONTEND_DIR)/coverage/index.html$(NC)"

# Code Quality Commands
lint: ## Run code linting
	@echo "$(BLUE)Running code linting...$(NC)"
	# Backend linting
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && flake8 app/ tests/ || true
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && mypy app/ || true
	# Frontend linting
	cd $(FRONTEND_DIR) && yarn lint || true
	@echo "$(GREEN)✅ Linting complete$(NC)"

format: ## Format code
	@echo "$(BLUE)Formatting code...$(NC)"
	# Backend formatting
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && black app/ tests/ || true
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && isort app/ tests/ || true
	# Frontend formatting
	cd $(FRONTEND_DIR) && yarn format || true
	@echo "$(GREEN)✅ Code formatting complete$(NC)"

# Build Commands
build: ## Build the application for production
	@echo "$(BLUE)Building $(PROJECT_NAME) for production...$(NC)"
	# Build frontend
	cd $(FRONTEND_DIR) && yarn build
	# Prepare backend
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && pip freeze > requirements-freeze.txt
	@echo "$(GREEN)✅ Build complete$(NC)"

build-frontend: ## Build frontend only
	@echo "$(BLUE)Building frontend...$(NC)"
	cd $(FRONTEND_DIR) && yarn build
	@echo "$(GREEN)✅ Frontend build complete$(NC)"

# Docker Commands
docker-build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	docker-compose build
	@echo "$(GREEN)✅ Docker images built$(NC)"

docker-up: ## Start services with Docker
	@echo "$(BLUE)Starting services with Docker...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Services started$(NC)"
	@echo "$(YELLOW)Frontend: http://localhost:3000$(NC)"
	@echo "$(YELLOW)Backend: http://localhost:8000$(NC)"

docker-down: ## Stop Docker services
	@echo "$(BLUE)Stopping Docker services...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Docker services stopped$(NC)"

# Database Commands
db-migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && alembic upgrade head
	@echo "$(GREEN)✅ Database migrations complete$(NC)"

db-reset: ## Reset database
	@echo "$(BLUE)Resetting database...$(NC)"
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && alembic downgrade base
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && alembic upgrade head
	@echo "$(GREEN)✅ Database reset complete$(NC)"

# Deployment Commands
deploy-local: build ## Deploy locally
	@echo "$(BLUE)Deploying locally...$(NC)"
	@$(MAKE) stop
	@$(MAKE) dev
	@echo "$(GREEN)✅ Local deployment complete$(NC)"

deploy-production: ## Deploy to production (placeholder)
	@echo "$(YELLOW)⚠️  Production deployment not yet implemented$(NC)"
	@echo "$(YELLOW)This will be implemented in future versions$(NC)"

# Utility Commands
logs: ## View application logs
	@echo "$(BLUE)Viewing application logs...$(NC)"
	@echo "$(YELLOW)Backend logs:$(NC)"
	@tail -f $(BACKEND_DIR)/logs/*.log 2>/dev/null || echo "No backend logs found"
	@echo "$(YELLOW)Frontend logs: Check browser console$(NC)"

update: ## Update dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	# Update backend dependencies
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && pip install --upgrade pip
	cd $(BACKEND_DIR) && . $(VENV_NAME)/bin/activate && pip list --outdated
	# Update frontend dependencies
	cd $(FRONTEND_DIR) && yarn upgrade
	@echo "$(GREEN)✅ Dependencies updated$(NC)"
	@echo "$(YELLOW)⚠️  Please test thoroughly after updates$(NC)"

backup: ## Create project backup
	@echo "$(BLUE)Creating project backup...$(NC)"
	@BACKUP_NAME="llb-backup-$(shell date +%Y%m%d-%H%M%S).tar.gz"; \
	tar --exclude='node_modules' --exclude='$(VENV_NAME)' --exclude='*.pyc' --exclude='__pycache__' \
		--exclude='.git' --exclude='htmlcov' --exclude='coverage' --exclude='dist' \
		--exclude='ai/cache' --exclude='ai/temp' \
		-czf "../$$BACKUP_NAME" .; \
	echo "$(GREEN)✅ Backup created: ../$$BACKUP_NAME$(NC)"