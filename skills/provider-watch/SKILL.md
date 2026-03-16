---
name: provider-watch
description: "Track low-cost provider changes and suggest safe config updates."
version: 1.0.0
cost_estimate: "$0.05-$0.20 per run"
---

# Provider Watch

## Goal

Monitor low-cost providers and identify changes that affect:

- pricing;
- rate limits;
- model availability;
- safe default routing.

## Inputs

- current OpenClaw config
- recent provider status pages or announcements

## Output format

1. summary of changes since last run
2. notable provider shifts (pricing, limits, removals)
3. recommended config updates
4. risks or regressions to watch

## Suggested cadence

- monthly
- immediately after major provider announcements
