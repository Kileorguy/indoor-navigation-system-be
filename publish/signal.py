from client import fast_mqtt

async def publish_signal(signal : str):
    if fast_mqtt.client.is_connected:
        fast_mqtt.publish("things/signal", signal, qos=2, retain=True)
        return {"result": signal, "message": "Published"}
    else:
        return {"result": signal, "message": "MQTT client not connected"}