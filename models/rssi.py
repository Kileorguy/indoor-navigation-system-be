from pydantic import BaseModel
from coordinate import TypeEnum

class RSSI(BaseModel):
    id: int
    type: TypeEnum
    rssi1: float
    rssi2 : float
    rssi3 : float
