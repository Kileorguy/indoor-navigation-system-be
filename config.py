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
    TX_POWER1: int = -70.16794738830454
    TX_POWER2: int = -67.09791779237294
    TX_POWER3: int = -63.82524304918069
    PATH_LOSS_EXPONENT1: int = 4.085764005566974   #n
    PATH_LOSS_EXPONENT2: int = 5.097879276404685   #n
    PATH_LOSS_EXPONENT3: int = 6.063730648004541   #n
    BEACON1_POS = (0,0)
    BEACON2_POS = (1,3)
    BEACON3_POS = (3,1)

class MotorConfig:
    FORWARD_UNIT : int = 100
    TURN90DEG_UNIT : int = 100

calculate_config = CalculationConfig()
motor_config = MotorConfig()
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

