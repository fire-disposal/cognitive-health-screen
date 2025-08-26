from typing import List, Optional, Dict, Any
from tortoise.transactions import atomic
from app.models.health.event import Event

from app.controllers.health import BaseCRUDController

class EventController(BaseCRUDController):
    def __init__(self):
        from app.models.health.event import Event
        super().__init__(Event)

    async def statistics(self) -> Dict[str, int]:
        total = await self.model.all().count()
        types = await self.model.all().distinct().values_list("event_type", flat=True)
        type_stats = {t: await self.model.filter(event_type=t).count() for t in types}
        return {"total": total, "by_type": type_stats}

event_controller = EventController()