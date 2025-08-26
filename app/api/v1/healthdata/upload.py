from fastapi import APIRouter, Query, Body, Path, HTTPException
from app.schemas.health.healthdatarecord import HealthDataRecordCreate
from app.service.health.event_pipeline import EventDrivenHealthPipeline

event_pipeline = EventDrivenHealthPipeline()
from app.schemas.base.response import SuccessResponse

router = APIRouter()


@router.post("/upload_by_patient", summary="按患者ID上传健康数据")
async def upload_by_patient(data: HealthDataRecordCreate = Body(..., description="健康数据上传参数")):
    """
    按患者ID上传健康数据
    """
    device_data = {
        "patient_id": data.patient_id,
        "device_id": data.device_id,
        "data_type": data.schema_type,
        "measurements": data.payload,
        "source": "patient_upload"
    }
    result = await event_pipeline.process_device_data(device_data)
    return SuccessResponse(msg="上传成功", data=result if result else [])


@router.post("/upload_by_device", summary="按设备ID上传健康数据")
async def upload_by_device(data: HealthDataRecordCreate = Body(..., description="健康数据上传参数")):
    """
    按设备ID上传健康数据
    """
    device_data = {
        "patient_id": data.patient_id,
        "device_id": data.device_id,
        "data_type": data.schema_type,
        "measurements": data.payload,
        "source": "device_upload"
    }
    result = await event_pipeline.process_device_data(device_data)
    return SuccessResponse(msg="上传成功", data=result if result else [])
