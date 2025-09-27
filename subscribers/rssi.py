import json
from gmqtt import Client as MQTTClient
from typing import Any
from client import fast_mqtt
from models.coordinate import CoordinateModel, Coordinate, StatusEnum
from publish import signal
import logging
from services import coordinate as service
from config import get_database
from ws.ws_manager import manager

logger = logging.getLogger("uvicorn")

@fast_mqtt.subscribe("things/rssi/start", qos=0)
async def save_start_rssi(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    payload = json.loads(payload.decode())

    rssi1 = payload["rssi1"]
    rssi2 = payload["rssi2"]
    rssi3 = payload["rssi3"]


    logger.error(f"{rssi1}, {rssi2}, {rssi3}")
    logger.error(f"{type(rssi1)}, {type(rssi2)}, {type(rssi3)}")

    x,y = service.rssi_to_coordinate(rssi1, rssi2, rssi3)

    dto = CoordinateModel(
        start_point=Coordinate(x=x, y=y),
        status=StatusEnum.PENDING,
        target_point=None,
        paths=None
    )

    # res = await service.insert_start_coordinate(coordinate_dto=dto)

    await manager.broadcast_json({
        "type": "rssi_start",
        "x": x,
        "y": y,
    })

    logger.info(res)
    return


@fast_mqtt.subscribe("things/rssi/target", qos=0)
async def save_target_rssi(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    payload = json.loads(payload.decode())

    rssi1 = payload["rssi1"]
    rssi2 = payload["rssi2"]
    rssi3 = payload["rssi3"]

    x,y = service.rssi_to_coordinate(rssi1, rssi2, rssi3)

    dto = CoordinateModel(
        start_point=None,
        status=StatusEnum.PENDING,
        target_point=Coordinate(x=x, y=y),
        paths=None
    )

    # res = await service.insert_end_coordinate(coordinate_dto=dto)
    
    await manager.broadcast_json({
            "type": "rssi_target",
            "x": x,
            "y": y,
    })
    
    logger.info(res)
    return