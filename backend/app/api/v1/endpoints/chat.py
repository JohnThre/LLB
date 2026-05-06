"""
Chat endpoints for AI conversations.
"""

import re
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.deps import get_ai_service
from app.core.logging import get_logger
from app.services.ai_service import AIService
from app.services.literature_service import LiteratureSource, literature_service

logger = get_logger(__name__)
router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message model."""

    message: str = Field(..., min_length=1)
    language: Optional[str] = "en"
    context: Optional[Dict[str, Any]] = None
    cultural_context: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model."""

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
    # Basic non-English signal for common accented Latin punctuation/letters.
    return bool(re.search(r"[¿¡áéíóúñüÁÉÍÓÚÑÜ]", text))


def _unsupported_language_response(
    requested_language: Optional[str],
) -> ChatResponse:
    """Build the supported-language refusal response."""
    language = "zh-CN" if requested_language == "zh-CN" else "en"
    if language == "zh-CN":
        response = "目前仅支持简体中文和英语。请使用其中一种语言重新提问。"
    else:
        response = (
            "Only English and Simplified Chinese are supported. "
            "Please ask your question again in one of those languages."
        )
    return ChatResponse(
        response=response,
        language=language,
        language_detected=requested_language or "unsupported",
        confidence=0.0,
        safety_score=1.0,
        status="refused",
        citations=[],
        refusal_reason="unsupported_language",
    )


def _no_source_response(language: str, detected_language: str) -> ChatResponse:
    """Build a refusal response for missing approved literature."""
    if language == "zh-CN":
        response = "我没有找到可审核的已批准资料来支持这个问题，因此不能可靠回答。"
    else:
        response = (
            "I could not find approved, reviewable literature to support this "
            "answer, so I cannot answer it reliably."
        )
    return ChatResponse(
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


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    message: ChatMessage, ai_service: AIService = Depends(get_ai_service)
) -> Any:
    """
    Send a message to the AI and get a response.

    Args:
        message: The chat message with text and optional language/context
        ai_service: AI service dependency

    Returns:
        AI response with confidence and safety scores
    """
    try:
        logger.info(f"Processing chat message: {message.message[:50]}...")

        if _is_unsupported_language(message.message, message.language):
            return _unsupported_language_response(message.language)

        response_language = _detect_supported_language(
            message.message, message.language
        )
        detected_language = response_language
        citations = literature_service.retrieve(
            message.message, response_language
        )

        if not citations:
            return _no_source_response(response_language, detected_language)

        # Generate AI response
        response = await ai_service.generate_response(
            message=message.message,
            language=response_language,
            context={
                **(message.context or {}),
                "citations": [_citation_dict(source) for source in citations],
            },
        )

        response["language"] = response_language
        response["language_detected"] = detected_language
        response["status"] = "answered"
        response["citations"] = [_citation_dict(source) for source in citations]
        response["refusal_reason"] = None

        return ChatResponse(**response)

    except Exception as e:
        logger.error(f"Chat processing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}",
        )


@router.get("/chat/languages")
async def get_supported_languages(
    ai_service: AIService = Depends(get_ai_service),
) -> Dict[str, Any]:
    """
    Get list of supported languages for chat.

    Returns:
        List of supported language codes and names
    """
    try:
        languages = ai_service.get_supported_languages()

        # Map language codes to names
        language_map = {
            "en": "English",
            "zh-CN": "Simplified Chinese",
        }

        return {
            "supported_languages": [
                {"code": lang, "name": language_map.get(lang, lang)}
                for lang in languages
                if lang in SUPPORTED_CHAT_LANGUAGES
            ]
        }

    except Exception as e:
        logger.error(f"Failed to get supported languages: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve supported languages",
        )


@router.get("/chat/status")
async def get_chat_status(
    ai_service: AIService = Depends(get_ai_service),
) -> Dict[str, Any]:
    """
    Get chat service status and capabilities.

    Returns:
        Chat service status and model information
    """
    try:
        return {
            "status": "ready" if ai_service.is_ready() else "not_ready",
            "model_info": ai_service.get_model_info(),
            "supported_languages": ai_service.get_supported_languages(),
            "memory_usage": ai_service.get_memory_usage(),
        }

    except Exception as e:
        logger.error(f"Failed to get chat status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chat status",
        )
