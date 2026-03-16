# Roadmap

This roadmap fixes the launch order for ClawStack so the project can go public fast without pretending the hosted product already exists.

Related map: [context-map.md](context-map.md)

## Source of truth

Use these documents in this order:

1. [../OPENCLAW_FINAL_SPEC.md](../OPENCLAW_FINAL_SPEC.md) for technical and research direction.
2. [context-map.md](context-map.md) for product boundaries and packaging.
3. [../README.md](../README.md) for the public promise.
4. [../business-model.md](../business-model.md) for internal monetization thinking.

## Launch principle

The first production launch is not "full SaaS". It is:

- a genuinely useful open-source repo;
- a frontend landing page that explains the offer;
- a paid service layer for setup and managed operations;
- a future option for dashboard/SaaS after real demand exists.

## Phase 1: public foundation

Status: in progress as of March 8, 2026.

- keep the repo honest and all README links working;
- publish starter configs for free and budget setups;
- publish workspace templates and one safe starter skill;
- publish security, model, budget, and provider guidance;
- define the product split between OSS core and paid layer.

Exit criteria:

- public repo is usable without paying;
- public docs match real repository contents;
- a user can understand what is available now in under five minutes.

## Phase 2: production-ready open-source kit

Build next:

- more starter skills and example setups;
- a sharper quick-start path for local machine and VPS deployment.

Now available:

- install/upgrade helpers in `scripts/openclaw.*`;
- config validation helper in `scripts/openclaw.* validate`;
- security audit helper in `scripts/openclaw.* audit`.
- starter config lint in `scripts/check_configs.py`.
- starter JSON schema in `configs/openclaw.schema.json`.
- starter skills: `config-audit`, `provider-watch`, `incident-brief`.
- example setups guide: `docs/example-setups.md`.
- CI workflow and local check runners in `scripts/run_checks.*`.
- static site-config fallback + nginx example.
- intake delivery retries/backoff via env vars.

Exit criteria:

- a self-hosting user can get from clone to working setup with low ambiguity;
- the repo can support organic SEO traffic without requiring private help.

## Phase 3: paid service layer

Ship before any real SaaS build:

- `Pro Setup`: one-time installation and migration service;
- `Managed`: recurring updates, monitoring, and support;
- custom integrations and premium skill packs where needed.

Frontend requirement for this phase:

- simple landing page;
- clear split between `DIY Free`, `Pro Setup`, and `Managed`;
- CTA to pay, book, or contact;
- no fake dashboard screenshots and no fake app claims.

Exit criteria:

- the paid layer sells convenience and support, not hidden basics;
- the open-source repo remains credible and complete for self-hosting.

## Phase 4: frontend product

Only after service demand is validated:

- dashboard for config generation and guided setup;
- pricing and packaging pages;
- lead capture, onboarding, and support flows;
- basic authenticated user area if it solves a real support bottleneck.

Important:

- the first frontend should be a marketing and conversion layer;
- it does not need multi-tenant architecture on day one.

## Phase 5: hosted SaaS

Build last, not first:

- team dashboard;
- billing and account management;
- usage analytics and alerts;
- managed multi-tenant controls;
- optional API product and hosted operations layer.

Exit criteria:

- repeatable paid demand already exists;
- the SaaS removes real operational pain discovered from service work.

## What not to do now

- do not build a heavy dashboard before the offer is clear;
- do not gate core configs or security guidance behind payment;
- do not describe future SaaS features in the README as current capability.

## Immediate next moves

1. Keep the repo as the open-source product core.
2. Build a simple frontend landing around three offers: `DIY Free`, `Pro Setup`, `Managed`.
3. Add a real backend intake path and centralized site config for links and public URLs.
4. Expand the open-source kit based on what early users fail on most.
