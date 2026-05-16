# Electron Desktop And AI Providers Design

## Summary

LLB will ship as a local desktop app for macOS, Windows, and GNU/Linux. Electron will provide the desktop shell, load the existing React frontend, and start the existing FastAPI backend as an internal child process. Users will not need to start a separate server.

The app will remain bring-your-own-key for external AI services. User API keys will be stored by the Electron main process using OS-backed credential storage where available, rehydrated into the local backend as in-memory credentials at app startup, and never committed to `.env`, source code, release artifacts, logs, or frontend local storage.

## Goals

- Package LLB for installable desktop use on macOS, Windows, and GNU/Linux.
- Keep the current FastAPI backend, React frontend, AI prompt layer, literature workflow, audio, and document processing paths.
- Start and stop the backend automatically from Electron.
- Support current major AI providers and model families through configurable model IDs.
- Require users to provide their own external provider API keys.
- Sign final release artifacts with the default GPG key.
- Use Apple Developer ID signing and notarization for macOS releases.

## Non-Goals

- BSD packaging is explicitly out of scope.
- Rewriting the Python backend into Node/Electron is out of scope.
- Shipping production traffic through project-owned external API keys is out of scope.
- Building a hosted web deployment replacement is out of scope.
- Native Windows Authenticode signing is not required unless a Windows code-signing certificate is provided later.

## Current Context

The active app path is `backend/app/main.py`, which mounts API v1 routes and legacy AI routes. AI generation currently flows through `backend/app/services/ai_service.py` into `backend/services/model_service.py` and `backend/services/ai_providers.py`. Provider fallback already supports Ollama, GitHub Models, OpenAI, Anthropic, and Gemini through environment variables, but several model defaults are stale and credentials are process-level rather than user-managed.

The frontend is a Vite React app in `frontend/`, with API calls routed through `frontend/src/config.ts`. The current development workflow starts the backend on port `8000` and Vite on port `3000`.

## Architecture

Electron will be added as a focused `desktop/` package. The Electron main process owns lifecycle, local service bootstrap, secret storage, and native release integration.

At runtime:

1. Electron resolves an available loopback port.
2. Electron generates a random per-launch local control token.
3. Electron starts the packaged backend executable with environment variables for the selected port, app data directory, and control token.
4. Electron waits for the backend health endpoint to return ready.
5. Electron loads the built React frontend from disk.
6. The renderer uses a runtime-provided API base URL instead of assuming `http://localhost:8000`.
7. On quit, Electron terminates the backend child process.

The backend remains a local HTTP API because this minimizes changes to the existing FastAPI service and frontend API code. The local API must bind to `127.0.0.1` only, require the per-launch token for sensitive desktop-only provider credential endpoints, and avoid exposing provider keys in status responses.

## Desktop Packaging

Use `electron-builder` for release artifacts because it has a mature target matrix for DMG/PKG, NSIS/MSI-style Windows installers, AppImage, deb, and rpm, and supports adding bundled backend resources.

Build outputs:

- macOS: `.dmg`; `.pkg` can be added after the DMG release path is working
- Windows: NSIS `.exe`; MSI is a future enhancement
- GNU/Linux: AppImage, `.deb`, and `.rpm`

The Python backend will be packaged per target OS as a backend executable using PyInstaller first because it is the most direct fit for a FastAPI app with existing Python dependencies. Heavy local model assets must not be embedded blindly into every installer. The desktop app stores local model data under the OS app data directory and allows external providers or Ollama to work without large bundled model weights.

## Signing And Release Artifacts

All final artifacts must receive detached GPG signatures with the default GPG key:

```bash
gpg --batch --yes --armor --detach-sign <artifact>
```

Release automation should also produce checksums:

```bash
shasum -a 256 <artifact> > <artifact>.sha256
gpg --batch --yes --armor --detach-sign <artifact>.sha256
```

macOS releases will additionally use Apple Developer ID signing and notarization. The release pipeline must support Apple credentials through CI secrets or local environment variables, not checked-in files. The minimum acceptable macOS release artifact is a notarized, stapled DMG plus its `.asc` and `.sha256` files.

Windows and Linux artifacts will receive GPG detached signatures. Windows Authenticode should be treated as an optional future enhancement unless a Windows certificate is supplied.

## AI Provider Model

Provider support will move from hardcoded environment defaults toward a provider registry. The registry defines provider metadata, default model IDs, API base URLs, request builders, response parsers, and credential requirements. Model IDs remain editable so users can select provider-specific latest aliases or pinned snapshots without code changes.

Initial provider set:

- OpenAI
- Anthropic Claude
- Google Gemini
- Mistral
- GitHub Models
- Ollama/local

Verified current defaults as of 2026-05-07:

