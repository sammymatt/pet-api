from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import text

from db import engine
from limiter import limiter
from routers import pets, users, weights, vaccines, appointments, tablets, records, feature_requests

app = FastAPI()
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"},
    )


app.add_middleware(SlowAPIMiddleware)

@app.get("/health", tags=["health"])
async def health_check():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected"},
        )


app.include_router(pets.router)
app.include_router(users.router)
app.include_router(weights.router)
app.include_router(vaccines.router)
app.include_router(appointments.router)
app.include_router(tablets.router)
app.include_router(records.router)
app.include_router(feature_requests.router)
