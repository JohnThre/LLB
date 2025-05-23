# LLB (爱学伴) - Local AI-Driven Sexual Health Education
# Makefile for development, testing, and deployment

.PHONY: help setup clean test dev build deploy

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

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
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(setup|install|clean)"
	@echo ""
	@echo "$(GREEN)Development Commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(dev|start|stop|restart)"
	@echo ""
	@echo "$(GREEN)Testing Commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(test|coverage)"
	@echo ""
	@echo "$(GREEN)Build & Deploy Commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -E "(build|deploy|docker)"
	@echo ""
	@echo "$(GREEN)Utility Commands:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST) | grep -vE "(setup|install|clean|dev|start|stop|restart|test|coverage|build|deploy|docker)"

# Setup Commands
setup: ## Run the complete project setup
	@echo "$(BLUE)Setting up $(PROJECT_NAME)...$(NC)"
	chmod +x scripts/setup/setup_project.sh
	./scripts/setup/setup_project.sh

install-deps: ## Install all dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@echo "$(YELLOW)Installing backend dependencies...$(NC)"
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && pip install -r requirements.txt
	@echo "$(YELLOW)Installing frontend dependencies...$(NC)"
	cd $(FRONTEND_DIR) && yarn install

verify-model: ## Verify AI model installation
	@echo "$(BLUE)Verifying AI model...$(NC)"
	@if [ -d "$(AI_DIR)/models/gemma3-keras-gemma3_1b-v3" ]; then \
		echo "$(GREEN)✅ Gemma model found$(NC)"; \
		python3 -c "import os; model_path='$(AI_DIR)/models/gemma3-keras-gemma3_1b-v3'; required=['config.json','model.weights.h5','tokenizer.json']; missing=[f for f in required if not os.path.exists(f'{model_path}/{f}')]; print('$(GREEN)✅ All required files present$(NC)' if not missing else '$(RED)❌ Missing files: ' + ', '.join(missing) + '$(NC)')"; \
	else \
		echo "$(RED)❌ Gemma model not found. Please download from Kaggle.$(NC)"; \
		echo "$(YELLOW)See docs/deployment/ai-model-setup.md for instructions$(NC)"; \
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
	(cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000) & \
	(cd $(FRONTEND_DIR) && yarn dev --host 0.0.0.0 --port 3000) & \
	wait

dev-backend: ## Start only the backend service
	@echo "$(BLUE)Starting backend service...$(NC)"
	@echo "$(YELLOW)Backend API: http://localhost:8000$(NC)"
	@echo "$(YELLOW)API docs: http://localhost:8000/docs$(NC)"
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

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
	@nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null && echo "$(GREEN)✅ NVIDIA GPU detected$(NC)" || echo "$(YELLOW)⚠️  No NVIDIA GPU detected (CPU mode)$(NC)"
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
	@echo "$(YELLOW)AI Models:$(NC)"
	@[ -d "$(AI_DIR)/models/gemma3-keras-gemma3_1b-v3" ] && echo "$(GREEN)✅ Gemma 3 1B model$(NC)" || echo "$(RED)❌ Gemma 3 1B model missing$(NC)"
	@[ -d "$(AI_DIR)/models/whisper" ] && echo "$(GREEN)✅ Whisper model directory$(NC)" || echo "$(YELLOW)⚠️  Whisper model directory (auto-created)$(NC)"

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

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && python -m pytest tests/unit/ -v -m unit
	cd $(FRONTEND_DIR) && yarn test --run src/**/*.test.tsx

test-integration: ## Run integration tests only
	@echo "$(BLUE)Running integration tests...$(NC)"
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && python -m pytest tests/integration/ -v -m integration

test-e2e: ## Run end-to-end tests
	@echo "$(BLUE)Running end-to-end tests...$(NC)"
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && python -m pytest tests/e2e/ -v -m e2e

test-performance: ## Run performance tests
	@echo "$(BLUE)Running performance tests...$(NC)"
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && python -m pytest tests/performance/ -v -m slow

coverage: ## Generate test coverage reports
	@echo "$(BLUE)Generating coverage reports...$(NC)"
	# Backend coverage
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && python -m pytest --cov=app --cov-report=html --cov-report=term-missing
	# Frontend coverage
	cd $(FRONTEND_DIR) && yarn test --coverage --run
	@echo "$(GREEN)✅ Coverage reports generated$(NC)"
	@echo "$(YELLOW)Backend coverage: $(BACKEND_DIR)/htmlcov/index.html$(NC)"
	@echo "$(YELLOW)Frontend coverage: $(FRONTEND_DIR)/coverage/index.html$(NC)"

# Code Quality Commands
lint: ## Run code linting
	@echo "$(BLUE)Running code linting...$(NC)"
	# Backend linting
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && flake8 app/ tests/
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && mypy app/
	# Frontend linting
	cd $(FRONTEND_DIR) && yarn lint
	@echo "$(GREEN)✅ Linting complete$(NC)"

