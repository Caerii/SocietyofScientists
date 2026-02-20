# Installation

## From Source

```bash
git clone https://github.com/Caerii/SocietyofScientists.git
cd SocietyofScientists
pip install -e .
```

## Dependencies Only

If you prefer not to install the package:

```bash
pip install -r requirements.txt
```

## Verify Installation

```python
import society_of_scientists
print(society_of_scientists.__version__)

from society_of_scientists import (
    create_society_of_mind_system,
    AI21JambaModelClient,
    get_tracker
)
print("Installation successful")
```

## Configure

Copy `.env.example` to `.env` and add your API keys:

```
AI21_API_KEY=your_ai21_key_here
EXA_API_KEY=your_exa_key_here
```

See [CONFIGURATION.md](CONFIGURATION.md) for all options.
