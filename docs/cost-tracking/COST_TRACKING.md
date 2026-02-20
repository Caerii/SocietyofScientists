# Cost Tracking & Measurement

## AI21 Jamba Model Pricing

Based on API response and current pricing (as of 2025):

### Jamba Large 1.7
- **Model**: `jamba-large-1.7-2025-07` or `jamba-large`
- **Prompt**: $0.002 per 1,000 tokens ($0.000002 per token)
- **Completion**: $0.008 per 1,000 tokens ($0.000008 per token)
- **Context**: 256,000 tokens
- **Best for**: High-quality, complex tasks

### Jamba Mini 2 (Recommended - Cheapest)
- **Model**: `jamba-mini-2-2026-01`
- **Prompt**: $0.0002 per 1,000 tokens ($0.0000002 per token)
- **Completion**: $0.0004 per 1,000 tokens ($0.0000004 per token)
- **Context**: 256,000 tokens
- **Best for**: Cost-effective operations (10x cheaper than Large)

### Jamba Mini 1.7
- **Model**: `jamba-mini-1.7-2025-07`
- **Prompt**: $0.0002 per 1,000 tokens ($0.0000002 per token)
- **Completion**: $0.0004 per 1,000 tokens ($0.0000004 per token)
- **Context**: 256,000 tokens

## Cost Calculation Examples

### Example 1: Small Request (Jamba Mini 2)
- Prompt: 100 tokens
- Completion: 50 tokens
- **Cost**: (100/1000 × $0.0002) + (50/1000 × $0.0004) = **$0.00004** (4 cents per 1000 requests)

### Example 2: Large Request (Jamba Large)
- Prompt: 1,000 tokens
- Completion: 500 tokens
- **Cost**: (1000/1000 × $0.002) + (500/1000 × $0.008) = **$0.006** (6 cents)

### Example 3: Full Context (Jamba Mini 2)
- Prompt: 200,000 tokens
- Completion: 4,000 tokens
- **Cost**: (200000/1000 × $0.0002) + (4000/1000 × $0.0004) = **$0.0416** (~4 cents)

## Cost Tracking Implementation

The system now automatically tracks costs using `society_of_scientists.utils.cost_tracker`:

### Features:
- ✅ Automatic cost calculation based on model pricing
- ✅ Token usage tracking (prompt + completion)
- ✅ Persistent logging to JSON file
- ✅ Per-model cost breakdown
- ✅ Total cost aggregation

### Usage:

```python
from society_of_scientists.utils import get_tracker

# Costs are automatically tracked when using Jamba client
# View summary:
tracker = get_tracker()
tracker.print_summary()

# Get statistics:
stats = tracker.get_usage_stats()
print(f"Total cost: ${stats['total_cost']:.6f}")
```

### Cost Log Location:
- File: `society_of_scientists/data/api_usage_log.json`
- Format: JSON with timestamp, model, tokens, cost per call

## Cost Optimization Tips

1. **Use Jamba Mini 2**: 10x cheaper than Large, latest version
2. **Use Cached Data**: Exported summaries avoid API calls (free)
3. **Batch Operations**: Group requests when possible
4. **Monitor Usage**: Check `api_usage_log.json` regularly
5. **Set Budget Alerts**: Review costs before large runs

## Estimated Costs

### Typical Grant Proposal Generation:
- ~10-15 agent interactions
- ~500 tokens per interaction (prompt + completion)
- **Jamba Mini 2**: ~$0.0001 per proposal
- **Jamba Large**: ~$0.001 per proposal

### 100 Grant Proposals:
- **Jamba Mini 2**: ~$0.01 (1 cent)
- **Jamba Large**: ~$0.10 (10 cents)

## Cost Tracking in Code

The `AI21JambaModelClient` now automatically:
1. Extracts token usage from API responses
2. Calculates cost based on model pricing
3. Records usage to persistent log
4. Returns cost in response object

No additional code needed - costs are tracked automatically!
