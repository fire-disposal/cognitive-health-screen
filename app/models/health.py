from datetime import datetime
from tortoise import fields
from app.models.base import BaseModel, TimestampMixin
from app.models.users import AppUser


class HealthProfile(BaseModel):
    """健康档案模型"""
    user = fields.ForeignKeyField(
        "models.AppUser",
        related_name="health_profiles",
        null=True,
        description="关联的应用用户",
        on_delete=fields.SET_NULL
    )
    name = fields.CharField(max_length=128, description="姓名")
    gender = fields.CharField(max_length=16, description="性别")
    birth_date = fields.DateField(description="出生日期")
    metadata = fields.JSONField(null=True, description="灵活字段")

    class Meta:
        table = "health_profiles"


class Device(BaseModel, TimestampMixin):
    """设备模型"""
    serial_number = fields.CharField(max_length=64, unique=True, description="设备唯一标识")
    name = fields.CharField(max_length=128, description="设备名称")
    device_type = fields.CharField(max_length=64, description="设备类型", index=True)
    is_active = fields.BooleanField(default=True, description="激活状态")

    class Meta:
        table = "devices"


class DeviceAssignment(BaseModel):
    """设备分配模型"""
    device = fields.ForeignKeyField(
        "models.Device",
        related_name="assignments",
        description="设备",
        on_delete=fields.CASCADE
    )
    health_profile = fields.ForeignKeyField(
        "models.HealthProfile",
        related_name="device_assignments",
        description="健康档案",
        on_delete=fields.CASCADE
    )
    assigned_at = fields.DatetimeField(auto_now_add=True, description="分配时间")
    unassigned_at = fields.DatetimeField(null=True, description="解除分配时间")

    class Meta:
        table = "device_assignments"


class HealthDataRecord(BaseModel, TimestampMixin):
    """健康数据记录模型"""
    health_profile = fields.ForeignKeyField(
        "models.HealthProfile",
        related_name="health_records",
        description="健康档案",
        on_delete=fields.CASCADE
    )
    device = fields.ForeignKeyField(
        "models.Device",
        related_name="health_records",
        null=True,
        description="设备",
        on_delete=fields.SET_NULL
    )
    schema_type = fields.CharField(max_length=64, description="数据类型")
    recorded_at = fields.DatetimeField(description="记录时间")
    payload = fields.JSONField(description="数据载荷")

    class Meta:
        table = "health_data_records"


class Event(BaseModel, TimestampMixin):
    """事件模型"""
    event_type = fields.CharField(max_length=64, description="事件类型")
    health_profile = fields.ForeignKeyField(
        "models.HealthProfile",
        related_name="events",
        description="健康档案",
        on_delete=fields.CASCADE
    )
    device = fields.ForeignKeyField(
        "models.Device",
        related_name="events",
        null=True,
        description="设备",
        on_delete=fields.SET_NULL
    )
    source_record = fields.ForeignKeyField(
        "models.HealthDataRecord",
        related_name="events",
        null=True,
        description="来源健康数据",
        on_delete=fields.SET_NULL
    )
    timestamp = fields.DatetimeField(description="事件时间")
    data = fields.JSONField(description="事件数据")
    metadata = fields.JSONField(null=True, description="元数据")

    class Meta:
        table = "events"


class Alert(BaseModel):
    """告警模型"""
    health_profile = fields.ForeignKeyField(
        "models.HealthProfile",
        related_name="alerts",
        null=True,
        description="健康档案",
        on_delete=fields.SET_NULL
    )
    device = fields.ForeignKeyField(
        "models.Device",
        related_name="alerts",
        null=True,
        description="设备",
        on_delete=fields.SET_NULL
    )
    source_event = fields.ForeignKeyField(
        "models.Event",
        related_name="alerts",
        null=True,
        description="来源事件",
        on_delete=fields.SET_NULL
    )
    rule_name = fields.CharField(max_length=128, description="规则名称")
    level = fields.CharField(max_length=32, description="告警级别")
    message = fields.TextField(description="告警消息")
    event_type = fields.CharField(max_length=64, description="事件类型")
    description = fields.TextField(description="详细描述")
    extra = fields.JSONField(description="额外信息")
    status = fields.CharField(max_length=32, description="告警状态")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    resolved_at = fields.DatetimeField(null=True, description="解决时间")

    class Meta:
        table = "alerts"