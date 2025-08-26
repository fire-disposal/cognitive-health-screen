import asyncio
import msgpack
from app.log import logger
from app.service.health.event_pipeline import event_pipeline

TCP_PORT = 5858
MAGIC = b"\xab\xcd"

import crcmod


def crc8(data: bytes) -> int:
    crc_func = crcmod.mkCrcFun(0x131, initCrc=0x00, xorOut=0x00)
    return crc_func(data)


async def process_payload(data: bytes):
    try:
        unpacked = msgpack.unpackb(data, raw=False)
        logger.info(f"成功接收msg报文: 原始data={data.hex()} 解包后={unpacked}")
        return unpacked
    except Exception as e:
        logger.error(f"数据处理异常: {e}, 原始data={data.hex()}")
        return None


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    buffer = b""
    while True:
        try:
            chunk = await reader.read(1024)
            if not chunk:
                break
            buffer += chunk

            while len(buffer) >= 4:
                if buffer[:2] != MAGIC:
                    idx = buffer.find(MAGIC)
                    if idx == -1:
                        logger.warning(f"丢弃无效数据: {buffer[:16].hex()}")
                        buffer = b""
                        break
                    logger.warning(f"跳过至Magic头: {buffer[:idx].hex()}")
                    buffer = buffer[idx:]
                    if len(buffer) < 4:
                        break

                length = buffer[2]
                crc_val = buffer[3]

                if not (1 <= length <= 256):
                    logger.warning(f"非法长度字段: {length}, 包头: {buffer[:16].hex()}")
                    buffer = buffer[4:]
                    continue

                if len(buffer) < 4 + length:
                    break  # 不完整，等待下次读入

                data = buffer[4 : 4 + length]
                if crc8(data) != crc_val:
                    logger.warning(f"CRC错误: recv={crc_val}, calc={crc8(data)}, data={data.hex()}")
                    buffer = buffer[4 + length :]
                    continue

                payload = await process_payload(data)
                if not payload:
                    buffer = buffer[4 + length :]
                    continue

                device_sn = payload.get("sn")
                if not device_sn:
                    logger.warning(f"缺失设备序列号: {payload}")
                    buffer = buffer[4 + length :]
                    continue

                # 统一调用 pipeline 处理数据，自动注册设备与患者
                # 使用全局 pipeline 单例，避免重复初始化
                device_data = {
                    "patient_id": payload.get("patient_id"),
                    "device_id": device_sn,
                    "data_type": "mattress",
                    "measurements": payload,
                    "source": "msgpack"
                }
                await event_pipeline.process_device_data(device_data)

                buffer = buffer[4 + length :]

        except Exception as e:
            logger.error(f"TCP处理异常: {e}")
            break


async def start_tcp_server():
    server = await asyncio.start_server(handle_client, host="0.0.0.0", port=TCP_PORT)
    logger.info(f"床垫数据监听端口: {TCP_PORT}")
    async with server:
        await server.serve_forever()
