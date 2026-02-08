from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WeightCreate(BaseModel):
    weight: float = Field(..., gt=0)
    recorded_at: Optional[datetime] = None
    notes: Optional[str] = None


class WeightUpdate(BaseModel):
    weight: Optional[float] = Field(None, gt=0)
    recorded_at: Optional[datetime] = None
    notes: Optional[str] = None
