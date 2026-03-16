from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles

from .config import Settings, load_settings
from .delivery import IntakeDelivery
from .models import (
    HealthResponse,
    IntakeRequest,
    IntakeResponse,
    LeadListResponse,
    LeadRecord,
    OfferItem,
    SiteConfigResponse,
)
from .protection import IntakeRateLimiter
from .render import (
    build_llms_txt,
    build_robots_txt,
    build_site_manifest,
    build_sitemap_xml,
    render_landing,
)
from .site_config import build_site_config
from .storage import IntakeStore


settings = load_settings()
store = IntakeStore(settings.intake_store_path)
delivery = IntakeDelivery(settings)
rate_limiter = IntakeRateLimiter(
    max_requests=settings.intake_rate_limit_count,
    window_seconds=settings.intake_rate_limit_window_seconds,
)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

PUBLIC_FILE_MAP = {
    "/styles.css": PROJECT_ROOT / "styles.css",
    "/app.js": PROJECT_ROOT / "app.js",
    "/favicon.svg": PROJECT_ROOT / "favicon.svg",
    "/favicon.ico": PROJECT_ROOT / "favicon.svg",
    "/og-card.svg": PROJECT_ROOT / "og-card.svg",
}


def _static_endpoint(path: Path):
    def _serve() -> FileResponse:
        return FileResponse(path)

    _serve.__name__ = f"serve_{path.name.replace('.', '_')}"
    return _serve

app = FastAPI(
    title="ClawStack Backend",
    summary="Minimal backend for the ClawStack landing and service layer.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins) or ["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


def _extract_client_id(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "").strip()
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def _require_admin_token(
    authorization: str | None,
    x_admin_token: str | None,
) -> None:
    if not settings.admin_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="admin endpoint is disabled",
        )
    bearer_token: str | None = None
    if authorization and authorization.lower().startswith("bearer "):
        bearer_token = authorization[7:].strip()
    token = x_admin_token or bearer_token
    if token != settings.admin_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid admin token",
        )


app.mount("/docs", StaticFiles(directory=PROJECT_ROOT / "docs"), name="docs")


@app.get("/", include_in_schema=False)
def landing() -> HTMLResponse:
    html = render_landing(settings, PROJECT_ROOT / "index.html")
    return HTMLResponse(html)


@app.get("/README.md", include_in_schema=False)
def readme_file() -> FileResponse:
    return FileResponse(PROJECT_ROOT / "README.md", media_type="text/markdown")


for route_path, file_path in PUBLIC_FILE_MAP.items():
    app.add_api_route(
        route_path,
        endpoint=_static_endpoint(file_path),
        methods=["GET"],
        include_in_schema=False,
    )


@app.get("/robots.txt", include_in_schema=False)
def robots_txt() -> PlainTextResponse:
    return PlainTextResponse(build_robots_txt(settings))


@app.get("/llms.txt", include_in_schema=False)
def llms_txt() -> PlainTextResponse:
    return PlainTextResponse(build_llms_txt(settings))


@app.get("/sitemap.xml", include_in_schema=False)
def sitemap_xml() -> Response:
    return Response(build_sitemap_xml(settings), media_type="application/xml")


@app.get("/site.webmanifest", include_in_schema=False)
def site_webmanifest() -> JSONResponse:
    return JSONResponse(
        build_site_manifest(settings),
        media_type="application/manifest+json",
    )


@app.get("/v1/site-config", response_model=SiteConfigResponse)
@app.get("/api/v1/site-config", response_model=SiteConfigResponse)
def site_config() -> SiteConfigResponse:
    return build_site_config(settings)


@app.get("/health", response_model=HealthResponse)
@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        environment=settings.environment,
        timestamp_utc=datetime.now(UTC),
    )

@app.get("/v1/offers", response_model=list[OfferItem])
@app.get("/api/v1/offers", response_model=list[OfferItem])
def offers() -> list[OfferItem]:
    return build_site_config(settings).offers


@app.get("/v1/leads", response_model=LeadListResponse)
@app.get("/api/v1/leads", response_model=LeadListResponse)
def leads(
    limit: int = 50,
    authorization: str | None = Header(default=None),
    x_admin_token: str | None = Header(default=None),
) -> LeadListResponse:
    _require_admin_token(authorization, x_admin_token)
    safe_limit = max(1, min(limit, 200))
    records = store.list_recent_leads(limit=safe_limit)
    return LeadListResponse(leads=[LeadRecord.model_validate(record) for record in records])


@app.post(
    "/v1/intake",
    response_model=IntakeResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
@app.post(
    "/api/v1/intake",
    response_model=IntakeResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def intake(payload: IntakeRequest, request: Request, response: Response) -> IntakeResponse:
    client_id = _extract_client_id(request)
    limit = rate_limiter.allow(client_id)
    if not limit.allowed:
        response.headers["Retry-After"] = str(limit.retry_after_seconds)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="intake rate limit exceeded",
            headers={"Retry-After": str(limit.retry_after_seconds)},
        )
    if payload.website:
        return IntakeResponse(
            status="accepted",
            lead_id="suppressed",
            delivery_channels=[],
        )
    record = store.create_lead(payload, client_id=client_id)
    delivery_channels = delivery.deliver(record)
    return IntakeResponse(
        status="accepted",
        lead_id=str(record["lead_id"]),
        delivery_channels=delivery_channels,
    )
