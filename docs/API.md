# LLB API Reference

Last updated: 2026-05-16

## Base URLs

- Web backend development: `http://localhost:8000`
- Versioned API prefix: `http://localhost:8000/api/v1`
- Legacy AI prefix: `http://localhost:8000/api/ai`
- File prefix: `http://localhost:8000/api/files`
- Interactive docs: `http://localhost:8000/docs` and `http://localhost:8000/redoc`

Protected endpoints require:

```http
Authorization: Bearer <jwt_token>
```

Desktop-control endpoints additionally require:

```http
x-llb-desktop-token: <per-launch-token>
```

## Health

```http
GET /health
GET /api/v1/health
GET /api/v1/health/ai
GET /api/v1/health/audio
GET /api/v1/health/documents
```

`/health` redirects to `/api/v1/health` in the full backend. The desktop backend returns a compact local health payload at `/health` and `/api/v1/health`.

## Authentication

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
```

Register creates a user account. Login returns a bearer token for protected routes.

## Users

```http
GET    /api/v1/users/me
PUT    /api/v1/users/me
GET    /api/v1/users/{user_id}
GET    /api/v1/users/
POST   /api/v1/users/me/change-password
DELETE /api/v1/users/me
GET    /api/v1/users/me/preferences
PUT    /api/v1/users/me/preferences
GET    /api/v1/users/me/settings
PUT    /api/v1/users/me/settings
```

These endpoints are protected and cover profile, account, preferences, and settings operations.

## Source-Backed Chat

```http
POST /api/v1/chat
GET  /api/v1/chat/languages
GET  /api/v1/chat/status
```

Chat accepts English and Simplified Chinese. Unsupported languages return a refusal response. Questions without approved, reviewable literature also return a refusal response.

Example request:

```json
{
  "message": "What are reliable contraception options?",
  "language": "en",
  "context": {}
}
```

Example response shape:

```json
{
  "response": "Educational answer text",
  "language": "en",
  "language_detected": "en",
  "confidence": 0.85,
  "safety_score": 0.95,
  "status": "answered",
  "citations": [
    {
      "id": "source-id",
      "title": "Source title",
      "publisher": "Publisher",
      "language": "en",
      "source_type": "official",
      "url": "https://example.org",
      "excerpt": "Relevant source excerpt"
    }
  ],
  "refusal_reason": null,
  "processing_time": null
}
```

## AI

```http
GET  /api/v1/ai/providers
POST /api/v1/ai/generate
POST /api/v1/ai/chat
POST /api/v1/ai/detect-language
POST /api/v1/ai/summarize
POST /api/v1/ai/analyze-sentiment
POST /api/v1/ai/classify
POST /api/v1/ai/extract-entities
```

`GET /api/v1/ai/providers` returns public provider/model metadata. The utility endpoints are protected and call the configured AI model layer.

Legacy AI routes are still registered under `/api/ai`:

```http
GET  /api/ai/model/status
GET  /api/ai/model/settings
POST /api/ai/model/settings
POST /api/ai/generate
POST /api/ai/chat
POST /api/ai/detect-language
POST /api/ai/transcribe
POST /api/ai/text-to-speech
GET  /api/ai/voices
POST /api/ai/process-document
```

## Literature

```http
GET  /api/v1/literature/sources
POST /api/v1/literature/sources
POST /api/v1/literature/sources/{source_id}/approve
POST /api/v1/literature/sources/{source_id}/archive
```

Listing sources is public. Creating, approving, and archiving sources require an authenticated admin or moderator.

Supported source languages are `en` and `zh-CN`. Supported source types are `official` and `peer_reviewed`.

## Knowledge

```http
GET  /api/v1/knowledge/entries
POST /api/v1/knowledge/update
GET  /api/v1/knowledge/updates
GET  /api/v1/knowledge/scheduler/status
POST /api/v1/knowledge/scheduler/start
POST /api/v1/knowledge/scheduler/stop
GET  /api/v1/knowledge/categories
GET  /api/v1/knowledge/languages
```

Knowledge entries can be filtered by category and language. Manual updates and scheduler controls call the backend scheduler service.

## Audio Streaming

```http
POST      /api/v1/audio-streaming/sessions
GET       /api/v1/audio-streaming/sessions
GET       /api/v1/audio-streaming/sessions/{session_id}/stats
DELETE    /api/v1/audio-streaming/sessions/{session_id}
WebSocket /api/v1/audio-streaming/ws/{session_id}
```

The WebSocket accepts structured messages for audio chunks, text requests, and controls. It returns connection, transcription, and audio-response messages from the streaming service.

## Voice and Documents

The full backend registers additional voice and document routers in `backend/app/main.py`:

```http
POST /api/v1/voice/transcribe
POST /api/v1/voice/synthesize
POST /api/v1/documents/upload
POST /api/v1/documents/analyze
GET  /api/v1/documents/knowledge
```

These routes are intended for speech and document workflows backed by the audio and document services.

## Files

```http
POST   /api/files/upload
GET    /api/files/{file_type}/{filename}
DELETE /api/files/{file_type}/{filename}
```

The file API stores and retrieves uploaded files by supported file type.

## Desktop Backend

The packaged Electron app uses `backend/app/desktop_main.py`, a lean FastAPI app that avoids loading the full local ML stack.

```http
GET  /health
GET  /api/v1/health
GET  /api/v1/ai/providers
POST /api/v1/chat
GET  /api/v1/chat/languages
GET  /api/v1/chat/status
POST /api/v1/desktop/provider-credentials
GET  /api/v1/literature/sources
POST /api/v1/literature/sources
POST /api/v1/literature/sources/{source_id}/approve
POST /api/v1/literature/sources/{source_id}/archive
```

`POST /api/v1/desktop/provider-credentials` is protected by `x-llb-desktop-token` and returns masked provider status only.

## Error Responses

FastAPI validation errors use the standard FastAPI error shape. Application routes may also return:

```json
{
  "detail": "Human readable error message"
}
```

Custom application exception handlers can return:

```json
{
  "error": "Application error message",
  "details": {}
}
```
