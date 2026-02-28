# SajiloHR bootstrap (Windows PowerShell)
# Creates venv, installs dependencies.

$ErrorActionPreference = "Stop"

Write-Host "[SajiloHR] Bootstrapping..." -ForegroundColor Cyan

if (!(Test-Path .\requirements.txt)) {
  Write-Host "Run this from the project root (where requirements.txt exists)." -ForegroundColor Red
  exit 1
}

if (!(Test-Path .\.venv)) {
  python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "" 
Write-Host "[SajiloHR] Done." -ForegroundColor Green
Write-Host "Next:" -ForegroundColor Green
Write-Host "  1) Start MongoDB (mongod)" 
Write-Host "  2) Terminal A: python -m server.app" 
Write-Host "  3) Terminal B: python -m client.main" 
