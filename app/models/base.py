import asyncio
import logging
from datetime import datetime
from typing import Optional, List, ClassVar, Dict, AnyStr, Any

from tortoise import fields, models
from app.settings import settings

logger = logging.getLogger(__name__)

class BaseModel(models.Model):
    """
    通用基础模型：使用自增 BigInt 主键，支持 m2m 序列化、字段排除
    """
    id = fields.BigIntField(pk=True, index=True)

    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True, index=True)

    class Meta:
        abstract = True
        default_connection = "postgres"

    async def to_dict(self, m2m: bool = False, exclude_fields: Optional[List[str]] = None):
        if exclude_fields is None:
            exclude_fields = []

        data = {}
        for field in self._meta.db_fields:
            if field not in exclude_fields:
                value = getattr(self, field)
                if isinstance(value, datetime):
                    value = value.strftime(settings.DATETIME_FORMAT)
                elif hasattr(value, "to_dict") and asyncio.iscoroutinefunction(value.to_dict):
                    value = await value.to_dict()
                elif hasattr(value, "to_dict"):
                    value = value.to_dict()
                data[field] = value

        if m2m:
            results = await asyncio.gather(*[
                self.__fetch_m2m_field(field, exclude_fields)
                for field in self._meta.m2m_fields
                if field not in exclude_fields
            ])
            for field_name, values in results:
                data[field_name] = values

        return data

    async def as_response(self):
        """
        递归转换所有字段为可序列化对象，适用于 FastAPI/JSONResponse
        """
        return await self.to_dict(m2m=True)

    async def __fetch_m2m_field(self, field, exclude_fields):
        values = await getattr(self, field).all().values()
        formatted_values = [
            {
                k: (v.strftime(settings.DATETIME_FORMAT) if isinstance(v, datetime) else v)
                for k, v in val.items() if k not in exclude_fields
            } for val in values
        ]
        return field, formatted_values


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True, index=True)
