from typing import Any, List, Optional
from pydantic import BaseModel, Field

class SuccessResponse(BaseModel):
    msg: Optional[str] = Field(None, description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")

class PaginatedResponse(BaseModel):
    total: int = Field(..., description="总条数")
    items: List[Any] = Field(..., description="数据列表")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")