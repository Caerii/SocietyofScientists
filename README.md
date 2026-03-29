# Society of Scientists

**1st place — AGI House × Sundai AI Agents Hackathon at MIT.** This project won the top prize for combining specialized AI agents, [AI21 Jamba](https://www.ai21.com/jamba) large-context models, and [Exa](https://exa.ai/)-powered literature discovery to accelerate scientific ideation and grant writing—building on ideas from [SciAgents](https://github.com/lamm-mit/SciAgentsDiscovery) and the work of Markus J. Buehler and Alireza Ghafarollahi on LLMs and agents for scientific discovery.

A production-ready multi-agent system that generates research grant proposals. Specialized AI agents — domain scientists, grant writers, and a critic — collaborate through structured group chat to produce detailed, interdisciplinary proposals from a single research prompt.

Built on [AG2](https://github.com/ag2ai/ag2) (AutoGen) and AI21 Jamba models, extending the SciAgents framework for automated scientific discovery.

### Hackathon team and judges

- **Team:** Dünya Baradari, Alif Jakir, Elior Benarous, Igor Sadalski  
- **Judges:** Tuan Ho, Mark Weber, Yaniv Markovski

## Features

- **Multi-Agent Collaboration**: 13+ specialized agents including domain scientists, grant writers, researchers, compliance checkers, and quality assessors
- **Agency-Specific Templates**: Built-in templates for NIH (R01, R21, R03), NSF (Standard, CAREER), and DOE grants
- **Compliance Checking**: Automated validation against agency requirements with detailed issue tracking
- **Quality Assessment**: NIH-style and NSF-style evaluation with scoring across multiple criteria
- **Research Integration**: PubMed, arXiv, CrossRef, and Semantic Scholar integration with citation management
- **Citation Formatting**: Automatic citation generation in APA, Vancouver, and BibTeX formats
- **Web Interface**: Modern React + TypeScript frontend with wizard-style proposal creation
- **Real-Time Updates**: WebSocket support for live proposal generation progress
- **Export Options**: Export proposals to PDF, DOCX, LaTeX, or Markdown

## How It Works

You provide a research topic. The system runs a structured multi-agent conversation:

1. **Domain scientists** (computer vision, language models, AI hardware) contribute relevant expertise
2. **A researcher** integrates literature search and manages citations
3. **A planner** synthesizes these inputs into a proposal outline
4. **Grant writers** expand each section — hypothesis, methodology, objectives, budget, ethics, novelty
5. **A compliance checker** validates against agency requirements
6. **A quality assessor** evaluates using NIH/NSF review criteria
7. **A critic** reviews the full proposal and suggests improvements

## Quick Start

### Backend

```bash
# Install dependencies
pip install -e .

# Configure your API keys
cp .env.example .env
# Edit .env with your AI21_API_KEY (EXA_API_KEY is optional)

# Start the API server
python -m society_of_scientists.api.server
```

The API server will run on `http://localhost:8000`.

### Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
pnpm install

# Start development server
pnpm dev
```

The web interface will be available at `http://localhost:5173`.

## Usage

### Web Interface

1. Open `http://localhost:5173`
2. Click "New Proposal"
3. Enter your research grant topic
4. Select funding agency (NIH, NSF, DOE)
5. Optionally specify grant amount and keywords
6. Click "Start Proposal Generation"
7. Review generated proposal with compliance and quality assessments
8. Export in your preferred format

### Python API

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

### Command Line

```bash
python -m society_of_scientists "Your research topic here"
```

## Project Structure

```
society_of_scientists/
├── agents/
│   ├── compliance.py      # Grant compliance checking system
│   ├── quality_scorer.py  # Quality assessment and scoring
│   ├── research_integrator.py  # Literature search & citations
│   ├── templates.py       # Agency-specific proposal templates
│   └── orchestrator.py    # Enhanced proposal orchestration
├── clients/              # AI21 Jamba model client
├── config/               # Settings and environment variable loading
├── tools/                # Exa search, cached data loading
├── utils/                # Cost tracking, AutoGen/AG2 compatibility
├── api/
│   ├── server.py         # FastAPI REST API server
│   ├── schemas.py        # Pydantic models for API
│   ├── session_db.py     # Session persistence
│   └── rate_limiter.py   # Rate limiting
├── data/                 # Cached research paper summaries
├── frontend/             # React + TypeScript frontend
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── stores/       # State management
│   │   └── utils/        # Utility functions
│   └── package.json
└── agent_list.py         # Agent system prompts
```

## API Endpoints

### Proposal Management
- `POST /api/proposal/start` - Start a new proposal generation
- `POST /api/proposal/stop` - Stop a running proposal
- `GET /api/proposal/status` - Get proposal status
- `GET /api/proposal/history` - Get proposal history
- `GET /api/proposal/{session_id}` - Get proposal details
- `POST /api/proposal/{session_id}/export` - Export proposal

### Compliance & Quality
- `POST /api/compliance/check` - Check proposal compliance against agency requirements
- `POST /api/quality/assess` - Assess proposal quality using NIH/NSF review criteria

### Templates
- `GET /api/templates` - List available proposal templates
- `GET /api/templates/{template_id}` - Get detailed template information

### System
- `GET /health` - Health check endpoint
- `GET /metrics` - System metrics and statistics
- `GET /api/stats` - Dashboard statistics
- `GET /api/cost/summary` - Cost tracking summary
- `GET /api/cost/details` - Detailed cost information

### WebSocket
- `WS /ws` - Real-time proposal generation updates

See `docs/api/REFERENCE.md` for detailed API documentation with request/response schemas.

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

- [System Architecture](docs/architecture/OVERVIEW.md) — components, data flow, design decisions
- [Agent Reference](docs/architecture/AGENTS.md) — all 12 agents and their roles
- [Generation Pipeline](docs/architecture/PIPELINE.md) — step-by-step proposal flow
- [API Reference](docs/api/REFERENCE.md) — all public functions, classes, and REST endpoints
- [Configuration](docs/CONFIGURATION.md) — environment variables and API keys
- [Cost Tracking](docs/cost-tracking/COST_TRACKING.md) — pricing and optimization

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
