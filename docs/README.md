# LLB Documentation

Last updated: 2026-05-16

This directory contains the maintained technical documentation for LLB. The README at the repository root is the entry point for setup and project orientation; these pages provide deeper implementation, deployment, and release context.

## Start Here

- [Architecture](ARCHITECTURE.md): System boundaries, runtime flows, security model, and Mermaid diagrams.
- [API Reference](API.md): Current REST and WebSocket routes exposed by the backend and desktop backend.
- [Deployment](DEPLOYMENT.md): Local, Docker, manual, and desktop release deployment notes.
- [Desktop AI Provider Design](electron-desktop-ai-providers-design.md): Electron packaging and BYOK provider credential design.
- [Project Status](PROJECT_STATUS.md): Current release status, completed work, active risks, and roadmap.
- [Documentation Summary](DOCUMENTATION_SUMMARY.md): Documentation ownership and maintenance checklist.

## Source of Truth

- Backend routes: `backend/app/api/v1/api.py`, `backend/app/main.py`, and `backend/app/desktop_main.py`.
- Frontend runtime configuration: `frontend/src/config.ts`.
- Desktop packaging: `desktop/electron-builder.yml` and `.github/workflows/desktop-installers.yml`.
- Release signing: `scripts/sign_release_artifacts.sh`.

## Maintenance Rules

- Update docs in the same change as behavior, configuration, API, or release-process changes.
- Keep diagrams in Mermaid unless a generated image is explicitly required.
- Prefer current repository paths and commands over aspirational or roadmap-only instructions.
- Do not document secrets, private keys, real tokens, or private user data.
