"""
Centralized dependency injection to avoid circular imports
"""
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.ai_service import AIService
    from app.services.audio_service import AudioService
    from app.services.document_service import DocumentService

# Global service instances
_ai_service: Optional["AIService"] = None
_audio_service: Optional["AudioService"] = None
_document_service: Optional["DocumentService"] = None


def set_ai_service(service: "AIService"):
    global _ai_service
    _ai_service = service


def get_ai_service() -> "AIService":
    if _ai_service is None:
        from app.services.ai_service import AIService
        return AIService()
    return _ai_service


def set_audio_service(service: "AudioService"):
    global _audio_service
    _audio_service = service


def get_audio_service() -> "AudioService":
    if _audio_service is None:
        from app.services.audio_service import AudioService
        return AudioService()
    return _audio_service


def set_document_service(service: "DocumentService"):
    global _document_service
    _document_service = service


def get_document_service() -> "DocumentService":
    if _document_service is None:
        from app.services.document_service import DocumentService
        return DocumentService()
    return _document_service