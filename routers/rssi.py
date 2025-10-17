from fastapi import APIRouter
from publish.navigation import start_navigation as start_nav
from fastapi.responses import JSONResponse
from services import coordinate as coordinate_service
from pydantic import BaseModel
from models.coordinate import CoordinateModel, Coordinate, StatusEnum

import logging
route = APIRouter(
    prefix="/rssi",
    tags=["rssi"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger("uvicorn")

"""
api untuk melakukan start pathfinding dan navigation
"""
@route.get("/start")
async def start_navigation():

    try:
        await start_nav()
        logger.debug("Start Navigation")
        result = await coordinate_service.start_navigation()
        logger.error(result)

        return JSONResponse(content={"message": result}, status_code=200)
    except Exception as e:

        logger.error("Error in /rssi/start/")
        return JSONResponse(content={"message": "Error during navigation", "error": str(e)}, status_code=500)


class Item(BaseModel):
    x: float
    y: float
@route.post("/target_coordinate")
async def target_coordinate(item: Item):

    try:
        dto = CoordinateModel(
            start_point=None,
            status=StatusEnum.PENDING,
            target_point=Coordinate(x=item.x, y=item.y),
            paths=None
        )

        await coordinate_service.insert_end_coordinate(dto)
        return JSONResponse(content={"message" : "Target point defined"}, status_code=200)

    except Exception as e:

        logger.error("Error in /rssi/target_coordinate/")
        return JSONResponse(content={"message": "Error during target coordinate", "error": str(e)}, status_code=500)

