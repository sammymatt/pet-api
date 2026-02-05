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


async def test_create_vaccine(client):
    pet_id = await create_pet(client)
    response = await client.post(f"/pets/{pet_id}/vaccines", json={
        "name": "Rabies",
        "administered_date": "2024-01-15",
        "next_due_date": "2025-01-15",
        "administered_by": "Dr. Smith"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Rabies"
    assert data["administered_date"] == "2024-01-15"
    assert data["pet_id"] == pet_id


async def test_create_vaccine_pet_not_found(client):
    response = await client.post("/pets/9999/vaccines", json={
        "name": "Rabies",
        "administered_date": "2024-01-15"
    })
    assert response.status_code == 404


async def test_list_pet_vaccines(client):
    pet_id = await create_pet(client)
    await client.post(f"/pets/{pet_id}/vaccines", json={
        "name": "Rabies",
        "administered_date": "2024-01-15"
    })
    await client.post(f"/pets/{pet_id}/vaccines", json={
        "name": "Distemper",
        "administered_date": "2024-02-15"
    })

    response = await client.get(f"/pets/{pet_id}/vaccines")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_update_vaccine(client):
    pet_id = await create_pet(client)
    create_response = await client.post(f"/pets/{pet_id}/vaccines", json={
        "name": "Rabies",
        "administered_date": "2024-01-15"
    })
    vaccine_id = create_response.json()["id"]

    response = await client.patch(f"/vaccines/{vaccine_id}", json={
        "next_due_date": "2025-01-15",
        "notes": "Annual booster"
    })
    assert response.status_code == 200
    assert response.json()["next_due_date"] == "2025-01-15"
    assert response.json()["notes"] == "Annual booster"


async def test_delete_vaccine(client):
    pet_id = await create_pet(client)
    create_response = await client.post(f"/pets/{pet_id}/vaccines", json={
        "name": "Rabies",
        "administered_date": "2024-01-15"
    })
    vaccine_id = create_response.json()["id"]

    response = await client.delete(f"/vaccines/{vaccine_id}")
    assert response.status_code == 204

    response = await client.get(f"/vaccines/{vaccine_id}")
    assert response.status_code == 404
