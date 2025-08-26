from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.base.base_model import BaseSchema

class AlertCreate(BaseModel):
    device_id: int = Field(..., description="设备ID")
    patient_id: int = Field(..., description="患者ID")
    rule_name: str = Field(..., max_length=64, description="告警规则名")
    level: str = Field(..., max_length=16, description="告警级别")
    message: str = Field(..., description="告警内容")
    event_type: str = Field(None, max_length=64, description="事件类型")
    description: str = Field(None, description="事件内容/详情")
    extra: dict = Field(None, description="扩展字段")

class AlertUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=16, description="告警状态")
    resolved_at: Optional[datetime] = Field(None, description="解除时间")
    message: Optional[str] = Field(None, description="告警内容")
    event_type: Optional[str] = Field(None, max_length=64, description="事件类型")
    description: Optional[str] = Field(None, description="事件内容/详情")
    extra: Optional[dict] = Field(None, description="扩展字段")

class AlertOut(BaseSchema):
    id: int
    device_id: int
    patient_id: int
    rule_name: str
    level: str
    message: str
    event_type: Optional[str]
    description: Optional[str]
    extra: Optional[dict]
    status: str
    created_at: datetime
    resolved_at: Optional[datetime]