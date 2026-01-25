from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from db import SessionLocal
from models import Pet
from dtos.requests.pet import PetCreate
from dtos.responses.pet import PetResponse
from models import User
from dtos.requests.user import UserCreate
from dtos.responses.user import UserResponse

app = FastAPI()

async def get_db():
    async with SessionLocal() as session:
        yield session


@app.post("/users/{user_id}/pets", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(user_id: int, pet: PetCreate, db: AsyncSession = Depends(get_db)):
    # Verify user exists
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
        user_id=user_id
    )
    db.add(new_pet)
    await db.commit()
    await db.refresh(new_pet)
    return new_pet

@app.get("/pets", response_model=List[PetResponse])
async def list_pets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet))
    return result.scalars().all()

@app.get("/pets/{pet_id}", response_model=PetResponse)
async def get_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="pet cant be found")
    return pet

@app.delete("/pets/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(pet_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="pet cant be found")
    
    await db.delete(pet)
    await db.commit()
    return None

from dtos.requests.pet_update import PetUpdate

@app.patch("/pets/{pet_id}", response_model=PetResponse)
async def update_pet(pet_id: int, pet_update: PetUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.id == pet_id))
    pet = result.scalar_one_or_none()
    if pet is None:
        raise HTTPException(status_code=404, detail="pet cant be found")
    
    # Update only provided fields
    update_data = pet_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(pet, field, value)
    
    await db.commit()
    await db.refresh(pet)
    return pet

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
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
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@app.get("/users/{user_id}/pets", response_model=List[PetResponse])
async def get_user_pets(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pet).where(Pet.user_id == user_id))
    return result.scalars().all()
