.PHONY: dev test build clean build-arm64 dev-arm64

dev:
	@trap 'kill 0' INT; \
	(cd backend && . llb-env/bin/activate && python -m uvicorn app.main:app --reload --port 8000) & \
	(cd frontend && npm run dev --port 3000) & \
	wait

test:
	cd backend && . llb-env/bin/activate && python -m pytest tests/ -v
	cd frontend && npm test

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
	rm -rf backend/htmlcov frontend/dist frontend/coverage