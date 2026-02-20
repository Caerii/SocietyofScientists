# Environment Variables Setup Guide

## Quick Setup

### Option 1: Use PowerShell Script (Recommended)

Run the setup script:
```powershell
.\scripts\setup-env.ps1
```

This will:
- Create `.env.example` if it doesn't exist
- Prompt you for your API keys
- Create `.env` file with your keys

### Option 2: Manual Setup

1. Copy the example file:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` with your favorite editor:
   ```powershell
   notepad .env
   # or
   code .env
   ```

3. Fill in your API keys:
   ```env
   AI21_API_KEY=your_actual_ai21_key_here
   EXA_API_KEY=your_actual_exa_key_here
   ```

### Option 3: PowerShell One-Liner

Create `.env` directly:
```powershell
@"
AI21_API_KEY=your_ai21_key_here
EXA_API_KEY=your_exa_key_here
JAMBA_MODEL=jamba-large-1.7-2025-07
JAMBA_TEMPERATURE=0.7
JAMBA_TOP_P=1.0
JAMBA_MAX_TOKENS=2048
AGENT_WORK_DIR=coding
AGENT_USE_DOCKER=false
"@ | Out-File -FilePath .env -Encoding utf8
```

Then edit `.env` and replace the placeholder values.

## Verify Setup

Check that your environment variables are set correctly:
```powershell
.\scripts\check-env.ps1
```

## Required Variables

- **AI21_API_KEY** (Required) - Your AI21 API key for Jamba models
- **EXA_API_KEY** (Optional) - Your Exa API key (can use cache-only mode if not set)

## Optional Variables

- `JAMBA_MODEL` - Model name (default: `jamba-large-1.7-2025-07`)
- `JAMBA_TEMPERATURE` - Temperature setting (default: `0.7`)
- `JAMBA_TOP_P` - Top-p setting (default: `1.0`)
- `JAMBA_MAX_TOKENS` - Max tokens (default: `2048`)
- `AGENT_WORK_DIR` - Working directory for agents (default: `coding`)
- `AGENT_USE_DOCKER` - Use Docker for code execution (default: `false`)

## Security Notes

⚠️ **Important:**
- Never commit `.env` files to git
- The `.gitignore` file is configured to exclude `.env`
- Keep your API keys secure and private
- Don't share your `.env` file

## Troubleshooting

### Script Execution Policy

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### File Not Found

Make sure you're in the project root directory:
```powershell
cd F:\Github\SocietyofScientists
```

### Check Current Values

View your current environment variables (without showing full keys):
```powershell
.\scripts\check-env.ps1
```
