# Deployment

This project now supports a simple first-production deployment shape:

- one FastAPI process serves the landing on `/`;
- the same process serves the API on `/api`;
- intake requests are persisted locally and can also be forwarded by webhook or SMTP.

## Recommended topology

For the first production slice:

- app on one domain;
- backend and landing on the same origin;
- reverse proxy or host platform handles TLS if needed.

## Environment

Start from [../backend/.env.example](../backend/.env.example).

Important variables:

- `CLAWSTACK_PUBLIC_SITE_URL`
- `CLAWSTACK_PUBLIC_API_URL`
- `CLAWSTACK_REPO_URL`
- `CLAWSTACK_CONTACT_EMAIL`
- `CLAWSTACK_INTAKE_WEBHOOK_URL`
- `CLAWSTACK_SMTP_*`
- `CLAWSTACK_TELEGRAM_*`
- `CLAWSTACK_ADMIN_TOKEN`

## Local run

```bash
python -m uvicorn clawstack_backend.app:app --app-dir backend --reload
```

## Docker

```bash
copy backend\\.env.example backend\\.env
docker compose up --build
```

## systemd on VPS

If you do not want Docker, run the backend directly behind a reverse proxy.

Sample unit:

- [../deploy/clawstack.service.example](../deploy/clawstack.service.example)

More concrete walkthroughs:

- [example-setups.md](example-setups.md)

Typical flow:

1. Create `/opt/clawstack`
2. Put the repo there
3. Create a virtualenv
4. Install the package
5. Copy `backend/.env.example` to `backend/.env`
6. Install the systemd unit
7. Put Caddy or another reverse proxy in front

Then open:

- `/`
- `/api/health`
- `/api/v1/site-config`

## Intake delivery modes

Minimum:

- JSONL persistence only.

Optional:

- webhook delivery via `CLAWSTACK_INTAKE_WEBHOOK_URL`;
- SMTP delivery via `CLAWSTACK_SMTP_*`.
- Telegram delivery via `CLAWSTACK_TELEGRAM_*`.

If delivery fails, the lead is still stored locally.

## Recommended first alert path

For a small first production setup, Telegram is usually the simplest operational channel:

- no CRM required;
- no mail deliverability setup required;
- immediate visibility for setup and managed leads.

Use:

- `CLAWSTACK_TELEGRAM_BOT_TOKEN`
- `CLAWSTACK_TELEGRAM_CHAT_ID`

## Intake protection

The first production slice now includes:

- honeypot suppression via the landing form;
- in-memory per-client rate limiting on intake;
- protected operator endpoint at `/api/v1/leads` using `CLAWSTACK_ADMIN_TOKEN`.

## Operator access

For local or server-side inspection without hitting the API manually:

```bash
python -m clawstack_backend.cli leads --limit 20
python -m clawstack_backend.cli site-config
```

## Reverse proxy

A same-origin deployment is the cleanest first setup:

- landing on `/`
- API on `/api`
- one public domain

Sample Caddy config:

- [../deploy/Caddyfile.example](../deploy/Caddyfile.example)

Sample Nginx config:

- [../deploy/nginx.conf.example](../deploy/nginx.conf.example)

## Canonical and SEO URLs

Do not edit the domain in multiple files by hand.

Set:

- `CLAWSTACK_PUBLIC_SITE_URL`
- `CLAWSTACK_PUBLIC_API_URL`

The backend uses those values for:

- landing HTML meta and JSON-LD;
- `robots.txt`;
- `sitemap.xml`;
- `site.webmanifest`;
- `site-config` API.

If your site lives under a path prefix instead of the domain root, the backend will carry that prefix into `public_api_base` as well.

## Static fallback

If you deploy the landing without the backend (for example GitHub Pages),
use `site-config.json` as a static fallback for links and contact email.

See: [site-config.md](site-config.md).
