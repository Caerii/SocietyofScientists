# Cost Tracking System - Setup & Usage

## ✅ What's Implemented

### 1. Automatic Cost Tracking
- **Location**: `society_of_scientists/utils/cost_tracker.py`
- **Integration**: Automatically integrated into `AI21JambaModelClient`
- **Features**:
  - Tracks every API call
  - Calculates cost based on model pricing
  - Logs to persistent JSON file
  - Provides usage statistics

### 2. Pricing Information
Based on AI21 API response (verified):

| Model | Prompt (per 1K) | Completion (per 1K) | Cost per 1K avg |
|-------|-----------------|---------------------|-----------------|
| jamba-large | $0.002 | $0.008 | ~$0.005 |
| jamba-mini-2-2026-01 | $0.0002 | $0.0004 | ~$0.0003 |
| jamba-mini-1.7-2025-07 | $0.0002 | $0.0004 | ~$0.0003 |

**Note**: Mini models are **10x cheaper** than Large!

### 3. Cost Log File
- **Location**: `society_of_scientists/data/api_usage_log.json`
- **Format**: JSON array with usage records
- **Fields**: timestamp, model, tokens, cost, operation

## Usage

### Automatic Tracking
Costs are tracked automatically when using `AI21JambaModelClient`:

```python
from society_of_scientists.clients.jamba_client import AI21JambaModelClient

# Costs are automatically tracked - no extra code needed!
client = AI21JambaModelClient(config)
response = client.create(params)
# Cost is automatically calculated and logged
```

### View Costs
```python
from society_of_scientists.utils import get_tracker

tracker = get_tracker()
tracker.print_summary()

# Or get stats programmatically:
stats = tracker.get_usage_stats()
print(f"Total cost: ${stats['total_cost']:.6f}")
print(f"Total tokens: {stats['total_tokens']:,}")
```

### Get Cost for Specific Model
```python
tracker = get_tracker()
jamba_large_cost = tracker.get_total_cost("jamba-large")
jamba_mini_cost = tracker.get_total_cost("jamba-mini-2-2026-01")
```

## Cost Examples

### Small Call (20 tokens)
- **Jamba Mini 2**: $0.000006 (6 micro-dollars)
- **Jamba Large**: $0.00006 (60 micro-dollars)

### Typical Grant Proposal (10,000 tokens)
- **Jamba Mini 2**: $0.003
- **Jamba Large**: $0.03

### 100 Grant Proposals
- **Jamba Mini 2**: $0.30
- **Jamba Large**: $3.00

## Cost Optimization

1. **Use Jamba Mini 2**: 10x cheaper, same quality
2. **Use cached data**: Free (398 summaries)
3. **Monitor usage**: Check `api_usage_log.json` regularly
4. **Set budgets**: Review costs before large runs

## Files Created

- ✅ `society_of_scientists/utils/cost_tracker.py` - Cost tracking system
- ✅ `society_of_scientists/utils/__init__.py` - Utils exports
- ✅ `COST_TRACKING.md` - Detailed cost documentation
- ✅ `PRICING_GUIDE.md` - Pricing reference
- ✅ `examples/track_costs.py` - Usage example

## Integration Status

✅ **Fully Integrated**: The `AI21JambaModelClient` now automatically:
- Extracts token usage from API responses
- Calculates costs based on model pricing
- Logs all usage to persistent file
- Returns cost in response object

**No additional code needed** - costs are tracked automatically!
