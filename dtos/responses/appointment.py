from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AppointmentResponse(BaseModel):
    id: int
    appointment_date: datetime
    reason: str
    vet_name: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    pet_id: int

    class Config:
        from_attributes = True
