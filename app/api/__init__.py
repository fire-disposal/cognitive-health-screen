from fastapi import APIRouter

from .v2 import v2_router

api_router = APIRouter()
api_router.include_router(v2_router)


__all__ = ["api_router"]
