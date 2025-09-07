import logging
from typing import List, Optional
from fastapi import APIRouter, Query, Body, Path, HTTPException, Depends

from app.controllers.health.datasheet import HealthDataRecordController
from app.schemas.base import SuccessResponse, PaginatedResponse
from app.schemas.health.healthdatarecord import (
    HealthDataRecordCreate,
    HealthDataRecordUpdate,
    HealthDataRecordOut,
    HealthDataRecordSimpleOut
)
from app.api.v2.auth import verify_admin_token, AdminTokenData

logger = logging.getLogger(__name__)
router = APIRouter()
healthdatarecord_controller = HealthDataRecordController()

@router.get("/records/statistics", summary="获取健康数据记录统计信息")
async def get_healthdatarecord_statistics(
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    stats = await healthdatarecord_controller.get_statistics()
    return SuccessResponse(data=stats)

@router.get("/records", summary="分页/过滤/搜索健康数据记录列表")
async def list_healthdatarecords(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    device_id: Optional[str] = Query(None, description="设备ID"),
    patient_id: Optional[str] = Query(None, description="患者ID"),
    schema_type: Optional[str] = Query(None, description="数据类型"),
    category: Optional[str] = Query(None, description="数据分类"),
    partition: Optional[str] = Query(None, description="分区键"),
    archived: Optional[bool] = Query(None, description="是否归档"),
    start_time: Optional[str] = Query(None, description="起始记录时间"),
    end_time: Optional[str] = Query(None, description="结束记录时间"),
    order_by: str = Query("-recorded_at", description="排序字段"),
    keyword: Optional[str] = Query(None, description="模糊搜索关键词"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    if keyword:
        result = await healthdatarecord_controller.search(keyword)
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
        "patient_id": patient_id,
        "schema_type": schema_type,
        "category": category,
        "partition": partition,
        "archived": archived,
        "start_time": start_time,
        "end_time": end_time
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    result = await healthdatarecord_controller.get_multi_by_filters(
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

@router.get("/records/{record_id}", summary="获取健康数据记录详情")
async def get_healthdatarecord(
    record_id: int = Path(..., description="数据ID"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    obj = await healthdatarecord_controller.get(id=record_id)
    if not obj:
        raise HTTPException(status_code=404, detail="HealthDataRecord not found")
    return SuccessResponse(data=await obj.to_dict())

@router.post("/records", summary="创建健康数据记录")
async def create_healthdatarecord(
    record_in: HealthDataRecordCreate,
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    obj = await healthdatarecord_controller.create(obj_in=record_in)
    return SuccessResponse(data=await obj.to_dict())

@router.put("/records/{record_id}", summary="更新健康数据记录")
async def update_healthdatarecord(
    record_id: int = Path(..., description="数据ID"),
    record_in: HealthDataRecordUpdate = Body(...),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    updated = await healthdatarecord_controller.update(id=record_id, obj_in=record_in)
    if not updated:
        raise HTTPException(status_code=404, detail="HealthDataRecord not found")
    return SuccessResponse(msg="Updated Successfully")

@router.delete("/records/{record_id}", summary="删除健康数据记录")
async def delete_healthdatarecord(
    record_id: int = Path(..., description="数据ID"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    deleted = await healthdatarecord_controller.remove(id=record_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="HealthDataRecord not found")
    return SuccessResponse(msg="Deleted Successfully")

@router.post("/records/bulk", summary="批量创建健康数据记录")
async def bulk_create_healthdatarecords(
    records: List[HealthDataRecordCreate] = Body(..., description="健康数据记录列表"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    result = await healthdatarecord_controller.bulk_create(records)
    return SuccessResponse(
        msg=f"Successfully created {len(result)} records",
        data=[await obj.to_dict() for obj in result]
    )

@router.delete("/records/bulk", summary="批量删除健康数据记录")
async def bulk_delete_healthdatarecords(
    record_ids: List[int] = Body(..., description="数据ID列表"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    await healthdatarecord_controller.bulk_delete(record_ids)
    return SuccessResponse(msg="Batch deletion completed")

@router.get("/records/{patient_id}/summary", summary="获取患者健康数据摘要")
async def get_patient_summary(
    patient_id: int,
    limit: int = Query(1, description="返回条数"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    summary = await healthdatarecord_controller.get_patient_summary(patient_id, limit)
    return SuccessResponse(data=summary)