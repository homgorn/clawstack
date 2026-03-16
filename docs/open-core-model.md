# Open-Core Model

This is the recommended product split for ClawStack.

## Principle

The public repo must be useful without paying you.

If the open repository only acts as a teaser, trust drops, stars do not convert, and the paid layer looks like gated basics.

## What belongs in open source

- baseline configs for free and budget setups;
- workspace templates and agent discipline files;
- security guidance and hardening checklists;
- starter skills that are safe for self-hosting;
- migration docs so users can leave the paid layer cleanly.

## What belongs in the paid layer

- done-for-you setup and migration;
- managed hosting, monitoring, and updates;
- premium skill packs for vertical workflows;
- custom integrations and team onboarding;
- dashboards, billing, analytics, and SLA support.

## What should not be paywalled

- the ability to self-host the core setup;
- core security fixes and safe default guidance;
- starter configs required for basic success;
- export or backup paths for user-owned config and data.

## Recommended monetization ladder

1. Public repo that solves the initial setup problem.
2. One-time setup service for users who do not want to configure it.
3. Managed operations subscription.
4. Hosted team product only after the public kit stabilizes.

## Why this works better

- Open source builds trust and search traffic.
- Services monetize speed and reduced operational burden.
- A hosted layer later can monetize collaboration and convenience.
- None of those require locking users into a private core.

## Operational guardrails

Borrowing the strongest pattern from `D:\bmad-project`:

- keep one source of truth for public positioning;
- define a minimal MVP and do not promise future code as if it exists;
- require human approval for risky operations in any paid managed layer.

For this repo, the public truth should live in:

- [../README.md](../README.md)
- [roadmap.md](roadmap.md)
- [../OPENCLAW_FINAL_SPEC.md](../OPENCLAW_FINAL_SPEC.md)
