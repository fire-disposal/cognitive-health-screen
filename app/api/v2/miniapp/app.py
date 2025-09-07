from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from app.models.admin import AppUser, AuditLog
from app.schemas.users import AppUserCreate, AppUserUpdate, AppUserResponse
from app.utils.password import get_password_hash
from app.api.v2.auth import verify_app_token, verify_admin_token
from app.schemas.auth import TokenData

app_router = APIRouter(prefix="/", tags=["小程序用户管理"])

class AppUserResponse(BaseModel):
    """小程序用户信息响应模型"""
    id: int
    username: str
    mobile: Optional[str] = None
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    device_id: Optional[str] = None

class AppUserListResponse(BaseModel):
    """小程序用户列表响应模型"""
    total: int
    items: List[AppUserResponse]

@app_router.get("/users", summary="获取小程序用户列表", response_model=AppUserListResponse)
async def list_app_users(
    mobile: Optional[str] = None,
    is_active: Optional[bool] = None,
    username: Optional[str] = None,
    has_device: Optional[bool] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    token_data: TokenData = Depends(verify_admin_token)
):
    """获取小程序用户列表（管理员访问）"""
    query = AppUser.all()
    
    # 应用筛选条件
    if mobile:
        query = query.filter(mobile__icontains=mobile)
    if is_active is not None:
        query = query.filter(is_active=is_active)
    if username:
        query = query.filter(username__icontains=username)
    if has_device is not None:
        if has_device:
            query = query.filter(device_id__isnull=False)
        else:
            query = query.filter(device_id__isnull=True)
    
    # 计算总数
    total = await query.count()
    
    # 分页查询
    users = await query.offset((page - 1) * page_size).limit(page_size).order_by("-created_at")
    
    return AppUserListResponse(
        total=total,
        items=[AppUserResponse(**user.__dict__) for user in users]
    )

@app_router.post("/users", summary="创建小程序用户", response_model=AppUserResponse)
async def create_app_user(
    user_create: AppUserCreate,
    token_data: TokenData = Depends(verify_admin_token)
):
    """创建新的小程序用户（管理员权限）"""
    # 检查用户名是否已存在
    if await AppUser.filter(username=user_create.username).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 创建新用户
    user = await AppUser.create(
        username=user_create.username,
        password_hash=get_password_hash(user_create.password),
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    
    return AppUserResponse(**user.__dict__)

@app_router.get("/users/{user_id}", summary="获取小程序用户信息", response_model=AppUserResponse)
async def get_app_user(
    user_id: int,
    token_data: TokenData = Depends(verify_admin_token)
):
    """获取指定小程序用户信息（管理员权限）"""
    user = await AppUser.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return AppUserResponse(**user.__dict__)

@app_router.put("/users/{user_id}", summary="更新小程序用户信息", response_model=AppUserResponse)
async def update_app_user(
    user_id: int,
    user_update: AppUserUpdate,
    token_data: TokenData = Depends(verify_admin_token)
):
    """更新小程序用户信息（管理员权限）"""
    user = await AppUser.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 更新信息
    update_data = {}
    if user_update.password:
        update_data["password_hash"] = get_password_hash(user_update.password)
    if user_update.is_active is not None:
        update_data["is_active"] = user_update.is_active
    
    if update_data:
        await user.update_from_dict(update_data).save()
    
    return AppUserResponse(**user.__dict__)

@app_router.post("/users/{user_id}/reset-password", summary="重置小程序用户密码")
async def reset_app_user_password(
    user_id: int,
    new_password: str = Field(..., min_length=6),
    token_data: TokenData = Depends(verify_admin_token)
):
    """重置小程序用户密码（管理员权限）"""
    user = await AppUser.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 更新密码
    user.password_hash = get_password_hash(new_password)
    await user.save()
    
    return {"message": "密码重置成功"}

@app_router.post("/users/{user_id}/bind-device", summary="绑定设备")
async def bind_device(
    user_id: int,
    device_id: str,
    token_data: TokenData = Depends(verify_admin_token)
):
    """绑定设备到小程序用户（管理员权限）"""
    user = await AppUser.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 检查设备是否已被其他用户绑定
    if await AppUser.filter(device_id=device_id).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该设备已被其他用户绑定"
        )
    
    user.device_id = device_id
    await user.save()
    
    return {"message": "设备绑定成功"}

@app_router.delete("/users/{user_id}/unbind-device", summary="解绑设备")
async def unbind_device(
    user_id: int,
    token_data: TokenData = Depends(verify_admin_token)
):
    """解绑小程序用户的设备（管理员权限）"""
    user = await AppUser.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    if not user.device_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未绑定设备"
        )
    
    device_id = user.device_id
    user.device_id = None
    await user.save()
    
    return {"message": "设备解绑成功"}

# 小程序用户自己访问的接口
@app_router.get("/profile", summary="获取个人信息", response_model=AppUserResponse)
async def get_profile(token_data: TokenData = Depends(verify_app_token)):
    """获取小程序用户自己的信息"""
    user = await AppUser.filter(id=token_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return AppUserResponse(**user.__dict__)

@app_router.put("/profile", summary="更新个人信息", response_model=AppUserResponse)
async def update_profile(
    new_password: Optional[str] = None,
    token_data: TokenData = Depends(verify_app_token)
):
    """更新小程序用户自己的信息"""
    user = await AppUser.filter(id=token_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    if new_password:
        if len(new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="密码长度不能小于6位"
            )
        user.password_hash = get_password_hash(new_password)
        await user.save()
    
    return AppUserResponse(**user.__dict__)