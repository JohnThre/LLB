"""
Tests for chat API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


def test_chat_endpoint(client: TestClient):
    """Test chat endpoint with basic message."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "What is sexual health?",
            "language": "en"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "language" in data
    assert "confidence" in data
    assert "safety_score" in data


def test_chat_chinese_message(client: TestClient):
    """Test chat endpoint with Chinese message."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "什么是性健康？",
            "language": "zh-CN"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["language"] in ["zh-CN", "en"]


def test_chat_with_context(client: TestClient):
    """Test chat endpoint with context."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Tell me about contraception",
            "language": "en",
            "context": {"topic": "contraception"}
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data


def test_chat_empty_message(client: TestClient):
    """Test chat endpoint with empty message."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "",
            "language": "en"
        }
    )
    assert response.status_code == 422  # Validation error


def test_get_supported_languages(client: TestClient):
    """Test get supported languages endpoint."""
    response = client.get("/api/v1/chat/languages")
    assert response.status_code == 200
    data = response.json()
    assert "supported_languages" in data
    assert len(data["supported_languages"]) > 0


def test_get_chat_status(client: TestClient):
    """Test get chat status endpoint."""
    response = client.get("/api/v1/chat/status")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_info" in data
    assert "supported_languages" in data