from typing import Optional, List, Any, Dict
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.base.base_model import BaseSchema

class TimeRangeQuery(BaseSchema):
    """
    时间范围查询参数
    """
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")

class PaginationQuery(BaseSchema):
    """
    分页查询参数
    """
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    
    def get_skip(self) -> int:
        """
        获取跳过的记录数
        """
        return (self.page - 1) * self.page_size
    
    def get_pagination(self) -> Dict[str, int]:
        """
        获取分页信息
        """
        return {
            "page": self.page,
            "page_size": self.page_size
        }

class SortQuery(BaseSchema):
    """
    排序查询参数
    """
    order_by: Optional[str] = Field(None, description="排序字段")
    order_direction: Optional[str] = Field("asc", description="排序方向，asc或desc")
    
    def get_order_by(self) -> Optional[str]:
        """
        获取排序字段
        """
        if not self.order_by:
            return None
        
        direction = "" if self.order_direction.lower() == "asc" else "-"
        return f"{direction}{self.order_by}"

class SearchQuery(BaseSchema):
    """
    搜索查询参数
    """
    keyword: Optional[str] = Field(None, description="搜索关键词")
    search_fields: Optional[List[str]] = Field(None, description="搜索字段列表")

class BaseQueryParams(PaginationQuery, SortQuery, SearchQuery):
    """
    基础查询参数，包含分页、排序和搜索
    """
    pass

class TimeRangeQueryParams(BaseQueryParams, TimeRangeQuery):
    """
    带时间范围的查询参数
    """
    pass