from fastapi import FastAPI

from routers import pets, users, weights, vaccines, appointments, tablets, records

app = FastAPI()

app.include_router(pets.router)
app.include_router(users.router)
app.include_router(weights.router)
app.include_router(vaccines.router)
app.include_router(appointments.router)
app.include_router(tablets.router)
app.include_router(records.router)
