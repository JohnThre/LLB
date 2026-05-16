#!/bin/sh

set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
REQ_FILE="${1:-backend/requirements/dev.txt}"
VENV_DIR="${BACKEND_VENV:-$ROOT_DIR/backend/llb-env}"
STAMP_FILE="$VENV_DIR/.requirements.stamp"

find_python() {
  if [ -n "${PYTHON:-}" ]; then
    printf '%s\n' "$PYTHON"
    return 0
  fi

  for candidate in python3.11 python3.12 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      if "$candidate" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 11) else 1)
PY
      then
        command -v "$candidate"
        return 0
      fi
    fi
  done

  return 1
}

PYTHON_BIN=$(find_python) || {
  echo "Python 3.11+ is required. Install Python 3.11 or set PYTHON=/path/to/python." >&2
  exit 1
}

create_venv() {
  if command -v uv >/dev/null 2>&1; then
    uv venv --clear --seed --python "$PYTHON_BIN" "$VENV_DIR" >&2
  else
    "$PYTHON_BIN" -m venv --clear "$VENV_DIR" >&2
  fi
}

venv_python() {
  if [ -x "$VENV_DIR/bin/python" ]; then
    printf '%s\n' "$VENV_DIR/bin/python"
    return 0
  fi

  if [ -x "$VENV_DIR/Scripts/python.exe" ]; then
    printf '%s\n' "$VENV_DIR/Scripts/python.exe"
    return 0
  fi

  return 1
}

install_requirements() {
  VENV_PYTHON=$(venv_python) || {
    echo "Python executable is unavailable in $VENV_DIR." >&2
    exit 1
  }

  if "$VENV_PYTHON" -m pip --version >/dev/null 2>&1; then
    PIP_NO_CACHE_DIR=1 "$VENV_PYTHON" -m pip install --disable-pip-version-check -q -r "$ROOT_DIR/$REQ_FILE" >&2
  elif command -v uv >/dev/null 2>&1; then
    uv pip install -q --python "$VENV_PYTHON" -r "$ROOT_DIR/$REQ_FILE" >&2
  else
    echo "pip is unavailable in $VENV_DIR and uv is not installed." >&2
    exit 1
  fi
}

requirements_fingerprint() {
  if command -v shasum >/dev/null 2>&1; then
    (
      for file in "$ROOT_DIR/backend/requirements.txt" "$ROOT_DIR/backend/requirements/"*.txt; do
        [ -f "$file" ] && shasum "$file"
      done
    ) | shasum | awk '{print $1}'
  else
    (
      for file in "$ROOT_DIR/backend/requirements.txt" "$ROOT_DIR/backend/requirements/"*.txt; do
        [ -f "$file" ] && cksum "$file"
      done
    ) | cksum | awk '{print $1}'
  fi
}

CURRENT_STAMP="$REQ_FILE:$(requirements_fingerprint)"

if ! VENV_PYTHON=$(venv_python) || ! "$VENV_PYTHON" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 11) else 1)
PY
then
  echo "[INFO] Creating backend virtual environment at $VENV_DIR" >&2
  create_venv
elif [ ! -f "$STAMP_FILE" ] || [ "$(cat "$STAMP_FILE")" != "$CURRENT_STAMP" ]; then
  echo "[INFO] Recreating backend virtual environment after requirements change" >&2
  create_venv
fi

install_requirements
printf '%s\n' "$CURRENT_STAMP" > "$STAMP_FILE"
venv_python
