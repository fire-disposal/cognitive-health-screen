from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.health.healthdatarecord import HealthDataRecord


HealthDataRecordBase = pydantic_model_creator(
    HealthDataRecord,
    name="HealthDataRecordBase",
    exclude=("created_at", "updated_at", "deleted_at")
)

# 创建数据记录时的验证模型
class HealthDataRecordCreate(BaseModel):
    patient_id: int = Field(..., description="患者ID（int主键）")
    recorded_at: datetime = Field(..., description="数据记录时间")
    schema_type: str = Field(..., max_length=64, description="数据类型（如 heart_rate、sleep 等）")
    payload: Dict[str, Any] = Field(..., description="原始数据载荷")

# 更新数据记录时的验证模型
class HealthDataRecordUpdate(BaseModel):
    recorded_at: Optional[datetime] = Field(None, description="数据记录时间")
    schema_type: Optional[str] = Field(None, max_length=64, description="数据类型")
    payload: Optional[Dict[str, Any]] = Field(None, description="原始数据载荷")

# 输出数据记录信息的验证模型（包含关联的设备和患者信息）
HealthDataRecordOut = pydantic_model_creator(
    HealthDataRecord,
    name="HealthDataRecordOut",
    exclude=("deleted_at",)
)

# 简化的数据记录信息输出模型（不包含关联信息）
HealthDataRecordSimpleOut = pydantic_model_creator(
    HealthDataRecord,
    name="HealthDataRecordSimpleOut",
    exclude=("deleted_at", "device", "patient")
)

__all__ = [
    "HealthDataRecordBase",
    "HealthDataRecordCreate",
    "HealthDataRecordUpdate",
    "HealthDataRecordOut",
    "HealthDataRecordSimpleOut",
]