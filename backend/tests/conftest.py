"""Shared test fixtures for LLB backend tests."""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base_class import Base
from app.config import get_settings
from app.api import deps
from app.services.ai_service import AIService
from app.services.audio_service import AudioService
from app.services.document_service import DocumentService

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db):
    """Create database session for tests."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
async def services():
    """Initialize services for testing."""
    ai_service = AIService()
    audio_service = AudioService()
    document_service = DocumentService()
    
    # Initialize services
    await ai_service.initialize()
    await audio_service.initialize()
    await document_service.initialize()
    
    # Set services in deps module
    deps.set_services(ai_service, audio_service, document_service)
    
    yield {
        "ai_service": ai_service,
        "audio_service": audio_service,
        "document_service": document_service
    }
    
    # Cleanup
    await ai_service.cleanup()
    await audio_service.cleanup()
    await document_service.cleanup()


@pytest.fixture(scope="module")
def client(services):
    """Create test client with initialized services."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def settings():
    """Get test settings."""
    return get_settings()
