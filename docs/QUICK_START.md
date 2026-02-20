# Quick Start Guide

## Installation

```bash
pip install societyofscientists
```

Or from source:
```bash
git clone <repo-url>
cd SocietyofScientists
pip install -e .
```

## Basic Usage

### 1. Simple Multi-Agent System

```python
from society_of_scientists import create_society_of_mind_system

# Create the system
agent, user_proxy, manager = create_society_of_mind_system(
    task="Propose a novel neural network architecture"
)

# Run
result = user_proxy.initiate_chat(agent, message="Propose a novel neural network architecture")
```

### 2. Command Line

```bash
python -m society_of_scientists "Your research task here"
```

### 3. Use Cached Research Data

```python
from society_of_scientists import get_computer_vision_context, ExaSearch

# Get cached summaries (no API calls)
cv_context = get_computer_vision_context()

# Or use ExaSearch (uses cache by default)
search = ExaSearch()
results = search.search_papers("computer vision")
```

### 4. Track Costs

```python
from society_of_scientists import get_tracker

# Costs are automatically tracked
tracker = get_tracker()
tracker.print_summary()
```

## Configuration

1. Copy `.env.example` to `.env`
2. Add your API keys:
   ```
   AI21_API_KEY=your_key_here
   EXA_API_KEY=your_key_here
   ```

## Examples

See `examples/` folder for:
- `basic_usage.py` - Simple example
- `multi_agent_system.py` - Full system example
- `track_costs.py` - Cost tracking example
- `use_cached_data.py` - Cached data usage

## Documentation

- [Full Documentation](docs/INDEX.md)
- [API Docs](docs/api/)
- [Cost Tracking](docs/cost-tracking/)
- [Usage Guides](docs/usage/)
