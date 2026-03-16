# Backend

Minimal FastAPI backend for the ClawStack landing and service layer.

## Scope

This backend is intentionally small.

It provides:

- landing page on `/`;
- healthcheck;
- public site config for frontend and service links;
- public offers endpoint;
- intake endpoint for paid setup or managed requests.
- runtime rendering for canonical, Open Graph, sitemap, robots, and manifest;
- optional webhook and SMTP delivery for intake requests.
- optional Telegram delivery for intake requests;
- protected lead listing for operators.

It does not try to be a customer dashboard or full SaaS.

## Run

```bash
python -m uvicorn clawstack_backend.app:app --app-dir backend --reload
```

Then open:

- `http://127.0.0.1:8000/` for the landing page
- `http://127.0.0.1:8000/api/v1/site-config` for public config
- `http://127.0.0.1:8000/api/health` for healthcheck

## Important environment variables

```bash
CLAWSTACK_PUBLIC_SITE_URL=https://example.com
CLAWSTACK_PUBLIC_API_URL=https://api.example.com
CLAWSTACK_REPO_URL=https://github.com/homgorn/clawstack
CLAWSTACK_CONTACT_EMAIL=hello@example.com
CLAWSTACK_INTAKE_STORE=backend/data/intake.jsonl
CLAWSTACK_CORS_ORIGINS=https://example.com,https://www.example.com
CLAWSTACK_INTAKE_WEBHOOK_URL=
CLAWSTACK_SMTP_HOST=
CLAWSTACK_SMTP_PORT=587
CLAWSTACK_SMTP_FROM_EMAIL=
CLAWSTACK_SMTP_TO_EMAIL=
CLAWSTACK_TELEGRAM_BOT_TOKEN=
CLAWSTACK_TELEGRAM_CHAT_ID=
CLAWSTACK_ADMIN_TOKEN=
CLAWSTACK_INTAKE_DELIVERY_RETRIES=0
CLAWSTACK_INTAKE_DELIVERY_BACKOFF_SECONDS=1
CLAWSTACK_INTAKE_RATE_LIMIT_COUNT=10
CLAWSTACK_INTAKE_RATE_LIMIT_WINDOW_SECONDS=3600
```

If `CLAWSTACK_PUBLIC_API_URL` is omitted, the backend falls back to `CLAWSTACK_PUBLIC_SITE_URL + /api`.

`CLAWSTACK_CONTACT_EMAIL` is used by the landing page footer and the intake error fallback message.

Delivery retries are controlled by:

- `CLAWSTACK_INTAKE_DELIVERY_RETRIES` (additional attempts per sink)
- `CLAWSTACK_INTAKE_DELIVERY_BACKOFF_SECONDS` (base backoff between attempts)

The backend will also auto-load `backend/.env` if it exists, unless a value is already present in the real process environment.

## Deployment shape

Preferred first production shape:

- one backend process serves the landing and `/api`;
- a reverse proxy or platform can sit in front if needed;
- if you later split static and API hosts, the frontend already knows how to consume `site-config`.

## Delivery behavior

Every intake request is stored locally in JSONL.

If configured, the backend will also try:

- webhook delivery;
- SMTP email delivery.
- Telegram delivery.

If outbound delivery fails, the lead is still kept in local storage.

## Intake protection

The intake flow now has:

- honeypot suppression;
- in-memory rate limiting per client;
- optional admin-token protection for lead listing via `/api/v1/leads`.

## Operator CLI

You can inspect the current setup or recent leads without calling the API manually:

```bash
python -m clawstack_backend.cli site-config
python -m clawstack_backend.cli leads --limit 20
python -m clawstack_backend.cli leads --limit 20 --json
```
