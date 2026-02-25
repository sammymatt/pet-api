from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from sqlalchemy.orm import DeclarativeBase

import os


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://pet:pet@db:5432/petdb")
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)


engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
