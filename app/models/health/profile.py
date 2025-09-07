from tortoise import fields
from app.models.base import BaseModel

class HealthProfile(BaseModel):
    user_id = fields.IntField(null=True, description="用户ID", index=True)
    name = fields.CharField(max_length=128, description="姓名")
    gender = fields.CharField(max_length=16, null=True, description="性别")
    birth_date = fields.DateField(null=True, description="出生日期")
    metadata = fields.JSONField(null=True, description="灵活字段")
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True, index=True)

    class Meta:
        table = "health_profiles"
        indexes = [
            ("user_id",),
        ]