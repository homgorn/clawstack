from __future__ import annotations

from datetime import datetime, UTC
import json
from typing import Any
from pathlib import Path
from uuid import uuid4

from .models import IntakeRequest


class IntakeStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def create_lead(
        self, payload: IntakeRequest, client_id: str | None = None
    ) -> dict[str, Any]:
        lead_id = uuid4().hex
        record: dict[str, Any] = {
            "lead_id": lead_id,
            "created_at_utc": datetime.now(UTC).isoformat(),
            **payload.model_dump(),
        }
        if client_id:
            record["client_id"] = client_id
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")
        return record

    def list_recent_leads(self, limit: int = 50) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        records: list[dict[str, Any]] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                records.append(json.loads(line))
        return list(reversed(records[-limit:]))
