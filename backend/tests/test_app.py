from dataclasses import replace

from fastapi.testclient import TestClient

import clawstack_backend.app as app_module
from clawstack_backend.protection import IntakeRateLimiter


client = TestClient(app_module.app)


def test_root_serves_html() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "ClawStack" in response.text
    assert 'content="https://homgorn.github.io/clawstack/"' in response.text


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_site_config_contains_offers() -> None:
    response = client.get("/v1/site-config")
    assert response.status_code == 200
    body = response.json()
    assert body["site_name"] == "ClawStack"
    assert len(body["offers"]) == 3
    assert body["canonical_url"] == "https://homgorn.github.io/clawstack/"
    assert body["public_api_base"] == "/clawstack/api"


def test_prefixed_site_config_route() -> None:
    response = client.get("/api/v1/site-config")
    assert response.status_code == 200
    assert response.json()["public_api_url"]


def test_dynamic_seo_files() -> None:
    robots = client.get("/robots.txt")
    sitemap = client.get("/sitemap.xml")
    manifest = client.get("/site.webmanifest")
    assert robots.status_code == 200
    assert "Sitemap:" in robots.text
    assert sitemap.status_code == 200
    assert "<urlset" in sitemap.text
    assert manifest.status_code == 200
    assert manifest.json()["name"] == "ClawStack"


def test_intake_accepts_valid_payload() -> None:
    response = client.post(
        "/v1/intake",
        json={
            "service_tier": "pro-setup",
            "name": "Alex Test",
            "email": "alex@example.com",
            "message": "Need setup help for a production-ready OpenClaw deployment.",
        },
    )
    assert response.status_code == 202
    assert response.json()["status"] == "accepted"
    assert response.json()["delivery_channels"] == []


def test_intake_honeypot_is_suppressed() -> None:
    response = client.post(
        "/api/v1/intake",
        json={
            "service_tier": "managed",
            "name": "Spam Bot",
            "email": "bot@example.com",
            "website": "https://spam.invalid",
            "message": "This should be suppressed.",
        },
    )
    assert response.status_code == 202
    assert response.json()["lead_id"] == "suppressed"


def test_intake_rate_limit(monkeypatch) -> None:
    monkeypatch.setattr(app_module, "rate_limiter", IntakeRateLimiter(1, 3600))
    first = client.post(
        "/api/v1/intake",
        json={
            "service_tier": "custom",
            "name": "Alex Test",
            "email": "alex@example.com",
            "message": "First request should pass.",
        },
    )
    second = client.post(
        "/api/v1/intake",
        json={
            "service_tier": "custom",
            "name": "Alex Test",
            "email": "alex@example.com",
            "message": "Second request should be limited.",
        },
    )
    assert first.status_code == 202
    assert second.status_code == 429
    assert second.headers["Retry-After"]
    monkeypatch.setattr(
        app_module,
        "rate_limiter",
        IntakeRateLimiter(
            app_module.settings.intake_rate_limit_count,
            app_module.settings.intake_rate_limit_window_seconds,
        ),
    )


def test_leads_endpoint_requires_admin_token() -> None:
    response = client.get("/api/v1/leads")
    assert response.status_code in {401, 503}


def test_leads_endpoint_with_admin_token(monkeypatch) -> None:
    monkeypatch.setattr(
        app_module,
        "settings",
        replace(app_module.settings, admin_token="secret-token"),
    )
    response = client.get("/api/v1/leads", headers={"X-Admin-Token": "secret-token"})
    assert response.status_code == 200
    assert "leads" in response.json()
    monkeypatch.setattr(app_module, "settings", replace(app_module.settings, admin_token=None))
