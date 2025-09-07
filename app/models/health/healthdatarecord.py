from tortoise import fields
from app.models.base import BaseModel
from app.models.health.device import Device
from app.models.health.profile import HealthProfile


class HealthDataRecord(BaseModel):
    health_profile_id = fields.IntField(description="健康档案ID", index=True)
    device_id = fields.IntField(null=True, description="设备ID", index=True)
    schema_type = fields.CharField(max_length=64, description="数据类型", index=True)
    recorded_at = fields.DatetimeField(description="数据记录时间", index=True)
    payload = fields.JSONField(description="数据内容")
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True, index=True)

    class Meta:
        table = "health_data_records"
        indexes = [
            ("health_profile_id", "recorded_at"),
            ("device_id", "recorded_at"),
        ]
