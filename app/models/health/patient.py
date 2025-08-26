from tortoise import fields

from app.models.base import BaseModel, TimestampMixin


class Patient(BaseModel):
    name = fields.CharField(max_length=64)
    age = fields.IntField()
    gender = fields.CharField(max_length=10)  # 或使用 GenderEnum
    status = fields.CharField(max_length=16, default="active", description="患者状态")

    def __str__(self):
        return f"{self.name} ({self.id})"
