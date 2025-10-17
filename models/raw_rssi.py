from pydantic import BaseModel, Field
from datetime import datetime, timezone, timedelta

GMT_PLUS_7 = timezone(timedelta(hours=7))

class RawRSSI(BaseModel):
    rssi1: list[float]
    rssi2 : list[float]
    rssi3 : list[float]
    timestamp: datetime = Field(default_factory=lambda: datetime.now(tz=GMT_PLUS_7)
)