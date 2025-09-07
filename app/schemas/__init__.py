"""
Root schemas package
"""

from app.schemas.users import (
    AdminUserBase, AdminUserCreate, AdminUserUpdate, AdminUserResponse,
    AppUserBase, AppUserCreate, AppUserUpdate, AppUserResponse,
)

from app.schemas.health import (
    HealthProfileBase, HealthProfileCreate, HealthProfileUpdate, HealthProfileResponse,
    DeviceBase, DeviceCreate, DeviceUpdate, DeviceResponse,
    DeviceAssignmentCreate, DeviceAssignmentUpdate, DeviceAssignmentResponse,
    HealthDataRecordCreate, HealthDataRecordUpdate, HealthDataRecordResponse,
    EventCreate, EventUpdate, EventResponse,
    AlertCreate, AlertUpdate, AlertResponse,
)

from app.schemas.auth import (
    LoginBase, TokenData, TokenResponse,
    AdminLogin, AppLogin, WechatLogin,
)

__all__ = [
    # User Schemas
    "AdminUserBase",
    "AdminUserCreate",
    "AdminUserUpdate", 
    "AdminUserResponse",
    "AppUserBase",
    "AppUserCreate",
    "AppUserUpdate",
    "AppUserResponse",
    
    # Health Schemas
    "HealthProfileBase",
    "HealthProfileCreate",
    "HealthProfileUpdate",
    "HealthProfileResponse",
    "DeviceBase",
    "DeviceCreate",
    "DeviceUpdate", 
    "DeviceResponse",
    "DeviceAssignmentCreate",
    "DeviceAssignmentUpdate",
    "DeviceAssignmentResponse",
    "HealthDataRecordCreate",
    "HealthDataRecordUpdate",
    "HealthDataRecordResponse",
    "EventCreate",
    "EventUpdate",
    "EventResponse",
    "AlertCreate",
    "AlertUpdate",
    "AlertResponse",

    # Auth Schemas
    "LoginBase",
    "TokenData",
    "TokenResponse",
    "AdminLogin",
    "AppLogin",
    "WechatLogin",
]
