# LLB - Ai Xue Ban

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

LLB is a privacy-first sexual health education app with a FastAPI backend, React frontend, Electron desktop shell, and configurable AI providers. It answers in English and Simplified Chinese, grounds chat responses in approved literature, and can run with local or bring-your-own-key provider credentials.

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ and Redis 7+ for the full stack
- SQLite/in-memory fallbacks are used by parts of the development setup

### Local Development

```bash
git clone git@github.com:JohnThre/LLB.git
cd LLB
cp .env.example .env
make dev
```

Development access points:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/api/v1/health`

If dependencies need to be installed manually:

```bash
cd backend
python3.11 -m venv llb-env
source llb-env/bin/activate
pip install -r requirements.txt

cd ../frontend
npm install
```

Apple Silicon users can run the backend Whisper setup helper when local audio features are needed:

```bash
cd backend
./setup_whisper.sh
```

## Features

- Source-backed chat answers with reviewable literature citations.
- English and Simplified Chinese chat support.
- Configurable provider order across Ollama/local, GitHub Models, OpenAI, Anthropic, Google Gemini, and Mistral.
- Voice transcription, text-to-speech, and streaming audio endpoints.
- Document upload and processing support.
- Knowledge update and scheduler APIs.
- JWT authentication, user profile/settings endpoints, and role-gated literature management.
- Electron desktop package that starts a local backend and stores BYOK provider credentials through the desktop shell.

## Commands

```bash
make dev             # Start backend on 8000 and Vite on 3000
make test            # Run the full test script
make test-backend    # Run backend pytest coverage
make test-frontend   # Run Vitest once
make test-desktop    # Run Electron helper and release-signing tests
make test-coverage   # Generate backend and frontend coverage reports
make build           # Build frontend and freeze backend requirements
make clean           # Remove local build/test artifacts
```

Docker development stack:

```bash
docker compose -f docker-compose.dev.yml up --build
```

Production-style stack:

```bash
docker compose up -d
```

## Project Layout

```text
backend/app/       FastAPI application, routes, schemas, services, database utilities
backend/tests/     Pytest suite
frontend/src/      React app, pages, components, hooks, services, Redux store, tests
desktop/           Electron shell, preload bridge, backend process bootstrap, installer config
ai/                AI helper configuration and local model support
docs/              Architecture, API, deployment, desktop, and project status docs
scripts/           Setup, test, build, deployment, and release helper scripts
```

## Configuration

Copy `.env.example` to `.env` before local development. Never commit real credentials.

Common provider variables:

```bash
AI_PROVIDER_ORDER=ollama,github,openai,anthropic,gemini,mistral
GITHUB_MODELS_TOKEN=github_pat_with_models_read
GITHUB_MODELS_MODELS=openai/gpt-5.2
GITHUB_MODELS_API_VERSION=2026-03-10
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5.2
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-opus-4-7
GOOGLE_API_KEY=...
GOOGLE_MODEL=gemini-3-pro-preview
MISTRAL_API_KEY=...
MISTRAL_MODEL=mistral-medium-3.5
OLLAMA_ENABLED=false
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

The default provider order is free-first: Ollama/local, GitHub Models, then direct paid API providers. GitHub Models requires a token with `models:read` access and is intended for rate-limited prototyping.

## Desktop Packaging

The Electron app in `desktop/` loads the React frontend and starts the FastAPI backend as a loopback-only local process. Desktop provider keys are sent through Electron IPC and the protected desktop-control endpoint, then stored in process memory for provider calls.

Release artifacts are produced by the tag-triggered `Desktop Installers` workflow. Final installer artifacts should be signed with detached GPG signatures:

```bash
scripts/sign_release_artifacts.sh desktop/dist
```

macOS release builds also require Apple Developer ID signing and notarization credentials supplied outside the repository.

## Documentation

- [Documentation Index](docs/README.md)
- [Architecture](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Deployment](docs/DEPLOYMENT.md)
- [Desktop AI Provider Design](docs/electron-desktop-ai-providers-design.md)
- [Project Status](docs/PROJECT_STATUS.md)
- [Contributing](CONTRIBUTING.md)

## Testing

Backend tests use Pytest and report coverage for `backend/app`. Frontend tests use Vitest with React Testing Library. Desktop tests use Node's built-in test runner plus a shell test for release signing behavior.

```bash
make test-backend
make test-frontend
make test-desktop
```

Coverage reports are written to:

- Backend: `backend/htmlcov/index.html`
- Frontend: `frontend/coverage/index.html`

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE).

---

Last updated: 2026-05-16
Version: 0.1.0
