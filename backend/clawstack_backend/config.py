from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


def _strip_wrapping_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        os.environ[key] = _strip_wrapping_quotes(value.strip())


def _normalize_url(value: str) -> str:
    value = value.strip()
    return value[:-1] if value.endswith("/") else value


def _split_csv(value: str) -> tuple[str, ...]:
    items = [item.strip() for item in value.split(",")]
    return tuple(item for item in items if item)


@dataclass(frozen=True)
class Settings:
    environment: str
    public_site_url: str
    public_api_url: str
    repo_url: str
    contact_email: str | None
    default_currency: str
    cors_origins: tuple[str, ...]
    intake_store_path: Path
    intake_webhook_url: str | None
    intake_timeout_seconds: float
    smtp_host: str | None
    smtp_port: int
    smtp_username: str | None
    smtp_password: str | None
    smtp_starttls: bool
    smtp_from_email: str | None
    smtp_to_email: str | None
    telegram_api_base: str
    telegram_bot_token: str | None
    telegram_chat_id: str | None
    admin_token: str | None
    intake_delivery_retries: int
    intake_delivery_backoff_seconds: float
    intake_rate_limit_count: int
    intake_rate_limit_window_seconds: int


def load_settings() -> Settings:
    project_root = Path(__file__).resolve().parents[2]
    env_file = Path(
        os.getenv("CLAWSTACK_ENV_FILE", str(project_root / "backend" / ".env"))
    )
    _load_env_file(env_file)
    default_site_url = "https://homgorn.github.io/clawstack"
    public_site_url = _normalize_url(
        os.getenv("CLAWSTACK_PUBLIC_SITE_URL", default_site_url)
    )
    public_api_url = _normalize_url(
        os.getenv("CLAWSTACK_PUBLIC_API_URL", f"{public_site_url}/api")
    )
    intake_store = os.getenv(
        "CLAWSTACK_INTAKE_STORE",
        str(project_root / "backend" / "data" / "intake.jsonl"),
    )
    cors_value = os.getenv("CLAWSTACK_CORS_ORIGINS", public_site_url)
    return Settings(
        environment=os.getenv("CLAWSTACK_ENV", "development"),
        public_site_url=public_site_url,
        public_api_url=public_api_url,
        repo_url=_normalize_url(
            os.getenv("CLAWSTACK_REPO_URL", "https://github.com/homgorn/clawstack")
        ),
        contact_email=os.getenv("CLAWSTACK_CONTACT_EMAIL"),
        default_currency=os.getenv("CLAWSTACK_DEFAULT_CURRENCY", "USD"),
        cors_origins=_split_csv(cors_value),
        intake_store_path=Path(intake_store),
        intake_webhook_url=os.getenv("CLAWSTACK_INTAKE_WEBHOOK_URL"),
        intake_timeout_seconds=float(
            os.getenv("CLAWSTACK_INTAKE_TIMEOUT_SECONDS", "10")
        ),
        smtp_host=os.getenv("CLAWSTACK_SMTP_HOST"),
        smtp_port=int(os.getenv("CLAWSTACK_SMTP_PORT", "587")),
        smtp_username=os.getenv("CLAWSTACK_SMTP_USERNAME"),
        smtp_password=os.getenv("CLAWSTACK_SMTP_PASSWORD"),
        smtp_starttls=os.getenv("CLAWSTACK_SMTP_STARTTLS", "true").lower()
        not in {"0", "false", "no"},
        smtp_from_email=os.getenv("CLAWSTACK_SMTP_FROM_EMAIL"),
        smtp_to_email=os.getenv("CLAWSTACK_SMTP_TO_EMAIL"),
        telegram_api_base=_normalize_url(
            os.getenv("CLAWSTACK_TELEGRAM_API_BASE", "https://api.telegram.org")
        ),
        telegram_bot_token=os.getenv("CLAWSTACK_TELEGRAM_BOT_TOKEN"),
        telegram_chat_id=os.getenv("CLAWSTACK_TELEGRAM_CHAT_ID"),
        admin_token=os.getenv("CLAWSTACK_ADMIN_TOKEN"),
        intake_delivery_retries=max(
            0, int(os.getenv("CLAWSTACK_INTAKE_DELIVERY_RETRIES", "0"))
        ),
        intake_delivery_backoff_seconds=float(
            os.getenv("CLAWSTACK_INTAKE_DELIVERY_BACKOFF_SECONDS", "1")
        ),
        intake_rate_limit_count=int(
            os.getenv("CLAWSTACK_INTAKE_RATE_LIMIT_COUNT", "10")
        ),
        intake_rate_limit_window_seconds=int(
            os.getenv("CLAWSTACK_INTAKE_RATE_LIMIT_WINDOW_SECONDS", "3600")
        ),
    )
