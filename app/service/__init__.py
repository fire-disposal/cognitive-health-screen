import asyncio

from app.core.event_bus import event_bus
from app.service.mqtt import mqtt_service
from app.service.msgpack import msgpack_service
from app.service.mock import mock_service
from app.service.ws import ws_service

from app.service.health.event_pipeline import (
    HealthDataPersistenceHandler,
)
from app.service.health.handler.mattress import MattressHandler
from app.service.health.handler.heart_rate import HeartRateHandler
from app.service.health.handler.blood_pressure import BloodPressureHandler

# 服务注册
def register_services():
    """注册所有服务，可扩展"""
    return [
        mqtt_service,
        msgpack_service,
        mock_service,
        ws_service,
    ]

# 健康数据事件处理器注册
def register_health_handlers():
    """注册所有健康数据 EventHandler"""
    handlers = [
        HealthDataPersistenceHandler(),
        MattressHandler(),
        HeartRateHandler(),
        BloodPressureHandler(),
    ]
    for handler in handlers:
        event_bus.subscribe("health_data", handler)

# 服务事件订阅
def subscribe_service_events():
    """订阅服务相关事件"""
    async def _on_service_start(_=None):
        asyncio.create_task(mqtt_service.start())
        asyncio.create_task(msgpack_service.start())
        asyncio.create_task(mock_service.start())
        asyncio.create_task(ws_service.start_cleanup())

    async def _on_service_stop(_=None):
        await mqtt_service.stop()
        await msgpack_service.stop()
        await mock_service.stop()
        await ws_service.stop()

    event_bus.subscribe("service_start", _on_service_start)
    event_bus.subscribe("service_stop", _on_service_stop)

# 初始化入口
register_services()
register_health_handlers()
subscribe_service_events()

