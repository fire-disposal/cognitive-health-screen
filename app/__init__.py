from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from tortoise import Tortoise

from app.log import logger
from app.core.exceptions import SettingNotFound
from app.core.init_db import init_manager
from app.core.init_app import (
    make_middlewares,
    register_exceptions,
    register_routers,
)

try:
    from app.settings.config import settings
except ImportError:
    raise SettingNotFound("Can not import settings")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ===== 初始化数据库 =====
    await Tortoise.init(config=settings.TORTOISE_ORM)
    await init_manager.run()

    # ===== 发布服务启动事件 =====
    from app.core.event_bus import event_bus, EventType
    try:
        await event_bus.publish(EventType.SERVICE_START, {"app": app})
    except Exception as e:
        logger.error(f"服务启动事件分发异常: {e}")

    yield  # 应用运行中

    # ===== 清理资源 =====
    logger.info("应用正在关闭...")
    await Tortoise.close_connections()

    # ===== 发布服务关闭事件 =====
    try:
        await event_bus.publish(EventType.SERVICE_STOP, {"app": app})
    except Exception as e:
        logger.error(f"服务关闭事件分发异常: {e}")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.VERSION,
        openapi_url="/openapi.json",
        middleware=make_middlewares(),
        lifespan=lifespan,
    )
    register_exceptions(app)
    register_routers(app, prefix="/api")
    return app


app = create_app()
