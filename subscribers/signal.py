from gmqtt import Client as MQTTClient
from typing import Any
from client import fast_mqtt
from publish import signal

import globals

import logging

logger = logging.getLogger("uvicorn")

@fast_mqtt.subscribe("things/toggle", qos=1)
async def toggle(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    msg = "Toggle Message: ", topic, payload.decode(), qos, properties

    logger.info(msg)
    if payload.decode() == "true": globals.boolean_val = True
    else : globals.boolean_val = False

    result = await signal.publish_signal()
    logger.info(result)

