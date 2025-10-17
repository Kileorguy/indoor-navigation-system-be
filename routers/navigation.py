from fastapi import APIRouter
from publish.navigation import start_navigation as start_nav
from fastapi.responses import JSONResponse

import logging
route = APIRouter(
    prefix="/navigation",
    tags=["navigation"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger("uvicorn")

"""
api untuk melakukan start pathfinding dan navigation
"""
@route.get("/start")
async def start_navigation():
    await start_nav()
    logger.debug("Start Navigation")
    return JSONResponse(content={"message": "Navigation started"}, status_code=200)