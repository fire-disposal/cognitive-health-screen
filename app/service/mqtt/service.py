import asyncio
import json
from typing import Callable, Dict, Optional, Set, Awaitable
from aiomqtt import Client, MqttError
from app.settings.config import settings
from app.models.health.device import Device
from app.service.mqtt.mqtt_handler import handle_mqtt_message
from app.log import logger

MessageHandler = Callable[[str, bytes, Dict[str, str]], Awaitable[None]]

class MQTTService:
    def __init__(self):
        self._active_topics: Set[str] = set()
        self._resubscribe_interval = 60
        self._client: Optional[Client] = None
        self._heartbeat_interval = 30
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._message_queue: asyncio.Queue = asyncio.Queue(maxsize=1000)
        self._retry_count = 3
        self._publisher_task: Optional[asyncio.Task] = None
        self._task = None

    def _get_client_params(self) -> Dict:
        params = settings.MQTT_CONFIG.copy()
        return {k: v for k, v in params.items() if v is not None}

    async def get_subscribe_topics(self) -> Set[str]:
        topics = set()
        devices = await Device.all() 
        for device in devices:
            if device.device_id:
                topics.add(f"device/{device.device_id}/data/+")
                topics.add(f"device/{device.device_id}/status")
                topics.add(f"device/{device.device_id}/config")
        return topics

    async def _subscribe_topics(self, client: Client, topics: Set[str]):
        for topic in topics:
            qos = 1 if any(x in topic for x in ["/status", "/config", "/data"]) else 0
            await client.subscribe(topic, qos=qos)

    async def run(self, handler: MessageHandler = handle_mqtt_message):
        while True:
            try:
                params = self._get_client_params()
                async with Client(**params) as client:
                    self._client = client
                    logger.info("🚀 MQTT 客户端连接成功")
                    self._heartbeat_task = asyncio.create_task(self._start_heartbeat(client))
                    self._publisher_task = asyncio.create_task(self._publish_queue_loop(client))
                    self._active_topics = await self.get_subscribe_topics()
                    await self._subscribe_topics(client, self._active_topics)
                    asyncio.create_task(self._resubscribe_loop(client))
                    async for message in client.messages:
                        topic = str(message.topic)
                        if handler:
                            await self._dispatch_message(topic, message.payload, handler)
            except MqttError as e:
                logger.error(f"MQTT 连接错误: {e}", exc_info=True)
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f"MQTT 客户端运行异常: {e}", exc_info=True)
                await asyncio.sleep(5)

    async def _dispatch_message(self, topic: str, payload: bytes, handler: MessageHandler):
        try:
            parts = topic.split("/")
            meta = {}
            if len(parts) >= 2:
                meta["device_id"] = parts[1]
            if len(parts) >= 3:
                meta["type"] = parts[2]
            await handler(topic, payload, meta)
        except Exception as e:
            logger.error(f"消息处理失败: {e}", exc_info=True)

    async def _resubscribe_loop(self, client: Client):
        while True:
            await asyncio.sleep(self._resubscribe_interval)
            try:
                latest_topics = await self.get_subscribe_topics()
                new_topics = latest_topics - self._active_topics
                if new_topics:
                    await self._subscribe_topics(client, new_topics)
                    self._active_topics.update(new_topics)
            except Exception as e:
                logger.error(f"自动订阅主题失败: {e}", exc_info=True)

    async def _start_heartbeat(self, client: Client):
        while True:
            try:
                await client.publish("heartbeat", "ping", qos=0)
            except Exception as e:
                logger.warning(f"MQTT心跳消息发送失败: {e}")
            await asyncio.sleep(self._heartbeat_interval)

    async def publish_with_retry(self, topic: str, payload: dict):
        await self._message_queue.put((topic, payload))

    async def _publish_queue_loop(self, client: Client):
        while True:
            topic, payload = await self._message_queue.get()
            for _ in range(self._retry_count):
                try:
                    await client.publish(topic, json.dumps(payload), qos=1)
                    break
                except Exception as e:
                    logger.error(f"MQTT消息发布失败: {e}，重试中...")
                    await asyncio.sleep(1)
            else:
                logger.error(f"MQTT消息最终发布失败: {topic}，消息丢弃")

    async def start(self):
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self.run())
            logger.info("MQTT服务已启动")
        else:
            logger.info("MQTT服务已在运行")

    async def stop(self):
        if self._task and not self._task.done():
            self._task.cancel()
            logger.info("MQTT服务已停止")

    def is_running(self):
        return self._task is not None and not self._task.done()

mqtt_service = MQTTService()
