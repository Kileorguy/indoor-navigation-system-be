from client import fast_mqtt
import globals
from config import motor_config


async def publish_motor(direction : str, enable : bool):
    if fast_mqtt.client.is_connected:
        fast_mqtt.publish("things/motor/", {
            "dir" : direction,
            "en" : enable,
            "unit": motor_config.FORWARD_UNIT
        }, qos=2, retain=True)
        return {"result": globals.boolean_val, "message": "Published"}
    else:
        return {"result": globals.boolean_val, "message": "MQTT client not connected"}