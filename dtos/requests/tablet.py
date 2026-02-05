from pydantic import BaseModel
from typing import Optional
from datetime import date


class TabletCreate(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    notes: Optional[str] = None


class TabletUpdate(BaseModel):
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    notes: Optional[str] = None
