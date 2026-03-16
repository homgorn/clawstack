# Docker Sandbox

Use Docker isolation when you need tool execution beyond pure chat or MCP workflows.

## Local profile

Good for a single machine:

- loopback-only gateway;
- no exposed public ports unless necessary;
- constrained CPU and memory;
- no `docker.sock` mount.

## Stronger production profile

Use:

- non-root user;
- read-only filesystem where possible;
- `no-new-privileges`;
- no direct public binding if a private network path is available;
- explicit secrets and environment handling.

## Red flags

- mounting the host Docker socket;
- broad write access to the host filesystem;
- no auth on the gateway;
- assuming sandbox is enabled without checking.
