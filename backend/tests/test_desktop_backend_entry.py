"""Tests for the packaged desktop backend entry point."""

from unittest.mock import Mock

from desktop_backend_entry import main


def test_desktop_backend_entry_runs_uvicorn_on_loopback(monkeypatch):
    """Packaged backend accepts host and port arguments for Electron."""
    uvicorn_run = Mock()
    monkeypatch.setattr("desktop_backend_entry.uvicorn.run", uvicorn_run)

    main(["--port", "49152"])

    uvicorn_run.assert_called_once_with(
        "app.desktop_main:app",
        host="127.0.0.1",
        port=49152,
        log_level="info",
    )
