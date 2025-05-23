"""
Configuration management for LLB Backend
Handles environment variables and application settings
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    app_name: str = "LLB Sexual Health Education API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = False
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # AI Models
    model_cache_dir: str = "../ai/cache"
    model_temp_dir: str = "../ai/temp"
    gemma_model_path: str = "../ai/models/gemma"
    whisper_model_path: str = "../ai/models/whisper"
    
    # File Upload
    upload_dir: str = "uploads"
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_file_types: List[str] = [
        "application/pdf",
        "audio/wav",
        "audio/mp3",
        "audio/mpeg"
    ]
    
    # Logging
    log_level: str = "INFO"
    log_dir: str = "logs"
    log_file: str = "llb_backend.log"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = "sqlite:///./llb.db"
    
    # Language Support
    supported_languages: List[str] = [
        "zh-CN",  # Simplified Chinese
        "zh-CN-henan",  # Henan Dialect
        "en-US",  # American English
        "en-GB"   # British English
    ]
    
    # Safety Settings
    default_safety_level: str = "standard"
    content_filter_enabled: bool = True
    
    @validator("cors_origins", pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from environment variable."""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("supported_languages", pre=True)
    def assemble_languages(cls, v):
        """Parse supported languages from environment variable."""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        env_prefix = "LLB_"


class DevelopmentSettings(Settings):
    """Development environment settings."""
    debug: bool = True
    reload: bool = True
    log_level: str = "DEBUG"


class ProductionSettings(Settings):
    """Production environment settings."""
    debug: bool = False
    reload: bool = False
    log_level: str = "WARNING"


class TestingSettings(Settings):
    """Testing environment settings."""
    debug: bool = True
    database_url: str = "sqlite:///./test_llb.db"
    log_level: str = "DEBUG"


@lru_cache()
def get_settings() -> Settings:
    """Get application settings based on environment."""
    environment = os.getenv("LLB_ENVIRONMENT", "development").lower()
    
    if environment == "production":
        return ProductionSettings()
    elif environment == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# Global settings instance
settings = get_settings() 