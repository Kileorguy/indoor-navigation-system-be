from pydantic import BaseModel
from coordinate import StatusEnum

class RSSI(BaseModel):
    id: int
    type: StatusEnum
    rssi1: float
    rssi2 : float
    rssi3 : float
