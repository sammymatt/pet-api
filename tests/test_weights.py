import pytest


async def create_pet(client):
    user_response = await client.post("/users", json={
        "firstname": "Test",
        "lastname": "User",
        "email": f"testweight{id(client)}@example.com"
    })
    user_id = user_response.json()["id"]
    pet_response = await client.post(f"/users/{user_id}/pets", json={
        "name": "Buddy",
        "species": "Dog",
        "age": 3
    })
    return pet_response.json()["id"]


async def test_create_weight(client):
    pet_id = await create_pet(client)
    response = await client.post(f"/pets/{pet_id}/weights", json={
        "weight": 25.5,
        "notes": "Regular checkup"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["weight"] == 25.5
    assert data["notes"] == "Regular checkup"
    assert data["pet_id"] == pet_id
    assert "recorded_at" in data


async def test_create_weight_with_date(client):
    pet_id = await create_pet(client)
    response = await client.post(f"/pets/{pet_id}/weights", json={
        "weight": 24.0,
        "recorded_at": "2025-06-15T10:00:00"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["weight"] == 24.0
    assert data["recorded_at"] == "2025-06-15T10:00:00"


async def test_create_weight_pet_not_found(client):
    response = await client.post("/pets/9999/weights", json={
        "weight": 25.5
    })
    assert response.status_code == 404


async def test_list_pet_weights(client):
    pet_id = await create_pet(client)
    await client.post(f"/pets/{pet_id}/weights", json={"weight": 25.0})
    await client.post(f"/pets/{pet_id}/weights", json={"weight": 26.0})

    response = await client.get(f"/pets/{pet_id}/weights")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_update_weight(client):
    pet_id = await create_pet(client)
    create_response = await client.post(f"/pets/{pet_id}/weights", json={
        "weight": 25.0
    })
    weight_id = create_response.json()["id"]

    response = await client.patch(f"/weights/{weight_id}", json={
        "weight": 26.5,
        "notes": "After diet change"
    })
    assert response.status_code == 200
    assert response.json()["weight"] == 26.5
    assert response.json()["notes"] == "After diet change"


async def test_update_weight_not_found(client):
    response = await client.patch("/weights/9999", json={
        "weight": 26.5
    })
    assert response.status_code == 404


async def test_delete_weight(client):
    pet_id = await create_pet(client)
    create_response = await client.post(f"/pets/{pet_id}/weights", json={
        "weight": 25.0
    })
    weight_id = create_response.json()["id"]

    response = await client.delete(f"/weights/{weight_id}")
    assert response.status_code == 204

    # Verify it's gone
    list_response = await client.get(f"/pets/{pet_id}/weights")
    weights = list_response.json()
    assert not any(w["id"] == weight_id for w in weights)


async def test_delete_weight_not_found(client):
    response = await client.delete("/weights/9999")
    assert response.status_code == 404
