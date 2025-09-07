import logging
from typing import List, Optional
from fastapi import APIRouter, Query, Body, Path, HTTPException, Depends

from app.controllers.health import patient_controller
from app.schemas.base import SuccessResponse, PaginatedResponse
from app.schemas.health.patient import PatientCreate, PatientUpdate, PatientResponse
from app.api.v2.auth import verify_admin_token, AdminTokenData

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/patients", summary="分页/过滤/搜索患者列表")
async def list_patients(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    name: Optional[str] = Query(None, description="姓名"),
    gender: Optional[str] = Query(None, description="性别"),
    age_min: Optional[int] = Query(None, description="最小年龄"),
    age_max: Optional[int] = Query(None, description="最大年龄"),
    status: Optional[str] = Query(None, description="状态"),
    order_by: str = Query("-created_at", description="排序字段"),
    keyword: Optional[str] = Query(None, description="模糊搜索关键词"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    if keyword:
        result = await patient_controller.search(keyword)
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
        "name": name,
        "gender": gender,
        "age_min": age_min,
        "age_max": age_max,
        "status": status
    }
    filters = {k: v for k, v in filters.items() if v is not None}
    result = await patient_controller.get_multi_by_filters(
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

@router.get("/patients/statistics", summary="获取患者统计信息")
async def get_patient_statistics(
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    stats = await patient_controller.get_statistics()
    return SuccessResponse(data=stats)

@router.get("/patients/{patient_id}", summary="获取患者详情")
async def get_patient(
    patient_id: int = Path(..., description="患者ID"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    patient_obj = await patient_controller.get(id=patient_id)
    if not patient_obj:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient_dict = await patient_obj.to_dict()
    return SuccessResponse(data=patient_dict)

@router.post("/patients", summary="创建患者")
async def create_patient(
    patient_in: PatientCreate,
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    new_patient = await patient_controller.create_patient(obj_in=patient_in)
    return SuccessResponse(msg="Created Successfully", data=await new_patient.to_dict())

@router.put("/patients/{patient_id}", summary="更新患者")
async def update_patient(
    patient_id: int = Path(..., description="患者ID"),
    patient_in: PatientUpdate = Body(...),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    await patient_controller.update(id=patient_id, obj_in=patient_in)
    return SuccessResponse(msg="Updated Successfully")

@router.delete("/patients/{patient_id}", summary="删除患者")
async def delete_patient(
    patient_id: int = Path(..., description="患者ID"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    await patient_controller.remove(id=patient_id)
    return SuccessResponse(msg="Deleted Successfully")

@router.post("/patients/bulk", summary="批量创建患者")
async def bulk_create_patients(
    patients: List[PatientCreate] = Body(..., description="患者列表"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    result = await patient_controller.bulk_create(patients)
    return SuccessResponse(
        msg=f"Successfully created {len(result)} patients",
        data=[await obj.to_dict() for obj in result]
    )

@router.delete("/patients/bulk", summary="批量删除患者")
async def bulk_delete_patients(
    patient_ids: List[int] = Body(..., description="患者ID列表"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    await patient_controller.bulk_delete(patient_ids)
    return SuccessResponse(msg="Batch deletion completed")

@router.get("/patients/by-status/{status}", summary="按状态查询患者")
async def get_patients_by_status(
    status: str,
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    result = await patient_controller.get_by_status(
        status=status,
        skip=(page - 1) * page_size,
        limit=page_size
    )
    return PaginatedResponse(
        data=[await obj.to_dict() for obj in result["items"]],
        total=result["total"],
        page=page,
        page_size=page_size
    )

@router.patch("/patients/{patient_id}/status", summary="更新患者状态")
async def update_patient_status(
    patient_id: int = Path(..., description="患者ID"),
    status: str = Body(..., embed=True, description="新状态"),
    token_data: AdminTokenData = Depends(verify_admin_token)
):
    result = await patient_controller.update_status(patient_id, status)
    if result:
        return SuccessResponse(msg="Status updated successfully")
    return SuccessResponse(code=404, msg="Patient not found")