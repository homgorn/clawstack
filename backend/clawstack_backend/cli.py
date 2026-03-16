from __future__ import annotations

import argparse
import json
from typing import Sequence

from .config import load_settings
from .site_config import build_site_config
from .storage import IntakeStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="clawstack-admin")
    subparsers = parser.add_subparsers(dest="command", required=True)

    leads = subparsers.add_parser("leads", help="Show recent intake leads")
    leads.add_argument("--limit", type=int, default=20)
    leads.add_argument("--json", action="store_true", dest="as_json")

    config = subparsers.add_parser("site-config", help="Show public site config")
    config.add_argument("--json", action="store_true", dest="as_json")

    offers = subparsers.add_parser("offers", help="Show public offers")
    offers.add_argument("--json", action="store_true", dest="as_json")

    return parser


def run_leads(limit: int, as_json: bool) -> int:
    settings = load_settings()
    records = IntakeStore(settings.intake_store_path).list_recent_leads(limit=max(1, limit))
    if as_json:
        print(json.dumps(records, ensure_ascii=True, indent=2))
        return 0
    if not records:
        print("No leads found.")
        return 0
    for record in records:
        print(
            " | ".join(
                [
                    str(record.get("created_at_utc", "")),
                    str(record.get("service_tier", "")),
                    str(record.get("name", "")),
                    str(record.get("email", "")),
                    str(record.get("lead_id", "")),
                ]
            )
        )
    return 0


def run_site_config(as_json: bool) -> int:
    settings = load_settings()
    payload = {
        "public_site_url": settings.public_site_url,
        "public_api_url": settings.public_api_url,
        "repo_url": settings.repo_url,
        "contact_email": settings.contact_email,
    }
    if as_json:
        print(json.dumps(payload, ensure_ascii=True, indent=2))
    else:
        for key, value in payload.items():
            print(f"{key}={value}")
    return 0


def run_offers(as_json: bool) -> int:
    settings = load_settings()
    offers = build_site_config(settings).offers
    if as_json:
        print(
            json.dumps(
                [offer.model_dump() for offer in offers],
                ensure_ascii=True,
                indent=2,
            )
        )
        return 0
    for offer in offers:
        print(
            " | ".join(
                [
                    offer.slug,
                    offer.title,
                    offer.price_label,
                    offer.kind,
                ]
            )
        )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "leads":
        return run_leads(limit=args.limit, as_json=args.as_json)
    if args.command == "site-config":
        return run_site_config(as_json=args.as_json)
    if args.command == "offers":
        return run_offers(as_json=args.as_json)
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
