.PHONY: dev test build clean

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

clean:
	find . -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf backend/htmlcov frontend/dist frontend/coverage