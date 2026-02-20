# Check Environment Variables Script
# Verifies that .env file exists and has required variables

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Environment Variables Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$envFile = ".env"

# Check if .env exists
if (-not (Test-Path $envFile)) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Run the setup script to create it:" -ForegroundColor Yellow
    Write-Host "   .\scripts\setup-env.ps1" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

Write-Host "✅ .env file found" -ForegroundColor Green
Write-Host ""

# Load .env file
$envVars = @{}
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $envVars[$key] = $value
    }
}

# Check required variables
$required = @("AI21_API_KEY")
$optional = @("EXA_API_KEY", "JAMBA_MODEL", "JAMBA_TEMPERATURE", "JAMBA_TOP_P", "JAMBA_MAX_TOKENS")

$allGood = $true

Write-Host "Required Variables:" -ForegroundColor Yellow
foreach ($var in $required) {
    if ($envVars.ContainsKey($var) -and $envVars[$var] -ne "" -and $envVars[$var] -notmatch "your_.*_here") {
        Write-Host "  ✅ $var = $($envVars[$var].Substring(0, [Math]::Min(20, $envVars[$var].Length)))..." -ForegroundColor Green
    } else {
        Write-Host "  ❌ $var = NOT SET or using placeholder" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host ""
Write-Host "Optional Variables:" -ForegroundColor Yellow
foreach ($var in $optional) {
    if ($envVars.ContainsKey($var) -and $envVars[$var] -ne "" -and $envVars[$var] -notmatch "your_.*_here") {
        Write-Host "  ✅ $var = $($envVars[$var])" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $var = Using default" -ForegroundColor Gray
    }
}

Write-Host ""

if ($allGood) {
    Write-Host "✅ All required environment variables are set!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "❌ Some required environment variables are missing!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Run the setup script to configure:" -ForegroundColor Yellow
    Write-Host "   .\scripts\setup-env.ps1" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}
