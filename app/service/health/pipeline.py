# import asyncio
# import datetime
# from typing import Any, Dict, Optional, List

# from app.models.health.healthdatarecord import HealthDataRecord
# from app.models.health.event import Event
# from app.service.ws.service import WebSocketService
# from app.service.health.handler.plugin_manager import PluginManager
# from app.service.health.alert_manager import AlertManager
# from app.log import logger


# class HealthDataPipeline:
#     def __init__(self, queue_size: int = 5000, workers: int = 4, batch_size: int = 50):
#         """
#         :param queue_size: 队列最大长度
#         :param workers: 并行消费者数量
#         :param batch_size: 批量入库大小
#         """
#         self.queue = asyncio.Queue(maxsize=queue_size)
#         self.workers = workers
#         self.batch_size = batch_size
#         self.plugin_manager = PluginManager()
#         self.alert_manager = AlertManager()
#         self.plugin_instances = {}
#         self.loaded_plugins = list(self.plugin_manager.all_plugins().keys())
#         self._load_plugins()

#     def _load_plugins(self):
#         if not self.loaded_plugins:
#             logger.warning("[健康插件加载] 未发现任何插件")
#             return

#         for plugin_name in self.loaded_plugins:
#             plugin_cls = self.plugin_manager.get_plugin(plugin_name)
#             try:
#                 plugin_instance = plugin_cls()
#                 if hasattr(plugin_instance, "set_history_query"):
#                     plugin_instance.set_history_query(self.get_history)
#                 self.plugin_instances[plugin_name] = plugin_instance
#                 logger.info(f"[健康插件加载成功] 插件: {plugin_name} - {getattr(plugin_instance, 'name', '')}")
#             except Exception as e:
#                 logger.error(f"[插件实例化失败] {plugin_name}: {e}")

#     async def get_history(self, patient_id: int, source_type: str, limit: int = 20):
#         try:
#             records = await Event.filter(
#                 patient_id=patient_id,
#                 analysis_type=source_type
#             ).order_by('-recorded_at').limit(limit)
#             return [r.result for r in records]
#         except Exception as e:
#             logger.error(f"[历史数据查询异常] patient_id={patient_id}, source_type={source_type}, error: {e}")
#             return []

#     async def enqueue(self, payload: Dict[str, Any], source_type: str, patient_id=None, device_id=None, recorded_at=None):
#         """
#         入队原始数据
#         """
#         await self.queue.put((payload, source_type, patient_id, device_id, recorded_at))

#     async def run(self):
#         """
#         启动多个并行 Worker
#         """
#         async def worker():
#             buffer = []
#             while True:
#                 try:
#                     item = await self.queue.get()
#                     buffer.append(item)
#                     if len(buffer) >= self.batch_size:
#                         await self._process_batch(buffer)
#                         buffer.clear()
#                 except Exception as e:
#                     logger.error(f"[队列处理异常] {e}")
#                 finally:
#                     self.queue.task_done()

#         logger.info(f"[Pipeline] 启动 {self.workers} 个消费者，每批 {self.batch_size} 条")
#         await asyncio.gather(*(worker() for _ in range(self.workers)))

#     async def _process_batch(self, batch_data: List[tuple]):
#         """
#         批量处理队列数据
#         """
#         from app.controllers.health.device import device_controller
#         from app.schemas.health.device import DeviceCreate
#         from app.controllers.health.patient import patient_controller
#         from app.schemas.health.patient import PatientCreate

#         raw_records_to_create = []
#         patient_map = {}
#         device_map = {}

