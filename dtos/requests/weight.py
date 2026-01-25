from pydantic import BaseModel, Field
from typing import Optional

class WeightCreate(BaseModel):
    weight: float = Field(..., gt=0)
    notes: Optional[str] = None
