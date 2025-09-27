import json
from gmqtt import Client as MQTTClient
from typing import Any
from client import fast_mqtt
from ws.ws_manager import manager
import logging

logger = logging.getLogger("uvicorn")

@fast_mqtt.subscribe("things/ultrasonic", qos=0)
async def save_start_rssi(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    payload = json.loads(payload.decode())

    ultrasonic1 = payload["ultrasonic1"]
    ultrasonic2 = payload["ultrasonic2"]
    ultrasonic3 = payload["ultrasonic3"]

    # await manager.broadcast_json({
    #     "type": "ultrasonic",
    #     "ultrasonic1": ultrasonic1,
    #     "ultrasonic2": ultrasonic2,
    #     "ultrasonic3": ultrasonic3,
    # })

    logger.info("Ultrasonic data sent to websocket")

