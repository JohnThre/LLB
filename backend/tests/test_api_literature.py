"""
Tests for approved literature management endpoints.
"""

from fastapi.testclient import TestClient

from app.api import deps
from app.models.user import User
from app.services.literature_service import LiteratureService


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


def test_non_admin_cannot_create_literature_source(app):
    """Mutating literature actions require an admin or moderator role."""

    def regular_user():
        return User(id=2, email="user@example.com", is_active=True, role="user")

    app.dependency_overrides[deps.get_current_active_user] = regular_user
    client = TestClient(app)

    response = client.post(
        "/api/v1/literature/sources",
        json={
            "title": "Blocked Source",
            "publisher": "Test Public Health Publisher",
            "language": "en",
            "source_type": "official",
            "url": "https://example.org/blocked-source",
            "topics": ["sti"],
            "excerpt": "This source should not be accepted from a regular user.",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "manage_literature permission required"

    app.dependency_overrides.pop(deps.get_current_active_user, None)


def test_approve_missing_literature_source_returns_404(client: TestClient):
    """Approving an unknown source returns a reviewable 404."""
    response = client.post("/api/v1/literature/sources/not-found/approve")

    assert response.status_code == 404
    assert response.json()["detail"] == "Source not found"


def test_admin_can_archive_literature_source(client: TestClient):
    """Admins can archive approved sources so they no longer support answers."""
    create_response = client.post(
        "/api/v1/literature/sources",
        json={
            "title": "Pending Source To Archive",
            "publisher": "Test Public Health Publisher",
            "language": "en",
            "source_type": "official",
            "url": "https://example.org/archive-source",
            "topics": ["contraception"],
            "excerpt": "This source can be archived after review in the test suite.",
        },
    )
    source_id = create_response.json()["id"]

    archive_response = client.post(f"/api/v1/literature/sources/{source_id}/archive")

    assert archive_response.status_code == 200
    assert archive_response.json()["status"] == "archived"


def test_archive_missing_literature_source_returns_404(client: TestClient):
    """Archiving an unknown source returns a reviewable 404."""
    response = client.post("/api/v1/literature/sources/not-found/archive")

    assert response.status_code == 404
    assert response.json()["detail"] == "Source not found"


def test_retrieve_returns_empty_for_unsupported_language():
    """Retrieval only supports English and Simplified Chinese."""
    service = LiteratureService()

    assert service.retrieve("How do condoms prevent STIs?", "es") == []
