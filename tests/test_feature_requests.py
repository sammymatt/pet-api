import pytest


async def test_create_feature_request(client):
    response = await client.post("/feature-requests", json={
        "title": "Dark mode",
        "category": "UI",
        "description": "Add dark mode support"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Dark mode"
    assert data["category"] == "UI"
    assert data["description"] == "Add dark mode support"
    assert data["votes"] == 0
    assert data["is_implemented"] is False


async def test_create_feature_request_minimal(client):
    response = await client.post("/feature-requests", json={
        "title": "Export data",
        "category": "Data"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Export data"
    assert data["description"] is None


async def test_create_feature_request_missing_fields(client):
    response = await client.post("/feature-requests", json={
        "title": "No category"
    })
    assert response.status_code == 422


async def test_list_feature_requests(client):
    await client.post("/feature-requests", json={
        "title": "Feature A",
        "category": "UI"
    })
    await client.post("/feature-requests", json={
        "title": "Feature B",
        "category": "API"
    })

    response = await client.get("/feature-requests")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_feature_request(client):
    create_response = await client.post("/feature-requests", json={
        "title": "Dark mode",
        "category": "UI"
    })
    feature_id = create_response.json()["id"]

    response = await client.get(f"/feature-requests/{feature_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Dark mode"


async def test_get_feature_request_not_found(client):
    response = await client.get("/feature-requests/9999")
    assert response.status_code == 404


async def test_update_feature_request(client):
    create_response = await client.post("/feature-requests", json={
        "title": "Dark mode",
        "category": "UI"
    })
    feature_id = create_response.json()["id"]

    response = await client.patch(f"/feature-requests/{feature_id}", json={
        "votes": 5,
        "is_implemented": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["votes"] == 5
    assert data["is_implemented"] is True
    assert data["title"] == "Dark mode"


async def test_update_feature_request_not_found(client):
    response = await client.patch("/feature-requests/9999", json={
        "votes": 1
    })
    assert response.status_code == 404


async def test_vote_feature_request(client):
    create_response = await client.post("/feature-requests", json={
        "title": "Dark mode",
        "category": "UI"
    })
    feature_id = create_response.json()["id"]
    assert create_response.json()["votes"] == 0

    response = await client.post(f"/feature-requests/{feature_id}/vote")
    assert response.status_code == 200
    assert response.json()["votes"] == 1

    response = await client.post(f"/feature-requests/{feature_id}/vote")
    assert response.status_code == 200
    assert response.json()["votes"] == 2


async def test_vote_feature_request_not_found(client):
    response = await client.post("/feature-requests/9999/vote")
    assert response.status_code == 404


async def test_delete_feature_request(client):
    create_response = await client.post("/feature-requests", json={
        "title": "Dark mode",
        "category": "UI"
    })
    feature_id = create_response.json()["id"]

    response = await client.delete(f"/feature-requests/{feature_id}")
    assert response.status_code == 204

    response = await client.get(f"/feature-requests/{feature_id}")
    assert response.status_code == 404


async def test_delete_feature_request_not_found(client):
    response = await client.delete("/feature-requests/9999")
    assert response.status_code == 404


async def test_create_feature_request_rate_limit(client):
    for i in range(5):
        response = await client.post("/feature-requests", json={
            "title": f"Feature {i}",
            "category": "UI"
        })
        assert response.status_code == 201

    response = await client.post("/feature-requests", json={
        "title": "One too many",
        "category": "UI"
    })
    assert response.status_code == 429


async def test_vote_feature_request_rate_limit(client):
    create_response = await client.post("/feature-requests", json={
        "title": "Popular feature",
        "category": "UI"
    })
    feature_id = create_response.json()["id"]

    for i in range(10):
        response = await client.post(f"/feature-requests/{feature_id}/vote")
        assert response.status_code == 200

    response = await client.post(f"/feature-requests/{feature_id}/vote")
    assert response.status_code == 429
