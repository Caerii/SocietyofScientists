# System Architecture

Society of Scientists is a multi-agent system built on AutoGen's [Society of Mind](https://microsoft.github.io/autogen/docs/topics/society-of-mind/) pattern. Twelve specialized agents collaborate through a managed group chat to produce a research grant proposal from a single topic prompt.

## Component Diagram

```
                          User
                           |
                     initiate_chat()
                           |
                    +--------------+
                    |  UserProxy   |  human_input_mode="NEVER"
                    +--------------+  executes tool calls
                           |
                  +------------------+
                  | SocietyOfMind    |  wraps the group chat
                  | Agent            |  as a single agent
                  +------------------+
                           |
                  +------------------+
                  | GroupChat        |  12 agents, round-robin
                  | Manager          |  or LLM-selected turns
                  +------------------+
                           |
          +----------------+----------------+
          |                |                |
   +-----------+   +-------------+   +-----------+
   | Domain    |   | Grant       |   | Review    |
   | Scientists|   | Writers     |   |           |
   | (3)       |   | (8)        |   | (1)       |
   +-----------+   +-------------+   +-----------+
          |                |                |
          +----------------+----------------+
                           |
                  +------------------+
                  | AI21 Jamba       |  all agents share
                  | Model Client     |  the same LLM client
                  +------------------+
                      |          |
               +------+    +----------+
               | AI21 |    | Cost     |
               | API  |    | Tracker  |
               +------+    +----------+
```

## Modules

The package is organized into five subsystems:

### `agents/` — Agent Creation

The `agent_factory.py` module provides factory functions that instantiate all 12 agents, register the Jamba model client on each, and wire them into a GroupChat wrapped by a SocietyOfMindAgent.

Entry point: `create_society_of_mind_system(task, max_rounds, speaker_selection_method, register_exa_tool)`

This function:
1. Loads LLM config from `Settings`
2. Creates domain scientists, grant writers, orchestrator, and critic
3. Assembles them into a `GroupChat` with a `GroupChatManager`
4. Wraps the group chat in a `SocietyOfMindAgent`
5. Creates a `UserProxyAgent` (no human input, no code execution)
6. Optionally registers the Exa search tool on the SocietyOfMindAgent

### `clients/` — LLM Interface

`jamba_client.py` implements `AI21JambaModelClient`, a custom model client that bridges AutoGen's expected interface with AI21's chat completions API. AutoGen expects four methods from a model client:

- `create(params)` — send messages to the LLM, return a response
- `message_retrieval(response)` — extract text from the response
- `cost(response)` — return the cost of the call
- `get_usage(response)` — return token counts

The client converts AutoGen's message format to AI21's `UserMessage` format, calls the API, then wraps the response in `SimpleNamespace` objects to match what AutoGen expects. Every call is recorded by `CostTracker`.

### `config/` — Settings

`settings.py` defines a `Settings` class that reads from environment variables (via `.env` files using `python-dotenv`). It provides:

- `get_jamba_config()` — returns the config dict that AutoGen needs for LLM configuration
- `get_exa_api_key()` — returns the Exa key or `None` for cache-only mode
- `validate()` — checks that required keys are present

### `tools/` — Research Tools

Three modules provide research data to agents:

- **`exa_search.py`** — `ExaSearch` class wrapping the Exa API. Defaults to cache-first behavior: if cached data is available, it returns that instead of making API calls. Also exposes `exa_search_function()` which is the AutoGen-compatible callable registered as a tool on agents.

- **`data_loader.py`** — loads pre-cached research paper summaries from `data/exported_*.txt` files. Summaries are organized by topic: computational neuroscience, computer vision, large language models, and AI hardware. ~100 summaries per topic, ~400 total.

- **`agent_context.py`** — convenience functions that format cached summaries into strings suitable for injection into agent prompts.

### `utils/` — Cost Tracking and Compatibility

- **`cost_tracker.py`** — `CostTracker` records every API call with token counts and costs. Persists to `data/api_usage_log.json`. Uses AI21's published pricing (per 1K tokens) to compute costs. A global singleton is available via `get_tracker()`.

- **`autogen_compat.py`** and related files — a compatibility layer that detects whether the installed package is AG2 (the active fork) or Microsoft AutoGen, and which version. Provides `create_agent()`, `register_model_client()`, and `register_function_compat()` that work across versions.

### `api/` — REST Server

`server.py` is a FastAPI application that exposes the multi-agent system over HTTP and WebSocket. Endpoints include starting/stopping proposal generation, retrieving cost summaries, and streaming agent activity in real time. Intended for use with the `frontend/` React application.

### `agent_list.py` — System Prompts

A ~1,200-line file containing the system prompts for all 12 agents. Each prompt defines the agent's expertise, instructions, and expected output format. The three domain scientist prompts each embed ~100 research paper summaries as in-context examples, giving the agents grounding in recent literature.

See [AGENTS.md](AGENTS.md) for a detailed breakdown of each agent's role and prompt.

## Key Design Decisions

**Why SocietyOfMindAgent?** AutoGen's `SocietyOfMindAgent` wraps a multi-agent group chat behind a single-agent interface. This means the entire 12-agent collaboration looks like one agent to the `UserProxyAgent`, simplifying the outer conversation loop.

**Why round-robin by default?** The `speaker_selection_method='round_robin'` ensures every agent gets a turn in a predictable order. The alternative, `'auto'`, lets the GroupChatManager's LLM choose which agent speaks next, which is more flexible but less predictable and costs extra LLM calls for the selection itself.

**Why a custom model client?** AutoGen's built-in model support targets OpenAI-compatible APIs. AI21's Jamba has a different API shape, so the custom client translates between the two formats. This also gives us a natural integration point for cost tracking.

**Why cache-first search?** The Exa API has rate limits and costs money. The system ships with 398 cached paper summaries across 4 domains. For most proposal topics, the cached data provides sufficient grounding. Live Exa search is available when the API key is configured, but the system works without it.

## Data Flow

See [PIPELINE.md](PIPELINE.md) for the step-by-step flow of a proposal generation run.
