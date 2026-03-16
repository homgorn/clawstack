Param(
  [Parameter(Position = 0)]
  [string]$Command = "all"
)

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

function Require-Command {
  param([string]$Name)
  if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
    throw "Missing command: $Name"
  }
}

function Run-ConfigLint {
  Write-Host "Running starter config lint..."
  & python (Join-Path $Root "scripts\check_configs.py")
}

function Run-Tests {
  Write-Host "Running backend tests (pytest)..."
  try {
    & python -m pytest --version | Out-Null
  } catch {
    throw "pytest not installed. Install dev deps with: python -m pip install -e `\".[dev]`\""
  }
  & python -m pytest (Join-Path $Root "backend\tests")
}

Require-Command python

switch ($Command.ToLower()) {
  "lint" {
    Run-ConfigLint
  }
  "tests" {
    Run-Tests
  }
  "all" {
    Run-ConfigLint
    Run-Tests
  }
  default {
    Write-Host "Usage: scripts\\run_checks.ps1 [lint|tests|all]"
    exit 1
  }
}

Write-Host "All checks passed."
