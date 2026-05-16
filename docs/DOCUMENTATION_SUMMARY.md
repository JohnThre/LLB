# Documentation Summary

Last updated: 2026-05-16

## Documentation Set

```text
LLB/
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── docs/
    ├── README.md
    ├── ARCHITECTURE.md
    ├── API.md
    ├── DEPLOYMENT.md
    ├── PROJECT_STATUS.md
    ├── DOCUMENTATION_SUMMARY.md
    └── electron-desktop-ai-providers-design.md
```

## Audience Map

- New developers: start with `README.md`, then `docs/README.md`, `CONTRIBUTING.md`, and `docs/ARCHITECTURE.md`.
- Frontend and API consumers: use `docs/API.md` and live Swagger docs at `/docs`.
- Backend maintainers: use `docs/ARCHITECTURE.md`, `docs/API.md`, and route files under `backend/app/api/`.
- Desktop/release maintainers: use `docs/electron-desktop-ai-providers-design.md`, `docs/DEPLOYMENT.md`, `desktop/electron-builder.yml`, and `.github/workflows/desktop-installers.yml`.
- Project stakeholders: use `docs/PROJECT_STATUS.md` and `CHANGELOG.md`.

## Current Coverage

- Setup and local development: documented in `README.md` and `docs/DEPLOYMENT.md`.
- Architecture and diagrams: documented in `docs/ARCHITECTURE.md` with Mermaid diagrams.
- API surface: documented in `docs/API.md` from current route registrations.
- Desktop packaging and provider credentials: documented in `docs/electron-desktop-ai-providers-design.md`.
- Release flow: documented in `docs/DEPLOYMENT.md` and `CHANGELOG.md`.

## Maintenance Checklist

- Update route docs when `backend/app/api/v1/api.py`, `backend/app/main.py`, or `backend/app/desktop_main.py` changes.
- Update desktop docs when `desktop/src/`, `backend/app/desktop_main.py`, `backend/desktop_backend_entry.py`, or `desktop/electron-builder.yml` changes.
- Update release docs when `.github/workflows/desktop-installers.yml` or `scripts/sign_release_artifacts.sh` changes.
- Update diagrams when a component boundary, credential flow, provider flow, or deployment target changes.
- Keep examples free of real secrets and private user data.

## Documentation Quality Bar

- Commands should be copy-pasteable from the repository root unless stated otherwise.
- Dates should use ISO format.
- Docs should describe implemented behavior separately from roadmap items.
- Mermaid diagrams should be small enough to review in a pull request.
- Stale placeholder domains, organization names, and old review dates should be removed unless they are explicitly examples.
