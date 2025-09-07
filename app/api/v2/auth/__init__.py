"""认证路由包"""

from .admin import router as admin_router
from .app import router as app_router

from .admin import (
    verify_admin_token,
)
from .app import (
    verify_app_token,
    TokenData
)
from app.schemas.auth import TokenData, AdminTokenData, UserTokenData

__all__ = [
    "admin_router",
    "app_router",
    "verify_admin_token",
    "verify_app_token",
    "TokenData",
    "AdminTokenData",
    "UserTokenData"
]