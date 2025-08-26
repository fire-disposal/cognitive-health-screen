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
    "DeptCreate",
    "DeptUpdate",
    "DeptResponse",
    "DeptQuery"
]

class DeptCreate(BaseCreateSchema):
    """
    部门创建模型
    """
    name: str = Field(..., description="部门名称")
    parent_id: Optional[int] = Field(None, description="父部门ID")
    order: Optional[int] = Field(0, description="排序")
    leader: Optional[str] = Field(None, description="部门负责人")
    phone: Optional[str] = Field(None, description="联系电话")
    email: Optional[str] = Field(None, description="邮箱")
    desc: Optional[str] = Field(None, description="备注")
    is_deleted: Optional[bool] = Field(False, description="是否删除")

class DeptUpdate(BaseUpdateSchema):
    """
    部门更新模型
    """
    name: Optional[str] = Field(None, description="部门名称")
    parent_id: Optional[int] = Field(None, description="父部门ID")
    order: Optional[int] = Field(None, description="排序")
    leader: Optional[str] = Field(None, description="部门负责人")
    phone: Optional[str] = Field(None, description="联系电话")
    email: Optional[str] = Field(None, description="邮箱")
    desc: Optional[str] = Field(None, description="备注")
    is_deleted: Optional[bool] = Field(None, description="是否删除")

class DeptResponse(BaseResponseSchema):
    """
    部门响应模型
    """
    name: str = Field(..., description="部门名称")
    parent_id: Optional[int] = Field(None, description="父部门ID")
    order: int = Field(..., description="排序")
    leader: Optional[str] = Field(None, description="部门负责人")
    phone: Optional[str] = Field(None, description="联系电话")
    email: Optional[str] = Field(None, description="邮箱")
    desc: Optional[str] = Field(None, description="备注")
    is_deleted: bool = Field(..., description="是否删除")
    children: List["DeptResponse"] = Field(default_factory=list, description="子部门")

class DeptQuery(BaseQueryParams):
    """
    部门查询参数
    """
    name: Optional[str] = Field(None, description="部门名称")
    parent_id: Optional[int] = Field(None, description="父部门ID")
    is_deleted: Optional[bool] = Field(None, description="是否删除")