# ClawStack

OpenClaw deployment toolkit focused on three things: lower running cost, safer defaults, and a clean path from self-hosted use to an optional paid service layer.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Repo](https://img.shields.io/badge/GitHub-homgorn%2Fclawstack-181717?logo=github)](https://github.com/homgorn/clawstack)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-v2026.3.2-green.svg)](https://github.com/openclaw/openclaw)
[![Security Notes](https://img.shields.io/badge/Security-Docs-red.svg)](docs/security.md)

[Quick Start](docs/quick-start.md) · [Context Map](docs/context-map.md) · [Open-Core Model](docs/open-core-model.md) · [Docs Index](docs/README.md) · [Roadmap](docs/roadmap.md) · [Research Spec](OPENCLAW_FINAL_SPEC.md)

## Why this repo exists

Most OpenClaw setups fail in one of four places:

- they are too expensive for day-to-day usage;
- they ship with unsafe defaults or weak operational hygiene;
- they are hard to reproduce across machines and teams;
- they jump from "DIY notes" straight to "pay us" without a usable open-source core.

ClawStack is intended to solve that with a docs-first, config-first public repo:

- starter configs for budget and free setups;
- workspace templates for model discipline and task routing;
- security guidance for local and VPS deployments;
- starter skills and operational patterns;
- an optional paid layer for setup, hosting, support, and premium integrations.

## Product split

The safest model here is open-core, but with strict boundaries.

| Layer | What users get | How it should be sold |
| --- | --- | --- |
| Open source | Configs, docs, workspace templates, starter skills, self-hosting path | Free, fully usable, no lock-in |
| Service layer | Done-for-you setup, migration, support, hardening, custom integrations | One-time and recurring services |
| Hosted product | Dashboard, managed updates, billing, team controls, alerts | Optional SaaS later, not required for core value |

What should stay open:

- all baseline configs needed to self-host;
- all security guidance and safe default patterns;
- starter skills and workspace templates;
- migration path in and out of the paid layer.

What can be paid without damaging trust:

- setup and migration work;
- managed hosting and monitoring;
- premium skill packs and vertical integrations;
- team dashboards, billing, analytics, and SLA-backed support.

More detail: [docs/open-core-model.md](docs/open-core-model.md)

## Current public scope

This repository is intentionally honest about its current state.

- It is a real public starter kit now.
- It is not yet a full hosted product.
- The source research is in the root markdown files.
- The `old/` folder is archive material, not canonical product truth.

Public assets available now:

- [configs/openclaw-budget.json](configs/openclaw-budget.json)
- [configs/openclaw-free.json](configs/openclaw-free.json)
- [workspace/SOUL.md](workspace/SOUL.md)
- [workspace/AGENTS.md](workspace/AGENTS.md)
- [workspace/COST_RULES.md](workspace/COST_RULES.md)
- [workspace/HEARTBEAT.md](workspace/HEARTBEAT.md)
- [skills/weekly-intel/SKILL.md](skills/weekly-intel/SKILL.md)
- [skills/config-audit/SKILL.md](skills/config-audit/SKILL.md)
- [skills/provider-watch/SKILL.md](skills/provider-watch/SKILL.md)
- [skills/incident-brief/SKILL.md](skills/incident-brief/SKILL.md)

## Quick start

1. Read [docs/quick-start.md](docs/quick-start.md).
2. Pick a config from [configs/README.md](configs/README.md).
3. Copy the workspace templates from [workspace/README.md](workspace/README.md).
4. Add the starter skill from [skills/README.md](skills/README.md) if you want scheduled research.
5. Optional helper scripts: [scripts/README.md](scripts/README.md).

## Repository structure

```text
clawstack/
├── README.md
├── LICENSE
├── index.html                    # landing page
├── styles.css                    # landing styles
├── app.js                        # landing-to-backend intake integration
├── OPENCLAW_FINAL_SPEC.md      # technical research source
├── business-model.md           # internal monetization notes
├── GITHUB_SEO.md               # SEO notes for repo/site
├── backend/                    # FastAPI backend for site config + intake
├── deploy/                     # production proxy examples
├── docs/                       # public documentation index
├── configs/                    # starter OpenClaw configs
├── scripts/                    # helper install/upgrade/validate scripts
├── workspace/                  # starter workspace templates
├── skills/                     # public starter skills
└── old/                        # archive / non-canonical drafts
```

## Documentation

| Doc | Purpose |
| --- | --- |
| [docs/quick-start.md](docs/quick-start.md) | Fast setup path for the public starter kit |
| [docs/example-setups.md](docs/example-setups.md) | Concrete local, VPS, and split-hosting examples |
| [docs/site-config.md](docs/site-config.md) | Site-config payload for dynamic links |
| [docs/context-map.md](docs/context-map.md) | Product boundaries, source of truth, and packaging map |
| [docs/open-core-model.md](docs/open-core-model.md) | Recommended split between OSS and paid product layers |
| [docs/security.md](docs/security.md) | Safe defaults and hardening checklist |
| [docs/models.md](docs/models.md) | Model-role mapping based on the local research notes |
| [docs/budget-calculator.md](docs/budget-calculator.md) | Budget scenarios from free to recommended |
| [docs/api-providers.md](docs/api-providers.md) | Free, trial, and cheap provider options |
| [docs/deployment.md](docs/deployment.md) | First-production deployment shape and runtime config |
| [docs/gws-setup.md](docs/gws-setup.md) | Google Workspace CLI setup notes |
| [docs/docker-sandbox.md](docs/docker-sandbox.md) | Docker isolation guidance |
| [docs/own-api.md](docs/own-api.md) | Minimal API wrapper approach |
| [docs/faq.md](docs/faq.md) | Questions about positioning and scope |
| [docs/roadmap.md](docs/roadmap.md) | What should be built next in public vs paid layers |
| [docs/wordpress-option.md](docs/wordpress-option.md) | How to move the landing into WordPress later |

Backend notes: [backend/README.md](backend/README.md)

Docs index: [docs/README.md](docs/README.md)

## Research sources

These files are useful when shaping the product, but they are not all public-facing docs:

- [OPENCLAW_FINAL_SPEC.md](OPENCLAW_FINAL_SPEC.md)
- [business-model.md](business-model.md)
- [GITHUB_SEO.md](GITHUB_SEO.md)
- [old/README.md](old/README.md)

## Positioning recommendation

The best path is not "open repo or paid product". It is:

1. Make the repo genuinely useful on its own.
2. Sell convenience, speed, support, and managed operations.
3. Delay a hosted SaaS until the open-source core and config patterns are stable.

That keeps the repo credible and gives the paid layer a clean value proposition.

## Contributing

Issues and PRs are welcome, especially for:

- safer config defaults;
- new provider profiles;
- extra workspace templates;
- starter skills that are safe to run self-hosted.
- local checks: `scripts/run_checks.sh` or `scripts/run_checks.ps1`.

## License

MIT. See [LICENSE](LICENSE).
