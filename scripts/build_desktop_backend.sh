#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"$ROOT_DIR/scripts/ensure_backend_env.sh" backend/requirements/desktop.txt >/dev/null

cd "$ROOT_DIR/backend"
./llb-env/bin/python -m PyInstaller --clean --noconfirm llb_backend.spec
