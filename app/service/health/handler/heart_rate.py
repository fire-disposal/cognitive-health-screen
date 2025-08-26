from typing import Any, Dict, List
from app.service.health.handler.base import EventHandler, HealthDataEvent

class HeartRateHandler(EventHandler):
    """
    心率数据插件：解析-分析-告警一体化
    支持异常事件自管理
    数据结构参数示例：
    原始数据 raw_data:
        {
            "rate": 75,                # 心率
            "timestamp": "2025-08-09T07:34:27Z"
        }
    解析后数据 parsed_data:
        {
            "heart_rate": 75,
            "recorded_at": "2025-08-09T07:34:27Z",
            "status": "normal"
        }
    分析结果 analysis_result:
        {
            "risk": "正常",
            "value": 75
        }
    告警 alerts:
        [
            {
                "rule_name": "心率异常",
                "level": "critical",
                "message": "心率异常: 130",
                "event_type": "heart_rate",
                "description": "自动检测心率异常",
                "extra": {"value": 130},
                "status": "active"
            }
        ]
    """
    def __init__(self):
        self.name = "心率支持"
        self.abnormal_events = []

    async def can_handle(self, event: HealthDataEvent) -> bool:
        return event.event_type == "heart_rate_received"

    async def handle(self, event: HealthDataEvent) -> dict:
        hr = event.data.get("rate")
        if hr is not None and (hr < 10 or hr > 300):
            return None

        risk = "正常"
        if hr is not None:
            if hr > 120:
                risk = "心率过快"
                self.abnormal_events.append({"type": "fast", "value": hr})
            elif hr < 50:
                risk = "心率过慢"
                self.abnormal_events.append({"type": "slow", "value": hr})

        alerts = []
        if risk != "正常":
            alerts.append({
                "rule_name": "心率异常",
                "level": "critical",
                "message": f"{risk}: {hr}",
                "event_type": "heart_rate",
                "description": "自动检测心率异常",
                "extra": {"value": hr, "events": self.abnormal_events},
                "status": "active"
            })
        return {
            "risk": risk,
            "value": hr,
            "alerts": alerts
        }