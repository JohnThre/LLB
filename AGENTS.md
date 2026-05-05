# Repository Guidelines

## Project Structure & Module Organization

LLB is a full-stack app with a Python/FastAPI backend, React frontend, and AI helper code. Backend code lives in `backend/app/`: API routes in `api/`, services in `services/`, schemas in `schemas/`, and database utilities in `db/`. Backend tests are in `backend/tests/`. Frontend code lives in `frontend/src/`, with components, pages, Redux slices, hooks, and Vitest tests in `components/`, `pages/`, `store/`, `hooks/`, and `test/` or adjacent `*.test.tsx` files. AI helpers are in `ai/`; docs are in `docs/`; scripts are in `scripts/`.

## Build, Test, and Development Commands

- `make dev`: starts backend on port `8000` and Vite frontend on port `3000`.
- `make test`: runs the full suite through `scripts/run_tests.sh`.
- `make test-backend`: runs `pytest` with coverage for `backend/app`.
- `make test-frontend`: runs Vitest once for frontend tests.
- `make test-coverage`: writes reports to `backend/htmlcov/` and `frontend/coverage/`.
- `make build`: builds the frontend and freezes backend Python dependencies.
- `docker compose -f docker-compose.dev.yml up --build`: runs the development stack in containers.

## Coding Style & Naming Conventions

Python code should follow PEP 8, use type hints for public functions, and include Google-style docstrings for public APIs. Keep backend modules grouped by responsibility: endpoints, services, schemas, core utilities, and CRUD/data access. TypeScript uses React functional components, hooks, MUI, Redux Toolkit, and Prettier via `cd frontend && npm run format`. Name components in `PascalCase`, hooks as `useSomething`, Redux slices as `somethingSlice.ts`, and tests as `*.test.ts` or `*.test.tsx`.

## Testing Guidelines

Backend tests use Pytest; `backend/pytest.ini` enforces `test_*.py` or `*_test.py` files, `Test*` classes, and `test_*` functions, while reporting coverage for `backend/app`. Frontend tests use Vitest with React Testing Library. Add tests for new services, endpoints, components, hooks, and Redux state changes. Prefer focused unit tests and API/workflow integration tests.

## Commit & Pull Request Guidelines

Use conventional commit prefixes already present in history, such as `feat:`, `fix:`, and `docs:`. Keep commits focused and imperative, for example `fix: improve service dependency injection`. Pull requests should describe the change, list verification commands, link issues, and include screenshots for UI changes. Update `README.md`, `docs/`, or API docs when behavior or setup changes.

## Security & Configuration Tips

Copy `.env.example` to `.env` for local setup, but never commit real secrets, API keys, JWT secrets, model credentials, or private user data. Validate and sanitize user input in backend endpoints and services, especially file, document, audio, and AI-processing paths.
