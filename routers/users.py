from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dependencies import get_db
from models import User, Pet
from dtos.requests.user import UserCreate
from dtos.responses.user import UserResponse
from dtos.responses.pet import PetResponse

router = APIRouter(tags=["users"])


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email
    )
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")


@router.get("/users/{user_id}/pets", response_model=List[PetResponse])
async def get_user_pets(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.user_id == user_id))
    return result.scalars().all()
