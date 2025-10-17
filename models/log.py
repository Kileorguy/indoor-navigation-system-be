from pydantic import BaseModel
from enum import Enum

class StatusEnum(str,Enum):
    MCU = "MCU"
    ACTIVITY = "ACTIVITY"

class Log(BaseModel):
    timestamp: str
    status: StatusEnum
    text: str
