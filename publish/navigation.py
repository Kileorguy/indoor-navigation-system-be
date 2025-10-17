from client import fast_mqtt
import globals
from config import motor_config
import logging

logger = logging.getLogger("uvicorn")

"""
function untuk publish navigasi motor
"""
async def start_navigation():



    if fast_mqtt.client.is_connected:
        fast_mqtt.publish("navigation/start/", {
            "start": True
        }, qos=2, retain=True)
        return {"result": globals.boolean_val, "message": "Published"}
    else:
        return {"result": globals.boolean_val, "message": "MQTT client not connected"}