.PHONY: dev test build clean build-arm64 dev-arm64

dev:
	@trap 'kill 0' INT; \
	(cd backend && . llb-env/bin/activate && python -m uvicorn app.main:app --reload --port 8000) & \
	(cd frontend && npm run dev --port 3000) & \
	wait

test:
	@echo "🧪 Running comprehensive test suite..."
	@./scripts/run_tests.sh

test-backend:
	@echo "🧪 Running backend tests..."
	cd backend && . llb-env/bin/activate && python -m pytest tests/ -v --cov=app

test-frontend:
	@echo "🧪 Running frontend tests..."
	cd frontend && npm test -- --run

test-watch:
	@echo "👀 Running tests in watch mode..."
	@trap 'kill 0' INT; \
	(cd backend && . llb-env/bin/activate && python -m pytest tests/ -v --cov=app -f) & \
	(cd frontend && npm test) & \
	wait

test-coverage:
	@echo "📊 Generating test coverage reports..."
	cd backend && . llb-env/bin/activate && python -m pytest tests/ --cov=app --cov-report=html:htmlcov
	cd frontend && npm test -- --run --coverage
	@echo "Coverage reports generated:"
	@echo "- Backend: backend/htmlcov/index.html"
	@echo "- Frontend: frontend/coverage/index.html"

build:
	cd frontend && npm run build
	cd backend && . llb-env/bin/activate && pip freeze > requirements-freeze.txt

build-arm64:
	docker buildx build --platform linux/arm64 -t llb-backend:arm64 ./backend
	docker buildx build --platform linux/arm64 -t llb-frontend:arm64 ./frontend

dev-arm64:
	DOCKER_DEFAULT_PLATFORM=linux/arm64 docker-compose -f docker-compose.dev.yml up --build

clean:
	find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf backend/htmlcov frontend/dist frontend/coverage backend/.pytest_cache frontend/node_modules/.cache
	@echo "🧹 Cleaned up build artifacts and cache files"