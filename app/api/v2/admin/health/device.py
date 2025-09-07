import logging
from typing import List, Optional
from fastapi import APIRouter, Query, Body, Path, HTTPException, Depends

from app.controllers.health import device_controller
from app.schemas.base import SuccessResponse, PaginatedResponse
from app.schemas.health import DeviceCreate, DeviceUpdate
from app.api.v2.auth import verify_admin_token, AdminTokenData

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/devices", summary="分页/过滤/搜索设备列表")
async def list_devices(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    device_id: Optional[str] = Query(None, description="设备ID"),
    name: Optional[str] = Query(None, description="设备名称"),
    patient_id: Optional[int] = Query(None, description="患者ID"),
    order_by: str = Query("-created_at", description="排序字段"),
    keyword: Optional[str] = Query(None, description="模糊搜索关键词"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    if keyword:
        result = await device_controller.search(keyword)
        start = (page - 1) * page_size
        end = start + page_size
        data = [await obj.to_dict() for obj in result[start:end]]
        return PaginatedResponse(
            data=data,
            total=len(result),
            page=page,
            page_size=page_size
        )
    filters = {
        "device_id": device_id,
        "name": name,
        "patient_id": patient_id
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    result = await device_controller.get_multi_by_filters(
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

@router.post("/devices/unbind-by-username", summary="通过用户名和设备ID解绑设备")
async def unbind_device_by_username(
    username: str = Body(..., embed=True, description="用户名"),
    device_id: str = Body(..., embed=True, description="设备ID"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    device = await device_controller.unbind_by_username_and_device_id(username, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="未找到对应绑定关系")
    return SuccessResponse(msg="解绑成功", data=await device.to_dict())

@router.get("/devices/statistics", summary="获取设备统计信息")
async def get_device_statistics(
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    stats = await device_controller.get_statistics()
    return SuccessResponse(data=stats)

@router.get("/devices/{device_id}", summary="获取设备详情")
async def get_device(
    device_id: int = Path(..., description="设备ID"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    device = await device_controller.get(id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return SuccessResponse(data=await device.to_dict())

@router.post("/devices", summary="创建设备")
async def create_device(
    device_in: DeviceCreate,
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    device = await device_controller.create(obj_in=device_in)
    return SuccessResponse(data=await device.to_dict())

@router.put("/devices/{device_id}", summary="更新设备")
async def update_device(
    device_id: int = Path(..., description="设备ID"),
    device_in: DeviceUpdate = Body(...),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    await device_controller.update(id=device_id, obj_in=device_in)
    return SuccessResponse(msg="Updated Successfully")

@router.delete("/devices/{device_id}", summary="删除设备")
async def delete_device(
    device_id: int = Path(..., description="设备ID"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    await device_controller.remove(id=device_id)
    return SuccessResponse(msg="Deleted Successfully")

@router.post("/devices/bulk", summary="批量创建设备")
async def bulk_create_devices(
    devices: List[DeviceCreate] = Body(..., description="设备列表"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    result = await device_controller.bulk_create(devices)
    return SuccessResponse(
        msg=f"Successfully created {len(result)} devices",
        data=[await obj.to_dict() for obj in result]
    )

@router.delete("/devices/bulk", summary="批量删除设备")
async def bulk_delete_devices(
    device_ids: List[int] = Body(..., description="设备ID列表"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    await device_controller.bulk_delete(device_ids)
    return SuccessResponse(msg="Batch deletion completed")

@router.get("/devices/patient/{patient_id}", summary="获取患者的所有设备")
async def get_patient_devices(
    patient_id: int = Path(..., description="患者ID"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    devices = await device_controller.get_patient_devices(patient_id)
    start = (page - 1) * page_size
    end = start + page_size
    return PaginatedResponse(
        data=[await obj.to_dict() for obj in devices[start:end]],
        total=len(devices),
        page=page,
        page_size=page_size
    )