from typing import Dict, Optional


from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.health.device import Device

# 使用Tortoise的pydantic生成器创建基础模型
DeviceBase = pydantic_model_creator(
    Device,
    name="DeviceBase",
    exclude=("created_at", "updated_at", "deleted_at")
)

# 创建设备时的验证模型
class DeviceCreate(BaseModel):
    device_id: str = Field(..., min_length=1, max_length=128, description="设备唯一标识")
    name: Optional[str] = Field(None, max_length=64, description="设备昵称")
    description: Optional[str] = Field(None, description="设备描述")
    current_patient_id: Optional[int] = Field(None, description="当前绑定的患者ID（int）")
    data_types: Optional[list[str]] = Field(
        None, description="设备支持的健康数据类型（如 heartrate, spo2, temperature 等）"
    )


# 更新设备信息时的验证模型
class DeviceUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=64, description="设备昵称")
    description: Optional[str] = Field(None, description="设备描述")
    current_patient_id: Optional[int] = Field(None, description="当前绑定的患者ID（int）")

# 输出设备信息的验证模型（包含关联的患者信息）
DeviceOut = pydantic_model_creator(
    Device,
    name="DeviceOut",
    exclude=("deleted_at",)
)

# 简化的设备信息输出模型（不包含关联信息）
DeviceSimpleOut = pydantic_model_creator(
    Device,
    name="DeviceSimpleOut",
    exclude=("deleted_at", "current_patient", "bindings", "data_records")
)

__all__ = [
    "DeviceBase",
    "DeviceCreate",
    "DeviceUpdate",
    "DeviceOut",
    "DeviceSimpleOut",
]