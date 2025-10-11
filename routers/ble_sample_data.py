from fastapi import APIRouter
from fastapi.openapi.utils import status_code_ranges
from fastapi.responses import JSONResponse
from models.ble_sample_data import BleSampleData
from publish import motor

route = APIRouter(
    prefix="/ble_sample",
    tags=["ble_sample"],
    responses={404: {"description": "Not found"}},
)

@route.post("/ble_sample")
async def insert_ble_sample_data(item: BleSampleData):
    result = await motor.publish_motor(item.direction, item.enable)
    return JSONResponse(content=result, status_code=200)