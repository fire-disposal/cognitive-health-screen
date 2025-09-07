import asyncio
from tortoise import Tortoise
from app.settings.config import settings
from dotenv import load_dotenv
import os
from loguru import logger

async def init():
    load_dotenv()
    
    # 打印数据库配置
    logger.info("数据库配置：")
    logger.info(f"HOST: {os.getenv('DB_HOST')}")
    logger.info(f"PORT: {os.getenv('DB_PORT')}")
    logger.info(f"USER: {os.getenv('DB_USER')}")
    logger.info(f"DB: {os.getenv('DB_NAME')}")
    
    tortoise_config = settings.TORTOISE_ORM
    logger.info("Tortoise配置：")
    logger.info(f"Connection: {tortoise_config['connections']['postgres']}")
    
    # 初始化 Tortoise ORM
    logger.info("正在初始化 Tortoise ORM...")
    await Tortoise.init(config=tortoise_config)
    
    # 生成 schema
    logger.info("正在生成数据库架构...")
    await Tortoise.generate_schemas()
    
    logger.info("数据库初始化完成")
    # 关闭连接
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(init())