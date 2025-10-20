from fastapi import APIRouter
from publish.navigation import start_navigation as start_nav
from fastapi.responses import JSONResponse
from services import coordinate as coordinate_service
from pydantic import BaseModel
from models.coordinate import CoordinateModel, Coordinate, StatusEnum
from helper import discord_webhook
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
        logger.debug("Start Navigation")
        x,y = await coordinate_service.start_navigation()
        logger.error(f"x: {x}, y: {y}")
        if x!=-1 and y!=-1:
            await start_nav(x,y)
            await discord_webhook.send_discord_alert(f"🟢 The car has started moving to coordinate ({x}, {y})")

        return JSONResponse(content={"message": "Start Processed"}, status_code=200)
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

