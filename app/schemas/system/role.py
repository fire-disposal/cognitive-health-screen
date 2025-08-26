from typing import List, Optional
from pydantic import Field

from app.schemas.base import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponseSchema,
    BaseQueryParams
)

__all__ = [
    "RoleCreate",
    "RoleUpdate",
    "RoleResponse",
    "RoleQuery",
    "RoleUpdateMenusApis"
]

class RoleCreate(BaseCreateSchema):
    """
    角色创建模型
    """
    name: str = Field(..., description="角色名称")
    desc: Optional[str] = Field(None, description="角色描述")
    menu_ids: Optional[List[int]] = Field(default=[], description="菜单ID列表")
    api_ids: Optional[List[int]] = Field(default=[], description="API ID列表")

class RoleUpdate(BaseUpdateSchema):
    """
    角色更新模型
    """
    name: Optional[str] = Field(None, description="角色名称")
    desc: Optional[str] = Field(None, description="角色描述")
    menu_ids: Optional[List[int]] = Field(None, description="菜单ID列表")
    api_ids: Optional[List[int]] = Field(None, description="API ID列表")

class RoleResponse(BaseResponseSchema):
    """
    角色响应模型
    """
    name: str = Field(..., description="角色名称")
    desc: Optional[str] = Field(None, description="角色描述")
    menus: List[dict] = Field(default_factory=list, description="菜单信息")
    apis: List[dict] = Field(default_factory=list, description="API信息")

class RoleQuery(BaseQueryParams):
    """
    角色查询参数
    """
    name: Optional[str] = Field(None, description="角色名称")

class RoleUpdateMenusApis(BaseSchema):
    """
    角色权限更新模型
    """
    id: int = Field(..., description="角色ID")
    menu_ids: List[int] = Field(default=[], description="菜单ID列表")
    api_infos: List[dict] = Field(default=[], description="API信息列表")