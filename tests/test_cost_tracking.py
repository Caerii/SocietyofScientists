"""Test cost tracking with real API call."""
from society_of_scientists.clients.jamba_client import AI21JambaModelClient
from society_of_scientists.utils import get_tracker

print("=" * 60)
print("Testing Cost Tracking with Real API Call")
print("=" * 60)

# Create client with working key
config = {
    "model": "jamba-large",
    "api_key": "9f7fbfd0-52aa-460a-9cdb-66b39947a6b3",
    "temperature": 0.7,
    "top_p": 1.0,
    "max_tokens": 50
}

client = AI21JambaModelClient(config)

# Make a test call
print("\nMaking API call...")
params = {
    "messages": [{"role": "user", "content": "Say hello in one sentence."}],
    "max_tokens": 50
}

response = client.create(params)

# Check usage
usage = AI21JambaModelClient.get_usage(response)
print(f"\nUsage:")
print(f"  Prompt tokens: {usage['prompt_tokens']}")
print(f"  Completion tokens: {usage['completion_tokens']}")
print(f"  Total tokens: {usage['total_tokens']}")
print(f"  Cost: ${usage['cost']:.6f}")

# Get tracker summary
print("\n" + "=" * 60)
tracker = get_tracker()
tracker.print_summary()
