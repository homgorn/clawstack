# Quick Start

This repo is currently a starter kit, not a one-command product.

If you want concrete deployment recipes, see [example-setups.md](example-setups.md).

## 1. Prerequisites

```bash
node --version
docker --version
```

Recommended from the local spec:

- Node.js `>= 22.12.0`
- Docker `>= 29.0` if you want sandboxing

## 2. Install OpenClaw

Helper scripts (recommended):

```bash
./scripts/openclaw.sh install
./scripts/openclaw.sh doctor
./scripts/openclaw.sh validate
```

PowerShell (Windows):

```powershell
.\scripts\openclaw.ps1 install
.\scripts\openclaw.ps1 doctor
.\scripts\openclaw.ps1 validate
```

Manual alternative:

```bash
npm install -g openclaw@latest
openclaw --version
openclaw doctor --fix
openclaw config validate --json
```

Optional onboarding step:

```bash
openclaw onboard --install-daemon
```

## 3. Choose a starter config

- Budget-first: [../configs/openclaw-budget.json](../configs/openclaw-budget.json)
- Free-first: [../configs/openclaw-free.json](../configs/openclaw-free.json)

Copy one into your OpenClaw config directory and review it before use.
Both starter configs include a `$schema` pointer for editor hints.

Optional repo lint for starter configs:

```bash
python ./scripts/check_configs.py
```

## 4. Add workspace templates

Start with:

- [../workspace/SOUL.md](../workspace/SOUL.md)
- [../workspace/AGENTS.md](../workspace/AGENTS.md)
- [../workspace/COST_RULES.md](../workspace/COST_RULES.md)
- [../workspace/HEARTBEAT.md](../workspace/HEARTBEAT.md)

## 5. Create an environment file

Use a private file such as `~/.openclaw/.env` and lock it down:

```bash
chmod 600 ~/.openclaw/.env
```

Typical variables:

```bash
OPENCLAW_GATEWAY_SECRET=replace_me
OPENROUTER_API_KEY=replace_me
GOOGLE_AI_STUDIO_KEY=replace_me
ANTHROPIC_API_KEY=replace_me
```

## 6. Optional modules

- Weekly research skill: [../skills/weekly-intel/SKILL.md](../skills/weekly-intel/SKILL.md)
- Config audit skill: [../skills/config-audit/SKILL.md](../skills/config-audit/SKILL.md)
- Provider watch skill: [../skills/provider-watch/SKILL.md](../skills/provider-watch/SKILL.md)
- Incident brief skill: [../skills/incident-brief/SKILL.md](../skills/incident-brief/SKILL.md)
- Google Workspace CLI notes: [gws-setup.md](gws-setup.md)
- Docker isolation notes: [docker-sandbox.md](docker-sandbox.md)

## 7. Safety pass before real usage

Read:

- [security.md](security.md)
- [models.md](models.md)

Optional security audit:

```bash
./scripts/openclaw.sh audit
```

PowerShell:

```powershell
.\scripts\openclaw.ps1 audit
```

The local research notes are strong, but you should still verify production details against official OpenClaw docs before deploying.

## Optional local checks

Run repo checks (config lint + backend tests):

```bash
./scripts/run_checks.sh
```

PowerShell:

```powershell
.\scripts\run_checks.ps1
```
