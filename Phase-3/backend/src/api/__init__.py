"""API routers."""
from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.api.health import router as health_router
from src.api.tasks import router as tasks_router
from src.api.chat import router as chat_router
from src.api.chatkit import router as chatkit_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(tasks_router, tags=["tasks"])
api_router.include_router(chat_router, tags=["chat"])
api_router.include_router(chatkit_router, tags=["chatkit"])

__all__ = ["api_router"]
