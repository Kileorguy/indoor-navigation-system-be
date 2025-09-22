from client import fast_mqtt

async def publish_signal(signal : str):
    fast_mqtt.publish("/things/signal", signal)
    return {"result": True, "message": "Published"}