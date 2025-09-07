from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class LoginBase(BaseModel):
    """基础登录模型"""
    username: str = Field(..., min_length=3, max_length=64, description="用户名")
    password: str = Field(..., min_length=6, max_length=32, description="密码")

class TokenData(BaseModel):
    """Token数据基类"""
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    user_type: str = Field(..., description="用户类型(admin/app)")
    exp: datetime = Field(..., description="过期时间")

class TokenResponse(BaseModel):
    """Token响应"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")
    user_id: int = Field(..., description="用户ID")
    username: str = Field(..., description="用户名")
    user_type: str = Field(..., description="用户类型")

class AdminLogin(LoginBase):
    """管理员登录"""
    pass

class AppLogin(LoginBase):
    """应用用户登录"""
    pass

# Optional: 如果需要微信登录
class WechatLogin(BaseModel):
    """微信登录"""
    code: str = Field(..., description="微信授权码")
    app_id: Optional[str] = Field(None, description="小程序appId")

__all__ = [
    "LoginBase",
    "TokenData",
    "TokenResponse",
    "AdminLogin",
    "AppLogin",
    "WechatLogin",
]