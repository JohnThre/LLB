"""Tests for AI provider metadata endpoints."""

from fastapi.testclient import TestClient


def test_provider_catalog_endpoint_returns_public_provider_metadata(
    client: TestClient,
):
    """Provider metadata is available without exposing credentials."""
    response = client.get("/api/v1/ai/providers")

    assert response.status_code == 200
    data = response.json()
    providers = {provider["name"]: provider for provider in data["providers"]}

    assert providers["openai"]["default_model"] == "gpt-5.2"
    assert providers["mistral"]["default_model"] == "mistral-medium-3.5"
    for provider in data["providers"]:
        assert "credential_env" not in provider
        assert "api_key" not in provider
        assert "token" not in provider
    assert "GITHUB_MODELS_TOKEN" not in str(data)
