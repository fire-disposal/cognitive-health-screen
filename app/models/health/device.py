from tortoise import fields
from typing import Dict, List

from app.models.base import BaseModel, TimestampMixin
from app.models.health.profile import HealthProfile

class Device(BaseModel):
    serial_number = fields.CharField(max_length=64, unique=True, description="设备唯一标识", index=True)
    name = fields.CharField(max_length=128, null=True, description="设备名称")
    device_type = fields.CharField(max_length=64, null=True, description="设备类型")
    is_active = fields.BooleanField(default=True, description="激活状态", index=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True, index=True)

    class Meta:
        table = "devices"
        indexes = [
            ("device_type",),
        ]
