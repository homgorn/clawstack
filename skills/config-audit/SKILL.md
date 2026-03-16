---
name: config-audit
description: "Review OpenClaw config for safe defaults, drift, and missing controls."
version: 1.0.0
cost_estimate: "$0.02-$0.08 per run"
---

# Config Audit

## Goal

Review the current OpenClaw config and highlight:

- unsafe defaults or drift;
- missing security controls;
- config fields that no longer match the recommended baseline.

## Inputs

- `~/.openclaw/openclaw.json`
- `~/.openclaw/.env`
- any custom workspace overrides

## Checks

- gateway binds to loopback only
- gateway auth required and secret injected via env
- sandbox explicitly enabled when desired
- skills directory and auto-load settings align with policy
- heartbeat cadence and direct policy match current guidance

## Output format

1. summary (pass/fail + short reason)
2. findings (each with severity + impact)
3. recommended changes (actionable steps)
4. optional diff snippet if safe to provide

## Suggested cadence

- run monthly
- run after OpenClaw upgrades
