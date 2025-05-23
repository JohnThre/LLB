from pathlib import Path
from typing import List

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "LLB API"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Local AI-Driven Education Web Application API"
    API_V1_STR: str = "/api/v1"

    # CORS Configuration
    CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "llb"
    SQLALCHEMY_DATABASE_URI: str | None = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v, info):
        if isinstance(v, str):
            return v
        values = info.data if info else {}
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"

    # AI Model Settings
    MODEL_PATH: str = "models/gemma-2b-it"
    MODEL_DEVICE: str = "cuda"  # or "cpu"
    MAX_LENGTH: int = 2048
    TEMPERATURE: float = 0.7

    # Storage Settings
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: set[str] = {
        # Audio
        ".mp3",
        ".wav",
        ".ogg",
        ".m4a",
        # Documents
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        # Images
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
    }

    model_config = {"case_sensitive": True, "env_file": ".env"}


settings = Settings()
