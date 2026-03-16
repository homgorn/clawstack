# Google Workspace CLI Setup

This repo treats Google Workspace CLI as optional.

## Why use it

It can add Gmail, Calendar, and Drive access to OpenClaw workflows with a compact MCP setup.

## Minimal setup

```bash
npm install -g @googleworkspace/cli
gws auth setup
gws auth login -s gmail.readonly,calendar.readonly,drive.readonly
```

## Minimal OpenClaw snippet

```json
{
  "mcp": {
    "servers": [
      {
        "name": "google-workspace",
        "command": "gws",
        "args": ["mcp", "--tool-mode", "compact"]
      }
    ]
  }
}
```

## Safety notes

- Prefer read-only scopes first.
- Do not hand broad admin scopes to an autonomous agent.
- Treat inbound mail and docs as prompt-injection surfaces.
