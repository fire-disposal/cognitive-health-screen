import asyncio
from app.log import logger
from app.service.msgpack.msgpack_handler import start_tcp_server

class MsgpackService:
    """Msgpack异步服务单例，管理TCP监听任务"""
    def __init__(self):
        self._task = None

    async def start(self):
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(start_tcp_server())
            logger.info("Msgpack TCP服务已启动")
        else:
            logger.info("Msgpack TCP服务已在运行")

    async def stop(self):
        if self._task and not self._task.done():
            self._task.cancel()
            logger.info("Msgpack TCP服务已停止")
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def is_running(self):
        return self._task is not None and not self._task.done()

# 单例实例
msgpack_service = MsgpackService()