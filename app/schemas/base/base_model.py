from typing import Any, Optional, TypeVar, Type, Dict, List, Generic
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from tortoise.models import Model

# 定义类型变量，用于表示 Tortoise ORM 模型
ModelType = TypeVar("ModelType", bound=Model)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class BaseSchema(BaseModel):
    """
    所有模型的基础Schema
    """
    model_config = ConfigDict(from_attributes=True)

class BaseCreateSchema(BaseSchema):
    """
    创建操作的基础Schema
    """
    pass

class BaseUpdateSchema(BaseSchema):
    """
    更新操作的基础Schema
    """
    pass

class BaseResponseSchema(BaseSchema):
    """
    响应操作的基础Schema
    """
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class BaseQuerySchema(BaseSchema):
    """
    查询操作的基础Schema
    """
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    order_by: Optional[str] = Field(None, description="排序字段")
    
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