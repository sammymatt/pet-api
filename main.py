from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

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

app.include_router(pets.router)
app.include_router(users.router)
app.include_router(weights.router)
app.include_router(vaccines.router)
app.include_router(appointments.router)
app.include_router(tablets.router)
app.include_router(records.router)
app.include_router(feature_requests.router)
