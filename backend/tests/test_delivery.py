from __future__ import annotations

import json

from clawstack_backend.config import Settings
from clawstack_backend.delivery import IntakeDelivery, TelegramSink, _format_telegram_text


def _settings(**overrides: object) -> Settings:
    base = {
        "environment": "test",
        "public_site_url": "https://example.com",
        "public_api_url": "https://example.com/api",
        "repo_url": "https://github.com/homgorn/clawstack",
        "contact_email": "hello@example.com",
        "default_currency": "USD",
        "cors_origins": ("https://example.com",),
        "intake_store_path": __import__("pathlib").Path("backend/data/test-intake.jsonl"),
        "intake_webhook_url": None,
        "intake_timeout_seconds": 10.0,
        "smtp_host": None,
        "smtp_port": 587,
        "smtp_username": None,
        "smtp_password": None,
        "smtp_starttls": True,
        "smtp_from_email": None,
        "smtp_to_email": None,
        "telegram_api_base": "https://api.telegram.org",
        "telegram_bot_token": None,
        "telegram_chat_id": None,
        "admin_token": None,
        "intake_delivery_retries": 0,
        "intake_delivery_backoff_seconds": 1.0,
        "intake_rate_limit_count": 10,
        "intake_rate_limit_window_seconds": 3600,
    }
    base.update(overrides)
    return Settings(**base)


def test_format_telegram_text() -> None:
    text = _format_telegram_text(
        {
            "lead_id": "abc123",
            "service_tier": "managed",
            "name": "Alex Test",
            "email": "alex@example.com",
            "company": "Claw Labs",
            "source": "https://example.com/",
            "message": "Need managed support.",
        }
    )
    assert "ClawStack lead: managed" in text
    assert "Alex Test" in text
    assert "Need managed support." in text


def test_telegram_sink_posts_to_bot_api(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class DummyResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_urlopen(request, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        captured["body"] = json.loads(request.data.decode("utf-8"))
        return DummyResponse()

    monkeypatch.setattr("clawstack_backend.delivery.urlopen", fake_urlopen)

    sink = TelegramSink(
        api_base="https://api.telegram.org",
        bot_token="123:token",
        chat_id="42",
        timeout_seconds=7.5,
    )
    sink.deliver(
        {
            "lead_id": "abc123",
            "service_tier": "pro-setup",
            "name": "Alex Test",
            "email": "alex@example.com",
            "company": None,
            "source": "https://example.com/",
            "message": "Need setup help.",
        }
    )

    assert captured["url"] == "https://api.telegram.org/bot123:token/sendMessage"
    assert captured["timeout"] == 7.5
    assert captured["body"]["chat_id"] == "42"
    assert "Need setup help." in captured["body"]["text"]


def test_intake_delivery_enables_telegram_sink() -> None:
    delivery = IntakeDelivery(
        _settings(
            telegram_bot_token="123:token",
            telegram_chat_id="42",
        )
    )
    assert any(sink.name == "telegram" for sink in delivery.sinks)


def test_intake_delivery_retries(monkeypatch) -> None:
    calls = {"count": 0}

    class FlakySink:
        name = "flaky"

        def deliver(self, record: dict[str, object]) -> None:
            calls["count"] += 1
            if calls["count"] < 2:
                raise RuntimeError("boom")

    monkeypatch.setattr("clawstack_backend.delivery.time.sleep", lambda _: None)

    delivery = IntakeDelivery(
        _settings(
            intake_delivery_retries=1,
            intake_delivery_backoff_seconds=0.01,
        )
    )
    delivery.sinks = [FlakySink()]
    delivered = delivery.deliver(
        {
            "lead_id": "abc123",
            "service_tier": "managed",
            "name": "Alex Test",
            "email": "alex@example.com",
            "company": None,
            "source": "https://example.com/",
            "message": "Need managed support.",
        }
    )

    assert delivered == ["flaky"]
    assert calls["count"] == 2
