from pydantic import BaseModel
from enum import Enum

class StatusEnum(str,Enum):
    PENDING = "PENDING"
    ONGOING = "ONGOING"
    FINISHED = "FINISHED"

class Coordinate(BaseModel):
    x: float
    y: float

class CoordinateModel(BaseModel):
    status : StatusEnum
    start_point : Coordinate | None
    target_point : Coordinate | None
    paths : list[Coordinate] | None


