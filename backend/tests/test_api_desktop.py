"""Tests for desktop-local control endpoints."""

from fastapi.testclient import TestClient

from services import ai_providers


def test_desktop_credentials_endpoint_requires_launch_token(
    client: TestClient, monkeypatch
):
    """Desktop credential updates require the per-launch control token."""
    monkeypatch.setenv("LLB_DESKTOP_CONTROL_TOKEN", "launch-token")

    response = client.post(
        "/api/v1/desktop/provider-credentials",
        json={
            "credentials": {
                "mistral": {
                    "api_key": "mistral-key",
                    "model": "mistral-medium-3.5",
                }
            }
        },
    )

    assert response.status_code == 403


def test_desktop_credentials_endpoint_stores_masked_credentials(
    client: TestClient, monkeypatch
):
    """Accepted desktop credentials are stored in memory and masked in output."""
    monkeypatch.setenv("LLB_DESKTOP_CONTROL_TOKEN", "launch-token")
    ai_providers.clear_desktop_provider_credentials()

    response = client.post(
        "/api/v1/desktop/provider-credentials",
        headers={"x-llb-desktop-token": "launch-token"},
        json={
            "credentials": {
                "mistral": {
                    "api_key": "mistral-key",
                    "model": "mistral-medium-3.5",
                }
            }
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data == {
        "providers": [
            {
                "name": "mistral",
                "model": "mistral-medium-3.5",
                "has_api_key": True,
            }
        ]
    }
    assert "mistral-key" not in str(data)
    assert ai_providers.get_desktop_provider_status() == data["providers"]

    ai_providers.clear_desktop_provider_credentials()
