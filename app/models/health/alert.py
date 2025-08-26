from tortoise import fields
from app.models.base import BaseModel, TimestampMixin
from app.models.health.device import Device
from app.models.health.patient import Patient

class Alert(BaseModel, TimestampMixin):
    device: fields.ForeignKeyRelation[Device] = fields.ForeignKeyField(
        "models.Device", related_name="alerts", index=True
    )
    patient: fields.ForeignKeyRelation[Patient] = fields.ForeignKeyField(
        "models.Patient", related_name="alerts", index=True
    )
    rule_name = fields.CharField(max_length=64, description="告警规则名")
    level = fields.CharField(max_length=16, description="告警级别")
    message = fields.TextField(description="告警内容")
    # 兼容事件类型
    event_type = fields.CharField(max_length=64, null=True, index=True, description="事件类型（如 fall, sleep_stage, abnormal, medication）")
    description = fields.TextField(null=True, description="事件内容/详情")
    extra = fields.JSONField(null=True, description="扩展字段")
    status = fields.CharField(max_length=16, default="active", description="告警状态")
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    resolved_at = fields.DatetimeField(null=True, index=True)

    class Meta:
        table = "alerts"
        indexes = [
            ("device_id", "patient_id", "rule_name", "status"),
            ("created_at", "resolved_at"),
        ]