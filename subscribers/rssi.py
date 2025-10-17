import json
from gmqtt import Client as MQTTClient
from typing import Any
from client import fast_mqtt
from models.coordinate import CoordinateModel, Coordinate, StatusEnum
import logging
from services import coordinate as service
from helper.validate import validate_payload
from helper.filter import filter_data
from config import get_database
from ws.ws_manager import manager
from services.raw_rssi import insert_raw_rssi_data
from models.raw_rssi import RawRSSI
from models.log import Log as LogModel, StatusEnum as LogEnum
from services.logs import insert_logs_data

logger = logging.getLogger("uvicorn")

"""
subscriber mqtt untuk menentukan start position
"""
@fast_mqtt.subscribe("things/rssi/start", qos=0)
async def save_start_rssi(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    payload = json.loads(payload.decode())

    rssi1 = payload["r1"]
    rssi2 = payload["r2"]
    rssi3 = payload["r3"]

    ultrasonic1 = payload["u1"]
    ultrasonic2 = payload["u2"]
    ultrasonic3 = payload["u3"]

    logger.debug(f"Ultrasonic: {ultrasonic1}, {ultrasonic2}, {ultrasonic3}")


    # check, msg = validate_payload(rssi1, rssi2, rssi3)
    # if not check:
    #     logger.error(msg)
    #     return
    # else:
    #     logger.info(msg)



    rssi1 = filter_data(rssi1)
    rssi2 = filter_data(rssi2)
    rssi3 = filter_data(rssi3)

    logger.error(f"{rssi1}, {rssi2}, {rssi3}")
    logger.error(f"{type(rssi1)}, {type(rssi2)}, {type(rssi3)}")

    x,y = service.rssi_to_coordinate(rssi1, rssi2, rssi3)

    dto = CoordinateModel(
        start_point=Coordinate(x=x, y=y),
        status=StatusEnum.PENDING,
        target_point=None,
        paths=None
    )

    res = await service.insert_start_coordinate(coordinate_dto=dto)

    await manager.broadcast_json({
        "type": "rssi_start",
        "x": x,
        "y": y,
        "ultrasonic1": ultrasonic1,
        "ultrasonic2": ultrasonic2,
        "ultrasonic3": ultrasonic3,
    })

    logger.info(res)
    return

"""
subscriber mqtt untuk menentukan target position
"""
@fast_mqtt.subscribe("things/rssi/target", qos=0)
async def save_target_rssi(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    pass
    payload = json.loads(payload.decode())

    rssi1 = payload["r1"]
    rssi2 = payload["r2"]
    rssi3 = payload["r3"]

    check, msg = validate_payload(rssi1, rssi2, rssi3)
    if not check:
        logger.error(msg)
        return
    else:
        logger.info(msg)

    rssi1 = filter_data(rssi1)
    rssi2 = filter_data(rssi2)
    rssi3 = filter_data(rssi3)

    logger.error(f"{rssi1}, {rssi2}, {rssi3}")
    logger.error(f"{type(rssi1)}, {type(rssi2)}, {type(rssi3)}")

    x,y = service.rssi_to_coordinate(rssi1, rssi2, rssi3)

    dto = CoordinateModel(
        start_point=None,
        status=StatusEnum.PENDING,
        target_point=Coordinate(x=x, y=y),
        paths=None
    )

    res = await service.insert_end_coordinate(coordinate_dto=dto)

    await manager.broadcast_json({
            "type": "rssi_target",
            "x": x,
            "y": y,
    })

    logger.info(res)
    return

"""
subscriber mqtt untuk mendapatkan historical data path device
"""
@fast_mqtt.subscribe("things/rssi/path", qos=0)
async def save_path_rssi(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    payload = json.loads(payload.decode())

    rssi1 = payload["r1"]
    rssi2 = payload["r2"]
    rssi3 = payload["r3"]

    raw_rssi_dto = RawRSSI(
        rssi1=rssi1,
        rssi2=rssi2,
        rssi3=rssi3,
    )

    _ = await insert_raw_rssi_data(raw_rssi_dto)
    # logger.error("RAW RSSI "+ result)


    ultrasonic1 = payload["u1"]
    ultrasonic2 = payload["u2"]
    ultrasonic3 = payload["u3"]

    rssi1 = filter_data(rssi1)
    rssi2 = filter_data(rssi2)
    rssi3 = filter_data(rssi3)

    x,y = service.rssi_to_coordinate(rssi1, rssi2, rssi3)


    dto = CoordinateModel(
        start_point=None,
        status=StatusEnum.PENDING,
        target_point=Coordinate(x=x, y=y),
        paths=None
    )

    await service.insert_path(path_dto=dto)
    
    await manager.broadcast_json({
        "type": "rssi_path",
        "x": x,
        "y": y,
        "ultrasonic1": ultrasonic1,
        "ultrasonic2": ultrasonic2,
        "ultrasonic3": ultrasonic3,
    })
    
    # logger.info(res)
    return

