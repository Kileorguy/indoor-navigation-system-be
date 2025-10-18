from fastapi import FastAPI, Query, APIRouter
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from datetime import datetime, timedelta, timezone

from fastapi.encoders import jsonable_encoder
from services import monitoring as monitoring_service
import logging

route = APIRouter(
    prefix="/monitoring",
    tags=["monitoring"],
    responses={404: {"description": "Not found"}},
)

GMT_PLUS_7 = timezone(timedelta(hours=7))
logger = logging.getLogger("uvicorn")


"""
api get untuk mendapatkan data monitoring
"""
@route.get("/")
async def get_monitoring_data(date: str = Query(..., description="Date in format YYYY-MM-DD")):
    logger.error(date)
    try:
        local_start = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=GMT_PLUS_7)
        local_end = local_start + timedelta(days=1)

        start_utc = local_start.astimezone(timezone.utc)
        end_utc = local_end.astimezone(timezone.utc)

        results = await monitoring_service.get_monitoring_data(start_utc, end_utc)
        logger.error(f"bbbb {date}")
        try:
            results = sorted(
                results,
                key=lambda x: x["timestamp"],
                reverse=True
            )
        except KeyError:
            logger.error("Data sorting failed: 'timestamp' key not found in a document.")
            return JSONResponse(content={"error": "Data processing error"}, status_code=500)

        data = jsonable_encoder(
            results,
            custom_encoder={
                ObjectId: str
            }
        )

        return JSONResponse(content={"data": data}, status_code=200)

    except Exception as e:
        logger.error(f"Error in /monitoring/get_monitoring_data: {e}")
        return JSONResponse(content={"error": "Internal server error"}, status_code=400)

