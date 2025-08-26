from typing import Optional, List
from pydantic import Field

from app.schemas.base import (
    BaseSchema,
    BaseCreateSchema,
    BaseUpdateSchema,
    BaseResponseSchema,
    BaseQueryParams
)

__all__ = [
    "ApiCreate",
    "ApiUpdate",
    "ApiResponse",
    "ApiQuery"
]

class ApiCreate(BaseCreateSchema):
    """
    API创建模型
    """
    method: str = Field(..., description="请求方法")
    path: str = Field(..., description="API路径")
    summary: str = Field(..., description="API描述")
    tags: Optional[str] = Field(None, description="API分组")

class ApiUpdate(BaseUpdateSchema):
    """
    API更新模型
    """
    method: Optional[str] = Field(None, description="请求方法")
    path: Optional[str] = Field(None, description="API路径")
    summary: Optional[str] = Field(None, description="API描述")
    tags: Optional[str] = Field(None, description="API分组")

class ApiResponse(BaseResponseSchema):
    """
    API响应模型
    """
    method: str = Field(..., description="请求方法")
    path: str = Field(..., description="API路径")
    summary: str = Field(..., description="API描述")
    tags: Optional[str] = Field(None, description="API分组")

class ApiQuery(BaseQueryParams):
    """
    API查询参数
    """
    method: Optional[str] = Field(None, description="请求方法")
    path: Optional[str] = Field(None, description="API路径")
    tags: Optional[str] = Field(None, description="API分组")