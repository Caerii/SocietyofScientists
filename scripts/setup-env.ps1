# Setup Environment Variables Script
# This script helps you create a .env file with your API keys

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Society of Scientists - Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$envFile = ".env"
$envExample = ".env.example"

# Check if .env already exists
if (Test-Path $envFile) {
    Write-Host "⚠️  .env file already exists!" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (y/N)"
    if ($overwrite -ne "y" -and $overwrite -ne "Y") {
        Write-Host "Keeping existing .env file. Exiting." -ForegroundColor Green
        exit 0
    }
}

# Check if .env.example exists
if (-not (Test-Path $envExample)) {
    Write-Host "❌ .env.example file not found!" -ForegroundColor Red
    Write-Host "Creating .env.example file..." -ForegroundColor Yellow
    
    $exampleContent = @"
# Society of Scientists - Environment Variables
# Copy this file to .env and fill in your API keys

# AI21 Jamba API Configuration
AI21_API_KEY=your_ai21_api_key_here
JAMBA_MODEL=jamba-large-1.7-2025-07
JAMBA_TEMPERATURE=0.7
JAMBA_TOP_P=1.0
JAMBA_MAX_TOKENS=2048

# Exa API Configuration
EXA_API_KEY=your_exa_api_key_here

# Agent Configuration
AGENT_WORK_DIR=coding
AGENT_USE_DOCKER=false

# Data Configuration (optional)
DATA_DIR=
"@
    Set-Content -Path $envExample -Value $exampleContent
    Write-Host "✅ Created .env.example" -ForegroundColor Green
}

# Read example file
$exampleContent = Get-Content $envExample -Raw

Write-Host ""
Write-Host "Please enter your API keys:" -ForegroundColor Yellow
Write-Host ""

# Get AI21 API Key
$ai21Key = Read-Host "Enter your AI21 API Key (or press Enter to skip)"
if ([string]::IsNullOrWhiteSpace($ai21Key)) {
    $ai21Key = "your_ai21_api_key_here"
    Write-Host "⚠️  Using placeholder for AI21_API_KEY" -ForegroundColor Yellow
} else {
    Write-Host "✅ AI21 API Key set" -ForegroundColor Green
}

# Get Exa API Key
$exaKey = Read-Host "Enter your Exa API Key (or press Enter to skip - optional)"
if ([string]::IsNullOrWhiteSpace($exaKey)) {
    $exaKey = "your_exa_api_key_here"
    Write-Host "⚠️  Using placeholder for EXA_API_KEY (optional)" -ForegroundColor Yellow
} else {
    Write-Host "✅ Exa API Key set" -ForegroundColor Green
}

# Replace placeholders
$envContent = $exampleContent
$envContent = $envContent -replace "your_ai21_api_key_here", $ai21Key
$envContent = $envContent -replace "your_exa_api_key_here", $exaKey

# Write .env file
Set-Content -Path $envFile -Value $envContent

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ .env file created successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Location: $((Get-Item $envFile).FullName)" -ForegroundColor Gray
Write-Host ""
Write-Host "⚠️  Remember:" -ForegroundColor Yellow
Write-Host "   - Never commit .env to git" -ForegroundColor Yellow
Write-Host "   - Keep your API keys secure" -ForegroundColor Yellow
Write-Host ""
