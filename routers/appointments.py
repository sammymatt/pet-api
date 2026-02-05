from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dependencies import get_db
from models import Pet, Appointment
from dtos.requests.appointment import AppointmentCreate, AppointmentUpdate
from dtos.responses.appointment import AppointmentResponse

router = APIRouter(tags=["appointments"])


@router.post("/pets/{pet_id}/appointments", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(pet_id: int, appointment_data: AppointmentCreate, db: AsyncSession = Depends(get_db)):
    pet_result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = pet_result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    # Strip timezone info for naive datetime column
    appt_date = appointment_data.appointment_date
    if appt_date.tzinfo is not None:
        appt_date = appt_date.replace(tzinfo=None)

    new_appointment = Appointment(
        appointment_date=appt_date,
        reason=appointment_data.reason,
        vet_name=appointment_data.vet_name,
        location=appointment_data.location,
        notes=appointment_data.notes,
        status=appointment_data.status,
        pet_id=pet_id
    )
    db.add(new_appointment)
    await db.commit()
    await db.refresh(new_appointment)
    return new_appointment


@router.get("/pets/{pet_id}/appointments", response_model=List[AppointmentResponse])
async def get_pet_appointments(pet_id: int, db: AsyncSession = Depends(get_db)):
    pet_result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = pet_result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    result = await db.execute(
        select(Appointment).where(Appointment.pet_id == pet_id).order_by(Appointment.appointment_date.desc())
    )
    return result.scalars().all()


@router.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(appointment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appointment = result.scalar_one_or_none()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.patch("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(appointment_id: int, appointment_update: AppointmentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appointment = result.scalar_one_or_none()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    update_data = appointment_update.model_dump(exclude_unset=True)
    # Strip timezone from appointment_date if present
    if 'appointment_date' in update_data and update_data['appointment_date'] is not None:
        if update_data['appointment_date'].tzinfo is not None:
            update_data['appointment_date'] = update_data['appointment_date'].replace(tzinfo=None)
    for field, value in update_data.items():
        setattr(appointment, field, value)

    await db.commit()
    await db.refresh(appointment)
    return appointment


@router.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appointment = result.scalar_one_or_none()
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    await db.delete(appointment)
    await db.commit()
    return None
