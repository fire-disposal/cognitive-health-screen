from typing import Optional

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.health.patient import Patient

# 使用Tortoise的pydantic生成器创建基础模型
PatientBase = pydantic_model_creator(
    Patient,
    name="PatientBase",
    exclude=("created_at", "updated_at", "deleted_at")
)

# 创建患者时的验证模型
class PatientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=64, description="患者姓名")
    age: int = Field(..., ge=0, le=150, description="患者年龄")
    gender: str = Field(..., pattern="^(male|female|other)$", description="患者性别")

# 更新患者信息时的验证模型
class PatientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=64, description="患者姓名")
    age: Optional[int] = Field(None, ge=0, le=150, description="患者年龄")
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$", description="患者性别")

# 输出患者信息的验证模型
PatientResponse = pydantic_model_creator(
    Patient,
    name="PatientResponse",
    exclude=("deleted_at",)
)

__all__ = [
    "PatientBase",
    "PatientCreate",
    "PatientUpdate",
    "PatientResponse",
]