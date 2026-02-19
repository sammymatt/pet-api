from pydantic import BaseModel
from typing import Optional
from datetime import date

class PetResponse(BaseModel):
    id: int
    name: str
    species: str
    age: Optional[int] = None
    description: Optional[str] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    color: Optional[str] = None
    birthday: Optional[date] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True
