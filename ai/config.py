"""
Configuration settings for AI models and processors in the LLB application.
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR / "cache"
TEMP_DIR = BASE_DIR / "temp"

# Create directories if they don't exist
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# AI Provider Configuration
# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Anthropic Claude
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-haiku-20240307")

# Google Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

# Ollama
OLLAMA_ENABLED = os.getenv("OLLAMA_ENABLED", "false").lower() == "true"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

# Chrome Web AI
CHROME_WEB_AI_ENABLED = os.getenv("CHROME_WEB_AI_ENABLED", "false").lower() == "true"

# Voice processing (Whisper)
WHISPER_MODEL = "base"  # Options: "tiny", "base", "small", "medium", "large"

# Language detection
SUPPORTED_LANGUAGES = ["en", "zh-CN"]
DEFAULT_LANGUAGE = "en"

# Document processing
MAX_PDF_PAGES = 50
MAX_PDF_SIZE_MB = 20

# Performance settings
MAX_TOKENS = 150
TEMPERATURE = 0.7