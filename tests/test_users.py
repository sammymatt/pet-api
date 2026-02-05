import pytest


async def test_create_user(client):
    response = await client.post("/users", json={
        "firstname": "John",
        "lastname": "Doe",
        "email": "john@example.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["firstname"] == "John"
    assert data["lastname"] == "Doe"
    assert data["email"] == "john@example.com"
    assert "id" in data


async def test_create_user_duplicate_email(client):
    await client.post("/users", json={
        "firstname": "John",
        "lastname": "Doe",
        "email": "duplicate@example.com"
    })
    response = await client.post("/users", json={
        "firstname": "Jane",
        "lastname": "Doe",
        "email": "duplicate@example.com"
    })
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]
