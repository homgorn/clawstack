#!/usr/bin/env bash
set -euo pipefail

SCRIPT_NAME="$(basename "$0")"
CONFIG_DIR="${HOME}/.openclaw"
CONFIG_FILE_PRIMARY="${CONFIG_DIR}/openclaw.json"
CONFIG_FILE_FALLBACK="${CONFIG_DIR}/config.json"

usage() {
  cat <<EOF
Usage: ${SCRIPT_NAME} <command>

Commands:
  install    Install the latest OpenClaw CLI via npm
  upgrade    Upgrade the OpenClaw CLI via npm
  doctor     Run OpenClaw doctor fixes
  audit      Run OpenClaw security audit
  validate   Validate the active OpenClaw config
  bootstrap  Run install + doctor + audit + validate
  help       Show this help

Notes:
  - Recommended Node.js version: >= 22.12.0
  - Config is expected at ${CONFIG_FILE_PRIMARY}
    (or ${CONFIG_FILE_FALLBACK} if you use that name)
  - Optional onboarding: openclaw onboard --install-daemon
EOF
}

log() {
  printf "%s\n" "$*"
}

fail() {
  printf "Error: %s\n" "$*" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing command: $1"
}

show_node_version() {
  if command -v node >/dev/null 2>&1; then
    log "Node version: $(node --version)"
  else
    log "Node not found. Install Node.js >= 22.12.0 first."
  fi
}

check_config() {
  if [[ -f "${CONFIG_FILE_PRIMARY}" || -f "${CONFIG_FILE_FALLBACK}" ]]; then
    return 0
  fi
  log "No config found at:"
  log "  - ${CONFIG_FILE_PRIMARY}"
  log "  - ${CONFIG_FILE_FALLBACK}"
  log "Copy a starter config from configs/ before validating."
  return 1
}

cmd="${1:-help}"

case "${cmd}" in
  help|-h|--help)
    usage
    ;;
  install)
    show_node_version
    require_cmd npm
    npm install -g openclaw@latest
    if command -v openclaw >/dev/null 2>&1; then
      openclaw --version
    fi
    ;;
  upgrade)
    show_node_version
    require_cmd npm
    npm install -g openclaw@latest
    if command -v openclaw >/dev/null 2>&1; then
      openclaw --version
    fi
    ;;
  doctor)
    require_cmd openclaw
    openclaw doctor --fix
    ;;
  audit)
    require_cmd openclaw
    openclaw security audit --deep
    ;;
  validate)
    require_cmd openclaw
    check_config
    openclaw config validate --json
    ;;
  bootstrap)
    "$0" install
    "$0" doctor
    "$0" audit
    "$0" validate
    ;;
  *)
    usage
    exit 1
    ;;
esac
