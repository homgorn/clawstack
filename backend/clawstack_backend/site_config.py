from __future__ import annotations

from .config import Settings
from .models import LinkItem, OfferItem, SiteConfigResponse
from .render import canonical_url, og_image_url, public_api_base


def _github_blob(settings: Settings, path: str) -> str:
    return f"{settings.repo_url}/blob/main/{path}"


def build_site_config(settings: Settings) -> SiteConfigResponse:
    docs = [
        LinkItem(label="Repository", href=settings.repo_url),
        LinkItem(label="README", href=settings.repo_url),
        LinkItem(label="Example Setups", href=_github_blob(settings, "docs/example-setups.md")),
        LinkItem(label="Context Map", href=_github_blob(settings, "docs/context-map.md")),
        LinkItem(label="Roadmap", href=_github_blob(settings, "docs/roadmap.md")),
        LinkItem(
            label="WordPress Option",
            href=_github_blob(settings, "docs/wordpress-option.md"),
        ),
    ]
    offers = [
        OfferItem(
            slug="diy-free",
            title="DIY Free",
            price_label="$0",
            summary="Use the open-source repo as the product core with configs, docs, templates, and starter skills.",
            cta_label="Open Repository",
            cta_href=settings.repo_url,
            kind="open-source",
        ),
        OfferItem(
            slug="pro-setup",
            title="Pro Setup",
            price_label="Custom quote",
            summary="Done-for-you installation, migration, hardening, and routing setup.",
            cta_label="Request setup",
            cta_href=f"{settings.public_api_url}/v1/intake",
            kind="service",
        ),
        OfferItem(
            slug="managed",
            title="Managed",
            price_label="Monthly",
            summary="Ongoing updates, monitoring, support, and operational help.",
            cta_label="Request managed plan",
            cta_href=f"{settings.public_api_url}/v1/intake",
            kind="managed",
        ),
    ]
    return SiteConfigResponse(
        site_name="ClawStack",
        tagline="Open-source OpenClaw toolkit with optional setup and managed support.",
        public_site_url=settings.public_site_url,
        public_api_base=public_api_base(settings),
        public_api_url=settings.public_api_url,
        canonical_url=canonical_url(settings),
        og_image_url=og_image_url(settings),
        repo_url=settings.repo_url,
        contact_email=settings.contact_email,
        docs=docs,
        offers=offers,
    )
