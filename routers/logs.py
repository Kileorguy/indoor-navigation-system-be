import logging
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from datetime import datetime, timedelta, timezone
from services import logs as logs_service
from bson.objectid import ObjectId

logger = logging.getLogger("uvicorn")

route = APIRouter(
    prefix="/logs",
    tags=["logs"],
    responses={404: {"description": "Not found"}},
)

@route.get("/")
async def get_logs(
    day: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD, local time)"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of logs per page"),
):
    query = {}

    if day:
        try:
            # Convert input day (local) to UTC range
            local_tz = timezone(timedelta(hours=7))  # GMT+7 for example
            start_of_day = datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=local_tz)
            end_of_day = start_of_day + timedelta(days=1)

            # Convert to UTC for MongoDB
            start_utc = start_of_day.astimezone(timezone.utc)
            end_utc = end_of_day.astimezone(timezone.utc)

            query["timestamp"] = {"$gte": start_utc, "$lt": end_utc}
        except ValueError:
            return JSONResponse(content={"error": "Invalid date format. Expected YYYY-MM-DD."}, status_code=400)

    try:
        json = await logs_service.get_logs_data(query, page, limit)
    except Exception as e:
        logger.error(f"Error in /logs/get_logs: {e}")
        return JSONResponse(content={"error": "Internal server error"}, status_code=500)
    json["data"] = jsonable_encoder(json["data"], custom_encoder={
                ObjectId: str
            })
    return JSONResponse(content=json, status_code=200)


