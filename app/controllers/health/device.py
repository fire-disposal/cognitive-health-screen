from typing import List, Optional, Dict, Any
from tortoise.expressions import Q
from tortoise.transactions import atomic

from datetime import datetime
from app.core.crud import CRUDBase
from app.models.health.device import Device
from app.schemas.health.device import DeviceCreate, DeviceUpdate
from app.log import logger

from app.models.health.profile import HealthProfile

class DeviceController(CRUDBase[Device, DeviceCreate, DeviceUpdate]):
    def __init__(self):
        super().__init__(model=Device)


    async def get_device_by_device_id(self, device_id: str) -> Optional[Device]:
        return await self.model.filter(device_id=device_id).first()

    async def get_multi_by_filters(
        self,
        *,
        filters: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 10,
        order_by: str = "-created_at"
    ) -> Dict[str, Any]:
        query = self.model.all()
        if filters:
            if device_id := filters.get("device_id"):
                query = query.filter(device_id__icontains=device_id)
            if name := filters.get("name"):
                query = query.filter(name__icontains=name)
            if patient_id := filters.get("patient_id"):
                query = query.filter(current_patient_id=patient_id)

        total = await query.count()
        data = await query.offset(skip).limit(limit).order_by(order_by)
        return {"total": total, "items": data}

    @atomic()
    async def bulk_create(self, obj_in_list: List[DeviceCreate]) -> List[Device]:
        devices = []
        for obj_in in obj_in_list:
            device = await self.create(obj_in)
            devices.append(device)
        return devices

    @atomic()
    async def bulk_delete(self, ids: List[int]) -> bool:
        deleted_count = await self.model.filter(id__in=ids).delete()
        return deleted_count > 0

    async def search(self, keyword: str) -> List[Device]:
        query = Q(device_id__icontains=keyword) | \
                Q(name__icontains=keyword) | \
                Q(description__icontains=keyword)
        return await self.model.filter(query).all()

    @atomic()
    async def bind_health_profile(self, device_id: int, health_profile_id: int) -> Optional[Device]:
        from app.models.health.deviceassignment import DeviceAssignment
        device = await self.model.get_or_none(id=device_id)
        if device:
            # 解绑当前分配
            await DeviceAssignment.filter(device_id=device_id, unassigned_at=None).update(unassigned_at=datetime.now())
            # 创建新分配
            await DeviceAssignment.create(device_id=device_id, health_profile_id=health_profile_id)
            return device
        return None

    @atomic()
    async def unbind_device(self, device_id: int) -> Optional[Device]:
        """解绑设备与健康档案"""
        from app.models.health.deviceassignment import DeviceAssignment
        device = await self.model.get_or_none(id=device_id)
        if device:
            await DeviceAssignment.filter(device_id=device_id, unassigned_at=None).update(unassigned_at=datetime.now())
            return device
        return None

    async def get_health_profile_devices(self, health_profile_id: int) -> List[Device]:
        from app.models.health.deviceassignment import DeviceAssignment
        assignments = await DeviceAssignment.filter(health_profile_id=health_profile_id, unassigned_at=None).all()
        device_ids = [a.device_id for a in assignments]
        return await self.model.filter(id__in=device_ids).all()


    async def unbind_by_username_and_device_id(self, username: str, device_id: str) -> Optional[Device]:
        """
        通过用户名和设备ID解绑设备与健康档案
        """
        from app.models.health.profile import HealthProfile
        from app.models.health.deviceassignment import DeviceAssignment
        profile = await HealthProfile.filter(name=username).first()
        device = await self.model.filter(device_id=device_id).first()
        if profile and device:
            await DeviceAssignment.filter(device_id=device.id, health_profile_id=profile.id, unassigned_at=None).update(unassigned_at=datetime.now())
            return device
        return None

    async def get_statistics(self) -> Dict[str, Any]:
        from tortoise.functions import Count

        total = await self.model.all().count()
        bound = await self.model.filter(current_patient_id__not_isnull=True).count()
        unbound = total - bound

        # 按 status 字段统计数量
        status_counts = await self.model.all().group_by('status').annotate(count=Count('id')).values('status', 'count')
        status_stat = {item['status']: item['count'] for item in status_counts}

        return {
            "total": total,
            "bound": bound,
            "unbound": unbound,
            "status_stat": status_stat
        }


    @atomic()
    async def create(self, obj_in: DeviceCreate) -> Device:
        """创建设备"""
        device = await super().create(obj_in)
        return device

device_controller = DeviceController()
# 设备分组控制器
