"""Executable entry point for the packaged Electron desktop backend."""

import argparse
from typing import Sequence

import uvicorn


def main(argv: Sequence[str] | None = None) -> None:
    """Run the FastAPI app on a local loopback port."""
    parser = argparse.ArgumentParser(description="Run the LLB desktop backend")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)

    uvicorn.run(
        "app.desktop_main:app",
        host=args.host,
        port=args.port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
