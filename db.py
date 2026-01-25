from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from sqlalchemy.orm import DeclarativeBase

import os


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://pet:pet@db:5432/petdb")


engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
