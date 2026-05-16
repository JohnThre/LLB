# Changelog

All notable changes to the LLB project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

No unreleased changes.

## [0.1.0] - 2026-05-16

### Added

- Electron desktop app scaffold with local backend process bootstrap.
- Lean desktop FastAPI backend for source-backed chat and external AI providers.
- Desktop BYOK provider credential flow protected by a per-launch control token.
- Provider catalog and fallback support for Ollama/local, GitHub Models, OpenAI, Anthropic, Google Gemini, and Mistral.
- Approved literature source workflow with listing, creation, approval, and archiving.
- Source-backed chat responses with citations and explicit refusal states.
- Desktop installer workflow for macOS DMG, Windows NSIS, and Linux AppImage/deb/rpm artifacts.
- Release artifact checksum and detached GPG signing helper.
- Updated documentation set with architecture, API, deployment, desktop, status, and documentation index pages.

### Changed

- Refreshed README setup, commands, configuration, desktop packaging, and documentation links.
- Updated API documentation to match current FastAPI route registration.
- Reorganized documentation around implemented behavior rather than stale roadmap entries.
- Clarified release process for draft GitHub releases and CI-built desktop artifacts.

### Security

- Documented secret-handling requirements for provider keys, desktop control tokens, release credentials, and environment files.
- Documented desktop credential masking and loopback-only local backend expectations.

## [0.0.9] - 2025-09-01

### Added

- AI-powered knowledge search and update system.
- Bauhaus design system implementation.
- Multi-language support for English and Chinese.
- Voice input processing with Whisper.
- Document analysis capabilities.
- Real-time chat foundations.

### Changed

- Migrated to FastAPI backend architecture.
- Implemented React 18 with TypeScript frontend.
- Added Redux Toolkit for state management.
- Integrated Material UI components.

### Security

- Implemented JWT-based authentication.
- Added content safety filtering.
- Established privacy-first local AI processing direction.

## [0.0.1] - 2025-08-15

### Added

- Initial project setup.
- Basic FastAPI backend structure.
- React frontend foundation.
- Docker configuration.
- Development environment setup.
- Core AI service integration.
