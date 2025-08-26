from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

class EventCreate(BaseModel):
    event_id: str = Field(..., description="事件ID")
    event_type: str = Field(..., description="事件类型")
    patient_id: str = Field(..., description="患者ID")
    device_id: str = Field(..., description="设备ID")
    timestamp: datetime = Field(..., description="事件时间")
    data: Dict[str, Any] = Field(..., description="事件数据")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")

class EventUpdate(BaseModel):
    event_id: Optional[str] = Field(None, description="事件ID")
    event_type: Optional[str] = Field(None, description="事件类型")
    patient_id: Optional[str] = Field(None, description="患者ID")
    device_id: Optional[str] = Field(None, description="设备ID")
    timestamp: Optional[datetime] = Field(None, description="事件时间")
    data: Optional[Dict[str, Any]] = Field(None, description="事件数据")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")

class EventOut(BaseModel):
    event_id: str
    event_type: str
    patient_id: str
    device_id: str
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any]

__all__ = [
    "EventCreate",
    "EventUpdate",
    "EventOut",
]