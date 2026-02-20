"""Example: Using cached research summaries instead of Exa API calls."""
from society_of_scientists.tools import (
    ExaSearch,
    exa_search_function,
    get_computer_vision_context,
    get_ai_language_models_context,
    get_ai_hardware_context,
    get_summary_count
)

# Example 1: Use ExaSearch with cache by default (no API calls)
print("=== Example 1: Using cached data ===")
search = ExaSearch(use_cache=True)  # use_cache=True is default
result = search.search_papers("computer vision", num_results=10, use_cache_first=True)
print(f"Found {len(result.results)} cached summaries")
for i, paper in enumerate(result.results[:3], 1):
    print(f"{i}. {paper.summary[:100]}...")

# Example 2: Use the AutoGen-compatible function (uses cache by default)
print("\n=== Example 2: Using exa_search_function ===")
formatted_results = exa_search_function("neural networks", use_cache=True)
print(formatted_results[:500] + "...")

# Example 3: Get context for specific agent topics
print("\n=== Example 3: Getting agent-specific context ===")
cv_context = get_computer_vision_context()
print(f"Computer Vision summaries: {len(cv_context.split('summary:')) - 1} papers")

llm_context = get_ai_language_models_context()
print(f"LLM summaries: {len(llm_context.split('summary:')) - 1} papers")

# Example 4: Check what data is available
print("\n=== Example 4: Summary counts ===")
counts = get_summary_count()
for topic, count in counts.items():
    print(f"{topic}: {count} summaries")

# Example 5: Force API call (if you have Exa API key)
# search_api = ExaSearch(use_cache=False)
# result = search_api.search_papers("new research", use_cache_first=False)
