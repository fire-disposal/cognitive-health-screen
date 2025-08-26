from .patient import patient_controller
from .device import device_controller

__all__ = ["patient_controller", "device_controller"]
from typing import Type, Any, Dict, Optional
from tortoise.transactions import atomic

class BaseCRUDController:
    def __init__(self, model: Any):
        self.model = model

    async def get(self, id: int) -> Optional[Any]:
        return await self.model.get_or_none(id=id)

    async def list(
        self,
        filters: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 10,
        order_by: str = "-id"
    ) -> Dict[str, Any]:
        query = self.model.all()
        if filters:
            for field, value in filters.items():
                if value is not None:
                    query = query.filter(**{field: value})
        total = await query.count()
        items = await query.offset(skip).limit(limit).order_by(order_by)
        return {"total": total, "items": items}

    @atomic()
    async def create(self, obj_in: dict) -> Any:
        obj = await self.model.create(**obj_in)
        return obj

    @atomic()
    async def update(self, id: int, obj_in: dict) -> Optional[Any]:
        obj = await self.model.get_or_none(id=id)
        if not obj:
            return None
        for field, value in obj_in.items():
            setattr(obj, field, value)
        await obj.save()
        return obj

    @atomic()
    async def remove(self, id: int) -> bool:
        deleted = await self.model.filter(id=id).delete()
        return deleted > 0
# 用于健康数据二次处理的业务逻辑目录