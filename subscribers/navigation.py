import json
from gmqtt import Client as MQTTClient
from typing import Any
from client import fast_mqtt
import logging

logger = logging.getLogger("uvicorn")

# code testing
@fast_mqtt.subscribe("navigation/end/", qos=0)
async def save_end_navigation(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    pass
