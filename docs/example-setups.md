# Example Setups

This page gives concrete, minimal setups that match the current repo scope.

## 1) Local dev (no Docker)

Best for quick evaluation or docs review.

1. Install OpenClaw and run the baseline checks:

```bash
npm install -g openclaw@latest
openclaw --version
openclaw doctor --fix
openclaw security audit --deep
openclaw config validate --json
```

2. Copy a starter config:

```bash
cp configs/openclaw-budget.json ~/.openclaw/openclaw.json
```

3. Add workspace templates:

```bash
mkdir -p ~/.openclaw/workspace
cp workspace/*.md ~/.openclaw/workspace/
```

4. Set secrets in `~/.openclaw/.env` and lock the file:

```bash
chmod 600 ~/.openclaw/.env
```

## 2) Local dev (Docker sandbox)

Best when you want sandbox isolation.

1. Install Docker and enable sandboxing:

```bash
export OPENCLAW_SANDBOX=1
```

2. Use the budget config (it already includes Docker sandbox defaults) and validate:

```bash
cp configs/openclaw-budget.json ~/.openclaw/openclaw.json
openclaw config validate --json
```

3. Confirm Docker is accessible to OpenClaw:

```bash
docker --version
openclaw doctor --fix
```

## 3) VPS (systemd + reverse proxy)

Best for a simple production deployment with the ClawStack backend.

1. Create `/opt/clawstack` and copy the repo.
2. Create a virtualenv and install the backend:

```bash
python -m venv .venv
./.venv/bin/pip install -e .
```

3. Configure `backend/.env` using `backend/.env.example`.
4. Install the systemd unit from `deploy/clawstack.service.example`.
5. Put a reverse proxy in front (see `deploy/Caddyfile.example`).
6. Verify:

```bash
curl -s http://127.0.0.1:8000/api/health
curl -s http://127.0.0.1:8000/api/v1/site-config
```

## 4) Static landing + API on subdomain

Best if you want GitHub Pages for the landing but keep the API separate.

1. Set the public URLs:

```
CLAWSTACK_PUBLIC_SITE_URL=https://yourname.github.io/clawstack
CLAWSTACK_PUBLIC_API_URL=https://api.example.com
```

2. Deploy the backend on the API host and keep CORS aligned with the site URL.
3. If the API is not on the same origin, copy `site-config.example.json` to `site-config.json` and
   update `public_api_base`, `repo_url`, and `contact_email`.
4. The landing page will pull `public_api_base` from `/v1/site-config` or `/site-config.json` automatically.

## Notes

- The backend uses `CLAWSTACK_PUBLIC_SITE_URL` and `CLAWSTACK_PUBLIC_API_URL` to render canonical, Open Graph, sitemap, robots, and manifest files.
- The starter configs are templates; validate them after editing.
