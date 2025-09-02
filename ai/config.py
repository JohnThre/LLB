import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR / "cache"
TEMP_DIR = BASE_DIR / "temp"

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "false").lower() == "true"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

SUPPORTED_LANGUAGES = ["en", "zh-CN"]
DEFAULT_LANGUAGE = "en"