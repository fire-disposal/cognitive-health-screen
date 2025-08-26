from typing import List, Optional, Dict, Any
from tortoise.expressions import Q
from tortoise.transactions import atomic

from app.core.crud import CRUDBase
from app.models.health.device import Device
from app.schemas.health.device import DeviceCreate, DeviceUpdate
from app.log import logger

from app.models.health.patient import Patient

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
    async def bind_patient(self, device_id: int, patient_id: int) -> Optional[Device]:
        device = await self.model.get_or_none(id=device_id)
        if device:
            from app.models.health.patient import Patient
            patient = await Patient.get_or_none(id=patient_id)
            if patient:
                await device.bind_patient(patient)
                return device
        return None

    @atomic()
    async def unbind_device(self, device_id: int) -> Device:
        """解绑设备"""
        device = await self.model.get(id=device_id)
        if device.current_patient_id:
            device.current_patient_id = None
            await device.save()
        return device

    async def get_patient_devices(self, patient_id: int) -> List[Device]:
        return await self.model.filter(current_patient_id=patient_id).all()


    async def unbind_by_username_and_device_id(self, username: str, device_id: str) -> Optional[Device]:
        """
        通过用户名和设备ID解绑设备与用户
        """
        patient = await Patient.filter(name=username).first()
        device = await self.model.filter(device_id=device_id).first()
        if patient and device and device.current_patient_id == patient.id:
            device.current_patient_id = None
            await device.save()
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
from app.models.health.devicegroup import DeviceGroup, DeviceGroupManager

class DeviceGroupController:
    def __init__(self):
        self.model = DeviceGroup
        self.manager = DeviceGroupManager()

    async def get(self, id: int) -> Optional[DeviceGroup]:
        return await self.model.get_or_none(id=id)

    async def list(self, skip: int = 0, limit: int = 20) -> List[DeviceGroup]:
        return await self.model.all().offset(skip).limit(limit).order_by("-id")

    async def create(self, obj_in: dict) -> DeviceGroup:
        return await self.model.create(**obj_in)

    async def update(self, id: int, obj_in: dict) -> Optional[DeviceGroup]:
        group = await self.model.get_or_none(id=id)
        if not group:
            return None
        for k, v in obj_in.items():
            setattr(group, k, v)
        await group.save()
        return group

    async def remove(self, id: int) -> bool:
        deleted = await self.model.filter(id=id).delete()
        return deleted > 0

    async def apply_group_rules(self, device_id: int) -> Optional[int]:
        from app.models.health.device import Device
        device = await Device.get_or_none(id=device_id)
        if not device:
            return None
        return await self.manager.apply_group_rules(device)

    async def batch_update_groups(self):
        await self.manager.batch_update_groups()

    async def get_devices_by_group(self, group_id: int) -> List["Device"]:
        from app.models.health.device import Device
        return await Device.filter(group_id=group_id).all()

devicegroup_controller = DeviceGroupController()

device_controller = DeviceController()
