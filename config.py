from pydantic_settings import BaseSettings
from fastapi_mqtt import MQTTConfig

class Settings(BaseSettings):
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_keepalive: int = 60
    mqtt_username: str | None = None
    mqtt_password: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
print("🔧 Loaded MQTT settings:", settings.model_dump())


mqtt_config = MQTTConfig(
    host=settings.mqtt_host,
    port=settings.mqtt_port,
    keepalive=settings.mqtt_keepalive,
    username=settings.mqtt_username,
    password=settings.mqtt_password,
)
