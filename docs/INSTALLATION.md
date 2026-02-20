# Installation Guide

## Install from PyPI (when published)

```bash
pip install societyofscientists
```

## Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/SocietyofScientists.git
cd SocietyofScientists

# Install in development mode
pip install -e .

# Or install directly
pip install .
```

## Development Installation

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Or install dependencies separately
pip install -r requirements.txt
```

## Verify Installation

```python
import society_of_scientists
print(society_of_scientists.__version__)

# Test imports
from society_of_scientists import (
    create_society_of_mind_system,
    AI21JambaModelClient,
    get_tracker
)
print("Installation successful!")
```

## Configuration

1. Copy `.env.example` to `.env`
2. Add your API keys:
   ```
   AI21_API_KEY=your_ai21_key_here
   EXA_API_KEY=your_exa_key_here
   ```

## Quick Start

```python
from society_of_scientists import create_society_of_mind_system

# Create system
agent, user_proxy, manager = create_society_of_mind_system(
    task="Your research task here"
)

# Run
result = user_proxy.initiate_chat(agent, message="Your research task here")
```
