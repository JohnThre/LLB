"""
AI core module stub
"""
from app.services.ai_service import AIService

_ai_service = None

def get_ai_model():
    """Get AI model instance"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service