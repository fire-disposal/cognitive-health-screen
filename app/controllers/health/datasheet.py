from typing import List, Optional, Dict, Any
from tortoise.expressions import Q
from tortoise.transactions import atomic

from app.models.health.healthdatarecord import HealthDataRecord
from app.schemas.health.healthdatarecord import HealthDataRecordCreate, HealthDataRecordUpdate

class HealthDataRecordController:
    def __init__(self):
        self.model = HealthDataRecord

    async def get(self, id: int) -> Optional[HealthDataRecord]:
        return await self.model.get_or_none(id=id)

    async def get_multi_by_filters(
        self,
        filters: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 10,
        order_by: str = "-recorded_at"
    ) -> Dict[str, Any]:
        query = self.model.all()
        if filters:
            if patient_id := filters.get("patient_id"):
                query = query.filter(patient_id=patient_id)
            if schema_type := filters.get("schema_type"):
                query = query.filter(schema_type=schema_type)
            if category := filters.get("category"):
                query = query.filter(category=category)
            if partition := filters.get("partition"):
                query = query.filter(partition=partition)
            if archived := filters.get("archived"):
                query = query.filter(archived=archived)
            if start_time := filters.get("start_time"):
                query = query.filter(recorded_at__gte=start_time)
        total = await query.count()
        items = await query.offset(skip).limit(limit).order_by(order_by)
        return {"total": total, "items": items}

    async def search(self, keyword: str) -> List[HealthDataRecord]:
        query = Q(schema_type__icontains=keyword) | Q(category__icontains=keyword) | Q(partition__icontains=keyword)
        return await self.model.filter(query).all()

    @atomic()
    async def create(self, obj_in: HealthDataRecordCreate) -> HealthDataRecord:
        obj = await self.model.create(
            patient_id=obj_in.patient_id,
            recorded_at=obj_in.recorded_at,
            schema_type=obj_in.schema_type,
            payload=obj_in.payload
        )
        return obj

    @atomic()
    async def update(self, id: int, obj_in: HealthDataRecordUpdate) -> Optional[HealthDataRecord]:
        obj = await self.model.get_or_none(id=id)
        if not obj:
            return None
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(obj, field, value)
        await obj.save()
        return obj

    @atomic()
    async def remove(self, id: int) -> bool:
        deleted = await self.model.filter(id=id).delete()
        return deleted > 0

    @atomic()
    async def bulk_create(self, obj_in_list: List[HealthDataRecordCreate]) -> List[HealthDataRecord]:
        objs = []
        for obj_in in obj_in_list:
            obj = await self.create(obj_in)
            objs.append(obj)
        return objs

    @atomic()
    async def bulk_delete(self, ids: List[int]) -> bool:
        deleted_count = await self.model.filter(id__in=ids).delete()
        return deleted_count > 0

    async def get_statistics(self) -> Dict[str, int]:
        total = await self.model.all().count()
        type_stats = {}
        types = await self.model.all().distinct().values_list("schema_type", flat=True)
        for t in types:
            type_stats[t] = await self.model.filter(schema_type=t).count()
        return {"total": total, "by_type": type_stats}

#TODO 多类型分析实现
    async def get_patient_summary(self, patient_id: int, limit: int = 1) -> dict:
        """
        获取患者健康摘要，聚合基本信息、最新体征、分析结果、异常告警等
        """
        from app.models.health.event import Event
        from app.models.health.healthdatarecord import HealthDataRecord
        from app.models.health.patient import Patient
        from app.models.health.alert import Alert
        import datetime
        from tortoise.functions import Max

        # 1. 基本信息
        patient = await Patient.get_or_none(id=patient_id)
        if not patient:
            return {"error": "Patient not found"}

        summary = {
            "patient": {
                "id": patient.id,
                "name": patient.name,
                "age": patient.age,
                "gender": patient.gender,
                "status": patient.status,
            }
        }

        # 2. 最新体征（取最近一条原始数据）
        latest_record = await HealthDataRecord.filter(patient_id=patient_id).order_by("-recorded_at").first()
        summary["latest_vitals"] = latest_record.payload if latest_record else {}

        # 3. 最新分析（每种分析类型各取一条）
        analysis_types = await Event.filter(patient_id=patient_id).distinct().values_list("analysis_type", flat=True)
        latest_analysis = {}
        for atype in analysis_types:
            record = await Event.filter(patient_id=patient_id, analysis_type=atype).order_by("-recorded_at").first()
            if record:
                latest_analysis[atype] = {
                    "recorded_at": record.recorded_at,
                    "result": record.result,
                    "comment": record.comment,
                }
        summary["latest_analysis"] = latest_analysis

        # 4. 近期异常/告警（近7天未解决）
        now = datetime.datetime.now()
        week_ago = now - datetime.timedelta(days=7)
        alerts = await Alert.filter(patient_id=patient_id, status="active", created_at__gte=week_ago).order_by("-created_at").limit(10)
        summary["recent_alerts"] = [
            {
                "id": a.id,
                "rule_name": a.rule_name,
                "level": a.level,
                "message": a.message,
                "event_type": a.event_type,
                "created_at": a.created_at,
                "description": a.description,
                "status": a.status,
            }
            for a in alerts
        ]

        suggestions = []
        for atype, analysis in latest_analysis.items():
            if atype == "risk_score" and analysis["result"].get("score", 0) > 80:
                suggestions.append("健康风险较高，请及时就医或咨询医生。")
            if atype == "sleep_stage" and analysis["result"].get("quality") == "poor":
                suggestions.append("近期睡眠质量较差，建议改善作息。")
        summary["suggestions"] = suggestions

        return summary
    async def get_patient_history_data(
        self,
        patient_id: int,
        data_type: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        查询指定患者指定类型的最近 limit 条健康分析数据
        :param patient_id: 患者ID
        :param data_type: 数据类型（如 'mattress'、'heart_rate' 等）
        :param limit: 查询条数
        :return: 历史数据列表
        """
        from app.models.health.event import Event
        records = await Event.filter(
            patient_id=patient_id,
            analysis_type=data_type
        ).order_by('-recorded_at').limit(limit)
        return [record.result async for record in records]
healthdatarecord_controller = HealthDataRecordController()