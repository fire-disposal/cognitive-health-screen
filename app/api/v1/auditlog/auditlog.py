from datetime import datetime
from fastapi import APIRouter, Query

from app.controllers.auditlog import auditlog_controller
from app.schemas import PaginatedResponse
from app.schemas.system.api import *

router = APIRouter()


@router.get("/list", summary="查看操作日志")
async def get_audit_log_list(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    username: str = Query("", description="操作人名称"),
    module: str = Query("", description="功能模块"),
    method: str = Query("", description="请求方法"),
    summary: str = Query("", description="接口描述"),
    status: int = Query(None, description="状态码"),
    start_time: datetime = Query("", description="开始时间"),
    end_time: datetime = Query("", description="结束时间"),
):
    audit_logs, total = await auditlog_controller.get_audit_logs(
        page=page,
        page_size=page_size,
        username=username,
        module=module,
        method=method,
        summary=summary,
        status=status,
        start_time=start_time,
        end_time=end_time,
    )
    data = [await audit_log.to_dict() for audit_log in audit_logs]
    return PaginatedResponse(data=data, total=total, page=page, page_size=page_size)
