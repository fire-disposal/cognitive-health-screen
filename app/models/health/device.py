from tortoise import fields
from typing import Dict, List

from app.models.base import BaseModel, TimestampMixin
from app.models.health.patient import Patient

class Device(BaseModel):
    # 基础信息
    device_id = fields.CharField(max_length=128, unique=True, index=True)
    name = fields.CharField(max_length=64, null=True, index=True)
    description = fields.TextField(null=True)
    model = fields.CharField(max_length=64, null=True)  # 型号
    device_type = fields.CharField(max_length=32, null=True, index=True)  # 类型

    # 分组信息
    group_id = fields.IntField(null=True, index=True)
    tags = fields.JSONField(default=list, description="设备标签，用于灵活分组")

    # 状态信息
    status = fields.CharField(max_length=32, default="offline", index=True)

    # 配置信息
    config = fields.JSONField(default=dict, description="设备配置")
    data_types = fields.JSONField(default=list, description="设备支持的健康数据类型")


    # 关联患者
    current_patient: fields.ForeignKeyNullableRelation["Patient"] = fields.ForeignKeyField(
        "models.Patient",
        related_name="active_devices",
        null=True,
        on_delete=fields.SET_NULL
    )

    class Meta:
        table = "devices"
        indexes = [
            ("device_type", "status"),
            ("group_id", "status"),
            ("device_id", "name"),
            ("current_patient_id",),
        ]

    async def bind_patient(self, patient: "Patient"):
        self.current_patient = patient
        await self.save()
