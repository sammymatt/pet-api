from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dependencies import get_db
from models import Pet, Tablet
from dtos.requests.tablet import TabletCreate, TabletUpdate
from dtos.responses.tablet import TabletResponse

router = APIRouter(tags=["tablets"])


@router.post("/pets/{pet_id}/tablets", response_model=TabletResponse, status_code=status.HTTP_201_CREATED)
async def create_tablet(pet_id: int, tablet_data: TabletCreate, db: AsyncSession = Depends(get_db)):
    pet_result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = pet_result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    new_tablet = Tablet(
        name=tablet_data.name,
        dosage=tablet_data.dosage,
        frequency=tablet_data.frequency,
        start_date=tablet_data.start_date,
        end_date=tablet_data.end_date,
        notes=tablet_data.notes,
        pet_id=pet_id
    )
    db.add(new_tablet)
    await db.commit()
    await db.refresh(new_tablet)
    return new_tablet


@router.get("/pets/{pet_id}/tablets", response_model=List[TabletResponse])
async def get_pet_tablets(pet_id: int, db: AsyncSession = Depends(get_db)):
    pet_result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = pet_result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    result = await db.execute(
        select(Tablet).where(Tablet.pet_id == pet_id).order_by(Tablet.start_date.desc())
    )
    return result.scalars().all()


@router.get("/tablets/{tablet_id}", response_model=TabletResponse)
async def get_tablet(tablet_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tablet).where(Tablet.id == tablet_id))
    tablet = result.scalar_one_or_none()
    if tablet is None:
        raise HTTPException(status_code=404, detail="Tablet not found")
    return tablet


@router.patch("/tablets/{tablet_id}", response_model=TabletResponse)
async def update_tablet(tablet_id: int, tablet_update: TabletUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tablet).where(Tablet.id == tablet_id))
    tablet = result.scalar_one_or_none()
    if tablet is None:
        raise HTTPException(status_code=404, detail="Tablet not found")

    update_data = tablet_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(tablet, field, value)

    await db.commit()
    await db.refresh(tablet)
    return tablet


@router.delete("/tablets/{tablet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tablet(tablet_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tablet).where(Tablet.id == tablet_id))
    tablet = result.scalar_one_or_none()
    if tablet is None:
        raise HTTPException(status_code=404, detail="Tablet not found")

    await db.delete(tablet)
    await db.commit()
    return None
