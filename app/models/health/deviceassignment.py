from app.models.base import BaseModel
from tortoise import fields

class DeviceAssignment(BaseModel):
    device_id = fields.IntField(description="设备ID", index=True)
    health_profile_id = fields.IntField(description="健康档案ID", index=True)
    assigned_at = fields.DatetimeField(auto_now_add=True, description="分配时间", index=True)
    unassigned_at = fields.DatetimeField(null=True, description="解绑时间", index=True)

    class Meta:
        table = "device_assignments"
        indexes = [
            ("health_profile_id",),
            ("device_id",),
        ]