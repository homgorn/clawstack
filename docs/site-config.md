# Site Config

The landing page can read a `site-config` payload to update links and contact details.

## Backend source (recommended)

When the FastAPI backend is running, the site will fetch:

- `/api/v1/site-config` (or `/v1/site-config`)

That payload is generated from `CLAWSTACK_*` environment variables.

## Static fallback (GitHub Pages or static hosting)

If no API is available, the frontend will try:

- `/site-config.json`

To use it:

1. Copy `site-config.example.json` to `site-config.json`.
2. Update the URLs, repo, and contact email.
3. Deploy the file alongside `index.html`.

You can generate the file from the backend config:

```bash
python -m clawstack_backend.cli site-config --json > site-config.json
```

The frontend uses this data to update:

- repo links
- docs links
- contact email
- displayed API base
- offer cards (title, price, summary, CTA)

## Fields

The structure matches the backend response:

- `site_name`, `tagline`
- `public_site_url`, `public_api_base`, `public_api_url`
- `canonical_url`, `og_image_url`
- `repo_url`, `contact_email`
- `docs[]`
- `offers[]`
