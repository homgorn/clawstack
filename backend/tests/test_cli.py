from __future__ import annotations

import json
from pathlib import Path
import shutil
from uuid import uuid4

from clawstack_backend.cli import main


def _test_dir() -> Path:
    path = Path("backend/tests/_tmp") / uuid4().hex
    path.mkdir(parents=True, exist_ok=True)
    return path


def test_cli_leads_json(monkeypatch, capsys) -> None:
    tmp_dir = _test_dir()
    leads_path = tmp_dir / "intake.jsonl"
    leads_path.write_text(
        json.dumps(
            {
                "lead_id": "lead-1",
                "created_at_utc": "2026-03-09T08:00:00+00:00",
                "service_tier": "pro-setup",
                "name": "Alex Test",
                "email": "alex@example.com",
                "company": None,
                "source": None,
                "website": None,
                "message": "Need help.",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("CLAWSTACK_INTAKE_STORE", str(leads_path))

    exit_code = main(["leads", "--limit", "1", "--json"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "lead-1" in output
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_cli_site_config(monkeypatch, capsys) -> None:
    monkeypatch.setenv("CLAWSTACK_PUBLIC_SITE_URL", "https://clawstack.example")
    monkeypatch.setenv("CLAWSTACK_PUBLIC_API_URL", "https://clawstack.example/api")

    exit_code = main(["site-config"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "public_site_url=https://clawstack.example" in output


def test_cli_offers_json(monkeypatch, capsys) -> None:
    monkeypatch.setenv("CLAWSTACK_PUBLIC_SITE_URL", "https://clawstack.example")
    monkeypatch.setenv("CLAWSTACK_PUBLIC_API_URL", "https://clawstack.example/api")

    exit_code = main(["offers", "--json"])
    output = capsys.readouterr().out

    assert exit_code == 0
    payload = json.loads(output)
    assert any(item["slug"] == "diy-free" for item in payload)
