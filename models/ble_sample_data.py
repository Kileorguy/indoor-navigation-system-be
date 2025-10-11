from typing import List
from pydantic import BaseModel

class BleSampleData(BaseModel):
  id: int
  distance: int
  data: List[int]
