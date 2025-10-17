from client import fast_mqtt
import globals
from config import motor_config
import logging
from services.logs import insert_logs_data

from models.log import Log as LogModel, StatusEnum as LogEnum

logger = logging.getLogger("uvicorn")

"""
function untuk publish navigasi motor
"""
async def start_navigation():

    if fast_mqtt.client.is_connected:
        fast_mqtt.publish("navigation/start/", {
            "start": True
        }, qos=2, retain=True)

        start_log = LogModel(status=LogEnum.ACTIVITY, text="Start navigation")

        await insert_logs_data(start_log)


        return {"result": globals.boolean_val, "message": "Published"}
    else:
        return {"result": globals.boolean_val, "message": "MQTT client not connected"}