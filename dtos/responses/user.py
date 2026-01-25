from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr

    class Config:
        from_attributes = True
