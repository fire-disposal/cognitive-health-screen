from typing import Union, Optional
from datetime import datetime, timedelta

import jwt
from app.utils.jwt_utils import decode_access_token
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from app.core.ctx import CTX_USER_ID
from app.models.users import AdminUser, AppUser
from app.settings import settings

# 定义不同端点的OAuth2认证
admin_oauth2 = OAuth2PasswordBearer(tokenUrl="/v2/auth/admin/login")
app_oauth2 = OAuth2PasswordBearer(tokenUrl="/v2/auth/app/login")

class TokenBlacklist:
    """简单的Token黑名单实现"""
    _blacklist = set()

    @classmethod
    def add(cls, token: str) -> None:
        cls._blacklist.add(token)

    @classmethod
    def remove(cls, token: str) -> None:
        cls._blacklist.discard(token)

    @classmethod
    def contains(cls, token: str) -> bool:
        return token in cls._blacklist

class AuthService:
    """认证服务"""

    @staticmethod
    def create_token(user_id: int, username: str, user_type: str) -> str:
        """创建JWT token"""
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        data = {
            "user_id": user_id,
            "username": username,
            "user_type": user_type,
            "exp": expire
        }
        token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return token

    @staticmethod
    async def get_admin_user(token: str = Depends(admin_oauth2)) -> AdminUser:
        """验证管理员用户"""
        try:
            if TokenBlacklist.contains(token):
                raise HTTPException(status_code=401, detail="Token has been blacklisted")

            payload = decode_access_token(token)
            user_id = payload.get("user_id")
            user_type = payload.get("user_type")

            if user_type != "admin":
                raise HTTPException(status_code=403, detail="Not an admin token")

            user = await AdminUser.get_or_none(id=user_id)
            if not user or not user.is_active:
                raise HTTPException(status_code=401, detail="User not found or inactive")

            CTX_USER_ID.set(user_id)
            return user

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Could not validate token")

    @staticmethod
    async def get_app_user(token: str = Depends(app_oauth2)) -> AppUser:
        """验证应用用户"""
        try:
            if TokenBlacklist.contains(token):
                raise HTTPException(status_code=401, detail="Token has been blacklisted")

            payload = decode_access_token(token)
            user_id = payload.get("user_id")
            user_type = payload.get("user_type")

            if user_type != "app":
                raise HTTPException(status_code=403, detail="Not an app user token")

            user = await AppUser.get_or_none(id=user_id)
            if not user or not user.is_active:
                raise HTTPException(status_code=401, detail="User not found or inactive")

            CTX_USER_ID.set(user_id)
            return user

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Could not validate token")

class PermissionControl:
    """权限控制"""

    @staticmethod
    def is_admin_path(path: str) -> bool:
        """检查是否管理员API路径"""
        return path.startswith("/v2/admin")

    @staticmethod
    def is_app_path(path: str) -> bool:
        """检查是否应用用户API路径"""
        return path.startswith("/v2/app")

    @classmethod
    async def check_permission(
        cls,
        request: Request,
        user: Union[AdminUser, AppUser] = Depends(AuthService.get_admin_user)
    ) -> None:
        """检查用户权限"""
        path = request.url.path

        # 管理员API只允许管理员访问
        if cls.is_admin_path(path):
            if not isinstance(user, AdminUser):
                raise HTTPException(status_code=403, detail="Admin privileges required")
            return

        # 应用API只允许对应的应用用户访问
        if cls.is_app_path(path):
            if not isinstance(user, AppUser):
                raise HTTPException(status_code=403, detail="App user privileges required")
            return

        # 其他API需要具体判断权限
        if isinstance(user, AdminUser):
            # 管理员可以访问所有API
            return
        elif isinstance(user, AppUser):
            # 应用用户只能访问自己的数据
            # 在具体API中处理
            return
        else:
            raise HTTPException(status_code=403, detail="Unknown user type")

# 依赖注入
DependAdminUser = Depends(AuthService.get_admin_user)
DependAppUser = Depends(AuthService.get_app_user)
DependPermission = Depends(PermissionControl.check_permission)
