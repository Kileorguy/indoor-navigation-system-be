from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from client import fast_mqtt
from gmqtt import Client as MQTTClient
from subscribers import signal, rssi, ultrasonic, ble_sample_data
import logging
from routers.signal import route as signal_route
from routers.ws import route as ws_route
from routers.motor import route as motor_route

logger = logging.getLogger("uvicorn")

logger.info("Starting uvicorn serverrrrrr...")

@asynccontextmanager
async def lifespan(app_: FastAPI):
    await fast_mqtt.mqtt_startup()
    yield
    await fast_mqtt.mqtt_shutdown()
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://148.230.101.206:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

app.include_router(signal_route)
app.include_router(ws_route)
app.include_router(motor_route)

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

