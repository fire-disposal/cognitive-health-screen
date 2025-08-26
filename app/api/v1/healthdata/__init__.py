from fastapi import APIRouter

from .datasheet import router as datasheet_router
from .device import router as device_router
from .patient import router as patient_router
from .devicegroup import router as devicegroup_router
from .event import router as advancedrecord_router
from .alert import router as alert_router

from .upload import router as upload_router

health_data_router = APIRouter()
health_data_router.include_router(datasheet_router, tags=["健康数据模块"])
health_data_router.include_router(device_router, tags=["健康设备模块"])
health_data_router.include_router(devicegroup_router, tags=["设备分组模块"])
health_data_router.include_router(patient_router, tags=["健康患者模块"])
health_data_router.include_router(advancedrecord_router, tags=["高级健康数据模块"])
health_data_router.include_router(alert_router, tags=["告警管理模块"])
health_data_router.include_router(upload_router, tags=["健康数据上传"])

__all__ = ["health_data_router"]