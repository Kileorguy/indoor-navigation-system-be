from fastapi import APIRouter
from fastapi.openapi.utils import status_code_ranges
from fastapi.responses import JSONResponse
from publish import signal
import globals

route = APIRouter(
    prefix="/signal",
    tags=["signal"],
    responses={404: {"description": "Not found"}},
)

@route.get("/")
async def read_root():
    return JSONResponse(content={"bool_val": globals.boolean_val}, status_code=200)

@route.get("/toggle")
async def toggle_signal():
    globals.boolean_val = not globals.boolean_val
    signal.result = await signal.publish_signal()
    return JSONResponse(
        content={"message" : "Toggle Success"},
        status_code=200
    )