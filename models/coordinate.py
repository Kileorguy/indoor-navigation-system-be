from pydantic import BaseModel
from enum import Enum

class TypeEnum(Enum):
    start = "start"
    target = "target"
    current = "current"

class Coordinate(BaseModel):
    id: int
    type: TypeEnum
    x : float
    y : float