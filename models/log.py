from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta
from enum import Enum


GMT_PLUS_7 = timezone(timedelta(hours=7))

class StatusEnum(str,Enum):
    MCU = "MCU"
    ACTIVITY = "ACTIVITY"

class Log(BaseModel):
    status: StatusEnum
    text: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=GMT_PLUS_7))
