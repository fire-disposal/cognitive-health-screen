from tortoise import fields
from typing import List, Optional

from app.models.base import BaseModel
from app.models.health.device import Device

class DeviceGroup(BaseModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    description = fields.TextField(null=True)
    rules = fields.JSONField(default=list, description="分组规则，支持基于标签的动态分组")
    config = fields.JSONField(default=dict, description="组级别的配置")

    class Meta:
        table = "device_groups"

class DeviceGroupManager:
    async def apply_group_rules(self, device: Device) -> Optional[int]:
        """应用分组规则，返回匹配的分组ID"""
        for group in await DeviceGroup.all():
            if await self._match_rules(device, group.rules):
                return group.id
        return None

    async def _match_rules(self, device: Device, rules: List[dict]) -> bool:
        """简单标签匹配，可扩展为复杂规则"""
        device_tags = set(device.tags or [])
        for rule in rules:
            rule_tags = set(rule.get("tags", []))
            if rule_tags and rule_tags.issubset(device_tags):
                return True
        return False

    async def batch_update_groups(self):
        """批量更新设备分组"""
        devices = await Device.all()
        for device in devices:
            group_id = await self.apply_group_rules(device)
            if group_id != device.group_id:
                device.group_id = group_id
                await device.save()