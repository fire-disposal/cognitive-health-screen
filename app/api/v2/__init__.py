"""API v2版本路由模块

提供API v2版本的路由管理，包括：
1. 认证相关路由（无需权限验证）
2. 管理员相关路由（需要管理员权限）
3. 应用用户相关路由（需要应用用户权限）
"""

from fastapi import APIRouter
from fastapi import Depends
from app.core.dependency import AuthService
verify_admin_token = AuthService.get_admin_user
from app.core.dependency import DependAppUser

# 导入认证路由
from app.api.v2.auth import admin_router as admin_auth_router
from app.api.v2.auth import app_router as app_auth_router

# v2版本主路由
v2_router = APIRouter(prefix="/v2")

# 认证路由组 - 不需要权限验证
auth_router = APIRouter(prefix="/auth", tags=["认证"])
auth_router.include_router(admin_auth_router, prefix="/admin", tags=["管理员认证"])
auth_router.include_router(app_auth_router, prefix="/app", tags=["应用用户认证"])

# 管理员路由组 - 需要管理员权限
from app.api.v2.admin.admin import admin_router as admin_user_router

admin_router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(verify_admin_token)],
    tags=["管理后台"]
)
admin_router.include_router(admin_user_router, prefix="/users", tags=["管理员用户管理"])
# 应用用户路由组 - 需要应用用户权限
from app.api.v2.miniapp.app import app_router as miniapp_user_router

app_router = APIRouter(
    prefix="/app",
    dependencies=[Depends(AuthService.get_app_user)],
    tags=["应用接口"]
)
app_router.include_router(miniapp_user_router, prefix="/miniapp", tags=["小程序用户管理"])
# 注册所有路由组
v2_router.include_router(auth_router)    # 认证路由
v2_router.include_router(admin_router)   # 管理员路由
v2_router.include_router(app_router)     # 应用用户路由

__all__ = ["v2_router"]