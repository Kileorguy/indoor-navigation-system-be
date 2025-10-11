from models.ble_sample_data import BleSampleData
from config import get_database

async def insert_ble_sample_data(ble_sample_data_dto: BleSampleData):
    db = await get_database()
    result = await db.calibrate.insert_one(ble_sample_data_dto)

    return result