from fastapi import APIRouter

from app.api.v1.endpoints import ai, auth, chat, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
