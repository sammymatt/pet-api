import pytest


async def create_user(client):
    response = await client.post("/users", json={
        "firstname": "Test",
        "lastname": "User",
        "email": f"test{id(client)}@example.com"
    })
    return response.json()["id"]


async def test_create_pet(client):
    user_id = await create_user(client)
    response = await client.post(f"/users/{user_id}/pets", json={
        "name": "Buddy",
        "species": "Dog",
        "age": 3
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Buddy"
    assert data["species"] == "Dog"
    assert data["age"] == 3


async def test_create_pet_user_not_found(client):
    response = await client.post("/users/9999/pets", json={
        "name": "Buddy",
        "species": "Dog",
        "age": 3
    })
    assert response.status_code == 404


async def test_create_pet_with_optional_fields(client):
    user_id = await create_user(client)
    response = await client.post(f"/users/{user_id}/pets", json={
        "name": "Max",
        "species": "Cat",
        "age": 2,
        "description": "Fluffy cat",
        "gender": "male",
        "color": "orange",
        "birthday": "2022-05-15"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "Fluffy cat"
    assert data["gender"] == "male"
    assert data["color"] == "orange"
    assert data["birthday"] == "2022-05-15"


async def test_list_pets(client):
    user_id = await create_user(client)
    await client.post(f"/users/{user_id}/pets", json={"name": "Pet1", "species": "Dog", "age": 1})
    await client.post(f"/users/{user_id}/pets", json={"name": "Pet2", "species": "Cat", "age": 2})

    response = await client.get("/pets")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_pet(client):
    user_id = await create_user(client)
    create_response = await client.post(f"/users/{user_id}/pets", json={
        "name": "Buddy",
        "species": "Dog",
        "age": 3
    })
    pet_id = create_response.json()["id"]

    response = await client.get(f"/pets/{pet_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Buddy"


async def test_get_pet_not_found(client):
    response = await client.get("/pets/9999")
    assert response.status_code == 404


async def test_update_pet(client):
    user_id = await create_user(client)
    create_response = await client.post(f"/users/{user_id}/pets", json={
        "name": "Buddy",
        "species": "Dog",
        "age": 3
    })
    pet_id = create_response.json()["id"]

    response = await client.patch(f"/pets/{pet_id}", json={"name": "Max", "age": 4})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Max"
    assert data["age"] == 4
    assert data["species"] == "Dog"  # unchanged


async def test_delete_pet(client):
    user_id = await create_user(client)
    create_response = await client.post(f"/users/{user_id}/pets", json={
        "name": "Buddy",
        "species": "Dog",
        "age": 3
    })
    pet_id = create_response.json()["id"]

    response = await client.delete(f"/pets/{pet_id}")
    assert response.status_code == 204

    response = await client.get(f"/pets/{pet_id}")
    assert response.status_code == 404


async def test_get_user_pets(client):
    user_id = await create_user(client)
    await client.post(f"/users/{user_id}/pets", json={"name": "Pet1", "species": "Dog", "age": 1})
    await client.post(f"/users/{user_id}/pets", json={"name": "Pet2", "species": "Cat", "age": 2})

    response = await client.get(f"/users/{user_id}/pets")
    assert response.status_code == 200
    assert len(response.json()) == 2
