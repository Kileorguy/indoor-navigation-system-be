from pydantic_settings import BaseSettings
from fastapi_mqtt import MQTTConfig
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus

class Settings(BaseSettings):
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_keepalive: int = 60
    mqtt_username: str | None = None
    mqtt_password: str | None = None

    mongo_username: str | None = None
    mongo_password: str | None = None
    mongo_host: str | None = None
    mongo_port: int = 27017
    mongo_database: str | None = None

    class Config:
        env_file = ".env"

class CalculationConfig:
    TX_POWER: int = -83
    PATH_LOSS_EXPONENT: int = 4    #n
    BEACON1_POS = (0,0)
    BEACON2_POS = (5,5)
    BEACON3_POS = (2,10)

calculate_config = CalculationConfig()
settings = Settings()

mqtt_config = MQTTConfig(
    host=settings.mqtt_host,
    port=settings.mqtt_port,
    keepalive=settings.mqtt_keepalive,
    username=settings.mqtt_username,
    password=settings.mqtt_password,
)

PASSWORD = quote_plus(settings.mongo_password)
client = AsyncIOMotorClient(f"mongodb://{settings.mongo_username}:{PASSWORD}@{settings.mongo_host}:{settings.mongo_port}")
db = client[settings.mongo_database]

async def get_database():
    return db

