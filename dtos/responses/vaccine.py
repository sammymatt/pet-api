from pydantic import BaseModel
from typing import Optional
from datetime import date


class VaccineResponse(BaseModel):
    id: int
    name: str
    administered_date: date
    next_due_date: Optional[date] = None
    administered_by: Optional[str] = None
    frequency: Optional[str] = None
    up_to_date: Optional[bool] = None
    notes: Optional[str] = None
    pet_id: int

    class Config:
        from_attributes = True
