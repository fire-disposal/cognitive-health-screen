"""应用用户认证路由"""

from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from app.core.dependency import AuthService
from app.models.users import AppUser
from app.schemas.auth import AppLogin, WechatLogin, TokenResponse
from app.utils.password import verify_password, check_user_auth
from app.settings import settings

router = APIRouter()

# 统一鉴权异常处理已迁移至 utils.password.check_user_auth

@router.post("/login", response_model=TokenResponse, summary="应用用户账号密码登录")
async def app_login(form_data: AppLogin):
    """应用用户账号密码登录获取token"""
    user = await AppUser.get_or_none(username=form_data.username)
    check_user_auth(user, form_data.password)

    access_token = AuthService.create_token(
        user_id=user.id,
        username=user.username,
        user_type="app"
    )
    user.last_login = datetime.utcnow()
    await user.save()
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_id=user.id,
        username=user.username,
        user_type="app"
    )

@router.post("/wechat/login", response_model=TokenResponse, summary="微信小程序登录")
async def wechat_login(form_data: WechatLogin):
    """微信小程序登录获取token"""
    # TODO: 实现微信登录逻辑
    # 1. 使用code换取openid
    # 2. 根据openid查找或创建用户
    # 3. 生成token
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="微信登录功能尚未实现"
    )
from fastapi import Depends, HTTPException, status
from app.core.dependency import AuthService
from pydantic import BaseModel

from app.schemas.auth import TokenData

async def verify_app_token(token: TokenData = Depends(AuthService.get_app_user)):
    """
    校验应用用户token，返回TokenData对象
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的应用用户token"
        )
    return token
__all__ = [
    "router",
    "verify_app_token",
    "TokenData"
]