format: ## Format code
	@echo "$(BLUE)Formatting code...$(NC)"
	# Backend formatting
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && black app/ tests/
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && isort app/ tests/
	# Frontend formatting
	cd $(FRONTEND_DIR) && yarn format
	@echo "$(GREEN)✅ Code formatting complete$(NC)"

# Build Commands
build: ## Build the application for production
	@echo "$(BLUE)Building $(PROJECT_NAME) for production...$(NC)"
	# Build frontend
	cd $(FRONTEND_DIR) && yarn build
	# Prepare backend
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && pip freeze > requirements-freeze.txt
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

docker-logs: ## View Docker logs
	docker-compose logs -f

# Database Commands
db-migrate: ## Run database migrations
	@echo "$(BLUE)Running database migrations...$(NC)"
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && alembic upgrade head
	@echo "$(GREEN)✅ Database migrations complete$(NC)"

db-reset: ## Reset database
	@echo "$(BLUE)Resetting database...$(NC)"
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && alembic downgrade base
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && alembic upgrade head
	@echo "$(GREEN)✅ Database reset complete$(NC)"

# AI Model Commands
download-models: ## Download AI models (manual step required)
	@echo "$(YELLOW)⚠️  AI models must be downloaded manually$(NC)"
	@echo "$(YELLOW)Please follow the instructions in docs/deployment/ai-model-setup.md$(NC)"
	@echo "$(YELLOW)1. Create Kaggle account$(NC)"
	@echo "$(YELLOW)2. Download Gemma 3 1B model$(NC)"
	@echo "$(YELLOW)3. Extract to ai/models/gemma3-keras-gemma3_1b-v3/$(NC)"

benchmark-ai: ## Run AI performance benchmarks
	@echo "$(BLUE)Running AI performance benchmarks...$(NC)"
	cd $(AI_DIR) && source ../$(BACKEND_DIR)/$(VENV_NAME)/bin/activate && python scripts/benchmark_ai.py
	@echo "$(GREEN)✅ AI benchmarks complete$(NC)"

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

monitor: ## Monitor system resources
	@echo "$(BLUE)Monitoring system resources...$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to stop monitoring$(NC)"
	@while true; do \
		clear; \
		echo "$(BLUE)System Monitor - $(shell date)$(NC)"; \
		echo ""; \
		echo "$(YELLOW)Memory Usage:$(NC)"; \
		free -h; \
		echo ""; \
		echo "$(YELLOW)CPU Usage:$(NC)"; \
		top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $$1"%"}'; \
		echo ""; \
		echo "$(YELLOW)GPU Usage:$(NC)"; \
		nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits 2>/dev/null || echo "No NVIDIA GPU detected"; \
		echo ""; \
		echo "$(YELLOW)Disk Usage:$(NC)"; \
		df -h | grep -E "/$|/home"; \
		sleep 5; \
	done

update: ## Update dependencies
	@echo "$(BLUE)Updating dependencies...$(NC)"
	# Update backend dependencies
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && pip install --upgrade pip
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && pip list --outdated
	# Update frontend dependencies
	cd $(FRONTEND_DIR) && yarn upgrade
	@echo "$(GREEN)✅ Dependencies updated$(NC)"
	@echo "$(YELLOW)⚠️  Please test thoroughly after updates$(NC)"

backup: ## Create project backup
	@echo "$(BLUE)Creating project backup...$(NC)"
	@BACKUP_NAME="llb-backup-$(shell date +%Y%m%d-%H%M%S).tar.gz"; \
	tar --exclude='node_modules' --exclude='$(VENV_NAME)' --exclude='*.pyc' --exclude='__pycache__' \
		--exclude='.git' --exclude='htmlcov' --exclude='coverage' --exclude='dist' \
		--exclude='ai/models' --exclude='ai/cache' --exclude='ai/temp' \
		-czf "../$$BACKUP_NAME" .; \
	echo "$(GREEN)✅ Backup created: ../$$BACKUP_NAME$(NC)"

docs: ## Generate documentation
	@echo "$(BLUE)Generating documentation...$(NC)"
	# Backend API docs (auto-generated by FastAPI)
	@echo "$(YELLOW)Backend API docs available at: http://localhost:8000/docs$(NC)"
	# Frontend docs (if using Storybook or similar)
	@echo "$(YELLOW)Frontend docs: See README.md$(NC)"
	@echo "$(GREEN)✅ Documentation ready$(NC)"

# Development helpers
shell-backend: ## Open backend shell
	@echo "$(BLUE)Opening backend shell...$(NC)"
	cd $(BACKEND_DIR) && source $(VENV_NAME)/bin/activate && python

shell-frontend: ## Open frontend shell
	@echo "$(BLUE)Opening frontend shell...$(NC)"
	cd $(FRONTEND_DIR) && yarn

install-hooks: ## Install Git hooks
	@echo "$(BLUE)Installing Git hooks...$(NC)"
	@if [ -d ".git" ]; then \
		cp scripts/hooks/pre-commit .git/hooks/pre-commit; \
		chmod +x .git/hooks/pre-commit; \
		echo "$(GREEN)✅ Git hooks installed$(NC)"; \
	else \
		echo "$(RED)❌ Not a Git repository$(NC)"; \
	fi 