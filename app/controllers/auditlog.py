from datetime import datetime
from typing import List, Tuple, Optional
from tortoise.expressions import Q

from app.core.crud import CRUDBase
from app.models.admin import AuditLog
from app.schemas.system.api import ApiCreate, ApiUpdate


class AuditLogController(CRUDBase[AuditLog, ApiCreate, ApiUpdate]):
    def __init__(self):
        super().__init__(model=AuditLog)
    
    async def get_audit_logs(
        self,
        page: int,
        page_size: int,
        username: str = "",
        module: str = "",
        method: str = "",
        summary: str = "",
        status: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
    ) -> Tuple[List[AuditLog], int]:
        """获取审计日志列表及总数"""
        q = Q()
        if username:
            q &= Q(username__icontains=username)
        if module:
            q &= Q(module__icontains=module)
        if method:
            q &= Q(method__icontains=method)
        if summary:
            q &= Q(summary__icontains=summary)
        if status:
            q &= Q(status=status)
        if start_time and end_time:
            q &= Q(created_at__range=[start_time, end_time])
        elif start_time:
            q &= Q(created_at__gte=start_time)
        elif end_time:
            q &= Q(created_at__lte=end_time)

        audit_logs = await self.model.filter(q).offset((page - 1) * page_size).limit(page_size).order_by("-created_at")
        total = await self.model.filter(q).count()
        
        return audit_logs, total


auditlog_controller = AuditLogController()