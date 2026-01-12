import pytest
from fastapi import status


def test_get_vocabulary_requires_auth(client):
    """Test that vocabulary endpoints require authentication."""
    response = client.get("/api/v1/vocabulary")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_create_and_get_vocabulary(client, test_user_data, test_vocabulary_data):
    """Test creating and retrieving vocabulary items."""
    # Register and login
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create vocabulary item
    create_response = client.post(
        "/api/v1/vocabulary",
        json=test_vocabulary_data,
        headers=headers
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    created_item = create_response.json()
    assert created_item["word"] == test_vocabulary_data["word"]
    
    # Get vocabulary items
    get_response = client.get("/api/v1/vocabulary", headers=headers)
    assert get_response.status_code == status.HTTP_200_OK
    data = get_response.json()
    assert len(data["items"]) > 0
    assert data["total"] > 0

