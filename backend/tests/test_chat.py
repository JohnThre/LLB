"""
Tests for chat functionality
"""

from fastapi.testclient import TestClient


def test_chat_endpoint(client: TestClient):
    """Test basic chat endpoint functionality."""
    response = client.post(
        "/api/v1/chat",
        json={"message": "Hello, how are you?", "language": "en"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "language" in data
    assert "confidence" in data
    assert "safety_score" in data


def test_chat_languages_endpoint(client: TestClient):
    """Test supported languages endpoint."""
    response = client.get("/api/v1/chat/languages")

    assert response.status_code == 200
    data = response.json()
    assert "supported_languages" in data
    assert isinstance(data["supported_languages"], list)


def test_chat_status_endpoint(client: TestClient):
    """Test chat status endpoint."""
    response = client.get("/api/v1/chat/status")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_info" in data
    assert "supported_languages" in data


def test_health_endpoint(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "services" in data


def test_root_endpoint(client: TestClient):
    """Test root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
