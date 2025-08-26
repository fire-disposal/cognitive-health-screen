from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod

@dataclass
class HealthDataEvent:
    """健康数据事件"""
    event_id: str
    event_type: str  # 'blood_pressure_received', 'heart_rate_received' etc.
    patient_id: str
    device_id: str
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

class EventHandler(ABC):
    """事件处理器基类"""
    @abstractmethod
    async def can_handle(self, event: HealthDataEvent) -> bool:
        pass

    @abstractmethod
    async def handle(self, event: HealthDataEvent) -> Optional[Dict[str, Any]]:
        pass
