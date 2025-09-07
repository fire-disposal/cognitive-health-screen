from tortoise import fields
from app.models.base import BaseModel, TimestampMixin
from app.models.health.device import Device
from app.models.health.profile import HealthProfile

class Alert(BaseModel):
    health_profile_id = fields.IntField(null=True, description="健康档案ID", index=True)
    device_id = fields.IntField(null=True, description="设备ID", index=True)
    source_event_id = fields.IntField(null=True, description="来源事件ID", index=True)
    rule_name = fields.CharField(max_length=128, null=True, description="告警规则名")
    level = fields.CharField(max_length=32, null=True, description="告警级别")
    message = fields.TextField(null=True, description="告警内容")
    event_type = fields.CharField(max_length=64, null=True, description="事件类型")
    description = fields.TextField(null=True, description="事件详情")
    extra = fields.JSONField(null=True, description="扩展字段")
    status = fields.CharField(max_length=32, null=True, description="告警状态")
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    resolved_at = fields.DatetimeField(null=True, index=True)

    class Meta:
        table = "alerts"
        indexes = [
            ("device_id", "status"),
            ("health_profile_id", "rule_name", "status"),
        ]