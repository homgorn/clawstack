---
name: incident-brief
description: "Produce a fast security incident brief for OpenClaw advisories."
version: 1.0.0
cost_estimate: "$0.03-$0.12 per run"
---

# Incident Brief

## Goal

Generate a short security brief when an OpenClaw issue, CVE, or provider incident is reported.

## Inputs

- advisory text or links
- current OpenClaw version in use
- deployment notes (if any)

## Output format

1. incident summary (what happened)
2. affected versions and impact
3. immediate mitigations
4. follow-up actions and monitoring steps

## Suggested cadence

- run on demand when new advisories appear
