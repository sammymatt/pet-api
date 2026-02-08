import pytest


async def create_user_with_pet(client, email_suffix=""):
    user_response = await client.post("/users", json={
        "firstname": "Test",
        "lastname": "User",
        "email": f"testrecords{email_suffix}{id(client)}@example.com"
    })
    user_id = user_response.json()["id"]
    pet_response = await client.post(f"/users/{user_id}/pets", json={
        "name": "Buddy",
        "species": "Dog",
        "age": 3
    })
    pet_id = pet_response.json()["id"]
    return user_id, pet_id


async def test_get_pet_records_empty(client):
    _, pet_id = await create_user_with_pet(client, "empty")
    response = await client.get(f"/pets/{pet_id}/records")
    assert response.status_code == 200
    data = response.json()
    assert data["vaccines"] == []
    assert data["tablets"] == []
    assert data["appointments"] == []


async def test_get_pet_records_with_data(client):
    _, pet_id = await create_user_with_pet(client, "data")

    # Add vaccine
    await client.post(f"/pets/{pet_id}/vaccines", json={
        "name": "Rabies",
        "administered_date": "2024-01-15",
        "frequency": "yearly",
        "up_to_date": True
    })

    # Add tablet
    await client.post(f"/pets/{pet_id}/tablets", json={
        "name": "Heartworm",
        "start_date": "2024-01-01",
        "frequency": "monthly"
    })

    # Add appointment
    await client.post(f"/pets/{pet_id}/appointments", json={
        "appointment_date": "2024-06-15T10:00:00",
        "reason": "Checkup"
    })

    response = await client.get(f"/pets/{pet_id}/records")
    assert response.status_code == 200
    data = response.json()
    assert len(data["vaccines"]) == 1
    assert len(data["tablets"]) == 1
    assert len(data["appointments"]) == 1
    assert data["vaccines"][0]["name"] == "Rabies"
    assert data["vaccines"][0]["frequency"] == "yearly"
    assert data["vaccines"][0]["up_to_date"] == True
    assert data["vaccines"][0]["pet_name"] == "Buddy"


async def test_get_pet_records_not_found(client):
    response = await client.get("/pets/9999/records")
    assert response.status_code == 404


async def test_get_user_records_empty(client):
    user_id, _ = await create_user_with_pet(client, "userempty")
    response = await client.get(f"/users/{user_id}/records")
    assert response.status_code == 200
    data = response.json()
    assert data["vaccines"] == []
    assert data["tablets"] == []
    assert data["appointments"] == []


async def test_get_user_records_multiple_pets(client):
    # Create user with two pets
    user_response = await client.post("/users", json={
        "firstname": "Multi",
        "lastname": "Pet",
        "email": f"multipet{id(client)}@example.com"
    })
    user_id = user_response.json()["id"]

    pet1_response = await client.post(f"/users/{user_id}/pets", json={
        "name": "Buddy",
        "species": "Dog",
        "age": 3
    })
    pet1_id = pet1_response.json()["id"]

    pet2_response = await client.post(f"/users/{user_id}/pets", json={
        "name": "Whiskers",
        "species": "Cat",
        "age": 2
    })
    pet2_id = pet2_response.json()["id"]

    # Add vaccines to both pets
    await client.post(f"/pets/{pet1_id}/vaccines", json={
        "name": "Rabies",
        "administered_date": "2024-01-15"
    })
    await client.post(f"/pets/{pet2_id}/vaccines", json={
        "name": "Feline Distemper",
        "administered_date": "2024-02-15"
    })

    response = await client.get(f"/users/{user_id}/records")
    assert response.status_code == 200
    data = response.json()
    assert len(data["vaccines"]) == 2

    pet_names = {v["pet_name"] for v in data["vaccines"]}
    assert pet_names == {"Buddy", "Whiskers"}


async def test_get_user_records_not_found(client):
    response = await client.get("/users/9999/records")
    assert response.status_code == 404
