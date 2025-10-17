from config import get_database
from models.raw_rssi import RawRSSI
import logging
logger = logging.getLogger("uvicorn")

"""
untuk masukin data logs ke database yang kemudian akan didisplay di frontend
"""
async def insert_raw_rssi_data(raw_rssi_dto: RawRSSI):
    db = await get_database()
    result = await db.raw_rssi.insert_one(raw_rssi_dto.model_dump())
    return result