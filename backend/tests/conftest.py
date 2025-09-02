"""
Test configuration and fixtures for LLB backend tests.
"""

import asyncio
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock

from app.main import create_app
from app.services.ai_service import AIService
from app.services.audio_service import AudioService
from app.services.document_service import DocumentService


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_ai_service():
    """Mock AI service for testing."""
    service = AsyncMock()
    service.is_initialized = True
    service.is_ready.return_value = True
    service.is_healthy.return_value = True
    service.is_model_loaded.return_value = True
    service.get_supported_languages.return_value = ["en", "zh-CN"]
    service.get_model_info.return_value = {"name": "Test Model", "loaded": True}
    service.get_memory_usage.return_value = {"model_memory": "1GB"}
    service.generate_response.return_value = {
        "response": "Test response",
        "language": "en",
        "language_detected": "en",
        "confidence": 0.95,
        "safety_score": 0.98
    }
    return service


@pytest.fixture
def mock_audio_service():
    """Mock audio service for testing."""
    service = AsyncMock()
    service.is_initialized = True
    return service


@pytest.fixture
def mock_document_service():
    """Mock document service for testing."""
    service = AsyncMock()
    service.is_initialized = True
    return service


@pytest.fixture
def app(mock_ai_service, mock_audio_service, mock_document_service):
    """Create test FastAPI app with mocked services."""
    app = create_app()
    
    # Override dependencies with mocks
    from app.api import deps
    deps.ai_service = mock_ai_service
    deps.audio_service = mock_audio_service
    deps.document_service = mock_document_service
    
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return TestClient(app)


@pytest.fixture
async def async_client(app):
    """Create async test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac