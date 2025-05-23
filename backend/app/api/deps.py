"""
Dependency injection for LLB Backend API
Provides service dependencies for FastAPI endpoints
"""

from app.core.exceptions import LLBException
from app.services.ai_service import AIService
from app.services.audio_service import AudioService
from app.services.document_service import DocumentService

# Global service instances (will be set by main.py)
_ai_service: AIService = None
_audio_service: AudioService = None
_document_service: DocumentService = None


def set_services(
    ai_service: AIService,
    audio_service: AudioService,
    document_service: DocumentService,
):
    """Set global service instances."""
    global _ai_service, _audio_service, _document_service
    _ai_service = ai_service
    _audio_service = audio_service
    _document_service = document_service


def get_ai_service() -> AIService:
    """Get AI service instance."""
    if _ai_service is None:
        raise LLBException("AI service not initialized")
    return _ai_service


def get_audio_service() -> AudioService:
    """Get audio service instance."""
    if _audio_service is None:
        raise LLBException("Audio service not initialized")
    return _audio_service


def get_document_service() -> DocumentService:
    """Get document service instance."""
    if _document_service is None:
        raise LLBException("Document service not initialized")
    return _document_service
