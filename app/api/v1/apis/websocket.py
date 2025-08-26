from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

from app.log import logger
from app.service.ws_server import ws_manager

router = APIRouter()

from app.controllers.ws_controller import WSController

@router.websocket("/ws/health")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket连接端点，所有订阅/取消订阅业务由 WSController 处理
    """
    await WSController.handle(websocket)