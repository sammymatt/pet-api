from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dependencies import get_db
from models import Pet, PetWeight
from dtos.requests.weight import WeightCreate
from dtos.responses.weight import WeightResponse

router = APIRouter(tags=["weights"])


@router.post("/pets/{pet_id}/weights", response_model=WeightResponse, status_code=status.HTTP_201_CREATED)
async def add_pet_weight(pet_id: int, weight_data: WeightCreate, db: AsyncSession = Depends(get_db)):
    pet_result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = pet_result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    new_weight = PetWeight(
        weight=weight_data.weight,
        notes=weight_data.notes,
        pet_id=pet_id
    )
    db.add(new_weight)
    await db.commit()
    await db.refresh(new_weight)
    return new_weight


@router.get("/pets/{pet_id}/weights", response_model=List[WeightResponse])
async def get_pet_weights(pet_id: int, db: AsyncSession = Depends(get_db)):
    pet_result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = pet_result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    result = await db.execute(
        select(PetWeight).where(PetWeight.pet_id == pet_id).order_by(PetWeight.recorded_at.desc())
    )
    return result.scalars().all()
