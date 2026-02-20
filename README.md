# Society of Scientists

A multi-agent system that generates research grant proposals. Specialized AI agents — domain scientists, grant writers, and a critic — collaborate through structured group chat to produce detailed, interdisciplinary proposals from a single research prompt.

Built on [AG2](https://github.com/ag2ai/ag2) (AutoGen) and [AI21 Jamba](https://www.ai21.com/jamba) models, extending the [SciAgents](https://github.com/lamm-mit/SciAgentsDiscovery) framework for automated scientific discovery.

## How It Works

You provide a research topic. The system runs a structured multi-agent conversation:

1. **Domain scientists** (computer vision, language models, AI hardware) contribute relevant expertise
2. **A planner** synthesizes these inputs into a proposal outline
3. **Grant writers** expand each section — hypothesis, methodology, objectives, budget, ethics, novelty, and comparison to prior work
4. **A critic** reviews the full proposal and suggests improvements

The output is a complete grant proposal with all standard sections.

## Quick Start

```bash
pip install -e .
```

Configure your API keys:
```bash
cp .env.example .env
# Edit .env with your AI21_API_KEY and EXA_API_KEY
```

Run from Python:
```python
from society_of_scientists import create_society_of_mind_system

agent, user_proxy, manager = create_society_of_mind_system(
    task="Propose a neural architecture that combines spiking networks with transformer attention"
)

result = user_proxy.initiate_chat(
    agent,
    message="Propose a neural architecture that combines spiking networks with transformer attention"
)
```

Or from the command line:
```bash
python -m society_of_scientists "Your research topic here"
```

## Project Structure

```
society_of_scientists/
├── agents/           # Agent creation and group chat setup
├── clients/          # AI21 Jamba model client
├── config/           # Settings and environment variable loading
├── tools/            # Exa search, cached data loading
├── utils/            # Cost tracking, AutoGen/AG2 compatibility
├── api/              # REST API server (FastAPI)
├── data/             # Cached research paper summaries
└── agent_list.py     # Agent system prompts
```

## Configuration

The system needs at minimum an **AI21 API key**. The Exa API key is optional — without it, the system uses cached research summaries (398 papers across 4 domains).

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for all environment variables and setup options.

## Cost Tracking

All API calls are automatically tracked. View costs at any time:

```python
from society_of_scientists import get_tracker
tracker = get_tracker()
tracker.print_summary()
```

Jamba Mini 2 costs roughly $0.0003 per 1K tokens. A typical proposal generation run costs under a cent. See [docs/cost-tracking/COST_TRACKING.md](docs/cost-tracking/COST_TRACKING.md) for pricing details.

## Documentation

- [Installation](docs/INSTALLATION.md) — PyPI, source, and development installs
- [Quick Start](docs/QUICK_START.md) — Usage examples
- [Configuration](docs/CONFIGURATION.md) — Environment variables and API keys
- [Cost Tracking](docs/cost-tracking/COST_TRACKING.md) — Pricing and optimization
- [Jamba Models](docs/api/JAMBA_MODELS_AVAILABLE.md) — Available models and capabilities
- [Package Structure](docs/development/PACKAGE_STRUCTURE.md) — Module layout and public API

## Attribution

This project builds on [SciAgents](https://github.com/lamm-mit/SciAgentsDiscovery) by Ghafarollahi & Buehler (MIT), which introduced multi-agent graph reasoning for automated scientific discovery. See [docs/README_SciAgents.md](docs/README_SciAgents.md) for the original research context.

```bibtex
@article{ghafarollahi2024sciagents,
  title={SciAgents: Automating Scientific Discovery Through Bioinspired Multi-Agent Intelligent Graph Reasoning},
  author={Ghafarollahi, Alireza and Buehler, Markus J},
  journal={Advanced Materials},
  pages={2413523},
  year={2024},
  publisher={Wiley Online Library}
}
```

## License

See LICENSE.txt for license information.
