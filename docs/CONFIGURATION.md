# Configuration

## Environment Variables

### Setup

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```env
   AI21_API_KEY=your_actual_ai21_key_here
   EXA_API_KEY=your_actual_exa_key_here
   ```

3. The application will automatically load these from the `.env` file.

### PowerShell Setup (Windows)

Run the setup script:
```powershell
.\scripts\setup-env.ps1
```

Or create `.env` manually:
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

### Verify Setup

```powershell
.\scripts\check-env.ps1
```

## Required Variables

- **AI21_API_KEY** (Required) - Your AI21 API key for Jamba models
- **EXA_API_KEY** (Optional) - Your Exa API key (can use cache-only mode if not set)

## Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `JAMBA_MODEL` | `jamba-large-1.7-2025-07` | Model name |
| `JAMBA_TEMPERATURE` | `0.7` | Temperature setting |
| `JAMBA_TOP_P` | `1.0` | Top-p setting |
| `JAMBA_MAX_TOKENS` | `2048` | Max tokens |
| `AGENT_WORK_DIR` | `coding` | Working directory for agents |
| `AGENT_USE_DOCKER` | `false` | Use Docker for code execution |

## Security

Never commit `.env` files to git. The `.gitignore` file is configured to exclude them.

## Troubleshooting

### PowerShell Execution Policy

If you get an execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
