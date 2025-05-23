"""
Configuration settings for AI models and processors in the LLB application.
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models" / "downloaded"
CACHE_DIR = BASE_DIR / "cache"
TEMP_DIR = BASE_DIR / "temp"

# Create directories if they don't exist
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Gemma model configuration
GEMMA_MODEL_ID = str(MODELS_DIR / "gemma-3-1b")  # Local path to downloaded model

# Model quantization
USE_4BIT_QUANTIZATION = True  # For systems with limited VRAM
USE_8BIT_QUANTIZATION = False

# Voice processing (Whisper)
WHISPER_MODEL = "base"  # Options: "tiny", "base", "small", "medium", "large"

# Language detection
SUPPORTED_LANGUAGES = ["en", "zh-CN"]
DEFAULT_LANGUAGE = "en"

# Document processing
MAX_PDF_PAGES = 50
MAX_PDF_SIZE_MB = 20

# System resources
MAX_GPU_MEMORY = 8  # in GB
USE_CPU_OFFLOADING = True
NUM_CPU_THREADS = 4

# Performance settings
ENABLE_FLASH_ATTENTION = True
LOW_CPU_MEM_USAGE = True 