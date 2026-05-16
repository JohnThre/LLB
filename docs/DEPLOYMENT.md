# LLB Deployment Guide

Last updated: 2026-05-16

## Prerequisites

- Python 3.11+ for local backend development.
- Node.js 18+ for frontend development; CI also tests Node 20.
- Docker and Docker Compose for container deployments.
- PostgreSQL 15+ and Redis 7+ for the full production-style stack.
- GPG for signing release artifacts.

## Local Development

```bash
git clone git@github.com:JohnThre/LLB.git
cd LLB
cp .env.example .env
make dev
```

`make dev` starts:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`

Manual backend/frontend setup:

```bash
cd backend
python3.11 -m venv llb-env
source llb-env/bin/activate
pip install -r requirements.txt

cd ../frontend
npm install
npm run dev -- --port 3000
```

In a second shell:

```bash
cd backend
source llb-env/bin/activate
uvicorn app.main:app --reload --port 8000
```

## Docker Deployment

Development containers with hot reload:

```bash
docker compose -f docker-compose.dev.yml up --build
```

Development container access points:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8001`
- PostgreSQL: host port `5433`
- Redis: host port `6380`

Production-style containers:

```bash
docker compose up -d
docker compose ps
docker compose logs -f
```

Production-style container access points:

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- PostgreSQL: host port `5432`
- Redis: host port `6379`

## Environment

Copy `.env.example` to `.env` and provide deployment-specific values. Keep secrets in environment variables, CI secrets, or a secret manager; do not commit them.

Core variables:

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/llb_db
REDIS_URL=redis://localhost:6379
SECRET_KEY=replace-me
JWT_SECRET_KEY=replace-me
```

Provider variables:

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

GitHub Models requires a token with `models:read` access. Use production-grade paid or self-hosted providers when rate limits or data policy require it.

## Manual Production Build

```bash
cd frontend
npm ci
npm run build

cd ../backend
python3.11 -m venv llb-env
source llb-env/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For a real production host, place a TLS-terminating reverse proxy in front of the backend/frontend, set strict CORS origins, rotate secrets, and configure database backups.

## Desktop Releases

Desktop releases are built from tags by `.github/workflows/desktop-installers.yml`.

Workflow targets:

- macOS DMG on `macos-latest`.
- Windows NSIS installer on `windows-latest`.
- Linux AppImage, deb, and rpm on `ubuntu-latest`.

Release process:

1. Commit release-ready changes to `main`.
2. Push `main`.
3. Create and push an annotated tag such as `v0.1.0`.
4. Let the `Desktop Installers` workflow build artifacts.
5. Download workflow artifacts.
6. Sign artifacts and checksums:

   ```bash
   scripts/sign_release_artifacts.sh <artifact-directory>
   ```

7. Upload installers, `.sha256`, and `.asc` files to the draft GitHub release.

macOS public releases should also use Apple Developer ID signing and notarization credentials configured outside the repository.

## Health Checks

- Full backend: `GET /api/v1/health`
- AI health: `GET /api/v1/health/ai`
- Audio health: `GET /api/v1/health/audio`
- Document health: `GET /api/v1/health/documents`
- Desktop backend: `GET /api/v1/health`

## Verification

Run these before publishing deployment or release changes:

```bash
make test-backend
make test-frontend
make test-desktop
```

For release changes, also verify:

```bash
git diff --check
gh auth status
gh release view v0.1.0
```
