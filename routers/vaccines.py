from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dependencies import get_db
from models import Pet, Vaccine
from dtos.requests.vaccine import VaccineCreate, VaccineUpdate
from dtos.responses.vaccine import VaccineResponse

router = APIRouter(tags=["vaccines"])


@router.post("/pets/{pet_id}/vaccines", response_model=VaccineResponse, status_code=status.HTTP_201_CREATED)
async def create_vaccine(pet_id: int, vaccine_data: VaccineCreate, db: AsyncSession = Depends(get_db)):
    pet_result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = pet_result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    new_vaccine = Vaccine(
        name=vaccine_data.name,
        administered_date=vaccine_data.administered_date,
        next_due_date=vaccine_data.next_due_date,
        administered_by=vaccine_data.administered_by,
        frequency=vaccine_data.frequency,
        up_to_date=vaccine_data.up_to_date,
        notes=vaccine_data.notes,
        pet_id=pet_id
    )
    db.add(new_vaccine)
    await db.commit()
    await db.refresh(new_vaccine)
    return new_vaccine


@router.get("/pets/{pet_id}/vaccines", response_model=List[VaccineResponse])
async def get_pet_vaccines(pet_id: int, db: AsyncSession = Depends(get_db)):
    pet_result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = pet_result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    result = await db.execute(
        select(Vaccine).where(Vaccine.pet_id == pet_id).order_by(Vaccine.administered_date.desc())
    )
    return result.scalars().all()


@router.get("/vaccines/{vaccine_id}", response_model=VaccineResponse)
async def get_vaccine(vaccine_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vaccine).where(Vaccine.id == vaccine_id))
    vaccine = result.scalar_one_or_none()
    if vaccine is None:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return vaccine


@router.patch("/vaccines/{vaccine_id}", response_model=VaccineResponse)
async def update_vaccine(vaccine_id: int, vaccine_update: VaccineUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vaccine).where(Vaccine.id == vaccine_id))
    vaccine = result.scalar_one_or_none()
    if vaccine is None:
        raise HTTPException(status_code=404, detail="Vaccine not found")

    update_data = vaccine_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vaccine, field, value)

    await db.commit()
    await db.refresh(vaccine)
    return vaccine


@router.delete("/vaccines/{vaccine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vaccine(vaccine_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vaccine).where(Vaccine.id == vaccine_id))
    vaccine = result.scalar_one_or_none()
    if vaccine is None:
        raise HTTPException(status_code=404, detail="Vaccine not found")

    await db.delete(vaccine)
    await db.commit()
    return None
