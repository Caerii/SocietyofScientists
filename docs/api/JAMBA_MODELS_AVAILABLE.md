# Available Jamba Models from AI21 API

## ✅ Models Listed by API

The AI21 API endpoint `https://api.ai21.com/studio/v1/models` returned the following available models:

### 1. Jamba Large 1.7
- **Model ID**: `jamba-large-1.7-2025-07`
- **Name**: AI21: Jamba Large 1.7
- **Updated**: 2025-07
- **Context Length**: 256,000 tokens
- **Quantization**: FP8
- **Max Completion Tokens**: 4,096
- **Pricing**:
  - Prompt: $0.000002 per token
  - Completion: $0.000008 per token

### 2. Jamba Mini 1.7
- **Model ID**: `jamba-mini-1.7-2025-07`
- **Name**: AI21: Jamba Mini 1.7
- **Updated**: 2025-07
- **Context Length**: 256,000 tokens
- **Quantization**: FP8
- **Max Completion Tokens**: 4,096
- **Pricing**:
  - Prompt: $0.0000002 per token
  - Completion: $0.0000004 per token

### 3. Jamba Mini 2 (Latest)
- **Model ID**: `jamba-mini-2-2026-01`
- **Name**: AI21: Jamba Mini 2
- **Updated**: 2026-01 (Most recent)
- **Context Length**: 256,000 tokens
- **Quantization**: FP8
- **Max Completion Tokens**: 4,096
- **Pricing**:
  - Prompt: $0.0000002 per token
  - Completion: $0.0000004 per token

## ⚠️ Access Status

**Current Issue**: All models return **403 Access Denied** when attempting to use them.

**What This Means**:
- ✅ The API key is **valid** (can query models endpoint)
- ✅ Models are **available** (listed in API response)
- ❌ Account **doesn't have access** to use these models

**Possible Reasons**:
1. Account needs to be upgraded/enabled for Jamba model access
2. Account may need to request access to Jamba models
3. Billing/payment setup may be required
4. Model access may require special permissions

## 🔧 Recommended Actions

1. **Check AI21 Account Dashboard**:
   - Log into https://studio.ai21.com
   - Check account status and model access
   - Verify billing/payment setup

2. **Update Code to Use Available Models**:
   - Replace `jamba-1.5-large` with one of the available models:
     - `jamba-large-1.7-2025-07` (most capable)
     - `jamba-mini-2-2026-01` (latest, most cost-effective)
     - `jamba-mini-1.7-2025-07` (older mini version)

3. **Update Model Name in Configuration**:
   ```python
   # In .env:
   JAMBA_MODEL=jamba-large-1.7-2025-07    # Most capable
   # or
   JAMBA_MODEL=jamba-mini-2-2026-01       # Latest & cheapest
   ```

## 📊 Model Comparison

| Model | Context | Cost (Prompt) | Cost (Completion) | Best For |
|-------|---------|---------------|-------------------|----------|
| jamba-large-1.7-2025-07 | 256K | $0.000002 | $0.000008 | High quality, complex tasks |
| jamba-mini-2-2026-01 | 256K | $0.0000002 | $0.0000004 | Cost-effective, latest version |
| jamba-mini-1.7-2025-07 | 256K | $0.0000002 | $0.0000004 | Cost-effective, older version |

**Recommendation**: Use `jamba-mini-2-2026-01` - it's the latest version and 10x cheaper than the large model.
