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
async def start_navigation(x:int, y:int):

    if fast_mqtt.client.is_connected:
        fast_mqtt.publish("navigation/start/", {
            "x": x,
            "y": y
        }, qos=2, retain=True)

        start_log = LogModel(status=LogEnum.ACTIVITY, text="Start navigation")

        await insert_logs_data(start_log)


        return {"message": "Published"}
    else:
        return {"message": "MQTT client not connected"}