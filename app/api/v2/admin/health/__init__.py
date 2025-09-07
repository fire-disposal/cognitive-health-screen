from fastapi import APIRouter

from .alert import router as alert_router
from .datasheet import router as datasheet_router
from .device import router as device_router
from .patient import router as patient_router
from .devicegroup import router as devicegroup_router
from .event import router as event_router

health_admin_router = APIRouter(prefix="/api/v2/admin/health", tags=["健康数据管理"])

health_admin_router.include_router(alert_router)
health_admin_router.include_router(datasheet_router)
health_admin_router.include_router(device_router)
health_admin_router.include_router(patient_router)
health_admin_router.include_router(devicegroup_router)
health_admin_router.include_router(event_router)

__all__ = ["health_admin_router"]