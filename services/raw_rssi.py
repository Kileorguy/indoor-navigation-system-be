from config import get_database
from models.raw_rssi import RawRSSI
import logging
import numpy as np
logger = logging.getLogger("uvicorn")

"""
untuk masukin data logs ke database yang kemudian akan didisplay di frontend
"""
async def insert_raw_rssi_data(raw_rssi_dto: RawRSSI):
    db = await get_database()
    raw_rssi_json = raw_rssi_dto.model_dump()
    raw_rssi_json["variance1"] = np.var(raw_rssi_json['rssi1'], ddof=1)
    raw_rssi_json["variance2"] = np.var(raw_rssi_json['rssi2'], ddof=1)
    raw_rssi_json["variance3"] = np.var(raw_rssi_json['rssi3'], ddof=1)

    raw_rssi_json["mean1"] = np.mean(raw_rssi_json['rssi1'])
    raw_rssi_json["mean2"] = np.mean(raw_rssi_json['rssi2'])
    raw_rssi_json["mean3"] = np.mean(raw_rssi_json['rssi3'])
    result = await db.raw_rssi.insert_one(raw_rssi_json)
    return result