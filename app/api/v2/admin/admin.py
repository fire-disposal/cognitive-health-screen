from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from app.models.users import AdminUser
from app.schemas.users import AdminUserCreate, AdminUserUpdate, AdminUserResponse, AppUserCreate, AppUserUpdate, AppUserResponse
from app.utils.password import get_password_hash
from app.api.v2.auth import verify_admin_token, AdminTokenData
import jwt
from fastapi import Request
from app.settings import settings
from app.schemas.auth import TokenData

def get_current_admin_user(request: Request) -> TokenData:
    """从请求头解析并校验管理员JWT，返回TokenData"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="缺少或无效的认证信息"
        )
    token = auth_header.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("user_type") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="非管理员token"
            )
        return TokenData(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token已过期"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的Token"
        )

admin_router = APIRouter(prefix="/", tags=["管理员用户管理"])

class AdminResponse(BaseModel):
    """管理员信息响应模型"""
    id: int
    username: str
    role: Optional[str] = None
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime

class AdminListResponse(BaseModel):
    """管理员列表响应模型"""
    total: int
    items: List[AdminResponse]

@admin_router.get("", summary="获取管理员列表", response_model=AdminListResponse)
async def list_admins(
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    username: Optional[str] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(20, gt=0, le=100),
    token_data: TokenData = Depends(get_current_admin_user)
):
    """获取管理员列表（需要超级管理员权限）"""
    query = AdminUser.all()
    
    # 应用筛选条件
    if role:
        query = query.filter(role=role)
    if is_active is not None:
        query = query.filter(is_active=is_active)
    if username:
        query = query.filter(username__icontains=username)
    
    # 计算总数
    total = await query.count()
    
    # 分页查询
    users = await query.offset((page - 1) * page_size).limit(page_size).order_by("-created_at")
    
    return AdminListResponse(
        total=total,
        items=[AdminResponse(**user.__dict__) for user in users]
    )

@admin_router.post("", summary="创建管理员", response_model=AdminResponse)
async def create_admin(
    user_create: AdminUserCreate,
    token_data: TokenData = Depends(get_current_admin_user)
):
    """创建新管理员（需要超级管理员权限）"""
    # 检查用户名是否已存在
    if await AdminUser.filter(username=user_create.username).exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 创建新管理员
    user = await AdminUser.create(
        username=user_create.username,
        password_hash=get_password_hash(user_create.password),
        role=user_create.role,
        is_active=True,
        created_at=datetime.now(timezone.utc)
    )
    
    return AdminResponse(**user.__dict__)

@admin_router.get("/{user_id}", summary="获取管理员信息", response_model=AdminResponse)
async def get_admin(
    user_id: int,
    token_data: TokenData = Depends(get_current_admin_user)
):
    """获取指定管理员信息"""
    user = await AdminUser.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 普通管理员只能查看自己的信息
    if token_data.role != "super_admin" and user_id != token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限查看其他管理员信息"
        )
    
    return AdminResponse(**user.__dict__)

@admin_router.put("/{user_id}", summary="更新管理员信息", response_model=AdminResponse)
async def update_admin(
    user_id: int,
    user_update: AdminUserUpdate,
    token_data: TokenData = Depends(get_current_admin_user)
):
    """更新管理员信息"""
    user = await AdminUser.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 权限检查
    is_self = user_id == token_data.user_id
    is_super_admin = token_data.role == "super_admin"
    
    if not (is_self or is_super_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权限修改其他管理员信息"
        )
    
    # 非超级管理员不能修改角色和状态
    if not is_super_admin:
        if user_update.role is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限修改角色"
            )
        if user_update.is_active is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限修改账号状态"
            )
    
    # 更新信息
    update_data = {}
    if user_update.password:
        update_data["password_hash"] = get_password_hash(user_update.password)
    if user_update.role is not None and is_super_admin:
        update_data["role"] = user_update.role
    if user_update.is_active is not None and is_super_admin:
        update_data["is_active"] = user_update.is_active
    
    if update_data:
        await user.update_from_dict(update_data).save()
    
    return AdminResponse(**user.__dict__)

@admin_router.post("/{user_id}/reset-password", summary="重置管理员密码")
async def reset_admin_password(
    user_id: int,
    new_password: str = Field(..., min_length=6),
    token_data: TokenData = Depends(get_current_admin_user)
):
    """重置管理员密码（需要超级管理员权限）"""
    user = await AdminUser.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 不能重置自己的密码（应该使用修改密码接口）
    if user_id == token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能通过此接口重置自己的密码"
        )
    
    # 更新密码
    user.password_hash = get_password_hash(new_password)
    await user.save()
    return {"message": "密码重置成功"}

@admin_router.delete("/{user_id}", summary="删除管理员")
async def delete_admin(
    user_id: int,
    token_data: AdminTokenData = Depends(lambda: verify_admin_token(required_role="super_admin"))
):
    """删除管理员（需要超级管理员权限）"""
    user = await AdminUser.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 不能删除自己
    if user_id == token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除自己的账号"
        )
    
    # 删除用户
    await user.delete()
    return {"message": "删除成功"}