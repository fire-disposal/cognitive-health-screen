from tortoise import fields
from app.models.base import BaseModel
from app.models.health.device import Device
from app.models.health.patient import Patient


class HealthDataRecord(BaseModel):
    """
    健康数据记录模型
    patient: 关联患者
    schema_type: 数据类型（如 heart_rate、sleep 等），建议与 source_type 统一
    recorded_at: 数据记录时间
    received_at: 数据接收时间
    payload: 原始数据载荷
    """
    patient = fields.ForeignKeyField("models.Patient", related_name="health_data_points", index=True)
    schema_type = fields.CharField(max_length=64, index=True, description="数据类型（如 heart_rate、sleep 等），与 source_type 对齐")
    recorded_at = fields.DatetimeField(index=True, description="数据记录时间")
    payload = fields.JSONField(description="原始数据载荷")
    status = fields.CharField(max_length=32, default="raw", description="数据状态（raw, filtered, invalid）")

    class Meta:
        table = "health_data_records"
        indexes = [
            ("patient_id", "recorded_at"),
        ]
