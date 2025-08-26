import json
from typing import Any, Dict
from datetime import datetime
from app.log import logger
from app.service.health.event_pipeline import event_pipeline

# 使用全局 pipeline 单例

async def handle_mqtt_message(topic: str, payload: bytes, meta: Dict[str, Any]):
    try:
        topic_parts = topic.split("/")
        if len(topic_parts) < 4 or topic_parts[0] != "device":
            logger.error(f"MQTT topic格式错误: {topic}")
            return

        device_id = topic_parts[1]
        message_type = topic_parts[2]
        data_type_str = topic_parts[3]

        if message_type != "data":
            # 仅处理 data 类型
            return

        try:
            raw = json.loads(payload.decode("utf-8"))
        except Exception as e:
            logger.error(f"MQTT数据解码失败: {e}")
            return

        data_field = raw.get("data")
        timestamp = raw.get("timestamp")
        if not isinstance(data_field, dict):
            logger.error("MQTT数据格式错误: data字段不是dict")
            return

        if not data_type_str:
            logger.error(f"数据类型无效: {data_type_str}")
            return

        # 统一入口调用 pipeline，自动处理设备与患者
        device_data = {
            "patient_id": meta.get("patient_id"),
            "device_id": device_id,
            "data_type": data_type_str,
            "measurements": data_field,
            "source": "mqtt",
            "device_model": meta.get("device_model"),
        }
        await event_pipeline.process_device_data(device_data)

        logger.info(f"健康数据已处理: device={device_id}, type={data_type_str}, value={data_field}")

    except Exception as e:
        logger.error(f"数据处理失败: {e}")
