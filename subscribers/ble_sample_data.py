import json
from gmqtt import Client as MQTTClient
from typing import Any
from client import fast_mqtt
import logging
import services.ble_sample_data as service 

logger = logging.getLogger("uvicorn")

@fast_mqtt.subscribe("things/calibrate", qos=0)
async def insert_ble_sample_data(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    logger.error("AHHH")
    payload = json.loads(payload.decode())
    await service.insert_ble_sample_data(payload)

    return