import asyncio
import logging
from typing import Callable, Dict, List, Any, Coroutine, Set
from enum import Enum, auto

logger = logging.getLogger("event_bus")

class EventType(Enum):
    SERVICE_START = "service_start"
    SERVICE_STOP = "service_stop"
    # 可扩展更多事件类型

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[Any], Coroutine]]] = {}
        self._exception_subscribers: Set[Callable[[Exception], Coroutine]] = set()

    def subscribe(self, event_type: str | EventType, handler: Callable[[Any], Coroutine]):
        """订阅指定类型事件"""
        key = event_type.value if isinstance(event_type, EventType) else event_type
        if key not in self._subscribers:
            self._subscribers[key] = []
        self._subscribers[key].append(handler)

    def unsubscribe(self, event_type: str | EventType, handler: Callable[[Any], Coroutine]):
        """取消订阅"""
        key = event_type.value if isinstance(event_type, EventType) else event_type
        if key in self._subscribers:
            self._subscribers[key].remove(handler)

    def subscribe_exception(self, handler: Callable[[Exception], Coroutine]):
        """订阅异常事件"""
        self._exception_subscribers.add(handler)

    def unsubscribe_exception(self, handler: Callable[[Exception], Coroutine]):
        self._exception_subscribers.discard(handler)

    async def publish(self, event_type: str | EventType, event: Any):
        """异步发布事件，分发给所有订阅者"""
        key = event_type.value if isinstance(event_type, EventType) else event_type
        handlers = self._subscribers.get(key, [])
        tasks = []
        for handler in handlers:
            try:
                tasks.append(asyncio.create_task(handler(event)))
            except Exception as e:
                await self._publish_exception(e)
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _publish_exception(self, exc: Exception):
        """分发异常事件"""
        for handler in self._exception_subscribers:
            try:
                await handler(exc)
            except Exception as e:
                logger.error(f"异常分发失败: {e}")

# 单例实例
event_bus = EventBus()