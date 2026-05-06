"""
Tests for approved literature management endpoints.
"""

from fastapi.testclient import TestClient


def test_list_literature_sources(client: TestClient):
    """Users can review approved literature sources."""
    response = client.get("/api/v1/literature/sources?language=en")

    assert response.status_code == 200
    data = response.json()
    assert data["sources"]
    assert data["sources"][0]["status"] == "approved"
    assert data["sources"][0]["publisher"]


def test_admin_can_create_literature_source(client: TestClient):
    """Admins can add a pending source for review."""
    response = client.post(
        "/api/v1/literature/sources",
        json={
            "title": "Test Reviewed Source",
            "publisher": "Test Public Health Publisher",
            "language": "en",
            "source_type": "official",
            "url": "https://example.org/reviewed-source",
            "topics": ["contraception"],
            "excerpt": "Condoms reduce the risk of many sexually transmitted infections when used correctly.",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Reviewed Source"
    assert data["status"] == "pending"


def test_admin_can_approve_literature_source(client: TestClient):
    """Admins can approve a pending source."""
    create_response = client.post(
        "/api/v1/literature/sources",
        json={
            "title": "Pending Source To Approve",
            "publisher": "Test Public Health Publisher",
            "language": "en",
            "source_type": "official",
            "url": "https://example.org/pending-source",
            "topics": ["sti"],
            "excerpt": "Testing and prevention are important parts of STI care.",
        },
    )
    source_id = create_response.json()["id"]

    approve_response = client.post(f"/api/v1/literature/sources/{source_id}/approve")

    assert approve_response.status_code == 200
    assert approve_response.json()["status"] == "approved"
