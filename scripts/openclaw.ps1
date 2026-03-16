Param(
  [Parameter(Position = 0)]
  [string]$Command = "help"
)

$ScriptName = Split-Path -Leaf $MyInvocation.MyCommand.Path
$ConfigDir = Join-Path $env:USERPROFILE ".openclaw"
$ConfigPrimary = Join-Path $ConfigDir "openclaw.json"
$ConfigFallback = Join-Path $ConfigDir "config.json"

function Show-Usage {
  @"
Usage: $ScriptName <command>

Commands:
  install    Install the latest OpenClaw CLI via npm
  upgrade    Upgrade the OpenClaw CLI via npm
  doctor     Run OpenClaw doctor fixes
  audit      Run OpenClaw security audit
  validate   Validate the active OpenClaw config
  bootstrap  Run install + doctor + audit + validate
  help       Show this help

Notes:
  - Recommended Node.js version: >= 22.12.0
  - Config is expected at $ConfigPrimary
    (or $ConfigFallback if you use that name)
  - Optional onboarding: openclaw onboard --install-daemon
"@
}

function Require-Command {
  param([string]$Name)
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    throw "Missing command: $Name"
  }
}

function Show-NodeVersion {
  if (Get-Command node -ErrorAction SilentlyContinue) {
    Write-Host ("Node version: {0}" -f (node --version))
  } else {
    Write-Host "Node not found. Install Node.js >= 22.12.0 first."
  }
}

function Check-Config {
  if ((Test-Path $ConfigPrimary) -or (Test-Path $ConfigFallback)) {
    return $true
  }
  Write-Host "No config found at:"
  Write-Host ("  - {0}" -f $ConfigPrimary)
  Write-Host ("  - {0}" -f $ConfigFallback)
  Write-Host "Copy a starter config from configs/ before validating."
  return $false
}

$normalized = $Command.ToLower()

switch ($normalized) {
  "help" {
    Show-Usage
  }
  "-h" {
    Show-Usage
  }
  "--help" {
    Show-Usage
  }
  "install" {
    Show-NodeVersion
    Require-Command npm
    npm install -g openclaw@latest
    if (Get-Command openclaw -ErrorAction SilentlyContinue) {
      openclaw --version
    }
  }
  "upgrade" {
    Show-NodeVersion
    Require-Command npm
    npm install -g openclaw@latest
    if (Get-Command openclaw -ErrorAction SilentlyContinue) {
      openclaw --version
    }
  }
  "doctor" {
    Require-Command openclaw
    openclaw doctor --fix
  }
  "audit" {
    Require-Command openclaw
    openclaw security audit --deep
  }
  "validate" {
    Require-Command openclaw
    if (Check-Config) {
      openclaw config validate --json
    } else {
      exit 1
    }
  }
  "bootstrap" {
    & $MyInvocation.MyCommand.Path install
    & $MyInvocation.MyCommand.Path doctor
    & $MyInvocation.MyCommand.Path audit
    & $MyInvocation.MyCommand.Path validate
  }
  default {
    Show-Usage
    exit 1
  }
}
