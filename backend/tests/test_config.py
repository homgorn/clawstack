from __future__ import annotations

from pathlib import Path
import shutil
from uuid import uuid4

from clawstack_backend.config import load_settings


def _test_dir() -> Path:
    path = Path("backend/tests/_tmp") / uuid4().hex
    path.mkdir(parents=True, exist_ok=True)
    return path


def test_load_settings_reads_env_file(monkeypatch) -> None:
    tmp_dir = _test_dir()
    env_file = tmp_dir / ".env"
    env_file.write_text(
        "\n".join(
            [
                "CLAWSTACK_PUBLIC_SITE_URL=https://clawstack.example",
                "CLAWSTACK_CONTACT_EMAIL=ops@example.com",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("CLAWSTACK_ENV_FILE", str(env_file))
    monkeypatch.delenv("CLAWSTACK_PUBLIC_SITE_URL", raising=False)
    monkeypatch.delenv("CLAWSTACK_CONTACT_EMAIL", raising=False)

    settings = load_settings()

    assert settings.public_site_url == "https://clawstack.example"
    assert settings.contact_email == "ops@example.com"
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_load_settings_does_not_override_real_env(monkeypatch) -> None:
    tmp_dir = _test_dir()
    env_file = tmp_dir / ".env"
    env_file.write_text(
        "CLAWSTACK_PUBLIC_SITE_URL=https://from-file.example\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CLAWSTACK_ENV_FILE", str(env_file))
    monkeypatch.setenv("CLAWSTACK_PUBLIC_SITE_URL", "https://from-env.example")

    settings = load_settings()

    assert settings.public_site_url == "https://from-env.example"
    shutil.rmtree(tmp_dir, ignore_errors=True)
