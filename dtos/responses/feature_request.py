from pydantic import BaseModel
from typing import Optional


class FeatureRequestResponse(BaseModel):
    id: int
    title: str
    category: str
    description: Optional[str] = None
    votes: int
    is_implemented: bool

    class Config:
        from_attributes = True
