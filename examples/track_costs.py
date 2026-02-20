"""Example: How to track API costs."""
from society_of_scientists.utils import get_tracker

# Get the cost tracker
tracker = get_tracker()

# Example: Record usage after an API call
# This would be called from your AI21 client wrapper
tracker.record_usage(
    model="jamba-large",
    prompt_tokens=150,
    completion_tokens=50,
    operation="Grant proposal generation"
)

# Record another call
tracker.record_usage(
    model="jamba-mini-2-2026-01",
    prompt_tokens=200,
    completion_tokens=100,
    operation="Research summary"
)

# Print summary
tracker.print_summary()

# Get statistics programmatically
stats = tracker.get_usage_stats()
print(f"\nTotal cost so far: ${stats['total_cost']:.6f}")

# Get cost for specific model
jamba_large_cost = tracker.get_total_cost("jamba-large")
print(f"Jamba Large cost: ${jamba_large_cost:.6f}")
