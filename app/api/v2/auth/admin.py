"""管理员认证路由"""

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status
from app.core.dependency import AuthService
from app.models.users import AdminUser
from app.schemas.auth import AdminLogin, TokenResponse
from app.utils.password import verify_password
from app.settings import settings

router = APIRouter()

def handle_auth_exception(user, password=None):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    if password is not None and not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户已被禁用"
        )

@router.post("/login", response_model=TokenResponse, summary="管理员登录")
async def admin_login(form_data: AdminLogin):
    """管理员登录获取token"""
    user = await AdminUser.get_or_none(username=form_data.username)
    handle_auth_exception(user, form_data.password)

    access_token = AuthService.create_token(
        user_id=user.id,
        username=user.username,
        user_type="admin"
    )
    user.last_login = datetime.utcnow()
    await user.save()
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_id=user.id,
        username=user.username,
        user_type="admin"
    )
from fastapi import Depends, HTTPException, status, Request
from app.core.dependency import AuthService

async def verify_admin_token(token: str = Depends(AuthService.get_admin_user)):
    """
    校验管理员token，返回管理员用户对象
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的管理员token"
        )
    return token