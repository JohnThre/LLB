#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

BACKEND_PYTHON="$("$ROOT_DIR/scripts/ensure_backend_env.sh" backend/requirements/desktop.txt)"

cd "$ROOT_DIR/backend"
"$BACKEND_PYTHON" -m PyInstaller --clean --noconfirm llb_backend.spec
