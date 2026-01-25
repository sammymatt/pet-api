import asyncio
import os
from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import Pet, Base, User
from db import SessionLocal

fake = Faker()

async def seed_data():
    print("Seeding database...")
    async with SessionLocal() as session:
        # Create users
        users = []
        for _ in range(5):
            user = User(
                firstname=fake.first_name(),
                lastname=fake.last_name(),
                email=fake.unique.email()
            )
            users.append(user)
        session.add_all(users)
        await session.flush() # flush to get IDs

        pets = []
        for _ in range(20):
            pet = Pet(
                name=fake.first_name(),
                species=fake.random_element(elements=('Dog', 'Cat', 'Bird', 'Fish', 'Hamster', 'Rabbit')),
                age=fake.random_int(min=1, max=15),
                description=fake.sentence(),
                gender=fake.random_element(elements=('Male', 'Female')),
                weight=round(fake.random.uniform(1.0, 40.0), 1),
                color=fake.color_name(),
                user_id=fake.random_element(elements=[u.id for u in users])
            )
            pets.append(pet)
        
        session.add_all(pets)
        await session.commit()
        print(f"Successfully added {len(users)} users and {len(pets)} fake pets!")

if __name__ == "__main__":
    # If running locally without docker networking, 'db' hostname won't resolve.
    # The default in db.py is 'postgresql+asyncpg://pet:pet@db:5432/petdb'.
    # If that fails, it might be nice to hint the user or fallback, but let's stick to standard env vars.
    # To run locally: export DATABASE_URL=postgresql+asyncpg://pet:pet@localhost:5432/petdb
    
    try:
        asyncio.run(seed_data())
    except Exception as e:
        print(f"Error seeding data: {e}")
        print("Tip: If running locally, ensure your database is accessible and DATABASE_URL is set correctly.")
        print("Example: export DATABASE_URL='postgresql+asyncpg://pet:pet@localhost:5432/petdb'")
