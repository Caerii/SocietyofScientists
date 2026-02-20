# Package Structure - Ready for pip install

## Package Name
**`societyofscientists`** - Install with `pip install societyofscientists`

## Clean Package Structure

```
society_of_scientists/          # Main package
├── __init__.py                 # Package exports (all public API)
├── __main__.py                 # CLI entry point
├── agent_list.py               # Agent prompts (internal)
├── agents/
│   ├── __init__.py
│   └── agent_factory.py        # Centralized agent creation
├── clients/
│   ├── __init__.py
│   └── jamba_client.py         # AI21 Jamba client with cost tracking
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuration management
├── tools/
│   ├── __init__.py
│   ├── exa_search.py           # Exa API with cache
│   ├── data_loader.py           # Load cached summaries
│   └── agent_context.py        # Context helpers
├── utils/
│   ├── __init__.py
│   └── cost_tracker.py          # Cost tracking
└── data/                        # Data files
    └── exported_*.txt          # Cached research summaries
```

## Public API (from `__init__.py`)

Users can import:

```python
from society_of_scientists import (
    # Agents
    create_society_of_mind_system,
    create_scientist_agents,
    create_grant_writers,
    
    # Clients
    AI21JambaModelClient,
    
    # Config
    Settings,
    
    # Tools
    ExaSearch,
    load_research_summaries,
    get_computer_vision_context,
    
    # Utils
    CostTracker,
    get_tracker,
)
```

## Installation

```bash
pip install societyofscientists
```

## Usage

```python
import society_of_scientists

# Use the package
from society_of_scientists import create_society_of_mind_system
```

## Files Organized

### ✅ Core Package Files
- All in `society_of_scientists/` with proper structure
- Proper `__init__.py` files
- Centralized exports

### ✅ Documentation
- All markdown docs in `docs/` subfolders
- Organized by category (api, cost-tracking, usage, development)

### ✅ Examples
- All examples in `examples/` folder
- Clear usage patterns

### ✅ Tests
- Test files in `tests/` folder

### ⚠️ Legacy Files (to clean up)
- `society_of_scientists/jamba_working.py` - Keep for now (backward compat)
- `society_of_scientists/exa*.py` - Duplicates, can be removed
- `society_of_scientists/tools.py` - Duplicate, can be removed
- `society_of_scientists/old/` - Archive, can be removed
