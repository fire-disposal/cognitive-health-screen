from datetime import datetime, timedelta, timezone

from fastapi import APIRouter

from app.controllers.api import api_controller
from app.controllers.menu import menu_controller
from app.controllers.user import user_controller
from app.core.ctx import CTX_USER_ID
from app.core.dependency import DependAuth
from app.models.admin import User
from app.schemas.base import FailResponse, SuccessResponse
from app.schemas.system.login import *
from app.schemas.system.user import (
    PasswordUpdate, UserRegister,
    ThemeUpdate, LogoUpdate
)
from app.settings import settings
from app.utils.jwt_utils import create_access_token
from app.utils.password import verify_password

router = APIRouter()


@router.post("/access_token", summary="获取token")
async def login_access_token(credentials: LoginForm):
    user: User = await user_controller.authenticate(credentials)
    await user_controller.update_last_login(user.id)
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires

    data = TokenResponse(
        access_token=create_access_token(
            data=TokenData(
                user_id=user.id,
                username=user.username,
                is_superuser=user.is_superuser,
                exp=expire,
            )
        ),
        expires_in=int(access_token_expires.total_seconds()),
    )
    return SuccessResponse(data=data.model_dump())


@router.get("/userinfo", summary="查看用户信息", dependencies=[DependAuth])
async def get_userinfo():
    user_id = CTX_USER_ID.get()
    user_obj = await user_controller.get(id=user_id)
    data = await user_obj.to_dict(exclude_fields=["password"])
    data["avatar"] = "https://avatars.githubusercontent.com/u/54677442?v=4"
    return SuccessResponse(data=data)


@router.get("/usermenu", summary="查看用户菜单", dependencies=[DependAuth])
async def get_user_menu():
    user_id = CTX_USER_ID.get()
    user_obj = await user_controller.get(id=user_id)
    menus = await menu_controller.get_user_menus(user_obj)
    return SuccessResponse(data=menus)


@router.get("/userapi", summary="查看用户API", dependencies=[DependAuth])
async def get_user_api():
    user_id = CTX_USER_ID.get()
    user_obj = await user_controller.get(id=user_id)
    apis = await api_controller.get_user_apis(user_obj)
    return SuccessResponse(data=apis)


@router.post("/update_password", summary="修改密码", dependencies=[DependAuth])
async def update_user_password(req_in: PasswordUpdate):
    user_id = CTX_USER_ID.get()
    user = await user_controller.get(user_id)
    verified = verify_password(req_in.old_password, user.password)
    if not verified:
        return FailResponse(msg="旧密码验证错误！")
    await user_controller.update_password(user_id, req_in.new_password)
    return SuccessResponse(msg="修改成功")


@router.post("/register", summary="用户注册", dependencies=[])
async def register_user(
    user_in: UserRegister,
):
    user = await user_controller.get_by_email(user_in.email)
    if user:
        return FailResponse(code=400, msg="The user with this email already exists in the system.")
    return SuccessResponse(msg="Registered Successfully")


@router.post("/update_theme", summary="更新主题配置", dependencies=[DependAuth])
async def update_user_theme(theme_update: ThemeUpdate):
    """
    更新用户主题配置
    支持的主题: blue, red, green, purple
    """
    user_id = CTX_USER_ID.get()
    await user_controller.update_theme(user_id=user_id, theme=theme_update.theme)
    return SuccessResponse(msg="主题配置已更新")


@router.post("/update_logo", summary="更新Logo类型", dependencies=[DependAuth])
async def update_user_logo(logo_update: LogoUpdate):
    """
    更新用户Logo类型
    支持的类型: type1, type2
    """
    user_id = CTX_USER_ID.get()
    await user_controller.update_logo_type(user_id=user_id, logo_type=logo_update.logo_type)
    return SuccessResponse(msg="Logo类型已更新")
