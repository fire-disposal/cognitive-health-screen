from typing import List, Optional, Dict, Any
from tortoise.expressions import Q
from tortoise.transactions import atomic

from app.core.crud import CRUDBase
from app.models.health.patient import Patient
from app.schemas.health.patient import PatientCreate, PatientUpdate, PatientResponse


class PatientController(CRUDBase[Patient, PatientCreate, PatientUpdate]):
    def __init__(self):
        super().__init__(model=Patient)

    async def get_patient_by_name(self, name: str) -> Optional[Patient]:
        return await self.model.filter(name=name).first()
    
    async def list(self, page: int, page_size: int, search: Optional[str] = None):
        """
        支持分页和模糊查询的患者列表
        """
        query = self.model.all()
        if search and search.strip():
            query = query.filter(name__icontains=search.strip())

        total = await query.count()
        data = await query.offset((page - 1) * page_size).limit(page_size).order_by("-created_at")
        return total, data


    async def create_patient(self, obj_in: PatientCreate) -> Patient:
        obj = await self.create(obj_in)
        return obj
    
    async def update_patient(self, db_obj: Patient, obj_in: PatientUpdate) -> Patient:
        updated_obj = await self.update(db_obj, obj_in)
        return updated_obj
    
    async def get_patients(self, skip: int = 0, limit: int = 100) -> List[Patient]:
        return await self.model.all().offset(skip).limit(limit).order_by('id')
    
    async def delete_patient(self, db_obj: Patient) -> None:
        await self.delete(db_obj)

    async def get_multi_by_filters(
        self,
        *,
        filters: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 10,
        order_by: str = "-created_at"
    ) -> List[Patient]:
        """
        多条件过滤查询
        """
        query = self.model.all()
        if filters:
            if name := filters.get("name"):
                query = query.filter(name__icontains=name)
            if gender := filters.get("gender"):
                query = query.filter(gender=gender)
            if age_min := filters.get("age_min"):
                query = query.filter(age__gte=age_min)
            if age_max := filters.get("age_max"):
                query = query.filter(age__lte=age_max)
            if status := filters.get("status"):
                query = query.filter(status=status)

        total = await query.count()
        data = await query.offset(skip).limit(limit).order_by(order_by)
        return {"total": total, "items": data}

    @atomic()
    async def bulk_create(self, obj_in_list: List[PatientCreate]) -> List[Patient]:
        """
        批量创建病人记录
        """
        patients = []
        for obj_in in obj_in_list:
            patient = await self.create_patient(obj_in)
            patients.append(patient)
        return patients

    @atomic()
    async def bulk_delete(self, ids: List[int]) -> bool:
        """
        批量删除病人记录
        """
        deleted_count = await self.model.filter(id__in=ids).delete()
        return deleted_count > 0

    async def search(self, keyword: str) -> List[Patient]:
        """
        综合搜索功能
        """
        query = Q(name__icontains=keyword) | \
                Q(phone__icontains=keyword) | \
                Q(address__icontains=keyword) | \
                Q(medical_history__icontains=keyword)
        return await self.model.filter(query).all()

    async def get_by_status(self, status: str, skip: int = 0, limit: int = 10) -> Dict[str, Any]:
        """
        按状态查询病人
        """
        query = self.model.filter(status=status)
        total = await query.count()
        items = await query.offset(skip).limit(limit).order_by("-created_at")
        return {"total": total, "items": items}

    @atomic()
    async def update_status(self, patient_id: int, new_status: str) -> Optional[Patient]:
        """
        更新病人状态
        """
        patient = await self.model.get_or_none(id=patient_id)
        if patient:
            patient.status = new_status
            await patient.save()
        return patient

    async def get_statistics(self) -> Dict[str, Any]:
        """
        获取病人统计信息，包含总数、按状态/性别聚合
        """
        from tortoise.functions import Count

        total = await self.model.all().count()

        # 按 status 分类统计
        status_counts = await self.model.all().group_by('status').annotate(count=Count('id')).values('status', 'count')
        status_stat = {item['status']: item['count'] for item in status_counts}

        # 按 gender 分类统计
        gender_counts = await self.model.all().group_by('gender').annotate(count=Count('id')).values('gender', 'count')
        gender_stat = {item['gender']: item['count'] for item in gender_counts}

        return {
            "total": total,
            "status_stat": status_stat,
            "gender_stat": gender_stat
        }

patient_controller = PatientController()