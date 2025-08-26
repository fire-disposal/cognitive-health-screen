from enum import StrEnum
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
    "MenuType",
    "MenuCreate",
    "MenuUpdate",
    "MenuResponse",
    "MenuQuery"
]

class MenuType(StrEnum):
    CATALOG = "catalog"  # 目录
    MENU = "menu"  # 菜单

class MenuCreate(BaseCreateSchema):
    """
    菜单创建模型
    """
    name: str = Field(..., description="菜单名称")
    path: Optional[str] = Field(None, description="菜单路径")
    component: Optional[str] = Field(None, description="组件路径")
    redirect: Optional[str] = Field(None, description="重定向路径")
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    icon: Optional[str] = Field(None, description="图标")
    order: Optional[int] = Field(0, description="排序")
    is_hidden: Optional[bool] = Field(False, description="是否隐藏")
    menu_type: Optional[MenuType] = Field(None, description="菜单类型")
    keepalive: Optional[bool] = Field(True, description="是否缓存")
    remark: Optional[dict] = Field(None, description="备注信息")

class MenuUpdate(BaseUpdateSchema):
    """
    菜单更新模型
    """
    name: Optional[str] = Field(None, description="菜单名称")
    path: Optional[str] = Field(None, description="菜单路径")
    component: Optional[str] = Field(None, description="组件路径")
    redirect: Optional[str] = Field(None, description="重定向路径")
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    icon: Optional[str] = Field(None, description="图标")
    order: Optional[int] = Field(None, description="排序")
    is_hidden: Optional[bool] = Field(None, description="是否隐藏")
    menu_type: Optional[MenuType] = Field(None, description="菜单类型")
    keepalive: Optional[bool] = Field(None, description="是否缓存")
    remark: Optional[dict] = Field(None, description="备注信息")

class MenuResponse(BaseResponseSchema):
    """
    菜单响应模型
    """
    name: str = Field(..., description="菜单名称")
    path: Optional[str] = Field(None, description="菜单路径")
    component: Optional[str] = Field(None, description="组件路径")
    redirect: Optional[str] = Field(None, description="重定向路径")
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    icon: Optional[str] = Field(None, description="图标")
    order: int = Field(..., description="排序")
    is_hidden: bool = Field(..., description="是否隐藏")
    menu_type: MenuType = Field(..., description="菜单类型")
    keepalive: bool = Field(..., description="是否缓存")
    remark: Optional[dict] = Field(None, description="备注信息")
    children: List["MenuResponse"] = Field(default_factory=list, description="子菜单")

class MenuQuery(BaseQueryParams):
    """
    菜单查询参数
    """
    name: Optional[str] = Field(None, description="菜单名称")
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    menu_type: Optional[MenuType] = Field(None, description="菜单类型")
    is_hidden: Optional[bool] = Field(None, description="是否隐藏")