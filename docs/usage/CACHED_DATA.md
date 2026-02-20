# Using Cached Research Data

The exported `.txt` files in `society_of_scientists/data/` are now **automatically used by default** to avoid Exa API calls. This provides:

1. **Faster responses** - No API latency
2. **Cost savings** - No API usage charges
3. **Reliability** - Works offline
4. **Consistent examples** - Same data every time

## How It Works

### Default Behavior
By default, all search functions use cached data from the exported files:

```python
from society_of_scientists.tools import ExaSearch, exa_search_function

# Uses cache by default (no API call)
search = ExaSearch()  # use_cache=True is default
result = search.search_papers("computer vision")
```

### Getting Agent Context
Load research summaries for specific agent topics:

```python
from society_of_scientists.tools import (
    get_computer_vision_context,
    get_ai_language_models_context,
    get_ai_hardware_context,
    get_computational_neuroscience_context
)

# Get formatted summaries for agent prompts
cv_summaries = get_computer_vision_context()
llm_summaries = get_ai_language_models_context()
```

### Using in Agent Prompts
You can now dynamically load summaries instead of hardcoding them:

```python
from society_of_scientists.tools import get_computer_vision_context

# Load summaries dynamically
summaries = get_computer_vision_context()

agent_prompt = f"""
You are a computer vision engineer. 
You have access to recent research:

{summaries}

Use this knowledge to inform your responses.
"""
```

### Force API Call (Optional)
If you need fresh data from Exa API:

```python
# Force API call instead of cache
search = ExaSearch(use_cache=False)
result = search.search_papers("new topic", use_cache_first=False)
```

## Available Data

The cached files contain:
- `exported_computational_neuroscience_100.txt` - ~100 neuroscience papers
- `exported_computer_vision_100.txt` - ~100 computer vision papers  
- `exported_large_language_models_100.txt` - ~100 LLM papers
- `exported_hardware_for_AI_100.txt` - ~100 AI hardware papers

Total: ~400 research paper summaries ready to use!

## Benefits

✅ **No API calls by default** - Uses local cached data  
✅ **Fast** - Instant access to summaries  
✅ **Free** - No Exa API costs  
✅ **Reliable** - Works without internet  
✅ **Easy to update** - Just regenerate files when needed
