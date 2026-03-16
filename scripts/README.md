# Scripts

Helper scripts for installing, upgrading, and validating OpenClaw.

## Bash (macOS/Linux)

```bash
chmod +x ./scripts/openclaw.sh
./scripts/openclaw.sh install
./scripts/openclaw.sh doctor
./scripts/openclaw.sh audit
./scripts/openclaw.sh validate
./scripts/openclaw.sh bootstrap
```

## PowerShell (Windows)

```powershell
.\scripts\openclaw.ps1 install
.\scripts\openclaw.ps1 doctor
.\scripts\openclaw.ps1 audit
.\scripts\openclaw.ps1 validate
.\scripts\openclaw.ps1 bootstrap
```

## Notes

- Recommended Node.js version is `>= 22.12.0`.
- Config is expected at `~/.openclaw/openclaw.json` (or `config.json`).
- Optional onboarding step: `openclaw onboard --install-daemon`.

## Repo checks

Run local checks (config lint + backend tests):

```bash
chmod +x ./scripts/run_checks.sh
./scripts/run_checks.sh
```

PowerShell:

```powershell
.\scripts\run_checks.ps1
```

## Config lint

Validate the starter configs in `configs/`:

```bash
python ./scripts/check_configs.py
```

Schema for editor hints:

- `configs/openclaw.schema.json`

Target a specific config:

```bash
python ./scripts/check_configs.py ./configs/openclaw-budget.json
```
