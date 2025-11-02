from config import get_database
from models.log import Log
import logging
logger = logging.getLogger("uvicorn")

"""
untuk masukin data logs ke database yang kemudian akan didisplay di frontend
"""
async def insert_logs_data(log_dto: Log):
    db = await get_database()
    result = await db.logs.insert_one(log_dto.model_dump())
    return result

async def get_logs_data(query, page, limit=10):
    """Untuk mendapatkan data logs dari database ke dashboard"""
    db = await get_database()
    skip = (page - 1) * limit

    # Fetch logs with filter and pagination
    cursor = db.logs.find(query).sort("timestamp", -1).skip(skip).limit(limit)
    logs = await cursor.to_list(length=limit)

    # Total count for pagination info
    total_logs = await db.logs.count_documents(query)
    total_pages = (total_logs + limit - 1) // limit

    json = {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "total_logs": total_logs,
        "data": logs,
    }

    return json