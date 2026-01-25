from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)

    pets = relationship("Pet", back_populates="owner")

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    species = Column(String)
    age = Column(Integer)
    description = Column(String)
    gender = Column(String)
    weight = Column(Float)
    color = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="pets")

from datetime import datetime
from sqlalchemy import DateTime

class PetWeight(Base):
    __tablename__ = "pet_weights"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(String)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

    pet = relationship("Pet", backref="weight_entries")
