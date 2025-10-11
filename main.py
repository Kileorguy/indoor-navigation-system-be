from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from client import fast_mqtt
from gmqtt import Client as MQTTClient
from subscribers import rssi, ultrasonic, ble_sample_data
import logging
from routers.ws import route as ws_route
from routers.motor import route as motor_route

# setup logger buat ngeprint info ke terminal
logger = logging.getLogger("uvicorn")
logger.info("Starting uvicorn serverrrrrr...")

# fungsi ini jalan pas server nyala dan matiin koneksi mqtt pas server stop
@asynccontextmanager
async def lifespan(app_: FastAPI):
    await fast_mqtt.mqtt_startup()   # nyalain koneksi mqtt
    yield                            # jalanin semua proses server
    await fast_mqtt.mqtt_shutdown()  # matiin koneksi mqtt pas server mati

# bikin instance fastapi dan pakai lifespan di atas
app = FastAPI(lifespan=lifespan)

# setup cors biar frontend di alamat ini bisa akses api ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://148.230.101.206:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# include semua router dari folder routers
app.include_router(ws_route)
app.include_router(motor_route)

# event pas mqtt connect ke broker
@fast_mqtt.on_connect()
def connect(client: MQTTClient, flags: int, rc: int, properties):
    # client.subscribe("things/+/+")
    message = ("Connected: ", client, flags, rc, properties)
    logger.info(message)

# event pas mqtt disconnect (buat debug)
@fast_mqtt.on_disconnect()
def disconnect(client: MQTTClient, packet, exc=None):
    print("Disconnected")

# event pas mqtt subscribe (buat debug)
@fast_mqtt.on_subscribe()
def subscribe(client: MQTTClient, mid: int, qos: int, properties):
    print("subscribed", client, mid, qos, properties)

# route basic di root url
@app.get("/")
async def root():
    return {"message": "Hello World"}
