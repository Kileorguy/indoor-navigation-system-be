import asyncio
from fastapi import APIRouter, WebSocket
from ws.ws_manager import manager

route = APIRouter()

@route.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            _ = await ws.receive_text()
    finally:
        manager.disconnect(ws)