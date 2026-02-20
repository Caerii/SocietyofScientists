# Start Backend Server in Background
# This script starts the FastAPI backend server as a background process

Write-Host "Starting Society of Scientists Backend Server in background..." -ForegroundColor Cyan
Write-Host ""

# Change to project root
Set-Location $PSScriptRoot\..

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "⚠️  Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Run .\scripts\setup-env.ps1 first to create it." -ForegroundColor Yellow
    Write-Host ""
}

# Start the server in background
$job = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    python -m society_of_scientists.api.server
}

Write-Host "✅ Backend server started in background (Job ID: $($job.Id))" -ForegroundColor Green
Write-Host ""
Write-Host "To check status: Get-Job | Receive-Job" -ForegroundColor Gray
Write-Host "To stop: Stop-Job $($job.Id); Remove-Job $($job.Id)" -ForegroundColor Gray
Write-Host ""
Write-Host "Server should be available at: http://localhost:8000" -ForegroundColor Cyan

# Wait a moment and check if it's running
Start-Sleep -Seconds 3
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/" -TimeoutSec 2 -UseBasicParsing
    Write-Host "✅ Server is responding!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Server may still be starting. Check logs with: Get-Job | Receive-Job" -ForegroundColor Yellow
}
