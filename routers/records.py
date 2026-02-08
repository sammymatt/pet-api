from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from dependencies import get_db
from models import Pet, User, Vaccine, Tablet, Appointment
from dtos.responses.records import RecordsResponse, VaccineRecord, TabletRecord, AppointmentRecord

router = APIRouter(tags=["records"])


@router.get("/pets/{pet_id}/records", response_model=RecordsResponse)
async def get_pet_records(pet_id: int, db: AsyncSession = Depends(get_db)):
    """Get all vaccines, tablets, and appointments for a specific pet."""
    pet_result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = pet_result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")

    vaccines_result = await db.execute(
        select(Vaccine).where(Vaccine.pet_id == pet_id).order_by(Vaccine.administered_date.desc())
    )
    vaccines = [
        VaccineRecord(
            id=v.id,
            name=v.name,
            administered_date=v.administered_date,
            next_due_date=v.next_due_date,
            administered_by=v.administered_by,
            frequency=v.frequency,
            up_to_date=v.up_to_date,
            notes=v.notes,
            pet_id=v.pet_id,
            pet_name=pet.name
        )
        for v in vaccines_result.scalars().all()
    ]

    tablets_result = await db.execute(
        select(Tablet).where(Tablet.pet_id == pet_id).order_by(Tablet.start_date.desc())
    )
    tablets = [
        TabletRecord(
            id=t.id,
            name=t.name,
            dosage=t.dosage,
            frequency=t.frequency,
            start_date=t.start_date,
            end_date=t.end_date,
            notes=t.notes,
            pet_id=t.pet_id,
            pet_name=pet.name
        )
        for t in tablets_result.scalars().all()
    ]

    appointments_result = await db.execute(
        select(Appointment).where(Appointment.pet_id == pet_id).order_by(Appointment.appointment_date.desc())
    )
    appointments = [
        AppointmentRecord(
            id=a.id,
            appointment_date=a.appointment_date,
            reason=a.reason,
            vet_name=a.vet_name,
            location=a.location,
            notes=a.notes,
            status=a.status,
            pet_id=a.pet_id,
            pet_name=pet.name
        )
        for a in appointments_result.scalars().all()
    ]

    return RecordsResponse(vaccines=vaccines, tablets=tablets, appointments=appointments)


@router.get("/users/{user_id}/records", response_model=RecordsResponse)
async def get_user_records(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get all vaccines, tablets, and appointments for all pets belonging to a user."""
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    pets_result = await db.execute(select(Pet).where(Pet.user_id == user_id))
    pets = pets_result.scalars().all()
    pet_ids = [p.id for p in pets]
    pet_names = {p.id: p.name for p in pets}

    if not pet_ids:
        return RecordsResponse(vaccines=[], tablets=[], appointments=[])

    vaccines_result = await db.execute(
        select(Vaccine).where(Vaccine.pet_id.in_(pet_ids)).order_by(Vaccine.administered_date.desc())
    )
    vaccines = [
        VaccineRecord(
            id=v.id,
            name=v.name,
            administered_date=v.administered_date,
            next_due_date=v.next_due_date,
            administered_by=v.administered_by,
            frequency=v.frequency,
            up_to_date=v.up_to_date,
            notes=v.notes,
            pet_id=v.pet_id,
            pet_name=pet_names.get(v.pet_id)
        )
        for v in vaccines_result.scalars().all()
    ]

    tablets_result = await db.execute(
        select(Tablet).where(Tablet.pet_id.in_(pet_ids)).order_by(Tablet.start_date.desc())
    )
    tablets = [
        TabletRecord(
            id=t.id,
            name=t.name,
            dosage=t.dosage,
            frequency=t.frequency,
            start_date=t.start_date,
            end_date=t.end_date,
            notes=t.notes,
            pet_id=t.pet_id,
            pet_name=pet_names.get(t.pet_id)
        )
        for t in tablets_result.scalars().all()
    ]

    appointments_result = await db.execute(
        select(Appointment).where(Appointment.pet_id.in_(pet_ids)).order_by(Appointment.appointment_date.desc())
    )
    appointments = [
        AppointmentRecord(
            id=a.id,
            appointment_date=a.appointment_date,
            reason=a.reason,
            vet_name=a.vet_name,
            location=a.location,
            notes=a.notes,
            status=a.status,
            pet_id=a.pet_id,
            pet_name=pet_names.get(a.pet_id)
        )
        for a in appointments_result.scalars().all()
    ]

    return RecordsResponse(vaccines=vaccines, tablets=tablets, appointments=appointments)
