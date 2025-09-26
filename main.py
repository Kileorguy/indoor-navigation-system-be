from contextlib import asynccontextmanager

from fastapi import FastAPI
from client import fast_mqtt
from gmqtt import Client as MQTTClient
from subscribers import signal, rssi
import logging
from routers.signal import  route as signal_route


logger = logging.getLogger("uvicorn")

logger.info("Starting uvicorn serverrrrrr...")

@asynccontextmanager
async def lifespan(app_: FastAPI):
    await fast_mqtt.mqtt_startup()
    yield
    await fast_mqtt.mqtt_shutdown()
app = FastAPI(lifespan=lifespan)

app.include_router(signal_route)


@fast_mqtt.on_connect()
def connect(client: MQTTClient, flags: int, rc: int, properties):
    # client.subscribe("things/+/+")
    message = ("Connected: ", client, flags, rc, properties)
    logger.info(message)

# debug
@fast_mqtt.on_disconnect()
def disconnect(client: MQTTClient, packet, exc=None):
    print("Disconnected")

# debug
@fast_mqtt.on_subscribe()
def subscribe(client: MQTTClient, mid: int, qos: int, properties):
    print("subscribed", client, mid, qos, properties)

@app.get("/")
async def root():
    return {"message": "Hello World"}

