from __future__ import annotations

from email.message import EmailMessage
import json
import logging
import smtplib
import time
from typing import Any
from urllib.request import Request, urlopen

from .config import Settings


logger = logging.getLogger(__name__)


class DeliverySink:
    name: str

    def deliver(self, record: dict[str, Any]) -> None:  # pragma: no cover - interface
        raise NotImplementedError


class WebhookSink(DeliverySink):
    name = "webhook"

    def __init__(self, url: str, timeout_seconds: float) -> None:
        self.url = url
        self.timeout_seconds = timeout_seconds

    def deliver(self, record: dict[str, Any]) -> None:
        body = json.dumps(record, ensure_ascii=True).encode("utf-8")
        request = Request(
            self.url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=self.timeout_seconds):
            return


class SmtpSink(DeliverySink):
    name = "smtp"

    def __init__(
        self,
        host: str,
        port: int,
        username: str | None,
        password: str | None,
        starttls: bool,
        from_email: str,
        to_email: str,
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.starttls = starttls
        self.from_email = from_email
        self.to_email = to_email

    def deliver(self, record: dict[str, Any]) -> None:
        message = EmailMessage()
        message["Subject"] = f"[ClawStack] New {record['service_tier']} request"
        message["From"] = self.from_email
        message["To"] = self.to_email
        message.set_content(
            "\n".join(
                [
                    f"Lead ID: {record['lead_id']}",
                    f"Created: {record['created_at_utc']}",
                    f"Tier: {record['service_tier']}",
                    f"Name: {record['name']}",
                    f"Email: {record['email']}",
                    f"Company: {record.get('company') or '-'}",
                    f"Source: {record.get('source') or '-'}",
                    "",
                    "Message:",
                    str(record["message"]),
                ]
            )
        )
        with smtplib.SMTP(self.host, self.port, timeout=20) as smtp:
            if self.starttls:
                smtp.starttls()
            if self.username:
                smtp.login(self.username, self.password or "")
            smtp.send_message(message)


class TelegramSink(DeliverySink):
    name = "telegram"

    def __init__(
        self,
        api_base: str,
        bot_token: str,
        chat_id: str,
        timeout_seconds: float,
    ) -> None:
        self.api_base = api_base
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.timeout_seconds = timeout_seconds

    def deliver(self, record: dict[str, Any]) -> None:
        body = {
            "chat_id": self.chat_id,
            "text": _format_telegram_text(record),
            "disable_web_page_preview": True,
        }
        request = Request(
            f"{self.api_base}/bot{self.bot_token}/sendMessage",
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=self.timeout_seconds):
            return


def _format_telegram_text(record: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"ClawStack lead: {record['service_tier']}",
            f"Lead ID: {record['lead_id']}",
            f"Name: {record['name']}",
            f"Email: {record['email']}",
            f"Company: {record.get('company') or '-'}",
            f"Source: {record.get('source') or '-'}",
            "",
            "Message:",
            str(record["message"]),
        ]
    )


class IntakeDelivery:
    def __init__(self, settings: Settings) -> None:
        self.sinks: list[DeliverySink] = []
        self.max_retries = max(0, settings.intake_delivery_retries)
        self.backoff_seconds = max(0.0, settings.intake_delivery_backoff_seconds)
        if settings.intake_webhook_url:
            self.sinks.append(
                WebhookSink(
                    url=settings.intake_webhook_url,
                    timeout_seconds=settings.intake_timeout_seconds,
                )
            )
        if settings.smtp_host and settings.smtp_from_email and settings.smtp_to_email:
            self.sinks.append(
                SmtpSink(
                    host=settings.smtp_host,
                    port=settings.smtp_port,
                    username=settings.smtp_username,
                    password=settings.smtp_password,
                    starttls=settings.smtp_starttls,
                    from_email=settings.smtp_from_email,
                    to_email=settings.smtp_to_email,
                )
            )
        if settings.telegram_bot_token and settings.telegram_chat_id:
            self.sinks.append(
                TelegramSink(
                    api_base=settings.telegram_api_base,
                    bot_token=settings.telegram_bot_token,
                    chat_id=settings.telegram_chat_id,
                    timeout_seconds=settings.intake_timeout_seconds,
                )
            )

    def deliver(self, record: dict[str, Any]) -> list[str]:
        delivered: list[str] = []
        total_attempts = 1 + self.max_retries
        for sink in self.sinks:
            attempt = 1
            while attempt <= total_attempts:
                try:
                    sink.deliver(record)
                except Exception as exc:  # pragma: no cover - network side effects
                    if attempt < total_attempts:
                        logger.warning(
                            "intake delivery failed via %s (attempt %s/%s): %s",
                            sink.name,
                            attempt,
                            total_attempts,
                            exc,
                        )
                        if self.backoff_seconds:
                            time.sleep(self.backoff_seconds * (2 ** (attempt - 1)))
                        attempt += 1
                        continue
                    logger.exception(
                        "intake delivery failed via %s after %s attempts: %s",
                        sink.name,
                        total_attempts,
                        exc,
                    )
                    break
                if attempt > 1:
                    logger.info(
                        "intake delivery recovered via %s after %s attempts",
                        sink.name,
                        attempt,
                    )
                delivered.append(sink.name)
                break
        return delivered
