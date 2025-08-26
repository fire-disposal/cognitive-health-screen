from typing import Any, Dict, List
from app.service.health.handler.base import EventHandler, HealthDataEvent

class BloodPressureHandler(EventHandler):
    """
    本插件用于血压健康数据的解析、分析与自动告警，支持异常事件自管理。
    血压数据插件：解析-分析-告警一体化
    支持异常事件自管理
    数据结构参数示例：
    原始数据 raw_data:
        {
            "systolic": 120,      # 收缩压
            "diastolic": 80,      # 舒张压
            "pulse": 70,          # 脉搏
            "timestamp": "2025-08-09T07:34:27Z"
        }
    解析后数据 parsed_data:
        {
            "systolic": 120,
            "diastolic": 80,
            "pulse": 70,
            "recorded_at": "2025-08-09T07:34:27Z",
            "status": "normal"
        }
    分析结果 analysis_result:
        {
            "risk": "正常",
            "value": 120
        }
    告警 alerts:
        [
            {
                "rule_name": "血压异常",
                "level": "warning",
                "message": "血压异常: 150",
                "event_type": "blood_pressure",
                "description": "自动检测血压异常",
                "extra": {"value": 150},
                "status": "active"
            }
        ]
    """
    def __init__(self):
        self.name = "血压支持"
        self.abnormal_events = []

    async def can_handle(self, event: HealthDataEvent) -> bool:
        return event.event_type == "blood_pressure_received"

    async def handle(self, event: HealthDataEvent) -> dict:
        systolic = event.data.get("systolic")
        diastolic = event.data.get("diastolic")
        pulse = event.data.get("pulse")
        # 极端异常过滤
        if systolic is not None and (systolic < 40 or systolic > 300):
            return None
        if diastolic is not None and (diastolic < 20 or diastolic > 200):
            return None
        if pulse is not None and (pulse < 20 or pulse > 250):
            return None

        risk = "正常"
        if systolic is not None:
            if systolic > 140:
                risk = "高血压"
                self.abnormal_events.append({"type": "high", "value": systolic})
            elif systolic < 90:
                risk = "低血压"
                self.abnormal_events.append({"type": "low", "value": systolic})

        alerts = []
        if risk != "正常":
            alerts.append({
                "rule_name": "血压异常",
                "level": "warning",
                "message": f"{risk}: {systolic}",
                "event_type": "blood_pressure",
                "description": "自动检测血压异常",
                "extra": {"value": systolic, "events": self.abnormal_events},
                "status": "active"
            })
        return {
            "risk": risk,
            "value": systolic,
            "alerts": alerts
        }