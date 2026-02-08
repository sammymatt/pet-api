from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime

from dependencies import get_db
from models import Pet, PetWeight
from dtos.requests.weight import WeightCreate, WeightUpdate
from dtos.responses.weight import WeightResponse

router = APIRouter(tags=["weights"])


@router.post("/pets/{pet_id}/weights", response_model=WeightResponse, status_code=status.HTTP_201_CREATED)
async def add_pet_weight(pet_id: int, weight_data: WeightCreate, db: AsyncSession = Depends(get_db)):
    pet_result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = pet_result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    recorded_at = weight_data.recorded_at
    if recorded_at is not None and recorded_at.tzinfo is not None:
        recorded_at = recorded_at.replace(tzinfo=None)

    new_weight = PetWeight(
        weight=weight_data.weight,
        recorded_at=recorded_at or datetime.utcnow(),
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


@router.patch("/weights/{weight_id}", response_model=WeightResponse)
async def update_weight(weight_id: int, weight_update: WeightUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PetWeight).where(PetWeight.id == weight_id))
    weight = result.scalar_one_or_none()
    if weight is None:
        raise HTTPException(status_code=404, detail="Weight record not found")

    update_data = weight_update.model_dump(exclude_unset=True)
    if 'recorded_at' in update_data and update_data['recorded_at'] is not None:
        if update_data['recorded_at'].tzinfo is not None:
            update_data['recorded_at'] = update_data['recorded_at'].replace(tzinfo=None)
    for field, value in update_data.items():
        setattr(weight, field, value)

    await db.commit()
    await db.refresh(weight)
    return weight


@router.delete("/weights/{weight_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_weight(weight_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PetWeight).where(PetWeight.id == weight_id))
    weight = result.scalar_one_or_none()
    if weight is None:
        raise HTTPException(status_code=404, detail="Weight record not found")

    await db.delete(weight)
    await db.commit()
    return None
