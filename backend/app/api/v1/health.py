"""
Health check API endpoints
Provides system status and health monitoring
"""

from typing import Any, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_ai_service, get_audio_service, get_document_service
from app.config import settings
from app.core.logging import get_logger
from app.services.ai_service import AIService
from app.services.audio_service import AudioService
from app.services.document_service import DocumentService

logger = get_logger(__name__)
router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    version: str
    environment: str
    services: Dict[str, Any]
    system_info: Dict[str, Any]


@router.get("/health", response_model=HealthResponse)
async def health_check(
    ai_service: AIService = Depends(get_ai_service),
    audio_service: AudioService = Depends(get_audio_service),
    document_service: DocumentService = Depends(get_document_service),
):
    """
    Comprehensive health check endpoint.

    Returns:
        System health status and service information
    """
    try:
        # Check service health
        services_status = {
            "ai_service": {
                "status": "healthy" if ai_service.is_healthy() else "unhealthy",
                "model_loaded": ai_service.is_model_loaded(),
                "supported_languages": ai_service.get_supported_languages(),
            },
            "audio_service": {
                "status": (
                    "healthy" if audio_service.is_healthy() else "unhealthy"
                ),
                "supported_formats": audio_service.get_supported_formats(),
            },
            "document_service": {
                "status": (
                    "healthy" if document_service.is_healthy() else "unhealthy"
                ),
                "supported_formats": document_service.get_supported_formats(),
            },
        }

        # System information
        system_info = {
            "supported_languages": ["en", "zh-CN"],
            "max_file_size": getattr(settings, 'MAX_UPLOAD_SIZE', 50*1024*1024),
            "allowed_file_types": list(getattr(settings, 'ALLOWED_EXTENSIONS', [])),
            "safety_level": "high",
        }

        # Determine overall status
        overall_status = "healthy"
        for service_name, service_info in services_status.items():
            if service_info["status"] != "healthy":
                overall_status = "degraded"
                logger.warning(f"Service {service_name} is unhealthy")

        return HealthResponse(
            status=overall_status,
            version=getattr(settings, 'VERSION', '0.1.0'),
            environment="development" if getattr(settings, 'debug', False) else "production",
            services=services_status,
            system_info=system_info,
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            version=getattr(settings, 'VERSION', '0.1.0'),
            environment="unknown",
            services={},
            system_info={"error": str(e)},
        )


@router.get("/health/ai")
async def ai_health_check(ai_service: AIService = Depends(get_ai_service)):
    """
    AI service specific health check.

    Returns:
        AI service health and model information
    """
    try:
        return {
            "status": "healthy" if ai_service.is_healthy() else "unhealthy",
            "model_loaded": ai_service.is_model_loaded(),
            "model_info": ai_service.get_model_info(),
            "supported_languages": ai_service.get_supported_languages(),
            "memory_usage": ai_service.get_memory_usage(),
        }
    except Exception as e:
        logger.error(f"AI health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}


@router.get("/health/audio")
async def audio_health_check(
    audio_service: AudioService = Depends(get_audio_service),
):
    """
    Audio service specific health check.

    Returns:
        Audio service health and capability information
    """
    try:
        return {
            "status": "healthy" if audio_service.is_healthy() else "unhealthy",
            "supported_formats": audio_service.get_supported_formats(),
            "whisper_loaded": audio_service.is_whisper_loaded(),
            "processing_capabilities": audio_service.get_capabilities(),
        }
    except Exception as e:
        logger.error(f"Audio health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}


@router.get("/health/documents")
async def document_health_check(
    document_service: DocumentService = Depends(get_document_service),
):
    """
    Document service specific health check.

    Returns:
        Document service health and processing information
    """
    try:
        return {
            "status": (
                "healthy" if document_service.is_healthy() else "unhealthy"
            ),
            "supported_formats": document_service.get_supported_formats(),
            "processing_capabilities": document_service.get_capabilities(),
            "max_file_size": getattr(settings, 'MAX_UPLOAD_SIZE', 50*1024*1024),
        }
    except Exception as e:
        logger.error(f"Document health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}
