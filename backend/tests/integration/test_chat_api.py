"""Integration tests for chat API."""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
def test_chat_endpoint(client: TestClient):
    """Test chat endpoint integration."""
    payload = {"message": "What is sexual health?", "language": "en"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "language_detected" in data


@pytest.mark.integration
def test_chat_multilingual(client: TestClient):
    """Test multilingual chat support."""
    # Test Chinese
    payload = {"message": "什么是性健康？", "cultural_context": "chinese"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["language_detected"] in ["zh-CN", "zh"]
