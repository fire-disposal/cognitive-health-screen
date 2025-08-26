import logging
from typing import List, Optional
from fastapi import APIRouter, Query, Body, Path, HTTPException

from app.controllers.health.event import event_controller
from app.schemas.base import SuccessResponse, PaginatedResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/events/statistics", summary="获取健康事件统计信息")
async def get_event_statistics():
    stats = await event_controller.statistics()
    return SuccessResponse(data=stats)

@router.get("/events", summary="分页/过滤/搜索健康事件列表")
async def list_events(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    device_id: Optional[str] = Query(None, description="设备ID"),
    patient_id: Optional[str] = Query(None, description="患者ID"),
    event_type: Optional[str] = Query(None, description="事件类型"),
    order_by: str = Query("-timestamp", description="排序字段"),
):
    filters = {
        "device_id": device_id,
        "patient_id": patient_id,
        "event_type": event_type,
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    result = await event_controller.list(
        filters=filters,
        skip=(page - 1) * page_size,
        limit=page_size,
        order_by=order_by
    )
    return PaginatedResponse(
        data=[await obj.to_dict() for obj in result["items"]],
        total=result["total"],
        page=page,
        page_size=page_size
    )

@router.get("/events/{event_id}", summary="获取健康事件详情")
async def get_event(
    event_id: str = Path(..., description="事件ID"),
):
    obj = await event_controller.get(event_id=event_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")
    return SuccessResponse(data=await obj.to_dict())

@router.post("/events", summary="创建健康事件")
async def create_event(
    event_in: dict,
):
    obj = await event_controller.create(obj_in=event_in)
    return SuccessResponse(data=await obj.to_dict())

@router.put("/events/{event_id}", summary="更新健康事件")
async def update_event(
    event_id: str = Path(..., description="事件ID"),
    event_in: dict = Body(...),
):
    updated = await event_controller.update(event_id=event_id, obj_in=event_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Event not found")
    return SuccessResponse(msg="Updated Successfully")

@router.delete("/events/{event_id}", summary="删除健康事件")
async def delete_event(
    event_id: str = Path(..., description="事件ID"),
):
    deleted = await event_controller.remove(event_id=event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Event not found")
    return SuccessResponse(msg="Deleted Successfully")