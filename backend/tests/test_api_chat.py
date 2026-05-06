"""
Tests for chat API endpoints.
"""

import pytest
from fastapi.testclient import TestClient


def test_chat_detects_language_when_request_language_is_null(client: TestClient):
    """Null language values fall back to supported content detection."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "How do condoms help prevent STIs?",
            "language": None,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert data["language"] == "en"


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


def test_chat_detects_chinese_without_requested_language(client: TestClient):
    """Chinese content is detected when the caller omits language."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "安全套如何帮助预防艾滋？",
            "language": None,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "answered"
    assert data["language"] == "zh-CN"


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


def test_chat_returns_chinese_language_refusal_for_chinese_ui(client: TestClient):
    """Unsupported text from the Chinese UI returns a Chinese refusal."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "¿Qué es la anticoncepción?",
            "language": "zh-CN",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "refused"
    assert data["language"] == "zh-CN"
    assert data["refusal_reason"] == "unsupported_language"
    assert "简体中文" in data["response"]


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


def test_chat_declines_without_chinese_source_support(client: TestClient):
    """Chinese no-source refusals are localized."""
    response = client.post(
        "/api/v1/chat",
        json={
            "message": "请回答 outside sexual health 这个没有资料支持的问题",
            "language": "zh-CN",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "refused"
    assert data["language"] == "zh-CN"
    assert data["refusal_reason"] == "no_approved_source"
    assert "已批准资料" in data["response"]


def test_chat_endpoint_returns_500_when_generation_fails(
    client: TestClient, mock_ai_service
):
    """Generation failures are surfaced as chat endpoint errors."""
    mock_ai_service.generate_response.side_effect = RuntimeError("model unavailable")

    response = client.post(
        "/api/v1/chat",
        json={
            "message": "How do condoms help prevent STIs?",
            "language": "en",
        },
    )

    assert response.status_code == 500
    assert "Failed to process chat message" in response.json()["detail"]


def test_get_supported_languages_returns_500_when_service_fails(
    client: TestClient, mock_ai_service
):
    """Language metadata failures return a 500 response."""
    mock_ai_service.get_supported_languages.side_effect = RuntimeError("service down")

    response = client.get("/api/v1/chat/languages")

    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to retrieve supported languages"


def test_get_chat_status_returns_500_when_service_fails(
    client: TestClient, mock_ai_service
):
    """Status metadata failures return a 500 response."""
    mock_ai_service.is_ready.side_effect = RuntimeError("service down")

    response = client.get("/api/v1/chat/status")

    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to retrieve chat status"
