from typing import List, Optional
from datetime import datetime
from pydantic import Field, EmailStr

from app.schemas.base import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponseSchema,
    BaseQueryParams
)

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserQuery",
    "UserRegister",
    "PasswordUpdate",
    "ThemeUpdate",
    "LogoUpdate"
]

class UserCreate(BaseCreateSchema):
    """
    用户创建模型
    """
    email: EmailStr = Field(..., example="admin@example.com", description="邮箱")
    username: str = Field(..., example="admin", description="用户名")
    password: str = Field(..., example="123456", description="密码")
    is_active: Optional[bool] = Field(True, description="是否激活")
    is_superuser: Optional[bool] = Field(False, description="是否超级管理员")
    is_patientuser: Optional[bool] = Field(False, description="是否患者用户")
    role_ids: Optional[List[int]] = Field(default=[], description="角色ID列表")
    dept_id: Optional[int] = Field(0, description="部门ID")
    theme: Optional[str] = Field(default="blue", description="主题颜色")
    logo_type: Optional[str] = Field(default="type1", description="Logo类型")

class UserUpdate(BaseUpdateSchema):
    """
    用户更新模型
    """
    email: Optional[EmailStr] = Field(None, description="邮箱")
    username: Optional[str] = Field(None, description="用户名")
    is_active: Optional[bool] = Field(None, description="是否激活")
    is_superuser: Optional[bool] = Field(None, description="是否超级管理员")
    is_patientuser: Optional[bool] = Field(None, description="是否患者用户")
    role_ids: Optional[List[int]] = Field(None, description="角色ID列表")
    dept_id: Optional[int] = Field(None, description="部门ID")

class UserResponse(BaseResponseSchema):
    """
    用户响应模型
    """
    email: EmailStr = Field(..., description="邮箱")
    username: str = Field(..., description="用户名")
    is_active: bool = Field(..., description="是否激活")
    is_superuser: bool = Field(..., description="是否超级管理员")
    is_patientuser: bool = Field(..., description="是否患者用户")
    last_login: Optional[datetime] = Field(None, description="最后登录时间")
    roles: List[dict] = Field(default_factory=list, description="角色信息")
    dept_id: Optional[int] = Field(None, description="部门ID")
    theme: Optional[str] = Field(None, description="主题颜色 (blue/red/green/purple)")
    logo_type: Optional[str] = Field(None, description="Logo类型 (type1/type2)")

class UserQuery(BaseQueryParams):
    """
    用户查询参数
    """
    username: Optional[str] = Field(None, description="用户名")
    email: Optional[str] = Field(None, description="邮箱")
    is_active: Optional[bool] = Field(None, description="是否激活")
    is_superuser: Optional[bool] = Field(None, description="是否超级管理员")
    is_patientuser: Optional[bool] = Field(None, description="是否患者用户")
    role_id: Optional[int] = Field(None, description="角色ID")
    dept_id: Optional[int] = Field(None, description="部门ID")

class UserRegister(BaseCreateSchema):
    """
    用户注册模型
    """
    email: EmailStr = Field(..., example="user@example.com", description="邮箱")
    username: str = Field(..., example="newuser", description="用户名")
    password: str = Field(..., example="securepassword", description="密码")

class PasswordUpdate(BaseSchema):
    """
    密码更新模型
    """
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., description="新密码")

class ThemeUpdate(BaseUpdateSchema):
    """主题更新模型"""
    theme: str = Field(..., description="主题颜色")

class LogoUpdate(BaseUpdateSchema):
    """Logo更新模型"""
    logo_type: str = Field(..., description="Logo类型")
