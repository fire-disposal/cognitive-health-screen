"""管理系统模型定义

包含角色、API等基础模型
"""

from tortoise import fields

from .base import BaseModel, TimestampMixin
from .enums import MethodType


class Api(BaseModel, TimestampMixin):
    """API模型"""
    path = fields.CharField(max_length=100, description="API路径", index=True)
    method = fields.CharEnumField(MethodType, description="请求方法", index=True)
    summary = fields.CharField(max_length=500, description="请求简介", index=True)
    tags = fields.CharField(max_length=100, description="API标签", index=True)

    class Meta:
        table = "api"