#         # 第一步：批量准备原始数据记录
#         for payload, source_type, patient_id, device_id, recorded_at in batch_data:
#             try:
#                 # 查找患者或设备（缓存避免重复 DB 查询）
#                 patient = None
#                 device = None
#                 if patient_id:
#                     if patient_id not in patient_map:
#                         p = await patient_controller.model.get_or_none(id=patient_id)
#                         if not p:
#                             p = await patient_controller.create_patient(
#                                 PatientCreate(name=f"患者_{patient_id}", age=99, gender="other")
#                             )
#                         patient_map[patient_id] = p
#                     patient = patient_map[patient_id]
#                     if device_id and device_id not in device_map:
#                         d = await device_controller.get_device_by_device_id(device_id)
#                         if d:
#                             await device_controller.bind_patient(d.id, patient.id)
#                         device_map[device_id] = d
#                 elif device_id:
#                     if device_id not in device_map:
#                         d = await device_controller.get_device_by_device_id(device_id)
#                         if not d:
#                             d = await device_controller.create(
#                                 DeviceCreate(
#                                     device_id=device_id,
#                                     name=f"设备_{device_id}",
#                                     description="自动注册设备",
#                                     mqtt_enabled=True,
#                                     data_types=[source_type],
#                                 )
#                             )
#                         if not getattr(d, "current_patient_id", None):
#                             default_patient = await patient_controller.create_patient(
#                                 PatientCreate(name="默认患者", age=99, gender="other")
#                             )
#                             await device_controller.bind_patient(d.id, default_patient.id)
#                             d.current_patient_id = default_patient.id
#                         device_map[device_id] = d
#                     device = device_map[device_id]
#                     patient = getattr(device, "current_patient", None)

#                 if not patient:
#                     logger.error("[数据异常] patient_id/device_id 无法获取患者，数据未入库")
#                     continue

#                 raw_records_to_create.append({
#                     "patient": patient,
#                     "recorded_at": recorded_at,
#                     "schema_type": source_type,
#                     "payload": payload,
#                     "status": "raw"
#                 })
#             except Exception as e:
#                 logger.error(f"[批量准备原始数据异常] {e}")

#         if not raw_records_to_create:
#             return

#         # 第二步：批量插入原始数据
#         created_records = await HealthDataRecord.bulk_create([
#             HealthDataRecord(**record) for record in raw_records_to_create
#         ])

#         # 第三步：并行跑插件处理
#         await asyncio.gather(*(self._process_single_record(r) for r in created_records))

#     async def _process_single_record(self, raw_record: HealthDataRecord):
#         """
#         处理单条记录（解析、分析、告警、推送）
#         """
#         source_type = raw_record.schema_type
#         payload = raw_record.payload
#         patient = raw_record.patient
#         device = getattr(raw_record, "device", None)

#         plugin = self.plugin_instances.get(source_type)
#         if not plugin:
#             logger.error(f"[插件池缺失] 未找到 source_type={source_type} 对应插件实例")
#             return

#         try:
#             parsed = await plugin.parse(payload)
#             try:
#                 parsed = await plugin.filter_data(parsed)
#             except NotImplementedError:
#                 pass
#             if not parsed:
#                 await raw_record.update_from_dict({"status": "invalid"}).save()
#                 return
#         except Exception as e:
#             logger.error(f"[插件异常] {source_type} parse error: {e}")
#             await raw_record.update_from_dict({"status": "invalid"}).save()
#             return

#         parsed_list = parsed if isinstance(parsed, list) else [parsed]
#         for item in parsed_list:
#             try:
#                 analysis_result = await plugin.analyze(item)
#             except Exception as e:
#                 logger.error(f"[插件异常] {source_type} analyze error: {e}")
#                 analysis_result = {}

#             result = {**item, **analysis_result}
#             try:
#                 analysis_time = datetime.datetime.now()
#                 risk = analysis_result.get("risk", "未知")
#                 comment = (
#                     f"{source_type}自动分析 | 风险:{risk} | 设备:{getattr(device, 'id', '未知')} "
#                     f"| 患者:{getattr(patient, 'id', '未知')} | 时间:{analysis_time.strftime('%Y-%m-%d %H:%M:%S')}"
#                 )
#                 advanced_record = await Event.create(
#                     patient=patient,
#                     device=device,
#                     recorded_at=raw_record.recorded_at,
#                     analysis_time=analysis_time,
#                     analysis_type=source_type,
#                     result=result,
#                     source_raw=raw_record,
#                     comment=comment,
#                 )
#             except Exception as e:
#                 logger.error(f"[高级记录创建异常] {e}")
#                 continue

#             try:
#                 alerts = await plugin.check_alert(analysis_result)
#             except Exception as e:
#                 logger.error(f"[插件异常] {source_type} check_alert error: {e}")
#                 alerts = []

#             await self.alert_manager.check_and_alert(advanced_record, alerts=alerts)

#             try:
#                 await WebSocketService.push_health_data(patient.id, advanced_record.result)
#             except Exception as e:
#                 logger.error(f"[健康数据推送异常] patient_id={patient.id}, error: {e}")


# pipeline = HealthDataPipeline()
