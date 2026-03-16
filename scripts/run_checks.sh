#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

log() {
  printf "%s\n" "$*"
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    log "Missing command: $1"
    exit 1
  }
}

require_cmd python

log "Running starter config lint..."
python "${ROOT}/scripts/check_configs.py"

log "Running backend tests (pytest)..."
if python -m pytest --version >/dev/null 2>&1; then
  python -m pytest "${ROOT}/backend/tests"
else
  log "pytest not installed. Install dev deps with: python -m pip install -e \".[dev]\""
  exit 1
fi

log "All checks passed."
