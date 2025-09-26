from typing import Tuple

from fastapi import Depends

from config import get_database
from models.coordinate import CoordinateModel


async def rssi_to_coordinate(rssi1 : float,
                             rssi2 : float,
                             rssi3 :float ) -> Tuple[float,float]:
    """Function buat convert RSSI jadi 2D Coordinate"""
    return rssi1, rssi2


async def insert_start_coordinate(coordinate_dto: CoordinateModel, db=Depends(get_database)):
    update_fields = {}
    if coordinate_dto.start_point is not None:
        update_fields["start_point"] = coordinate_dto.start_point.model_dump()

    # Check kalo ada yang masih ongoing, dia gabisa kalo masih ongoing
    check = await db.coordinate.find(
        {"status": {"$eq": "ONGOING"}})
    if check:
        return "There is ongoing orders, cannot insert new"

    # Check kalo endpointnya belum defined tapi startpointnya udah, dia update startpointnya yang udah ada
    check = await db.coordinate.find_one(
        {"start_point": {"$exists": True}, "end_point": {"$exists": False}},
    )

    if check:
        result = await db.coordinate.update_one(
            {"run_id": {"$eq": check["run_id"]}},
            {"$set": update_fields},
        )

        return "Updated Existing", check.upserted_id

    # Kalo startPointnya belum ada, dia insert baru atau update data sebelumnya
    result = await db.coordinate.update_one(
        {"start_point": {"$exists": False}},
        {"$set": update_fields},
        upsert=True  # insert if not exists
    )

    if result.upserted_id:
        return "Inserted", result.upserted_id, "Data : ", result
    elif result.modified_count:
        return "Updated existing", result.upserted_id, "Data : ", result
    else:
        return "Nothing Changed"

async def insert_end_coordinate(coordinate_dto: CoordinateModel, db=Depends(get_database)):
    update_fields = {}
    if coordinate_dto.target_point is not None:
        update_fields["target_point"] = coordinate_dto.target_point.model_dump()


    # Check kalo ada yang masih ongoing, dia gabisa kalo masih ongoing
    check = await db.coordinate.find(
        {"status": {"$eq": "ONGOING"}} )
    if check:
        return "There is ongoing orders, cannot insert new"

    # Check kalo startpointnya belum defined tapi endpointnya udah, dia update endpointnya yang udah ada
    check = await db.coordinate.find_one(
        {"start_point": {"$exists": False}, "end_point": {"$exists": True}},
    )

    if check:
        result = await db.coordinate.update_one(
            {"run_id": {"$eq": check["run_id"]}},
            {"$set":update_fields},
        )

        return "Updated Existing", check.upserted_id


    # Kalo targetPointnya belum ada, dia insert baru atau update data sebelumnya
    result = await db.coordinate.update_one(
        {"target_point": {"$exists": False}},
        {"$set": update_fields},
        upsert=True  # insert if not exists
    )

    if result.upserted_id:
        return "Inserted", result.upserted_id, "Data : ", result
    elif result.modified_count:
        return "Updated existing", result.upserted_id, "Data : ", result
    else:
        return "Nothing Changed"