- OpenAI: `gpt-5.2` as the flagship default, with `gpt-5-mini` or `gpt-5-nano` for lower-cost workloads.
- Anthropic: Claude Opus 4.7 for complex tasks, Claude Sonnet 4.6 for speed/intelligence balance, Claude Haiku 4.5 for fastest low-cost use.
- Google Gemini: `gemini-3-pro-preview` and `gemini-3-flash-preview` are current Gemini 3 preview choices; `gemini-2.5-pro` remains a stable production option.
- Mistral: Mistral Medium 3.5, Mistral Small 4, and Mistral Large 3 are current prominent choices.
- GitHub Models: keep model IDs configurable because the catalog changes and may proxy models from multiple providers.
- Ollama/local: keep `OLLAMA_MODEL` configurable and do not assume a model is installed until `/api/tags` confirms local availability.

The registry must not imply that every model is available to every user. Provider status should distinguish configured, credential-present, reachable, and active model states.

## BYOK Secret Handling

The frontend must never directly store provider keys in browser local storage. Provider key forms will send key material through Electron IPC to the main process. The main process stores keys using Electron `safeStorage` and an encrypted JSON file in `app.getPath("userData")`. If OS-backed encryption is unavailable on a Linux desktop, the app should offer session-only keys and explain that persistent key storage needs a working Secret Service or equivalent keyring.

Backend credential flow:

1. Electron decrypts saved keys in the main process.
2. Electron sends provider credentials to a local backend desktop-control endpoint after startup.
3. The backend keeps keys in memory only.
4. Provider calls read credentials from the in-memory desktop credential resolver.
5. Status endpoints report provider names and masked key presence only.

This keeps external keys user-owned and local while avoiding project-owned keys in environment files or release builds.

## Frontend Changes

The React app will need a desktop-aware API base URL. In web development it can keep using `VITE_API_URL` or the current default. In Electron, a preload script will expose a safe read-only runtime config containing the local backend URL.

Settings UI will add an AI provider section:

- Provider selector.
- Model selector or editable model ID field.
- API key entry with save, replace, remove, and test connection actions.
- Provider status indicators that do not reveal secret values.
- Ollama base URL and model settings for local use.

The settings UI should remain quiet and operational, matching the current app style. It should not become a landing page or marketing flow.

## Backend Changes

Backend work should be scoped to:

- Add provider registry structures and tests.
- Add Mistral provider support.
- Update stale defaults for existing providers.
- Add a desktop credential resolver that can override environment credentials in local packaged mode.
- Add local desktop-control endpoints protected by the per-launch token.
- Keep existing environment-variable configuration for server/developer deployments.
- Sanitize logs to ensure API keys, authorization headers, and desktop control tokens are never logged.

The current legacy split between `backend/app/services` and `backend/services` should not be broadly refactored as part of this feature. Touch the existing provider manager where it is currently used, and defer structural cleanup unless tests prove it is necessary.

## Error Handling

Electron should show a local startup error view if the backend fails to start, including a path to logs but not raw secret values. The backend should return clear provider errors for missing key, invalid key, unsupported model, rate limit, and provider unavailable. Provider fallback should skip only recoverable provider failures; authentication failures for an explicitly selected provider should be surfaced to the user.

## Testing

Backend tests:

- Provider registry defaults and model metadata.
- Mistral request/response handling with fake HTTP clients.
- Credential precedence: desktop in-memory credentials before environment variables.
- Secret masking in provider info.
- Desktop-control endpoint rejects missing or invalid launch token.

Frontend tests:

- Provider settings render supported provider choices.
- Saving a key calls the Electron bridge rather than local storage.
- Provider status masks key values.
- API base URL uses desktop runtime config when present.

Desktop tests:

- Main process starts the backend with a random port and token.
- Backend shutdown occurs on app quit.
- GPG signing script signs all artifacts in the release directory.

Manual release verification:

- macOS DMG is signed, notarized, stapled, and has `.asc` and `.sha256`.
- Windows installer is produced and has `.asc` and `.sha256`.
- Linux AppImage, deb, and rpm are produced and have `.asc` and `.sha256`.

## Documentation

Update README and deployment docs with:

- Desktop install instructions for macOS, Windows, and GNU/Linux.
- BYOK provider setup.
- Local-only runtime behavior.
- GPG signature verification examples.
- macOS notarization requirements for maintainers.

## References

- Electron overview: https://www.electronjs.org/docs/latest
- Electron distribution overview: https://www.electronjs.org/docs/latest/tutorial/distribution-overview
- Electron code signing: https://www.electronjs.org/docs/latest/tutorial/code-signing
- electron-builder macOS configuration: https://www.electron.build/mac.html
- electron-builder Linux configuration: https://www.electron.build/linux
- OpenAI models: https://developers.openai.com/api/docs/models
- Anthropic models overview: https://platform.claude.com/docs/en/about-claude/models/overview
- Google Gemini models: https://ai.google.dev/models/gemini
- Mistral models overview: https://docs.mistral.ai/models/overview
