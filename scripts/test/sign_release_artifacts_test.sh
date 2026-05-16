#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TMP_DIR="$(mktemp -d)"
BIN_DIR="$TMP_DIR/bin"
ARTIFACT_DIR="$TMP_DIR/artifacts"
LOG_FILE="$TMP_DIR/gpg.log"

mkdir -p "$BIN_DIR" "$ARTIFACT_DIR"

cat > "$BIN_DIR/gpg" <<'GPG'
#!/usr/bin/env bash
set -euo pipefail
echo "$*" >> "$GPG_LOG_FILE"
artifact="${@: -1}"
touch "$artifact.asc"
GPG
chmod +x "$BIN_DIR/gpg"

touch \
  "$ARTIFACT_DIR/LLB.dmg" \
  "$ARTIFACT_DIR/LLB.AppImage" \
  "$ARTIFACT_DIR/.DS_Store" \
  "$ARTIFACT_DIR/builder-debug.yml"

PATH="$BIN_DIR:$PATH" GPG_LOG_FILE="$LOG_FILE" \
  "$ROOT_DIR/scripts/sign_release_artifacts.sh" "$ARTIFACT_DIR"

test -f "$ARTIFACT_DIR/LLB.dmg.asc"
test -f "$ARTIFACT_DIR/LLB.dmg.sha256"
test -f "$ARTIFACT_DIR/LLB.dmg.sha256.asc"
test -f "$ARTIFACT_DIR/LLB.AppImage.asc"
test -f "$ARTIFACT_DIR/LLB.AppImage.sha256"
test -f "$ARTIFACT_DIR/LLB.AppImage.sha256.asc"
test ! -f "$ARTIFACT_DIR/.DS_Store.asc"
test ! -f "$ARTIFACT_DIR/.DS_Store.sha256"
test ! -f "$ARTIFACT_DIR/builder-debug.yml.asc"
test ! -f "$ARTIFACT_DIR/builder-debug.yml.sha256"

grep -q -- "--detach-sign" "$LOG_FILE"
grep -q -- "--armor" "$LOG_FILE"

rm -rf "$TMP_DIR"
