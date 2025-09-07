from .admin import admin_router
from .role import role_router
from .health import health_admin_router
from fastapi import APIRouter

admin_v2_router = APIRouter()
admin_v2_router.include_router(admin_router)
admin_v2_router.include_router(role_router)
admin_v2_router.include_router(health_admin_router)

__all__ = ["admin_v2_router"]