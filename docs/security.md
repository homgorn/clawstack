# Security

This page summarizes the safe defaults described in the local research notes.

## Baseline rules

- Bind the gateway to loopback only.
- Require gateway authentication.
- Store secrets in a private `.env` file.
- Use sandboxing explicitly and verify it is actually enabled.
- Restrict skill sources to trusted locations.
- Never mount `docker.sock` into the runtime container.

## Minimum checklist

```bash
openclaw doctor --fix
openclaw security audit --deep
openclaw config validate --json
chmod 600 ~/.openclaw/openclaw.json ~/.openclaw/.env
```

Optional repo lint for starter configs (does not replace OpenClaw validation):

```bash
python ./scripts/check_configs.py
```

## Deployment hygiene

- Use least-privilege API keys.
- Put monthly spend caps on providers before launch.
- Treat email and document tools as injection surfaces.
- Review any skill that requests broad filesystem, shell, or network access.

## Sandbox notes

If you use Docker isolation:

- disable network where possible;
- run as non-root;
- use read-only filesystem where practical;
- keep memory and CPU limits tight.

More: [docker-sandbox.md](docker-sandbox.md)

## Trust model

The public repo should include security guidance for everyone.

Paid offerings can sell hardening work, monitoring, and support. They should not hide the baseline safety information users need to self-host responsibly.
