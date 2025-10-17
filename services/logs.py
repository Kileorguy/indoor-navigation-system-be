from config import get_database
from models.log import Log
import logging
logger = logging.getLogger("uvicorn")

"""
untuk masukin data logs ke database yang kemudian akan didisplay di frontend
"""
async def insert_logs_data(log_dto: Log):
    db = await get_database()
    result = await db.logs.insert_one(log_dto)
    return result