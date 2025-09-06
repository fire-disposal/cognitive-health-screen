import os
import typing

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    VERSION: str = "0.1.0"
    APP_TITLE: str = "IoMT Digital Twin Platform"
    PROJECT_NAME: str = "VIoMT Digital Twin Platform"
    APP_DESCRIPTION: str = "Description"

    CORS_ORIGINS: typing.List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: typing.List = ["*"]
    CORS_ALLOW_HEADERS: typing.List = ["*"]

    DEBUG: bool = True

    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(BASE_DIR, "app/logs")
    SECRET_KEY: str = "ef883c8481d97cdf955bec005cad07e828bf9af0d911420b5664768c35d14361"  # openssl rand -hex 32
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 day
    TORTOISE_ORM: dict = {
        "connections": {
            "postgres": {
                "engine": "tortoise.backends.asyncpg",
                "credentials": {
                    "host": os.getenv("DB_HOST", "localhost"),  # Database host address
                    "port": int(os.getenv("DB_PORT", 5432)),  # Database port
                    "user": os.getenv("DB_USER", "postgres"),  # Database username
                    "password": os.getenv("DB_PASSWORD", "postgres"),  # Database password
                    "database": os.getenv("DB_NAME", "digital_twin"),  # Database name
                },
            },
        },
        "apps": {
            "models": {
                "models": ["app.models", "aerich.models"],
                "default_connection": "postgres",
            },
        },
        "use_tz": False,  # Whether to use timezone-aware datetimes
        "timezone": "Asia/Shanghai",  # Timezone setting
    }
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    # 数据库初始化配置
    INIT_MODE: str = os.getenv("INIT_MODE", "auto")
    AERICH_ENABLED: bool = os.getenv("AERICH_ENABLED", "true").lower() == "false"
    
    # 简化 MQTT 配置
    MQTT_CONFIG: dict = {
        "hostname": os.getenv("MQTT_BROKER_HOST", "localhost"),
        "port": int(os.getenv("MQTT_BROKER_PORT", 1883)),
        "username": os.getenv("MQTT_USERNAME"),
        "password": os.getenv("MQTT_PASSWORD"),
        "identifier": os.getenv("MQTT_CLIENT_ID"),
    }
    
    # WebSocket配置
    WS_HOST: str = os.getenv("WS_HOST", "0.0.0.0")
    WS_PORT: int = int(os.getenv("WS_PORT", 8765))
    WS_PATH: str = os.getenv("WS_PATH", "/ws/health")

    

settings = Settings()

