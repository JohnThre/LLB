"""Lean FastAPI application for the Electron desktop package.

This app intentionally avoids importing the full backend application because
the full app initializes local ML/audio services that make notarized desktop
installers very large.
"""

import re
from typing import Any, Dict, List, Literal, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.api.v1.endpoints import desktop, literature
from app.services.literature_service import LiteratureSource, literature_service
from services import ai_providers


class DesktopChatMessage(BaseModel):
    """Chat message payload used by the desktop app."""

    message: str = Field(..., min_length=1)
    language: Optional[str] = "en"
    context: Optional[Dict[str, Any]] = None
    cultural_context: Optional[str] = None


class DesktopChatResponse(BaseModel):
    """Chat response payload compatible with the existing frontend."""

    response: str
    language: str
    language_detected: str
    confidence: float
    safety_score: float
    status: Literal["answered", "refused"] = "answered"
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    refusal_reason: Optional[str] = None
    processing_time: Optional[float] = None


SUPPORTED_CHAT_LANGUAGES = {"en", "zh-CN"}


def _normalize_language(language: Optional[str]) -> Optional[str]:
    """Normalize UI locale codes to supported chat language codes."""
    if not language:
        return None
    if language.lower().startswith("en"):
        return "en"
    if language in {"zh", "zh-CN"} or language.lower().startswith("zh-cn"):
        return "zh-CN"
    return language


def _detect_supported_language(text: str, requested_language: Optional[str]) -> str:
    """Detect supported chat languages and preserve explicit supported choices."""
    requested_language = _normalize_language(requested_language)
    if requested_language in SUPPORTED_CHAT_LANGUAGES:
        return requested_language
    if re.search(r"[\u4e00-\u9fff]", text):
        return "zh-CN"
    return "en"


def _is_unsupported_language(text: str, requested_language: Optional[str]) -> bool:
    """Return true when the request is clearly outside supported languages."""
    requested_language = _normalize_language(requested_language)
    if requested_language and requested_language not in SUPPORTED_CHAT_LANGUAGES:
        return True
    if re.search(r"[\u4e00-\u9fff]", text):
        return False
    return bool(re.search(r"[¿¡áéíóúñüÁÉÍÓÚÑÜ]", text))


def _unsupported_language_response(
    requested_language: Optional[str],
) -> DesktopChatResponse:
    """Build the supported-language refusal response."""
    language = "zh-CN" if requested_language == "zh-CN" else "en"
    response = (
        "目前仅支持简体中文和英语。请使用其中一种语言重新提问。"
        if language == "zh-CN"
        else (
            "Only English and Simplified Chinese are supported. "
            "Please ask your question again in one of those languages."
        )
    )
    return DesktopChatResponse(
        response=response,
        language=language,
        language_detected=requested_language or "unsupported",
        confidence=0.0,
        safety_score=1.0,
        status="refused",
        citations=[],
        refusal_reason="unsupported_language",
    )


def _no_source_response(language: str, detected_language: str) -> DesktopChatResponse:
    """Build a refusal response for missing approved literature."""
    response = (
        "我没有找到可审核的已批准资料来支持这个问题，因此不能可靠回答。"
        if language == "zh-CN"
        else (
            "I could not find approved, reviewable literature to support this "
            "answer, so I cannot answer it reliably."
        )
    )
    return DesktopChatResponse(
        response=response,
        language=language,
        language_detected=detected_language,
        confidence=0.0,
        safety_score=1.0,
        status="refused",
        citations=[],
        refusal_reason="no_approved_source",
    )


def _citation_dict(source: LiteratureSource) -> Dict[str, Any]:
    """Return compact citation metadata for chat responses."""
    return {
        "id": source.id,
        "title": source.title,
        "publisher": source.publisher,
        "language": source.language,
        "source_type": source.source_type,
        "url": source.url,
        "excerpt": source.excerpt,
        "doi": source.doi,
        "pmid": source.pmid,
    }


def _source_backed_prompt(
    message: str,
    language: str,
    citations: List[LiteratureSource],
) -> str:
    """Build a compact source-backed prompt for external providers."""
    source_lines = "\n".join(
        f"- {source.title} ({source.publisher}): {source.excerpt}"
        for source in citations
    )
    if language == "zh-CN":
        return (
            "你是性健康教育助手。只基于以下已批准资料回答，并保持谨慎、教育性和非诊断语气。\n\n"
            f"资料：\n{source_lines}\n\n"
            f"问题：{message}\n\n答案："
        )
    return (
        "You are a sexual health education assistant. Answer only from the "
        "approved sources below. Keep the answer cautious, educational, and "
        "non-diagnostic.\n\n"
        f"Sources:\n{source_lines}\n\n"
        f"Question: {message}\n\nAnswer:"
    )


def create_desktop_app() -> FastAPI:
    """Create the lean desktop FastAPI app."""
    desktop_app = FastAPI(
        title="LLB Desktop Backend",
        description="Local desktop backend for external AI provider access",
        version="0.1.0",
    )
    desktop_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @desktop_app.get("/api/v1/health")
    async def health_check() -> Dict[str, object]:
        return {
            "status": "ok",
            "mode": "desktop",
            "local_ml": False,
            "features": ["ai_providers", "chat", "literature", "desktop"],
        }

    @desktop_app.get("/health")
    async def legacy_health_check() -> Dict[str, object]:
        return {"status": "ok", "mode": "desktop"}

    @desktop_app.get("/api/v1/ai/providers")
    async def get_ai_providers() -> Dict[str, object]:
        return {"providers": ai_providers.get_provider_catalog()}

    @desktop_app.post("/api/v1/chat", response_model=DesktopChatResponse)
    async def chat_with_provider(
        message: DesktopChatMessage,
    ) -> DesktopChatResponse:
        if _is_unsupported_language(message.message, message.language):
            return _unsupported_language_response(message.language)

        response_language = _detect_supported_language(
            message.message, message.language
        )
        citations = literature_service.retrieve(message.message, response_language)
        if not citations:
            return _no_source_response(response_language, response_language)

        prompt = _source_backed_prompt(
            message.message,
            response_language,
            citations,
        )
        manager = ai_providers.AIProviderManager()
        try:
            provider_response = await manager.generate_response(
                prompt,
                max_tokens=500,
                temperature=0.2,
            )
        except RuntimeError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(exc),
            ) from exc

        return DesktopChatResponse(
            response=provider_response,
            language=response_language,
            language_detected=response_language,
            confidence=0.85,
            safety_score=0.95,
            status="answered",
            citations=[_citation_dict(source) for source in citations],
        )

    @desktop_app.get("/api/v1/chat/languages")
    async def get_supported_languages() -> Dict[str, object]:
        return {
            "supported_languages": [
                {"code": "en", "name": "English"},
                {"code": "zh-CN", "name": "Simplified Chinese"},
            ]
        }

    @desktop_app.get("/api/v1/chat/status")
    async def get_chat_status() -> Dict[str, object]:
        manager = ai_providers.AIProviderManager()
        return {
            "status": "ready" if manager.providers else "needs_provider",
            "model_info": manager.get_provider_info(),
            "configured_providers": manager.get_configured_provider_status(),
            "supported_languages": ["en", "zh-CN"],
            "local_ml": False,
        }

    desktop_app.include_router(
        desktop.router,
        prefix="/api/v1/desktop",
        tags=["desktop"],
    )
    desktop_app.include_router(
        literature.router,
        prefix="/api/v1/literature",
        tags=["literature"],
    )
    return desktop_app


app = create_desktop_app()
