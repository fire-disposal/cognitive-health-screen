from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
import asyncio

from app.core.event_bus import event_bus
from app.service.health.handler.base import HealthDataEvent ,EventHandler

class EventDrivenHealthPipeline:
    """事件驱动健康数据处理主入口"""
    def __init__(self, handlers: Optional[List] = None):
        self.handlers = handlers or []
        for handler in self.handlers:
            event_bus.register_handler(handler)



    async def process_device_data(self, device_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        required_fields = ['patient_id', 'device_id', 'data_type', 'measurements']
        if not all(field in device_data for field in required_fields):
            raise ValueError("Invalid device data")
        event = HealthDataEvent(
            event_id=f"{device_data['device_id']}_{datetime.now().timestamp()}",
            event_type=f"{device_data['data_type']}_received",
            patient_id=device_data['patient_id'],
            device_id=device_data['device_id'],
            timestamp=datetime.now(),
            data=device_data['measurements'],
            metadata={
                'source': device_data.get('source', 'unknown'),
                'device_model': device_data.get('device_model')
            }
        )
        # 发布事件并收集结果
        results = await event_bus.publish_event(event)
        return results

# 全局单例实例
event_pipeline = EventDrivenHealthPipeline()

import asyncio
from app.models.health.healthdatarecord import HealthDataRecord
from app.models.health.event import Event
from app.service.ws.service import WebSocketService
from app.controllers.health.device import device_controller
from app.controllers.health.patient import patient_controller
from app.schemas.health.device import DeviceCreate
from app.schemas.health.patient import PatientCreate
from app.log import logger

class HealthDataPersistenceHandler(EventHandler):
    """事件驱动健康数据持久化与业务处理器"""
    def __init__(self, batch_size=50, batch_interval=2):
        self.queue = asyncio.Queue()
        self.batch_size = batch_size
        self.batch_interval = batch_interval
        self._batch_task = asyncio.create_task(self._batch_timer())

    async def _batch_timer(self):
        while True:
            await asyncio.sleep(self.batch_interval)
            if self.queue.qsize() > 0:
                await self._process_batch()

    async def can_handle(self, event: HealthDataEvent) -> bool:
        # 所有健康数据事件均处理
        return True

    async def handle(self, event: HealthDataEvent):
        await self.queue.put(event)
        # 仅入队，批处理由定时器和队列长度共同触发
        if self.queue.qsize() >= self.batch_size:
            await self._process_batch()

    async def _process_batch(self):
        batch = []
        while not self.queue.empty() and len(batch) < self.batch_size:
            batch.append(await self.queue.get())
        # 批量处理事件
        raw_records_to_create = []
        patient_map = {}
        device_map = {}
        for event in batch:
            patient_id = event.patient_id
            device_id = event.device_id
            # 自动注册患者/设备
            patient = None
            device = None
            if patient_id:
                if patient_id not in patient_map:
                    p = await patient_controller.model.get_or_none(id=patient_id)
                    if not p:
                        p = await patient_controller.create_patient(
                            PatientCreate(name=f"患者_{patient_id}", age=99, gender="other")
                        )
                    patient_map[patient_id] = p
                patient = patient_map[patient_id]
                if device_id and device_id not in device_map:
                    d = await device_controller.get_device_by_device_id(device_id)
                    if d:
                        await device_controller.bind_patient(d.id, patient.id)
                    device_map[device_id] = d
            elif device_id:
                if device_id not in device_map:
                    d = await device_controller.get_device_by_device_id(device_id)
                    if not d:
                        d = await device_controller.create(
                            DeviceCreate(
                                device_id=device_id,
                                name=f"设备_{device_id}",
                                description="自动注册设备",
                                mqtt_enabled=True,
                                data_types=[event.event_type],
                            )
                        )
                    if not getattr(d, "current_patient_id", None):
                        default_patient = await patient_controller.create_patient(
                            PatientCreate(name="默认患者", age=99, gender="other")
                        )
                        await device_controller.bind_patient(d.id, default_patient.id)
                        d.current_patient_id = default_patient.id
                    device_map[device_id] = d
                device = device_map[device_id]
                patient = getattr(device, "current_patient", None)
            if not patient:
                logger.error(
                    "[数据异常] patient_id/device_id 无法获取患者，数据未入库 | event=%s | device_id=%s | patient_id=%s | payload=%s",
                    event, device_id, patient_id, event.data
                )
                continue
            raw_records_to_create.append({
                "patient": patient,
                "recorded_at": event.timestamp,
                "schema_type": event.event_type,
                "payload": event.data,
                "status": "raw"
            })
        if not raw_records_to_create:
            return
        created_records = await HealthDataRecord.bulk_create([
            HealthDataRecord(**record) for record in raw_records_to_create
        ])
        # 推送健康数据
        for record in created_records:
            try:
                await WebSocketService.push_health_data(record.patient.id, record.payload)
            except Exception as e:
                logger.error(
                    f"[健康数据推送异常] patient_id={record.patient.id}, payload={record.payload}, error: {e}"
                )

