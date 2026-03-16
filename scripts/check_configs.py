#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_DIR = ROOT / "configs"
REQUIRED_TOP_KEYS = ("gateway", "env", "agents", "skills")


def _error(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"{path.as_posix()}: {message}")


def _load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _expect_dict(errors: list[str], path: Path, value: object, label: str) -> dict | None:
    if not isinstance(value, dict):
        _error(errors, path, f"{label} must be an object")
        return None
    return value


def _expect_list(errors: list[str], path: Path, value: object, label: str) -> list | None:
    if not isinstance(value, list):
        _error(errors, path, f"{label} must be a list")
        return None
    return value


def _check_gateway(errors: list[str], path: Path, gateway: dict) -> None:
    bind = gateway.get("bind")
    if bind != "loopback":
        _error(errors, path, "gateway.bind must be 'loopback'")
    port = gateway.get("port")
    if not isinstance(port, int) or not (1 <= port <= 65535):
        _error(errors, path, "gateway.port must be an integer between 1 and 65535")
    auth = gateway.get("auth")
    auth_obj = _expect_dict(errors, path, auth, "gateway.auth")
    if not auth_obj:
        return
    if auth_obj.get("required") is not True:
        _error(errors, path, "gateway.auth.required must be true")
    secret = auth_obj.get("secret")
    if not isinstance(secret, str) or not secret.strip():
        _error(errors, path, "gateway.auth.secret must be a non-empty string")
    elif "OPENCLAW_GATEWAY_SECRET" not in secret:
        _error(errors, path, "gateway.auth.secret should reference ${OPENCLAW_GATEWAY_SECRET}")


def _check_env(errors: list[str], path: Path, env: dict) -> None:
    env_file = env.get("file")
    if not isinstance(env_file, str) or not env_file.strip():
        _error(errors, path, "env.file must be a non-empty string")
    elif ".openclaw/.env" not in env_file:
        _error(errors, path, "env.file should point to ~/.openclaw/.env")


def _check_agents(errors: list[str], path: Path, agents: dict) -> None:
    defaults = agents.get("defaults")
    defaults_obj = _expect_dict(errors, path, defaults, "agents.defaults")
    if not defaults_obj:
        return

    model = defaults_obj.get("model")
    model_obj = _expect_dict(errors, path, model, "agents.defaults.model")
    if model_obj:
        primary = model_obj.get("primary")
        if not isinstance(primary, str) or not primary.strip():
            _error(errors, path, "agents.defaults.model.primary must be a non-empty string")
        fallbacks = model_obj.get("fallbacks")
        if not isinstance(fallbacks, list) or not fallbacks:
            _error(errors, path, "agents.defaults.model.fallbacks must be a non-empty list")

    heartbeat = defaults_obj.get("heartbeat")
    heartbeat_obj = _expect_dict(errors, path, heartbeat, "agents.defaults.heartbeat")
    if heartbeat_obj:
        if not isinstance(heartbeat_obj.get("model"), str) or not heartbeat_obj.get("model"):
            _error(errors, path, "agents.defaults.heartbeat.model must be a non-empty string")
        interval = heartbeat_obj.get("interval")
        if not isinstance(interval, int) or interval <= 0:
            _error(errors, path, "agents.defaults.heartbeat.interval must be a positive integer")
        if heartbeat_obj.get("directPolicy") != "block":
            _error(errors, path, "agents.defaults.heartbeat.directPolicy must be 'block'")

    sandbox = defaults_obj.get("sandbox")
    if sandbox is not None:
        sandbox_obj = _expect_dict(errors, path, sandbox, "agents.defaults.sandbox")
        if sandbox_obj:
            mode = sandbox_obj.get("mode")
            if not isinstance(mode, str) or not mode:
                _error(errors, path, "agents.defaults.sandbox.mode must be a non-empty string")
            if sandbox_obj.get("workspaceAccess") != "none":
                _error(errors, path, "agents.defaults.sandbox.workspaceAccess must be 'none'")

    agent_list = agents.get("list")
    list_obj = _expect_list(errors, path, agent_list, "agents.list")
    if not list_obj:
        return
    has_default = False
    for index, item in enumerate(list_obj):
        if not isinstance(item, dict):
            _error(errors, path, f"agents.list[{index}] must be an object")
            continue
        if not isinstance(item.get("id"), str) or not item.get("id"):
            _error(errors, path, f"agents.list[{index}].id must be a non-empty string")
        workspace = item.get("workspace")
        if not isinstance(workspace, str) or not workspace:
            _error(errors, path, f"agents.list[{index}].workspace must be a non-empty string")
        elif ".openclaw/workspace" not in workspace:
            _error(errors, path, f"agents.list[{index}].workspace should point to ~/.openclaw/workspace")
        if item.get("default") is True:
            has_default = True
    if not has_default:
        _error(errors, path, "agents.list must include one default agent")


def _check_skills(errors: list[str], path: Path, skills: dict) -> None:
    for key in ("autoLoad", "sandboxFirstRun"):
        if skills.get(key) is not True:
            _error(errors, path, f"skills.{key} must be true")
    directory = skills.get("directory")
    if not isinstance(directory, str) or not directory.strip():
        _error(errors, path, "skills.directory must be a non-empty string")
    elif "workspace/skills" not in directory.replace("\\", "/"):
        _error(errors, path, "skills.directory should point to ~/.openclaw/workspace/skills")


def _is_repo_config(path: Path) -> bool:
    try:
        path.resolve().relative_to(DEFAULT_CONFIG_DIR.resolve())
    except ValueError:
        return False
    return True


def _check_config(path: Path, data: dict, errors: list[str]) -> None:
    if _is_repo_config(path):
        schema = data.get("$schema")
        if not isinstance(schema, str) or not schema.strip():
            _error(errors, path, "missing $schema reference")
        elif "openclaw.schema.json" not in schema:
            _error(errors, path, "$schema should reference ./openclaw.schema.json")
    for key in REQUIRED_TOP_KEYS:
        if key not in data:
            _error(errors, path, f"missing top-level key '{key}'")
    gateway = _expect_dict(errors, path, data.get("gateway"), "gateway")
    env = _expect_dict(errors, path, data.get("env"), "env")
    agents = _expect_dict(errors, path, data.get("agents"), "agents")
    skills = _expect_dict(errors, path, data.get("skills"), "skills")

    if gateway:
        _check_gateway(errors, path, gateway)
    if env:
        _check_env(errors, path, env)
    if agents:
        _check_agents(errors, path, agents)
    if skills:
        _check_skills(errors, path, skills)


def _resolve_targets(args: list[str]) -> list[Path]:
    if args:
        return [Path(arg).expanduser() for arg in args]
    return sorted(
        path
        for path in DEFAULT_CONFIG_DIR.glob("*.json")
        if path.name != "openclaw.schema.json"
    )


def main(argv: list[str]) -> int:
    args = [arg for arg in argv[1:] if not arg.startswith("-")]
    targets = _resolve_targets(args)
    if not targets:
        print("No config files found.")
        return 1

    errors: list[str] = []
    for path in targets:
        if not path.exists():
            _error(errors, path, "file does not exist")
            continue
        data = _load_json(path)
        if not isinstance(data, dict):
            _error(errors, path, "invalid JSON or not an object")
            continue
        _check_config(path, data, errors)

    if errors:
        print("Config lint failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Config lint passed ({len(targets)} file(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
