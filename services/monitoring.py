from config import get_database
import logging
logger = logging.getLogger("uvicorn")

"""
untuk mendapatkan data monitoring dari database
"""
async def get_monitoring_data(start, end):
    db = await get_database()
    cursor = db.raw_rssi.find({
        "timestamp": {"$gte": start, "$lt": end}
    }).limit(500)

    return await cursor.to_list(length=500)

