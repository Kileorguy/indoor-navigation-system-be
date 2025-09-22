from gmqtt import Client as MQTTClient
from typing import Any
from client import fast_mqtt
from publish import signal


import logging

logger = logging.getLogger("uvicorn")

@fast_mqtt.subscribe("things/toggle", qos=1)
async def toggle(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    msg = "Toggle Message: ", topic, payload.decode(), qos, properties

    logger.info(msg)

    logger.info(await signal.publish_signal(payload.decode()))

