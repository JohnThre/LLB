"""Tests for the lean Electron desktop FastAPI app."""

import json
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient


def test_desktop_app_exposes_health_and_provider_catalog():
    """Desktop app includes the local health and provider catalog endpoints."""
    from app.desktop_main import app

    client = TestClient(app)

    health_response = client.get("/api/v1/health")
    providers_response = client.get("/api/v1/ai/providers")

    assert health_response.status_code == 200
    assert health_response.json()["status"] == "ok"
    assert providers_response.status_code == 200
    assert "providers" in providers_response.json()


def test_desktop_app_import_does_not_load_local_ml_stack():
    """Importing the desktop app must not pull heavyweight local ML modules."""
    script = """
import importlib
import json
import sys

importlib.import_module("app.desktop_main")
heavy_modules = [
    "bitsandbytes",
    "librosa",
    "torch",
    "torchaudio",
    "transformers",
    "whisper",
]
loaded = [module for module in heavy_modules if module in sys.modules]
print(json.dumps(loaded))
raise SystemExit(1 if loaded else 0)
"""

    result = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == []


def test_desktop_requirements_exclude_local_ml_stack():
    """Desktop packaging requirements stay limited to the lean backend runtime."""
    requirements = (
        Path(__file__).resolve().parents[1] / "requirements" / "desktop.txt"
    ).read_text()

    excluded = [
        "base.txt",
        "bitsandbytes",
        "librosa",
        "openai-whisper",
        "torch",
        "torchaudio",
        "transformers",
    ]

    for package_name in excluded:
        assert package_name not in requirements
