from tortoise import fields, models
from tortoise.models import Model

class ChatSession(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(index=True)
    patient_id = fields.IntField(index=True)
    title = fields.CharField(max_length=128, default="")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class ChatRecord(Model):
    id = fields.IntField(pk=True)
    session = fields.ForeignKeyField("models.ChatSession", related_name="records")
    user_id = fields.IntField(index=True)
    patient_id = fields.IntField(index=True)
    role = fields.CharField(max_length=16)  # user/assistant
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)