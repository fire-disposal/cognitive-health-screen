from datetime import datetime
from typing import List, Optional

from fastapi.exceptions import HTTPException

from app.core.crud import CRUDBase
from app.models.admin import User
from app.schemas.system.login import LoginForm
from app.schemas.system.user import (
    UserCreate, UserRegister, UserUpdate
)
from app.utils.password import get_password_hash, verify_password

from .role import role_controller


class UserController(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(model=User)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.model.filter(email=email).first()

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.model.filter(username=username).first()

    async def create_user(self, obj_in: UserCreate) -> User:
        obj_in.password = get_password_hash(password=obj_in.password)
        obj = await self.create(obj_in)
        return obj

    async def update_last_login(self, id: int) -> None:
        user = await self.model.get(id=id)
        user.last_login = datetime.now()
        await user.save()

    async def authenticate(self, credentials: LoginForm) -> Optional["User"]:
        user = await self.model.filter(username=credentials.username).first()
        if not user:
            raise HTTPException(status_code=400, detail="无效的用户名")
        verified = verify_password(credentials.password, user.password)
        if not verified:
            raise HTTPException(status_code=400, detail="密码错误!")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="用户已被禁用")
        return user

    async def update_roles(self, user: User, role_ids: List[int]) -> None:
        await user.roles.clear()
        for role_id in role_ids:
            role_obj = await role_controller.get(id=role_id)
            await user.roles.add(role_obj)

    async def reset_password(self, user_id: int):
        user_obj = await self.get(id=user_id)
        if user_obj.is_superuser:
            raise HTTPException(status_code=403, detail="不允许重置超级管理员密码")
        user_obj.password = get_password_hash(password="123456")
        await user_obj.save()
    
    async def update_password(self, user_id: int, new_password: str) -> None:
        """更新用户密码"""
        user_obj = await self.get(id=user_id)
        user_obj.password = get_password_hash(password=new_password)
        await user_obj.save()

    async def update_theme(self, user_id: int, theme: str) -> None:
        """
        更新用户主题颜色
        Args:
            user_id: 用户ID
            theme: 主题颜色
        """
        user_obj = await self.get(id=user_id)
        user_obj.theme = theme
        await user_obj.save()

    async def update_logo_type(self, user_id: int, logo_type: str) -> None:
        """
        更新用户Logo类型
        Args:
            user_id: 用户ID
            logo_type: Logo类型
        """
        user_obj = await self.get(id=user_id)
        user_obj.logo_type = logo_type
        await user_obj.save()


user_controller = UserController()
