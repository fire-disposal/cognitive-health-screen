import os
from typing import Optional
from tortoise import Tortoise

from app.log import logger
from app.settings.config import settings
from app.core.init_data import DataInitializer


class DBInitManager:
    def __init__(self, mode: Optional[str] = None):
        self.mode = (mode or os.getenv("INIT_MODE", "auto")).lower()

    async def run(self):
        logger.info(f"数据库初始化模式（无 Aerich）: {self.mode}")

        if self.mode == "skip":
            logger.info("跳过所有数据库初始化")
            return

        await Tortoise.init(config=settings.TORTOISE_ORM)

        if self.mode == "rebuild":
            await self.drop_all_tables()
            await self.init_structure()
            await self.init_data(force=True)
        elif self.mode == "auto":
            await self.init_structure()
            await self.maybe_init_data(force=False)

        await Tortoise.close_connections()

    async def init_structure(self):
        try:
            await Tortoise.generate_schemas(safe=True)
            logger.info("数据库结构初始化完成")
        except Exception as e:
            logger.error(f"数据库结构初始化失败: {e}")

    async def drop_all_tables(self):
        logger.warning("重建模式启用：正在**彻底删除所有数据表**...")
        try:
            conn = Tortoise.get_connection("postgres")
            result = await conn.execute_query("""
                SELECT table_name FROM information_schema.tables
                WHERE table_schema='public';
            """)
            tables = [row[0] for row in result[1]]
            for table in tables:
                await conn.execute_query(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
            logger.info("所有表已成功删除")
        except Exception as e:
            logger.error(f"删除表失败: {e}")

    async def maybe_init_data(self, force: bool):
        try:
            conn = Tortoise.get_connection("postgres")
            result = await conn.execute_query("""
                SELECT COUNT(*) FROM information_schema.tables
                WHERE table_schema = 'public';
            """)
            table_count = result[1][0][0]
            if table_count > 0:
                logger.info("已检测到表结构，跳过业务数据初始化")
                return
        except Exception as e:
            logger.warning(f"表检测失败，执行默认数据初始化: {e}")

        await self.init_data(force)

    async def init_data(self, force: bool):
        try:
            await DataInitializer.initialize_basic_data()
            logger.info("业务数据初始化完成")
        except Exception as e:
            logger.error(f"业务数据初始化失败: {e}")


# 单例（推荐用于 main.py 或后台任务初始化）
init_manager = DBInitManager()
