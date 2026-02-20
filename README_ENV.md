# Environment Variables Setup

## Quick Start

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

## Required Variables

- `AI21_API_KEY` - Your AI21 API key for Jamba models
- `EXA_API_KEY` - Your Exa API key (optional, can use cache-only mode)

## Optional Variables

- `JAMBA_MODEL` - Model name (default: `jamba-large-1.7-2025-07`)
- `JAMBA_TEMPERATURE` - Temperature setting (default: `0.7`)
- `JAMBA_TOP_P` - Top-p setting (default: `1.0`)
- `JAMBA_MAX_TOKENS` - Max tokens (default: `2048`)

## Security

⚠️ **Never commit `.env` files to git!** The `.gitignore` file is configured to exclude them.
