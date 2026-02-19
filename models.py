from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, DateTime, Boolean
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
    birthday = Column(Date)
    image_url = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="pets")

class PetWeight(Base):
    __tablename__ = "pet_weights"

    id = Column(Integer, primary_key=True, index=True)
    weight = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(String)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

    pet = relationship("Pet", backref="weight_entries")


class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    administered_date = Column(Date, nullable=False)
    next_due_date = Column(Date)
    administered_by = Column(String)
    frequency = Column(String)
    up_to_date = Column(Boolean)
    notes = Column(String)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

    pet = relationship("Pet", backref="vaccines")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    appointment_date = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    vet_name = Column(String)
    location = Column(String)
    notes = Column(String)
    status = Column(String, default="scheduled")
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

    pet = relationship("Pet", backref="appointments")


class Tablet(Base):
    __tablename__ = "tablets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dosage = Column(String)
    frequency = Column(String)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    notes = Column(String)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

    pet = relationship("Pet", backref="tablets")


class FeatureRequest(Base):
    __tablename__ = "feature_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String)
    votes = Column(Integer, default=0)
    is_implemented = Column(Boolean, default=False)
