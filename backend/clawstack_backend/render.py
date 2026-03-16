from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from .config import Settings


DEFAULT_SITE_URL = "https://homgorn.github.io/clawstack/"
DEFAULT_REPO_URL = "https://github.com/homgorn/clawstack"


def canonical_url(settings: Settings) -> str:
    return f"{settings.public_site_url}/"


def og_image_url(settings: Settings) -> str:
    return f"{canonical_url(settings)}og-card.svg"


def public_api_base(settings: Settings) -> str:
    site = urlparse(settings.public_site_url)
    api = urlparse(settings.public_api_url)
    if (api.scheme, api.netloc) == (site.scheme, site.netloc):
        return api.path or "/api"
    return settings.public_api_url


def _replace_once(text: str, needle: str, value: str) -> str:
    return text.replace(needle, value)


def render_landing(settings: Settings, template_path: Path) -> str:
    canonical = canonical_url(settings)
    api_base = public_api_base(settings)
    og_image = og_image_url(settings)
    rendered = template_path.read_text(encoding="utf-8")
    rendered = _replace_once(
        rendered,
        '<meta name="clawstack-api-base" content="/api">',
        f'<meta name="clawstack-api-base" content="{api_base}">',
    )
    rendered = rendered.replace(DEFAULT_SITE_URL, canonical)
    rendered = rendered.replace(f"{DEFAULT_SITE_URL}og-card.svg", og_image)
    rendered = rendered.replace(DEFAULT_REPO_URL, settings.repo_url)
    rendered = rendered.replace('"priceCurrency": "USD"', f'"priceCurrency": "{settings.default_currency}"')
    return rendered


def build_site_manifest(settings: Settings) -> dict[str, object]:
    site_path = urlparse(canonical_url(settings)).path or "/"
    return {
        "name": "ClawStack",
        "short_name": "ClawStack",
        "description": "OpenClaw cost optimizer, secure deployment toolkit, and optional setup service.",
        "start_url": site_path,
        "display": "standalone",
        "background_color": "#f6efe8",
        "theme_color": "#f26a21",
        "icons": [
            {
                "src": "favicon.svg",
                "sizes": "any",
                "type": "image/svg+xml",
                "purpose": "any maskable",
            }
        ],
    }


def build_robots_txt(settings: Settings) -> str:
    return "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "",
            f"Sitemap: {canonical_url(settings)}sitemap.xml",
        ]
    )


def build_sitemap_xml(settings: Settings) -> str:
    loc = canonical_url(settings)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "  <url>\n"
        f"    <loc>{loc}</loc>\n"
        "    <changefreq>weekly</changefreq>\n"
        "    <priority>1.0</priority>\n"
        "  </url>\n"
        "</urlset>\n"
    )


def build_llms_txt(settings: Settings) -> str:
    lines = [
        "# ClawStack",
        "",
        "ClawStack is an open-source OpenClaw toolkit with an optional paid setup and managed support layer.",
        "",
        "## Primary facts",
        "",
        "- Open-source core: configs, docs, workspace templates, starter skills.",
        "- Paid layer: setup, migration, managed operations, monitoring, support, premium integrations.",
        "- Future layer: dashboard and hosted SaaS only after real demand proves the need.",
        "",
        "## Best source files",
        "",
        f"- {settings.repo_url}",
        f"- {settings.repo_url}/blob/main/docs/example-setups.md",
        f"- {settings.repo_url}/blob/main/docs/context-map.md",
        f"- {settings.repo_url}/blob/main/docs/roadmap.md",
        f"- {settings.repo_url}/blob/main/OPENCLAW_FINAL_SPEC.md",
        "",
        "## Product summary",
        "",
        "The repository is the product core.",
        "The landing page is the conversion layer around three paths:",
        "",
        "- DIY Free",
        "- Pro Setup",
        "- Managed",
    ]
    return "\n".join(lines) + "\n"
