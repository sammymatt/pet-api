from pydantic import BaseModel
from typing import Optional


class FeatureRequestCreate(BaseModel):
    title: str
    category: str
    description: Optional[str] = None


class FeatureRequestUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    votes: Optional[int] = None
    is_implemented: Optional[bool] = None
