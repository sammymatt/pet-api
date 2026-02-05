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


async def test_create_tablet(client):
    pet_id = await create_pet(client)
    response = await client.post(f"/pets/{pet_id}/tablets", json={
        "name": "Heartgard",
        "dosage": "1 tablet",
        "frequency": "Monthly",
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Heartgard"
    assert data["frequency"] == "Monthly"
    assert data["pet_id"] == pet_id


async def test_create_tablet_pet_not_found(client):
    response = await client.post("/pets/9999/tablets", json={
        "name": "Heartgard",
        "start_date": "2024-01-01"
    })
    assert response.status_code == 404


async def test_list_pet_tablets(client):
    pet_id = await create_pet(client)
    await client.post(f"/pets/{pet_id}/tablets", json={
        "name": "Heartgard",
        "start_date": "2024-01-01"
    })
    await client.post(f"/pets/{pet_id}/tablets", json={
        "name": "Flea Treatment",
        "start_date": "2024-01-15"
    })

    response = await client.get(f"/pets/{pet_id}/tablets")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_update_tablet(client):
    pet_id = await create_pet(client)
    create_response = await client.post(f"/pets/{pet_id}/tablets", json={
        "name": "Heartgard",
        "start_date": "2024-01-01"
    })
    tablet_id = create_response.json()["id"]

    response = await client.patch(f"/tablets/{tablet_id}", json={
        "end_date": "2024-06-30",
        "notes": "Completed course"
    })
    assert response.status_code == 200
    assert response.json()["end_date"] == "2024-06-30"


async def test_delete_tablet(client):
    pet_id = await create_pet(client)
    create_response = await client.post(f"/pets/{pet_id}/tablets", json={
        "name": "Heartgard",
        "start_date": "2024-01-01"
    })
    tablet_id = create_response.json()["id"]

    response = await client.delete(f"/tablets/{tablet_id}")
    assert response.status_code == 204

    response = await client.get(f"/tablets/{tablet_id}")
    assert response.status_code == 404
