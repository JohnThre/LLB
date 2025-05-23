"""
Chat endpoints for AI conversations.
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.api.deps import get_ai_service
from app.services.ai_service import AIService
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message model."""
    message: str
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
    processing_time: Optional[float] = None


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    message: ChatMessage,
    ai_service: AIService = Depends(get_ai_service)
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
        
        # Generate AI response
        response = await ai_service.generate_response(
            message=message.message,
            language=message.language or "en",
            context=message.context
        )
        
        return ChatResponse(**response)
        
    except Exception as e:
        logger.error(f"Chat processing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.get("/chat/languages")
async def get_supported_languages(
    ai_service: AIService = Depends(get_ai_service)
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
            "zh-TW": "Traditional Chinese"
        }
        
        return {
            "supported_languages": [
                {
                    "code": lang,
                    "name": language_map.get(lang, lang)
                }
                for lang in languages
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to get supported languages: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve supported languages"
        )


@router.get("/chat/status")
async def get_chat_status(
    ai_service: AIService = Depends(get_ai_service)
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
            "memory_usage": ai_service.get_memory_usage()
        }
        
    except Exception as e:
        logger.error(f"Failed to get chat status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chat status"
        ) 