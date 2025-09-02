import os
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "LLB Sexual Health Education API"
    debug: bool = False
    host: str = "127.0.0.1"
    port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000"]
    
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    ollama_enabled: bool = False
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    
    database_url: str = "sqlite:///./llb.db"
    
    model_config = {
        "env_file": ".env",
        "env_prefix": "LLB_",
    }

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()