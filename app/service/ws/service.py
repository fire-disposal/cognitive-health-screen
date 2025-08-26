import asyncio
from typing import Dict, Set, List
from fastapi import WebSocket
from collections import defaultdict
from app.log import logger

class WebSocketService:
    """
    高效 WebSocket 异步服务
    负责连接池、订阅、广播、自动清理等
    """

    async def push_health_data(self, patient_id: int, data: dict):
        """推送健康数据到指定患者主题"""
        topic = f"health_data:{patient_id}"
        await self.broadcast(topic, data)

    async def push_alert(self, patient_id: int, alert: dict):
        """推送告警到指定患者主题"""
        topic = f"alert:{patient_id}"
        await self.broadcast(topic, alert)
        
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()
        self._cleanup_task = None

    async def connect(self, websocket: WebSocket, topics: List[str]):
        await websocket.accept()
        async with self._lock:
            for topic in topics:
                self.active_connections[topic].add(websocket)
                logger.info(f"WebSocket客户端订阅主题: {topic}")

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            for topic, connections in self.active_connections.items():
                if websocket in connections:
                    connections.remove(websocket)
                    logger.info(f"已清理断开连接的订阅: {topic}")

    async def broadcast(self, topic: str, message: dict):
        if topic not in self.active_connections:
            return
        disconnected = set()
        send_tasks = []
        for websocket in self.active_connections[topic]:
            send_tasks.append(self._safe_send(websocket, message, disconnected))
        await asyncio.gather(*send_tasks)
        if disconnected:
            async with self._lock:
                self.active_connections[topic] -= disconnected

    async def _safe_send(self, websocket: WebSocket, message: dict, disconnected: set):
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"发送WebSocket消息失败: {e}")
            disconnected.add(websocket)

    async def start_cleanup(self, interval: int = 60):
        if self._cleanup_task is None or self._cleanup_task.done():
            self._cleanup_task = asyncio.create_task(self._cleanup_loop(interval))

    async def _cleanup_loop(self, interval: int):
        while True:
            await asyncio.sleep(interval)
            await self._cleanup_disconnected()

    async def _cleanup_disconnected(self):
        async with self._lock:
            for topic, connections in list(self.active_connections.items()):
                to_remove = {ws for ws in connections if ws.client_state.name != "CONNECTED"}
                if to_remove:
                    connections -= to_remove
                    logger.info(f"自动清理失效WebSocket连接: {topic}")

    async def stop(self):
        if self._cleanup_task and not self._cleanup_task.done():
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass

ws_service = WebSocketService()