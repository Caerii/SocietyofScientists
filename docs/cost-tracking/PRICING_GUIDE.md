# AI21 Jamba Pricing Guide

## Current Pricing (2025)

Based on API response from `https://api.ai21.com/studio/v1/models`:

### Jamba Large 1.7 / jamba-large
- **Prompt**: $0.002 per 1,000 tokens ($0.000002 per token)
- **Completion**: $0.008 per 1,000 tokens ($0.000008 per token)
- **Cost per 1K tokens (avg)**: ~$0.005
- **Example**: 1,000 prompt + 500 completion = $0.006

### Jamba Mini 2 (Recommended - 10x Cheaper)
- **Prompt**: $0.0002 per 1,000 tokens ($0.0000002 per token)
- **Completion**: $0.0004 per 1,000 tokens ($0.0000004 per token)
- **Cost per 1K tokens (avg)**: ~$0.0003
- **Example**: 1,000 prompt + 500 completion = $0.0004

### Jamba Mini 1.7
- **Prompt**: $0.0002 per 1,000 tokens
- **Completion**: $0.0004 per 1,000 tokens
- Same pricing as Mini 2

## Cost Examples

### Small Request (50 tokens total)
- **Jamba Mini 2**: ~$0.000015 (essentially free)
- **Jamba Large**: ~$0.00015

### Medium Request (1,000 tokens total)
- **Jamba Mini 2**: ~$0.0003
- **Jamba Large**: ~$0.003

### Large Request (10,000 tokens total)
- **Jamba Mini 2**: ~$0.003
- **Jamba Large**: ~$0.03

### Full Context (256K tokens)
- **Jamba Mini 2**: ~$0.077
- **Jamba Large**: ~$0.77

## Cost Tracking

The system automatically tracks all costs. View usage:

```python
from society_of_scientists.utils import get_tracker

tracker = get_tracker()
tracker.print_summary()
```

Costs are logged to: `society_of_scientists/data/api_usage_log.json`

## Cost Optimization

1. **Use Jamba Mini 2**: 10x cheaper, latest version
2. **Use cached data**: Free (398 summaries available)
3. **Batch operations**: Reduce API calls
4. **Monitor regularly**: Check `api_usage_log.json`

## Estimated Monthly Costs

### Light Usage (100 requests/day, ~1K tokens each)
- **Jamba Mini 2**: ~$0.90/month
- **Jamba Large**: ~$9/month

### Heavy Usage (1,000 requests/day, ~2K tokens each)
- **Jamba Mini 2**: ~$18/month
- **Jamba Large**: ~$180/month
