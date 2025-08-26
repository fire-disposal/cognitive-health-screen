from typing import List, Optional, Dict, Any
from tortoise.transactions import atomic
from app.models.health.alert import Alert
from app.schemas.health.alert import AlertCreate, AlertUpdate
from datetime import datetime

from app.controllers.health import BaseCRUDController

class AlertController(BaseCRUDController):
    def __init__(self):
        from app.models.health.alert import Alert
        super().__init__(Alert)

    async def statistics(self) -> Dict[str, int]:
        total = await self.model.all().count()
        active = await self.model.filter(status="active").count()
        resolved = await self.model.filter(status="resolved").count()
        return {"total": total, "active": active, "resolved": resolved}

alert_controller = AlertController()