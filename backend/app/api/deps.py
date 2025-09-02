"""
Dependency injection for LLB Backend API
Provides service dependencies for FastAPI endpoints
"""

from app.models.user import User
from app.core.dependencies import get_ai_service, get_audio_service, get_document_service


def get_current_active_user() -> User:
    """Get current active user (stub for testing)."""
    return User(id=1, email="test@example.com", is_active=True)


def get_db():
    """Get database session (stub for testing)."""
    return None
