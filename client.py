from fastapi_mqtt import FastMQTT
from config import mqtt_config

fast_mqtt = FastMQTT(config=mqtt_config)
