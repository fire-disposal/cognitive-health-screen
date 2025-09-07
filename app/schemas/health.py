from typing import Optional, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.health import (
    HealthProfile, Device, DeviceAssignment,
    HealthDataRecord, Event, Alert
)

# HealthProfile验证模型
HealthProfileBase = pydantic_model_creator(
    HealthProfile,
    name="HealthProfileBase",
    exclude=("created_at", "updated_at")
)

class HealthProfileCreate(BaseModel):
    user_id: Optional[int] = Field(None, description="用户ID")
    name: str = Field(..., min_length=1, max_length=128, description="姓名")
    gender: str = Field(..., pattern="^(male|female|other)$", description="性别")
    birth_date: date = Field(..., description="出生日期")
    metadata: Optional[Dict[str, Any]] = Field(None, description="灵活字段")

class HealthProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=128, description="姓名")
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$", description="性别")
    birth_date: Optional[date] = Field(None, description="出生日期")
    metadata: Optional[Dict[str, Any]] = Field(None, description="灵活字段")

# Device验证模型
DeviceBase = pydantic_model_creator(
    Device,
    name="DeviceBase",
    exclude=("created_at", "updated_at")
)

class DeviceCreate(BaseModel):
    serial_number: str = Field(..., max_length=64, description="设备唯一标识")
    name: str = Field(..., max_length=128, description="设备名称")
    device_type: str = Field(..., max_length=64, description="设备类型")
    is_active: bool = Field(True, description="激活状态")

class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=128, description="设备名称")
    device_type: Optional[str] = Field(None, max_length=64, description="设备类型")
    is_active: Optional[bool] = Field(None, description="激活状态")

# DeviceAssignment验证模型
class DeviceAssignmentCreate(BaseModel):
    device_id: int = Field(..., description="设备ID")
    health_profile_id: int = Field(..., description="健康档案ID")

class DeviceAssignmentUpdate(BaseModel):
    unassigned_at: Optional[datetime] = Field(None, description="解除分配时间")

# HealthDataRecord验证模型
class HealthDataRecordCreate(BaseModel):
    health_profile_id: int = Field(..., description="健康档案ID")
    device_id: Optional[int] = Field(None, description="设备ID")
    schema_type: str = Field(..., max_length=64, description="数据类型")
    recorded_at: datetime = Field(..., description="记录时间")
    payload: Dict[str, Any] = Field(..., description="数据载荷")

class HealthDataRecordUpdate(BaseModel):
    schema_type: Optional[str] = Field(None, max_length=64, description="数据类型")
    recorded_at: Optional[datetime] = Field(None, description="记录时间")
    payload: Optional[Dict[str, Any]] = Field(None, description="数据载荷")

# Event验证模型
class EventCreate(BaseModel):
    event_type: str = Field(..., max_length=64, description="事件类型")
    health_profile_id: int = Field(..., description="健康档案ID")
    device_id: Optional[int] = Field(None, description="设备ID")
    source_record_id: Optional[int] = Field(None, description="来源健康数据ID")
    timestamp: datetime = Field(..., description="事件时间")
    data: Dict[str, Any] = Field(..., description="事件数据")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")

class EventUpdate(BaseModel):
    event_type: Optional[str] = Field(None, max_length=64, description="事件类型")
    timestamp: Optional[datetime] = Field(None, description="事件时间")
    data: Optional[Dict[str, Any]] = Field(None, description="事件数据")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")

# Alert验证模型
class AlertCreate(BaseModel):
    health_profile_id: Optional[int] = Field(None, description="健康档案ID")
    device_id: Optional[int] = Field(None, description="设备ID")
    source_event_id: Optional[int] = Field(None, description="来源事件ID")
    rule_name: str = Field(..., max_length=128, description="规则名称")
    level: str = Field(..., max_length=32, description="告警级别")
    message: str = Field(..., description="告警消息")
    event_type: str = Field(..., max_length=64, description="事件类型")
    description: str = Field(..., description="详细描述")
    extra: Dict[str, Any] = Field(..., description="额外信息")
    status: str = Field(..., max_length=32, description="告警状态")

class AlertUpdate(BaseModel):
    rule_name: Optional[str] = Field(None, max_length=128, description="规则名称")
    level: Optional[str] = Field(None, max_length=32, description="告警级别")
    message: Optional[str] = Field(None, description="告警消息")
    description: Optional[str] = Field(None, description="详细描述")
    extra: Optional[Dict[str, Any]] = Field(None, description="额外信息")
    status: Optional[str] = Field(None, max_length=32, description="告警状态")
    resolved_at: Optional[datetime] = Field(None, description="解决时间")

# Response模型
HealthProfileResponse = pydantic_model_creator(
    HealthProfile,
    name="HealthProfileResponse"
)

DeviceResponse = pydantic_model_creator(
    Device,
    name="DeviceResponse"
)

DeviceAssignmentResponse = pydantic_model_creator(
    DeviceAssignment,
    name="DeviceAssignmentResponse"
)

HealthDataRecordResponse = pydantic_model_creator(
    HealthDataRecord,
    name="HealthDataRecordResponse"
)

EventResponse = pydantic_model_creator(
    Event,
    name="EventResponse"
)

AlertResponse = pydantic_model_creator(
    Alert,
    name="AlertResponse"
)

__all__ = [
    "HealthProfileBase",
    "HealthProfileCreate",
    "HealthProfileUpdate",
    "HealthProfileResponse",
    "DeviceBase",
    "DeviceCreate",
    "DeviceUpdate",
    "DeviceResponse",
    "DeviceAssignmentCreate",
    "DeviceAssignmentUpdate",
    "DeviceAssignmentResponse",
    "HealthDataRecordCreate",
    "HealthDataRecordUpdate",
    "HealthDataRecordResponse",
    "EventCreate",
    "EventUpdate",
    "EventResponse",
    "AlertCreate",
    "AlertUpdate",
    "AlertResponse",
]