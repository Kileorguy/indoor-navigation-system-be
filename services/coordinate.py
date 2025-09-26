from typing import Tuple

from fastapi import Depends

from config import get_database
from models.coordinate import CoordinateModel
import logging

logger = logging.getLogger("uvicorn")

def rssi_to_coordinate(rssi1 : float,
                             rssi2 : float,
                             rssi3 :float ) -> Tuple[float,float]:
    """Function buat convert RSSI jadi 2D Coordinate"""
    return rssi1, rssi2

async def insert_start_coordinate(coordinate_dto: CoordinateModel) -> str:
    db = await get_database()
    update_fields = {
        "status": coordinate_dto.status,
    }
    logger.error(f"update_fields: {update_fields}")

    if coordinate_dto.start_point is not None:
        update_fields["start_point"] = coordinate_dto.start_point.model_dump()

    # Check kalo ada yang masih ongoing/pending, dia gabisa kalo masih ongoing
    check = await db.coordinate.find_one(
        {"status": {"$eq": "ONGOING"}})
    if check:
        return "There is ongoing orders, cannot insert new"

    # Check kalo endpointnya belum defined tapi startpointnya udah, dia update startpointnya yang udah ada
    check = await db.coordinate.find_one(
        {"start_point": {"$exists": True}, "target_point": {"$exists": False}},
    )

    if check:
        result = await db.coordinate.update_one(
            {"_id": {"$eq": check["_id"]}},
            {"$set": update_fields},
        )

        return f"Updated Existing"

    # Kalo startPointnya belum ada, dia insert baru atau update data sebelumnya
    result = await db.coordinate.update_one(
        {
            "$or": [
                {"start_point": {"$exists": False}},
                {"status": "PENDING"}
            ]
        },
        {"$set": update_fields},
        upsert=True  # insert if not exists
    )
    logger.error(f"RESULT COUNT: {result.matched_count}")

    if result.upserted_id:
        return f"Inserted, ${result.upserted_id}, Data : , ${result}"
    elif result.modified_count:
        return f"Updated existing Data : , ${result}"
    else:
        return "Nothing Changed"

async def insert_end_coordinate(coordinate_dto: CoordinateModel) -> str:
    db = await get_database()

    update_fields = {
        "status": coordinate_dto.status,
    }
    if coordinate_dto.target_point is not None:
        update_fields["target_point"] = coordinate_dto.target_point.model_dump()


    # Check kalo ada yang masih ongoing, dia gabisa kalo masih ongoing
    check = await db.coordinate.find_one(
        {"status": {"$eq": "ONGOING"}} )
    if check:
        return "There is ongoing orders, cannot insert new"

    # Check kalo startpointnya belum defined tapi endpointnya udah, dia update endpointnya yang udah ada
    check = await db.coordinate.find_one(
        {"start_point": {"$exists": False}, "target_point": {"$exists": True}},
    )

    if check:
        result = await db.coordinate.update_one(
            {"_id": {"$eq": check["_id"]}},
            {"$set":update_fields},
        )

        return f"Updated Existing, ${check.upserted_id}"


    # Kalo targetPointnya belum ada, dia insert baru atau update data sebelumnya
    result = await db.coordinate.update_one(
        {
            "$or": [
                {"target_point": {"$exists": False}},
                {"status": "PENDING"}
            ]
        },
        {"$set": update_fields},
        upsert=True
    )

    if result.upserted_id:
        return f"Inserted, ${result.upserted_id}, Data : , ${result}"

    elif result.modified_count:
        return f"Updated existing, Data : , ${result}"
    else:
        return "Nothing Changed"
