import asyncio
from fastapi import APIRouter, WebSocket
from ws.ws_manager import manager
import json
from handlers import ws_handler as handler
route = APIRouter()

@route.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            msg = await ws.receive_text()
            request = json.loads(msg)
            handler.handle_ws_request(request)

    finally:
        manager.disconnect(ws)