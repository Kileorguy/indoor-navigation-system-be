import json
from gmqtt import Client as MQTTClient
from typing import Any
from client import fast_mqtt
import logging
from services import coordinate as coordinate_service
from services import logs as logs_service
from models.log import Log as LogModel, StatusEnum as LogEnum

logger = logging.getLogger("uvicorn")

# code testing
@fast_mqtt.subscribe("navigation/end/", qos=0)
async def save_end_navigation(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    result = await coordinate_service.end_navigation()

    end_log_dto = LogModel(status=LogEnum.ACTIVITY, text="Ended car navigation")
    result = await logs_service.insert_logs_data(end_log_dto)
    logger.error(result)
