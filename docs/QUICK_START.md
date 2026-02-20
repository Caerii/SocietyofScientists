# Quick Start

## Install

```bash
pip install -e .
```

Or install dependencies directly:
```bash
pip install -r requirements.txt
```

## Configure

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
AI21_API_KEY=your_key_here
EXA_API_KEY=your_key_here   # optional — cached data works without this
```

## Run

### Python API

```python
from society_of_scientists import create_society_of_mind_system

agent, user_proxy, manager = create_society_of_mind_system(
    task="Propose a novel neural network architecture"
)

result = user_proxy.initiate_chat(agent, message="Propose a novel neural network architecture")
```

### Command Line

```bash
python -m society_of_scientists "Your research task here"
```

### Use Cached Research Data

The system includes 398 cached research paper summaries. No API key needed:

```python
from society_of_scientists import get_computer_vision_context, ExaSearch

# Get cached summaries directly
cv_context = get_computer_vision_context()

# Or use ExaSearch (falls back to cache automatically)
search = ExaSearch()
results = search.search_papers("computer vision")
```

### Track Costs

```python
from society_of_scientists import get_tracker

tracker = get_tracker()
tracker.print_summary()
```

## Examples

See the `examples/` folder:
- `basic_usage.py` — Minimal working example
- `multi_agent_system.py` — Full system with all agents
- `track_costs.py` — Cost tracking
- `use_cached_data.py` — Working with cached research summaries

## Next Steps

- [Configuration](CONFIGURATION.md) — All environment variables and options
- [Cost Tracking](cost-tracking/COST_TRACKING.md) — Pricing and optimization
- [Package Structure](development/PACKAGE_STRUCTURE.md) — How the code is organized
