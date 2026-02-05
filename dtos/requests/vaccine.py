from pydantic import BaseModel
from typing import Optional
from datetime import date


class VaccineCreate(BaseModel):
    name: str
    administered_date: date
    next_due_date: Optional[date] = None
    administered_by: Optional[str] = None
    notes: Optional[str] = None


class VaccineUpdate(BaseModel):
    name: Optional[str] = None
    administered_date: Optional[date] = None
    next_due_date: Optional[date] = None
    administered_by: Optional[str] = None
    notes: Optional[str] = None
