import random
import asyncio
from typing import List, Dict, Any
from app.service.mock.patient_manager import PatientManager
from app.service.mock.mock_config import MOCK_CONFIG
from app.service.health.event_pipeline import event_pipeline

class HealthMockFactory:
    """
    健康数据模拟工厂：支持高频、大量、异步事件驱动健康数据流生成
    完全独立于 health.handler 与 plugin_manager
    """
    def __init__(self):
        pass

    async def generate_for_patient(self, patient_id: str, devices: List[Dict[str, Any]], count: int = 10, interval: float = 0.1) -> Dict[str, List[Any]]:
        """
        按病人配置异步高频生成健康数据流
        :param patient_id: 病人ID
        :param devices: 设备列表
        :param count: 每设备生成数据条数
        :param interval: 生成间隔（秒）
        :return: {设备类型: [处理结果列表]}
        """
        result = {}
        async def gen_device(device):
            device_type = device["type"]
            device_id = device.get("id", f"mock_{device_type}_{random.randint(1000,9999)}")
            bias = device.get("bias", {})
            scenario = device.get("scenario", "normal")
            data_list = []
            for _ in range(count):
                measurements = self._random_measurements(device_type, bias, scenario)
                device_data = {
                    "patient_id": patient_id,
                    "device_id": device_id,
                    "data_type": device_type,
                    "measurements": measurements
                }
                results = await event_pipeline.process_device_data(device_data)
                data_list.append(results)
                await asyncio.sleep(interval)
            return device_type, data_list

        tasks = [gen_device(device) for device in devices]
        device_results = await asyncio.gather(*tasks)
        for device_type, data_list in device_results:
            result[device_type] = data_list
        return result

    def _random_measurements(self, device_type: str, bias: dict, scenario: str) -> dict:
        # 根据设备类型生成合理 mock 数据，可扩展更多类型
        if device_type == "heart_rate":
            rate = random.randint(50, 120)
            rate += bias.get("rate", 0)
            return {"rate": rate, "scenario": scenario}
        elif device_type == "blood_pressure":
            sys = random.randint(100, 140) + bias.get("sys", 0)
            dia = random.randint(60, 90) + bias.get("dia", 0)
            return {"sys": sys, "dia": dia, "scenario": scenario}
        elif device_type == "mattress":
            hb = random.randint(60, 100) + bias.get("hb", 0)
            br = random.randint(12, 20) + bias.get("br", 0)
            we = random.randint(50, 80) + bias.get("we", 0)
            return {"hb": hb, "br": br, "we": we, "scenario": scenario}
        measurements = {**bias}
        measurements["scenario"] = scenario
        return measurements

    async def generate_all_patients(self, patients: List[Any], count: int = 10, interval: float = 0.1) -> Dict[str, Dict[str, List[Any]]]:
        """
        为所有虚拟病人异步高频生成健康数据流
        :param patients: 虚拟病人列表
        :param count: 每设备生成数据条数
        :param interval: 生成间隔（秒）
        :return: {病人ID: {设备类型: [处理结果列表]}}
        """
        all_data = {}
        tasks = [
            self.generate_for_patient(patient.id, patient.devices, count, interval)
            for patient in patients
        ]
        patient_results = await asyncio.gather(*tasks)
        for patient, data in zip(patients, patient_results):
            all_data[patient.id] = data
        return all_data

health_mock_factory = HealthMockFactory()