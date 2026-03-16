# Context Map

This document defines how ClawStack is packaged, what each layer includes, and which documents are allowed to speak for the product.

Related plan: [roadmap.md](roadmap.md)

## Core decision

ClawStack is an open-core product with a service-led frontend, not a full SaaS-first launch.

That means:

- the repository is the real product core;
- the frontend sells setup, support, and managed convenience;
- the dashboard and hosted platform come later if demand justifies them.

## Source of truth map

### Technical truth

- [../OPENCLAW_FINAL_SPEC.md](../OPENCLAW_FINAL_SPEC.md)

Use this for:

- OpenClaw configuration direction;
- model routing choices;
- security and operational assumptions;
- research-backed implementation decisions.

### Public product truth

- [../README.md](../README.md)
- [roadmap.md](roadmap.md)
- [open-core-model.md](open-core-model.md)
- [this document](context-map.md)

Use these for:

- what the repo claims publicly;
- what is open-source now;
- what is paid now;
- what is planned later.

### Internal commercial thinking

- [../business-model.md](../business-model.md)
- [../GITHUB_SEO.md](../GITHUB_SEO.md)

Use these for:

- packaging ideas;
- pricing experiments;
- SEO and positioning;
- internal GTM notes.

### Archive only

- [../old/README.md](../old/README.md)

And the rest of `old/`.

Use archive files only for background and idea recovery, never as current truth.

## Product boundary map

## Open-source core

Lives in this repository and must stay useful on its own.

Includes:

- starter configs in [../configs/README.md](../configs/README.md);
- workspace templates in [../workspace/README.md](../workspace/README.md);
- starter skills in [../skills/README.md](../skills/README.md);
- docs and hardening guidance in [README.md](README.md) and the rest of `docs/`.

Promise:

- self-hostable;
- transparent;
- no lock-in for baseline usage;
- safe defaults documented in public.

## Paid service layer

Sold on the frontend, not hidden inside the repo.

Includes:

- done-for-you setup;
- migration from messy or insecure installs;
- managed updates and monitoring;
- premium integrations and support;
- optional premium skill packs.

Promise:

- faster setup;
- less maintenance burden;
- expert help;
- optional recurring operations support.

## Future frontend product

Built only after the service layer proves demand.

Includes:

- guided setup UX;
- pricing and onboarding;
- lead capture and support workflows;
- lightweight authenticated customer area if needed.

Promise:

- better conversion and smoother handoff from repo to service.

## Future hosted SaaS

Not the first launch target.

Potential includes:

- team workspace;
- billing;
- managed configs;
- usage analytics;
- multi-tenant controls.

Promise:

- convenience at scale, not replacement of the open core.

## Frontend role

The first frontend should answer one question clearly:

"Do I want to run this myself, pay for setup, or pay for managed support?"

So the initial frontend should have three paths:

- `DIY Free`
- `Pro Setup`
- `Managed`

It should not start as a fake app shell with empty dashboard pages.

## Frontend and link governance

The frontend must distinguish between three link classes:

- repository and docs links;
- public site links;
- service and intake links.

Rules:

- repository and docs links stay relative whenever possible;
- canonical URL, Open Graph URL, sitemap host, and robots sitemap entry come from one public site base URL;
- paid CTA and intake links should be generated from one backend-owned site config, not hardcoded across multiple files;
- if the public domain changes, it should require one config update, not a repo-wide manual rewrite.

Current implementation direction:

- static landing for SEO and fast deployment;
- backend endpoint for site config and service offer metadata;
- future frontend can read backend config, but repository docs should remain stable even without that runtime.

Preferred deployment topology:

- same backend can serve the landing on `/` and API on `/api` for the first production slice;
- optional split topology: static site on `/` and backend behind `/api`;
- optional secondary topology: backend on `api.<domain>` if reverse proxying on the main host is not convenient.

## Backend role

The first backend is not the hosted SaaS.

Its job is narrower:

- healthcheck for deployment;
- central source for public site config and service links;
- intake endpoint for paid service requests;
- optional lightweight persistence for inbound leads.
- minimal operator visibility into recent leads;
- minimal abuse protection for public intake.

It should not begin with:

- multi-tenant auth;
- billing portal;
- customer dashboard;
- productized usage analytics.

## Open-source backend rule

The backend for the landing and service layer should remain open-source and self-hostable.

Paid value comes from:

- execution;
- setup speed;
- managed operations;
- support;
- premium integrations.

Paid value does not come from hiding the backend code that powers a simple landing or intake flow.

## Messaging rule

Public messaging must stay aligned with repository reality.

Allowed claims now:

- cost optimization starter kit;
- docs-first OpenClaw setup toolkit;
- security and model guidance;
- optional paid setup and managed path.

Not allowed now:

- claiming a full hosted dashboard exists;
- implying enterprise product maturity before it exists;
- linking to non-existent product surfaces.

## Build order

1. Open-source repo is the product core.
2. Frontend landing is the conversion layer.
3. Service sales are the first monetization layer.
4. Dashboard and SaaS happen only after repeated customer demand.

## Execution note

If there is a conflict between a marketing idea and repository reality, repository reality wins and marketing gets rewritten.
