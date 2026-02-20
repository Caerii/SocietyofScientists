# Start Backend Server Script
# This script starts the FastAPI backend server

Write-Host "Starting Society of Scientists Backend Server..." -ForegroundColor Cyan
Write-Host ""

# Change to project root
Set-Location $PSScriptRoot\..

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "⚠️  Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Run .\scripts\setup-env.ps1 first to create it." -ForegroundColor Yellow
    Write-Host ""
}

# Start the server
Write-Host "Starting server on http://localhost:8000..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

python -m society_of_scientists.api.server
