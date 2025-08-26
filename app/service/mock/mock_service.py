import asyncio
from app.log import logger
from app.service.mock.health_mock_factory import health_mock_factory
from app.service.mock.mock_config import MOCK_CONFIG
from app.service.mock.patient_manager import PatientManager

class MockService:
    def __init__(self):
        self.running = False
        self.tasks = []
        self.patient_manager = PatientManager(MOCK_CONFIG)

    async def start(self):
        self.running = True
        logger.info("虚拟病人模拟服务启动")
        # 按配置调度每个病人的设备数据生成
        for patient in self.patient_manager.get_patients():
            for device in patient.devices:
                interval = device.get("frequency", 60)
                task = asyncio.create_task(self._device_loop(patient.id, device, interval))
                self.tasks.append(task)

    async def _device_loop(self, patient_id, device, interval):
        plugin_type = device["type"]
        count = device.get("count", 1)
        while self.running:
            # 异步高频生成数据
            data = await health_mock_factory.generate_for_patient(
                patient_id, [device], count=count, interval=0
            )
            records = data.get(plugin_type, [])
            logger.info(f"模拟数据已生成: 病人[{patient_id}] 设备[{plugin_type}] 数据: {records}")
            await asyncio.sleep(interval)

    async def stop(self):
        self.running = False
        logger.info("虚拟病人模拟服务已停止")
        # 等待所有任务结束
        for task in self.tasks:
            task.cancel()
        self.tasks.clear()

    def is_running(self):
        return self.running

mock_service = MockService()
