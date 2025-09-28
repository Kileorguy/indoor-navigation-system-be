from fastapi import APIRouter
from fastapi.openapi.utils import status_code_ranges
from fastapi.responses import JSONResponse
from publish import motor
import globals

route = APIRouter(
    prefix="/motor",
    tags=["motor"],
    responses={404: {"description": "Not found"}},
)

@route.post("/drive")
async def drive_motor(direction: str, enable: bool):
    result = await motor.publish_motor(direction, enable)
    return JSONResponse(content=result, status_code=200)