import pytest


async def create_pet(client):
    user_response = await client.post("/users", json={
        "firstname": "Test",
        "lastname": "User",
        "email": f"test{id(client)}@example.com"
    })
    user_id = user_response.json()["id"]
    pet_response = await client.post(f"/users/{user_id}/pets", json={
        "name": "Buddy",
        "species": "Dog",
        "age": 3
    })
    return pet_response.json()["id"]


async def test_create_appointment(client):
    pet_id = await create_pet(client)
    response = await client.post(f"/pets/{pet_id}/appointments", json={
        "appointment_date": "2024-06-15T10:30:00",
        "reason": "Annual checkup",
        "vet_name": "Dr. Johnson",
        "location": "Pet Clinic"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["reason"] == "Annual checkup"
    assert data["status"] == "scheduled"
    assert data["pet_id"] == pet_id


async def test_create_appointment_pet_not_found(client):
    response = await client.post("/pets/9999/appointments", json={
        "appointment_date": "2024-06-15T10:30:00",
        "reason": "Checkup"
    })
    assert response.status_code == 404


async def test_list_pet_appointments(client):
    pet_id = await create_pet(client)
    await client.post(f"/pets/{pet_id}/appointments", json={
        "appointment_date": "2024-06-15T10:30:00",
        "reason": "Checkup"
    })
    await client.post(f"/pets/{pet_id}/appointments", json={
        "appointment_date": "2024-07-15T14:00:00",
        "reason": "Vaccination"
    })

    response = await client.get(f"/pets/{pet_id}/appointments")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_update_appointment_status(client):
    pet_id = await create_pet(client)
    create_response = await client.post(f"/pets/{pet_id}/appointments", json={
        "appointment_date": "2024-06-15T10:30:00",
        "reason": "Checkup"
    })
    appointment_id = create_response.json()["id"]

    response = await client.patch(f"/appointments/{appointment_id}", json={
        "status": "completed",
        "notes": "All good, healthy pet"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


async def test_delete_appointment(client):
    pet_id = await create_pet(client)
    create_response = await client.post(f"/pets/{pet_id}/appointments", json={
        "appointment_date": "2024-06-15T10:30:00",
        "reason": "Checkup"
    })
    appointment_id = create_response.json()["id"]

    response = await client.delete(f"/appointments/{appointment_id}")
    assert response.status_code == 204

    response = await client.get(f"/appointments/{appointment_id}")
    assert response.status_code == 404
