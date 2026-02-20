# Society of Scientists - Science Funding Grant Amplification Tool

A multi-agent AI system that simulates a collaborative research environment where specialized scientist agents work together to generate comprehensive research grant proposals. The system leverages multiple AI agents with distinct expertise areas to synthesize novel research ideas and create detailed grant applications.

## Overview

Society of Scientists implements a multi-agent framework where different AI agents play specialized roles:

- **Expert Scientists**: Domain specialists in computational neuroscience, computer vision, AI/language models, and AI hardware
- **Orchestrators**: Planner and assistant agents that coordinate the research proposal process
- **Grant Writers**: Specialized agents that expand on different aspects of grant proposals (hypothesis, objectives, methodology, ethics, budget, novelty, comparison)
- **Critic Agent**: Reviews and provides critical feedback on proposals

The system uses a "Society of Mind" approach where agents collaborate through group chat to synthesize interdisciplinary research proposals.

## Features

- **Multi-Agent Collaboration**: Multiple specialized agents work together using AutoGen's GroupChat framework
- **AI21 Jamba Integration**: Uses AI21's Jamba-1.5-large model for agent reasoning
- **Research Paper Search**: Integration with Exa API for finding and retrieving relevant research papers
- **Comprehensive Grant Writing**: Generates detailed grant proposals with all required sections
- **Interdisciplinary Synthesis**: Combines insights from multiple scientific domains

## Project Structure

```
SocietyofScientists/
├── society_of_scientists/    # Main package (pip installable)
│   ├── __init__.py          # Package exports
│   ├── __main__.py          # CLI entry point
│   ├── agent_list.py        # Agent prompt definitions
│   ├── agents/              # Agent creation and management
│   │   ├── agent_factory.py # Centralized agent creation
│   │   └── __init__.py
│   ├── clients/             # API clients
│   │   ├── jamba_client.py  # AI21 Jamba client with cost tracking
│   │   └── __init__.py
│   ├── config/              # Configuration management
│   │   ├── settings.py      # Centralized settings
│   │   └── __init__.py
│   ├── tools/               # Tools and utilities
│   │   ├── exa_search.py    # Exa API with cache support
│   │   ├── data_loader.py   # Load cached research summaries
│   │   ├── agent_context.py # Agent context helpers
│   │   └── __init__.py
│   ├── utils/               # Utility functions
│   │   ├── cost_tracker.py  # Cost tracking and measurement
│   │   └── __init__.py
│   └── data/                # Data files (cached summaries)
├── docs/                    # Documentation
│   ├── api/                 # API documentation
│   ├── cost-tracking/       # Cost tracking docs
│   ├── usage/               # Usage guides
│   └── development/         # Development docs
├── examples/                # Usage examples
├── tests/                   # Test files
├── README.md               # This file
├── setup.py                # Package setup
└── requirements.txt        # Dependencies
```

## Requirements

- Python 3.10+
- AutoGen (AG2)
- AI21 SDK (for Jamba models)
- Exa API (for research paper search)
- Panel (for UI components, optional)

## Installation

### Install from PyPI (Recommended)

```bash
pip install societyofscientists
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/SocietyofScientists.git
cd SocietyofScientists

# Install in development mode
pip install -e .

# Or install directly
pip install .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Configuration

### API Keys

You'll need to configure API keys for:

1. **AI21 Jamba API**: Set your API key in the configuration files
2. **Exa API**: Set your Exa API key for research paper search

Update the API keys in:
- `society_of_scientists/jamba_working.py`
- `society_of_scientists/exa_agent.py`
- `society_of_scientists/exa_files.py`

## Quick Start

### Basic Usage

```python
from society_of_scientists import create_society_of_mind_system

# Create the multi-agent system
agent, user_proxy, manager = create_society_of_mind_system(
    task="Propose a novel neural network architecture"
)

# Run the system
result = user_proxy.initiate_chat(agent, message="Propose a novel neural network architecture")
```

### Command Line Usage

```bash
python -m society_of_scientists "Your research task here"
```

### Using Cached Research Data

```python
from society_of_scientists import get_computer_vision_context, ExaSearch

# Use cached summaries (free, no API calls)
cv_summaries = get_computer_vision_context()

# Or use Exa search (uses cache by default)
search = ExaSearch()
results = search.search_papers("computer vision")  # Uses cached data
```

### Track Costs

```python
from society_of_scientists import get_tracker

# Costs are automatically tracked
tracker = get_tracker()
tracker.print_summary()  # View usage and costs
```

See `examples/` folder for more usage examples.

## Agent Roles

### Expert Scientists
- **Computer Vision Engineer**: Expert in computer vision, image processing, and visual AI
- **AI/Language Models Scientist**: Expert in large language models, NLP, and AI systems
- **AI Hardware Engineer**: Expert in AI hardware, chips, and computational infrastructure

### Orchestrators
- **Planner**: Creates comprehensive plans for grant proposal development
- **Assistant**: Coordinates tool usage and task execution

### Grant Writers
- **Scientist**: Synthesizes initial grant proposal with all key aspects
- **Hypothesis Agent**: Expands and refines the hypothesis section
- **Objective Agent**: Expands on research objectives and expected outcomes
- **Methodology Agent**: Details research methods, algorithms, and techniques
- **Ethics Agent**: Addresses ethical considerations and societal implications
- **Budget Agent**: Provides detailed budget estimates
- **Novelty Agent**: Highlights novel aspects and advances over existing work
- **Comparison Agent**: Compares with other approaches and technologies

### Review
- **Critic Agent**: Provides comprehensive review, strengths/weaknesses, and improvements

## Example Output

The system generates comprehensive grant proposals including:
- Detailed hypothesis with scientific reasoning
- Quantitative objectives with specific metrics
- Comprehensive methodology with algorithms and datasets
- Novelty assessment
- Ethical considerations
- Detailed budget breakdown
- Comparison with existing approaches
- Critical review and suggestions

## Documentation

Comprehensive documentation is available in the `docs/` folder:

- **API Documentation** (`docs/api/`) - API keys, models, testing
- **Cost Tracking** (`docs/cost-tracking/`) - Pricing, cost optimization
- **Usage Guides** (`docs/usage/`) - How to use features
- **Development** (`docs/development/`) - Development notes and plans

See `docs/INSTALLATION.md` for detailed installation instructions, or `docs/QUICK_START.md` for a quick start guide.

## License

See LICENSE.txt for license information.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Notes

- This project uses AutoGen (AG2) for multi-agent orchestration
- The system is designed to simulate collaborative scientific research environments
- API keys should be kept secure and not committed to version control
