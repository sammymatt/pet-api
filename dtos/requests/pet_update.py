from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    age: Optional[int] = Field(None, gt=0)
    description: Optional[str] = None
    gender: Optional[str] = None
    weight: Optional[float] = Field(None, gt=0)
    color: Optional[str] = None
    birthday: Optional[date] = None
    image_url: Optional[str] = None
