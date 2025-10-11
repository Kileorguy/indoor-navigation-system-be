import json
from typing import Set
from fastapi import WebSocket

"""
class untuk inisialisasi websocket
"""
class ConnectionManager:
    def __init__(self):
        self.clients: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.clients.add(ws)

    def disconnect(self, ws: WebSocket):
        self.clients.discard(ws)

    async def broadcast_json(self, data: dict):
        dead = []
        for ws in list(self.clients):
            try:
                await ws.send_text(json.dumps(data))
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

manager = ConnectionManager()