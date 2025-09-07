from tortoise import fields
from app.models.base import BaseModel, TimestampMixin


class AdminUser(BaseModel, TimestampMixin):
    """管理员用户模型"""
    username = fields.CharField(max_length=64, unique=True, description="用户名")
    email = fields.CharField(max_length=128, null=True, description="邮箱")
    phone = fields.CharField(max_length=32, null=True, description="手机号")
    password_hash = fields.CharField(max_length=256, description="密码哈希")
    role = fields.CharField(max_length=32, null=True, description="角色")
    is_active = fields.BooleanField(default=True, description="是否激活")
    last_login = fields.DatetimeField(null=True, description="最后登录时间")

    class Meta:
        table = "admin_users"
        default_connection = "postgres"
        abstract = False


class AppUser(BaseModel, TimestampMixin):
    """应用用户模型"""
    username = fields.CharField(max_length=64, unique=True, description="用户名")
    email = fields.CharField(max_length=128, null=True, description="邮箱")
    phone = fields.CharField(max_length=32, null=True, description="手机号")
    password_hash = fields.CharField(max_length=256, description="密码哈希")
    is_active = fields.BooleanField(default=True, description="是否激活")
    last_login = fields.DatetimeField(null=True, description="最后登录时间")
    wechat_openid = fields.CharField(max_length=128, null=True, description="微信OpenID")

    class Meta:
        table = "app_users"
        default_connection = "postgres"
        abstract = False