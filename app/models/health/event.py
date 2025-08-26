from tortoise import fields
from app.models.base import BaseModel
from app.models.health.device import Device
from app.models.health.patient import Patient

class Event(BaseModel):
    event_id = fields.CharField(max_length=64, unique=True, index=True, description="事件ID")
    event_type = fields.CharField(max_length=64, index=True, description="事件类型")
    patient = fields.ForeignKeyField("models.Patient", related_name="events", index=True)
    device = fields.ForeignKeyField("models.Device", related_name="events", index=True)
    timestamp = fields.DatetimeField(index=True, description="事件时间")
    data = fields.JSONField(description="事件数据")
    metadata = fields.JSONField(description="元数据", default=dict)

    class Meta:
        table = "events"
        indexes = [
            ("event_id",),
            ("event_type", "timestamp"),
            ("patient_id", "timestamp"),
            ("device_id", "timestamp"),
        ]