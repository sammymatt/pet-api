# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PetPal Backend - A Python FastAPI REST API for managing pets and users with PostgreSQL database.

## Development Commands

### Running the Application

```bash
# Start full stack with Docker (recommended)
docker compose up --build

# Run API locally (requires DATABASE_URL environment variable)
export DATABASE_URL='postgresql+asyncpg://pet:pet@localhost:5432/petdb'
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Database Migrations (Alembic)

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Run migrations (requires local postgres or docker db running)
alembic upgrade head

# Alembic uses psycopg2 (sync) configured in alembic.ini
# App uses asyncpg (async) configured via DATABASE_URL env var
```

### Seeding Data

```bash
# Seed with fake data (requires DATABASE_URL for local runs)
export DATABASE_URL='postgresql+asyncpg://pet:pet@localhost:5432/petdb'
python seed.py
```

## Architecture

### Core Components

- **main.py**: FastAPI app setup, middleware registration (SlowAPI rate limiting), and router includes
- **models.py**: SQLAlchemy ORM models (User, Pet, PetWeight, FeatureRequest) with relationships
- **db.py**: Async database engine and session configuration using asyncpg
- **limiter.py**: slowapi Limiter instance keyed by client IP (in-memory storage)

### Data Transfer Objects

- **dtos/requests/**: Pydantic models for validating incoming request data (PetCreate, PetUpdate, UserCreate, WeightCreate)
- **dtos/responses/**: Pydantic models for serializing response data (PetResponse, UserResponse, WeightResponse)

### Database

- PostgreSQL 15 with async access via asyncpg
- Alembic migrations in `migrations/versions/`
- Two connection strings: asyncpg for app runtime, psycopg2 for Alembic migrations

### Services (Docker)

- **api**: FastAPI application on port 8000
- **db**: PostgreSQL on port 5432 (credentials: pet/pet, database: petdb)
- **pgadmin**: Database admin UI on port 5050 (admin@admin.com/admin)

## API Endpoints

- `POST /users` - Create user
- `POST /users/{user_id}/pets` - Create pet for user
- `GET /users/{user_id}/pets` - List user's pets
- `GET /pets` - List all pets
- `GET /pets/{pet_id}` - Get pet by ID
- `PATCH /pets/{pet_id}` - Update pet (partial)
- `DELETE /pets/{pet_id}` - Delete pet
- `POST /pets/{pet_id}/weights` - Add weight record
- `GET /pets/{pet_id}/weights` - Get weight history
- `POST /feature-requests` - Create feature request (rate limited: 5/min per IP)
- `GET /feature-requests` - List feature requests (sorted by votes)
- `GET /feature-requests/{id}` - Get feature request by ID
- `PATCH /feature-requests/{id}` - Update feature request
- `POST /feature-requests/{id}/vote` - Vote on feature request (rate limited: 10/min per IP)
- `DELETE /feature-requests/{id}` - Delete feature request
