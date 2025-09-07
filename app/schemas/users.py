from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.users import AdminUser, AppUser

# AdminUser验证模型
AdminUserBase = pydantic_model_creator(
    AdminUser,
    name="AdminUserBase",
    exclude=("password_hash", "created_at", "updated_at")
)

class AdminUserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=64, description="用户名")
    email: Optional[str] = Field(None, max_length=128, description="邮箱")
    phone: Optional[str] = Field(None, max_length=32, description="手机号")
    password: str = Field(..., min_length=6, max_length=32, description="密码")
    role: Optional[str] = Field(None, max_length=32, description="角色")
    is_active: bool = Field(True, description="是否激活")

class AdminUserUpdate(BaseModel):
    email: Optional[str] = Field(None, max_length=128, description="邮箱")
    phone: Optional[str] = Field(None, max_length=32, description="手机号")
    password: Optional[str] = Field(None, min_length=6, max_length=32, description="密码")
    role: Optional[str] = Field(None, max_length=32, description="角色")
    is_active: Optional[bool] = Field(None, description="是否激活")
    last_login: Optional[datetime] = Field(None, description="最后登录时间")

# AppUser验证模型
AppUserBase = pydantic_model_creator(
    AppUser,
    name="AppUserBase",
    exclude=("password_hash", "created_at", "updated_at")
)

class AppUserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=64, description="用户名")
    email: Optional[str] = Field(None, max_length=128, description="邮箱")
    phone: Optional[str] = Field(None, max_length=32, description="手机号")
    password: str = Field(..., min_length=6, max_length=32, description="密码")
    wechat_openid: Optional[str] = Field(None, max_length=128, description="微信OpenID")
    is_active: bool = Field(True, description="是否激活")

class AppUserUpdate(BaseModel):
    email: Optional[str] = Field(None, max_length=128, description="邮箱")
    phone: Optional[str] = Field(None, max_length=32, description="手机号")
    password: Optional[str] = Field(None, min_length=6, max_length=32, description="密码")
    wechat_openid: Optional[str] = Field(None, max_length=128, description="微信OpenID")
    is_active: Optional[bool] = Field(None, description="是否激活")
    last_login: Optional[datetime] = Field(None, description="最后登录时间")

# Response模型
AdminUserResponse = pydantic_model_creator(
    AdminUser,
    name="AdminUserResponse",
    exclude=("password_hash",)
)

AppUserResponse = pydantic_model_creator(
    AppUser,
    name="AppUserResponse",
    exclude=("password_hash",)
)

__all__ = [
    "AdminUserBase",
    "AdminUserCreate",
    "AdminUserUpdate",
    "AdminUserResponse",
    "AppUserBase",
    "AppUserCreate", 
    "AppUserUpdate",
    "AppUserResponse",
]