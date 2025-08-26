import os
import sys
import asyncio
import uvicorn
from uvicorn.config import LOGGING_CONFIG
from dotenv import load_dotenv


def print_env():
    keys = [
        "TAG",
        "DB_HOST", 
        "DB_PORT",
        "DB_USER",
        "DB_PASSWORD",
        "DB_NAME",
        "INIT_MODE",
        "MQTT_BROKER_HOST",
        "MQTT_BROKER_PORT",
        "AI_API_KEY",
        "AI_BASE_URL",
        "AI_MODEL",
    ]
    print("=" * 60)
    for k in keys:
        print(f"{k}={os.getenv(k)}")
    print("=" * 60)

if __name__ == "__main__":
    if sys.platform == "win32":
        from asyncio import WindowsSelectorEventLoopPolicy
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    load_dotenv()
    print_env()

    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    LOGGING_CONFIG["formatters"]["default"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s - %(levelname)s - %(client_addr)s - "%(request_line)s" %(status_code)s'
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=9999,
        reload=False,
        log_config=LOGGING_CONFIG,
        loop="asyncio",
    )
