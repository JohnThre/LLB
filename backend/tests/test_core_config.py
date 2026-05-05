"""
Tests for core configuration.
"""

import pytest
from app.core.config import Settings


def test_settings_defaults():
    """Test default settings values."""
    settings = Settings()
    
    assert settings.PROJECT_NAME == "LLB API"
    assert settings.VERSION == "0.1.0"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.LOG_LEVEL == "INFO"
    assert settings.TEMPERATURE == 0.7
    assert settings.MAX_LENGTH == 2048


def test_cors_origins_string():
    """Test CORS origins from string."""
    settings = Settings(CORS_ORIGINS="http://localhost:3000,http://localhost:3001")
    assert len(settings.CORS_ORIGINS) == 2


def test_cors_origins_list():
    """Test CORS origins from list."""
    origins = ["http://localhost:3000", "http://localhost:3001"]
    settings = Settings(CORS_ORIGINS=origins)
    # Convert URLs to strings for comparison
    cors_origins_str = [str(origin) for origin in settings.CORS_ORIGINS]
    assert cors_origins_str == [origin + "/" for origin in origins]  # URLs add trailing slash


def test_database_uri_assembly():
    """Test database URI assembly."""
    settings = Settings(
        POSTGRES_SERVER="localhost",
        POSTGRES_USER="test",
        POSTGRES_PASSWORD="password",
        POSTGRES_DB="testdb"
    )
    expected = "postgresql://test:password@localhost/testdb"
    assert settings.SQLALCHEMY_DATABASE_URI == expected


def test_allowed_extensions():
    """Test allowed file extensions."""
    settings = Settings()
    
    assert ".pdf" in settings.ALLOWED_EXTENSIONS
    assert ".mp3" in settings.ALLOWED_EXTENSIONS
    assert ".jpg" in settings.ALLOWED_EXTENSIONS
    assert ".txt" in settings.ALLOWED_EXTENSIONS


def test_upload_settings():
    """Test upload-related settings."""
    settings = Settings()
    
    assert settings.MAX_UPLOAD_SIZE == 50 * 1024 * 1024  # 50MB
    assert settings.UPLOAD_DIR.name == "uploads"