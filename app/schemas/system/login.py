from datetime import datetime
from typing import Optional, List
from pydantic import Field, EmailStr

from app.schemas.base import (
    BaseSchema,
    BaseCreateSchema,
    BaseResponseSchema
)

__all__ = [
    "LoginForm",
    "TokenData",
    "TokenResponse",
    "LoginResponse"
]

class LoginForm(BaseSchema):
    """
    登录表单模型
    """
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class TokenData(BaseSchema):
    """
    Token数据模型
    """
    username: Optional[str] = Field(None, description="用户名")
    user_id: Optional[int] = Field(None, description="用户ID")
    is_superuser: Optional[bool] = Field(None, description="是否超级管理员")
    exp: Optional[datetime] = Field(None, description="过期时间")
    scopes: List[str] = Field(default_factory=list, description="权限范围")

class TokenResponse(BaseSchema):
    """
    Token响应模型
    """
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field("bearer", description="令牌类型")
    expires_in: int = Field(..., description="过期时间(秒)")

class LoginResponse(BaseResponseSchema):
    """
    登录响应模型
    """
    username: str = Field(..., description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    is_active: bool = Field(..., description="是否激活")
    is_superuser: bool = Field(..., description="是否超级管理员")
    is_patientuser: bool = Field(..., description="是否患者用户")
    token: TokenResponse = Field(..., description="令牌信息")
    roles: List[dict] = Field(default_factory=list, description="角色信息")
    permissions: List[str] = Field(default_factory=list, description="权限列表")