import logging
from typing import List, Optional
from fastapi import APIRouter, Query, Body, Path, HTTPException, Depends

from app.controllers.health.device import devicegroup_controller
from app.schemas.base import SuccessResponse, PaginatedResponse
from app.api.v2.auth import verify_admin_token, AdminTokenData

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/device-groups", summary="分页获取设备分组列表")
async def list_device_groups(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    groups = await devicegroup_controller.list(skip=(page - 1) * page_size, limit=page_size)
    total = len(groups)
    return PaginatedResponse(
        data=[group.__dict__ for group in groups],
        total=total,
        page=page,
        page_size=page_size
    )

@router.get("/device-groups/{group_id}", summary="获取设备分组详情")
async def get_device_group(
    group_id: int = Path(..., description="分组ID"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    group = await devicegroup_controller.get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="DeviceGroup not found")
    return SuccessResponse(data=group.__dict__)

@router.post("/device-groups", summary="创建设备分组")
async def create_device_group(
    group_in: dict = Body(..., description="分组信息"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    group = await devicegroup_controller.create(group_in)
    return SuccessResponse(data=group.__dict__)

@router.put("/device-groups/{group_id}", summary="更新设备分组")
async def update_device_group(
    group_id: int = Path(..., description="分组ID"),
    group_in: dict = Body(...),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    updated = await devicegroup_controller.update(group_id, group_in)
    if not updated:
        raise HTTPException(status_code=404, detail="DeviceGroup not found")
    return SuccessResponse(msg="Updated Successfully")

@router.delete("/device-groups/{group_id}", summary="删除设备分组")
async def delete_device_group(
    group_id: int = Path(..., description="分组ID"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    deleted = await devicegroup_controller.remove(group_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="DeviceGroup not found")
    return SuccessResponse(msg="Deleted Successfully")

@router.post("/device-groups/apply/{device_id}", summary="应用分组规则到指定设备")
async def apply_group_rules(
    device_id: int = Path(..., description="设备ID"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    group_id = await devicegroup_controller.apply_group_rules(device_id)
    return SuccessResponse(data={"group_id": group_id})

@router.post("/device-groups/batch-update", summary="批量应用分组规则")
async def batch_update_groups(
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    await devicegroup_controller.batch_update_groups()
    return SuccessResponse(msg="Batch group update completed")

@router.get("/device-groups/{group_id}/devices", summary="获取分组下所有设备")
async def get_devices_by_group(
    group_id: int = Path(..., description="分组ID"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    devices = await devicegroup_controller.get_devices_by_group(group_id)
    start = (page - 1) * page_size
    end = start + page_size
    return PaginatedResponse(
        data=[await device.to_dict() for device in devices[start:end]],
        total=len(devices),
        page=page,
        page_size=page_size
    )