from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PetCreate(BaseModel):
    name: str
    species: str
    age: int = Field(..., gt=0)
    description: Optional[str] = None
    gender: Optional[str] = None
    weight: Optional[float] = Field(None, gt=0)
    color: Optional[str] = None
    birthday: Optional[date] = None
    image_url: Optional[str] = None
