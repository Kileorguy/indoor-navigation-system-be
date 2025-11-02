from fastapi import APIRouter
from fastapi.openapi.utils import status_code_ranges
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from publish import motor
import globals

route = APIRouter(
    prefix="/motor",
    tags=["motor"],
    responses={404: {"description": "Not found"}},
)

class Item(BaseModel):
    direction: str
    enable: bool

"""
api post untuk publish arah gerak motor, digunakan untuk testing
"""
@route.post("/drive")
async def drive_motor(item: Item):
    result = await motor.publish_motor(item.direction, item.enable)
    return JSONResponse(content=result, status_code=200)