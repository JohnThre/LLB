#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <artifact-directory>" >&2
  exit 2
fi

ARTIFACT_DIR="$1"

if [[ ! -d "$ARTIFACT_DIR" ]]; then
  echo "Artifact directory not found: $ARTIFACT_DIR" >&2
  exit 2
fi

find "$ARTIFACT_DIR" -maxdepth 1 -type f \
  ! -name ".*" \
  ! -name "*.asc" \
  ! -name "*.sha256" \
  -print0 |
while IFS= read -r -d '' artifact; do
  case "$artifact" in
    *.AppImage|*.deb|*.dmg|*.exe|*.msi|*.pkg|*.rpm|*.tar.gz|*.zip) ;;
    *) continue ;;
  esac

  shasum -a 256 "$artifact" > "$artifact.sha256"
  gpg --yes --armor --detach-sign "$artifact"
  gpg --yes --armor --detach-sign "$artifact.sha256"
done
