from tortoise import fields
from app.models.base import BaseModel
from app.models.health.device import Device
from app.models.health.profile import HealthProfile

class Event(BaseModel):
    event_type = fields.CharField(max_length=64, description="事件类型", index=True)
    health_profile_id = fields.IntField(description="健康档案ID", index=True)
    device_id = fields.IntField(null=True, description="设备ID", index=True)
    source_record_id = fields.IntField(null=True, description="来源健康数据ID", index=True)
    timestamp = fields.DatetimeField(description="事件时间", index=True)
    data = fields.JSONField(description="事件数据")
    metadata = fields.JSONField(description="元数据", null=True)
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True, index=True)

    class Meta:
        table = "events"
        indexes = [
            ("event_type", "timestamp"),
            ("health_profile_id", "timestamp"),
            ("device_id", "timestamp"),
        ]