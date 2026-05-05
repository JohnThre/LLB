"""
Tests for health check endpoints.
"""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test basic health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data


def test_legacy_health_redirect(client: TestClient):
    """Test legacy health endpoint redirects."""
    response = client.get("/health", allow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/api/v1/health"


def test_root_endpoint(client: TestClient):
    """Test root endpoint returns HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "LLB" in response.text