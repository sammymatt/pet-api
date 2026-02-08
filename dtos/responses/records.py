from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime


class VaccineRecord(BaseModel):
    id: int
    name: str
    administered_date: date
    next_due_date: Optional[date] = None
    administered_by: Optional[str] = None
    frequency: Optional[str] = None
    up_to_date: Optional[bool] = None
    notes: Optional[str] = None
    pet_id: int
    pet_name: Optional[str] = None

    class Config:
        from_attributes = True


class TabletRecord(BaseModel):
    id: int
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    notes: Optional[str] = None
    pet_id: int
    pet_name: Optional[str] = None

    class Config:
        from_attributes = True


class AppointmentRecord(BaseModel):
    id: int
    appointment_date: datetime
    reason: str
    vet_name: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    pet_id: int
    pet_name: Optional[str] = None

    class Config:
        from_attributes = True


class RecordsResponse(BaseModel):
    vaccines: List[VaccineRecord]
    tablets: List[TabletRecord]
    appointments: List[AppointmentRecord]
