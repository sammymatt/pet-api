from pydantic import BaseModel
from typing import Optional
from datetime import date


class TabletResponse(BaseModel):
    id: int
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    notes: Optional[str] = None
    pet_id: int

    class Config:
        from_attributes = True
