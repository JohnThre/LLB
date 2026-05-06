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
    assert data["status"] == "answered"
    assert "citations" in data


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


def test_chat_normalizes_english_ui_locale(client: TestClient):
    """Frontend locale en-US is accepted as English chat language."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "What is sexual health?",
            "language": "en-US",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert data["language"] == "en"


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


def test_chat_rejects_unsupported_language(client: TestClient):
    """Unsupported-language questions ask the user to switch language."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "¿Qué es la anticoncepción?",
            "language": "es",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "refused"
    assert data["refusal_reason"] == "unsupported_language"
    assert data["citations"] == []


def test_chat_returns_citations_for_source_backed_answer(client: TestClient):
    """Supported questions include reviewed citations in the response."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "How do condoms help prevent STIs?",
            "language": "en",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert data["citations"]
    assert data["citations"][0]["publisher"]
    assert data["citations"][0]["url"]


def test_chat_declines_when_no_approved_source_matches(client: TestClient):
    """The assistant refuses rather than answering without reviewed sources."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "Tell me about a topic outside sexual health: sourdough starter ratios",
            "language": "en",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "refused"
    assert data["refusal_reason"] == "no_approved_source"
    assert data["citations"] == []
