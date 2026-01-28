"""
Comprehensive API integration tests using pytest and FastAPI TestClient.
This is the recommended approach for automated testing.
"""
import pytest
from fastapi import status


class TestAuthFlow:
    """Test complete authentication flow."""
    
    def _register_and_login(self, client, test_user_data):
        """Helper method to register and login, returns token."""
        # Register
        register_response = client.post("/api/v1/auth/register", json=test_user_data)
        assert register_response.status_code == status.HTTP_201_CREATED
        user_data = register_response.json()
        assert user_data["username"] == test_user_data["username"]
        
        # Login
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user_data["username"],
                "password": test_user_data["password"]
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        login_data = login_response.json()
        assert "access_token" in login_data
        return login_data["access_token"]
    
    def test_register_and_login(self, client, test_user_data):
        """Test complete registration and login flow."""
        token = self._register_and_login(client, test_user_data)
        assert token is not None
        assert len(token) > 0
    
    def test_authenticated_endpoint(self, client, test_user_data):
        """Test accessing protected endpoint with token."""
        # Get token
        token = self._register_and_login(client, test_user_data)
        headers = {"Authorization": f"Bearer {token}"}
        
        # Access protected endpoint
        response = client.get("/api/v1/vocabulary", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data


class TestVocabularyAPI:
    """Test vocabulary endpoints."""
    
    def _get_admin_auth_headers(self, client, test_admin_user):
        """Helper method to get admin authentication headers."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_admin_user["username"],
                "password": test_admin_user["password"]
            }
        )
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_create_and_get_vocabulary(self, client, test_admin_user, test_vocabulary_data):
        """Test creating and retrieving vocabulary items as admin."""
        # Login as admin
        headers = self._get_admin_auth_headers(client, test_admin_user)
        
        # Create vocabulary as admin
        create_response = client.post(
            "/api/v1/vocabulary",
            json=test_vocabulary_data,
            headers=headers
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        created_item = create_response.json()
        assert created_item["word"] == test_vocabulary_data["word"]
        
        # Get vocabulary list
        get_response = client.get("/api/v1/vocabulary", headers=headers)
        assert get_response.status_code == status.HTTP_200_OK
        data = get_response.json()
        assert len(data["items"]) > 0
        assert data["total"] > 0


class TestProgressAPI:
    """Test progress tracking endpoints."""
    
    def _get_auth_headers(self, client, test_user_data):
        """Helper method to get authentication headers for regular user."""
        client.post("/api/v1/auth/register", json=test_user_data)
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_user_data["username"],
                "password": test_user_data["password"]
            }
        )
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def _get_admin_auth_headers(self, client, test_admin_user):
        """Helper method to get admin authentication headers."""
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "username": test_admin_user["username"],
                "password": test_admin_user["password"]
            }
        )
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    
    def test_mark_word_as_mastered(self, client, test_user_data, test_admin_user, test_vocabulary_data):
        """Test marking a word as mastered."""
        # Create vocabulary as admin
        admin_headers = self._get_admin_auth_headers(client, test_admin_user)
        vocab_response = client.post(
            "/api/v1/vocabulary",
            json=test_vocabulary_data,
            headers=admin_headers
        )
        assert vocab_response.status_code == status.HTTP_201_CREATED
        vocab_id = vocab_response.json()["id"]
        
        # Login as regular user
        user_headers = self._get_auth_headers(client, test_user_data)
        
        # Mark as mastered (regular user can do this)
        progress_response = client.post(
            "/api/v1/progress/mastered",
            json={
                "vocabulary_item_id": vocab_id,
                "year": "year3"
            },
            headers=user_headers
        )
        assert progress_response.status_code == status.HTTP_201_CREATED
        progress_data = progress_response.json()
        assert progress_data["is_mastered"] is True
