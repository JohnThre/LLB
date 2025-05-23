"""
Import all models here for Alembic to detect them.
"""

from app.db.base_class import Base
from app.models.user import User
from app.models.chat import Chat, Message
from app.models.ai import ModelUsage, ModelAnalytics, ModelFeedback 