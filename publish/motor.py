from client import fast_mqtt
import globals

async def publish_motor(unit : int, direction : str):
    if fast_mqtt.client.is_connected:
        fast_mqtt.publish("things/motor/", {
            "dir" : direction,
            "unit": unit
        }, qos=2, retain=True)
        return {"result": globals.boolean_val, "message": "Published"}
    else:
        return {"result": globals.boolean_val, "message": "MQTT client not connected"}