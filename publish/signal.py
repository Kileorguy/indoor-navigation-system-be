from client import fast_mqtt
import globals

async def publish_signal():
    if fast_mqtt.client.is_connected:
        fast_mqtt.publish("things/signal", globals.boolean_val, qos=2, retain=True)
        return {"result": globals.boolean_val, "message": "Published"}
    else:
        return {"result": globals.boolean_val, "message": "MQTT client not connected"}