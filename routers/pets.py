from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dependencies import get_db
from models import Pet, User
from dtos.requests.pet import PetCreate
from dtos.requests.pet_update import PetUpdate
from dtos.responses.pet import PetResponse

router = APIRouter(tags=["pets"])


@router.post("/users/{user_id}/pets", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(user_id: int, pet: PetCreate, db: AsyncSession = Depends(get_db)):
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_pet = Pet(
        name=pet.name,
        species=pet.species,
        age=pet.age,
        description=pet.description,
        gender=pet.gender,
        weight=pet.weight,
        color=pet.color,
        birthday=pet.birthday,
        user_id=user_id
    )
    db.add(new_pet)
    await db.commit()
    await db.refresh(new_pet)
    return new_pet


@router.get("/pets", response_model=List[PetResponse])
async def list_pets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet))
    return result.scalars().all()


@router.get("/pets/{pet_id}", response_model=PetResponse)
async def get_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet


@router.patch("/pets/{pet_id}", response_model=PetResponse)
async def update_pet(pet_id: int, pet_update: PetUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    update_data = pet_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pet, field, value)

    await db.commit()
    await db.refresh(pet)
    return pet


@router.delete("/pets/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    await db.delete(pet)
    await db.commit()
    return None
