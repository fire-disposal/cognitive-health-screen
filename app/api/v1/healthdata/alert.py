import logging
from typing import List, Optional
from fastapi import APIRouter, Query, Body, Path, HTTPException

from app.controllers.health.alert import alert_controller
from app.schemas.base import SuccessResponse, PaginatedResponse
from app.schemas.health.alert import AlertCreate, AlertUpdate

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/alerts", summary="分页/过滤/查询告警列表")
async def list_alerts(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    device_id: Optional[int] = Query(None, description="设备ID"),
    patient_id: Optional[int] = Query(None, description="患者ID"),
    status: Optional[str] = Query(None, description="告警状态"),
    level: Optional[str] = Query(None, description="告警级别"),
    rule_name: Optional[str] = Query(None, description="告警规则名"),
    order_by: str = Query("-created_at", description="排序字段"),
):
    filters = {
        "device_id": device_id,
        "patient_id": patient_id,
        "status": status,
        "level": level,
        "rule_name": rule_name,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    result = await alert_controller.list(
        filters=filters,
        skip=(page - 1) * page_size,
        limit=page_size,
        order_by=order_by,
    )
    return PaginatedResponse(
        data=[await obj.to_dict() for obj in result["items"]],
        total=result["total"],
        page=page,
        page_size=page_size,
    )

@router.get("/alerts/statistics", summary="获取告警统计信息")
async def get_alert_statistics():
    stats = await alert_controller.statistics()
    return SuccessResponse(data=stats)

@router.get("/alerts/{alert_id}", summary="获取告警详情")
async def get_alert(
    alert_id: int = Path(..., description="告警ID"),
):
    obj = await alert_controller.get(id=alert_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Alert not found")
    return SuccessResponse(data=await obj.to_dict())

@router.post("/alerts", summary="创建告警")
async def create_alert(
    alert_in: AlertCreate,
):
    obj = await alert_controller.create(obj_in=alert_in)
    return SuccessResponse(data=await obj.to_dict())

@router.put("/alerts/{alert_id}", summary="更新告警")
async def update_alert(
    alert_id: int = Path(..., description="告警ID"),
    alert_in: AlertUpdate = Body(...),
):
    updated = await alert_controller.update(id=alert_id, obj_in=alert_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Alert not found")
    return SuccessResponse(msg="Updated Successfully")

@router.delete("/alerts/{alert_id}", summary="删除告警")
async def delete_alert(
    alert_id: int = Path(..., description="告警ID"),
):
    deleted = await alert_controller.remove(id=alert_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Alert not found")
    return SuccessResponse(msg="Deleted Successfully")