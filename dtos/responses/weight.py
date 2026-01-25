from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WeightResponse(BaseModel):
    id: int
    weight: float
    recorded_at: datetime
    notes: Optional[str] = None
    pet_id: int

    class Config:
        from_attributes = True
