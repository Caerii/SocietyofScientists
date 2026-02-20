# API Reference

All public symbols are importable from `society_of_scientists`:

```python
from society_of_scientists import create_society_of_mind_system, Settings, get_tracker
```

## Agent Creation

### `create_society_of_mind_system(task, max_rounds=50, speaker_selection_method='round_robin', register_exa_tool=True)`

Creates the complete 12-agent system, ready to run.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `task` | `str` | required | The research topic or task description |
| `max_rounds` | `int` | `50` | Maximum conversation turns in the group chat |
| `speaker_selection_method` | `str` | `'round_robin'` | `'round_robin'` for deterministic order, `'auto'` for LLM-selected |
| `register_exa_tool` | `bool` | `True` | Whether to register the Exa search tool |

**Returns:** `tuple` of `(society_of_mind_agent, user_proxy, manager)`

- `society_of_mind_agent` — the `SocietyOfMindAgent` wrapping the 12-agent group chat
- `user_proxy` — the `UserProxyAgent` that initiates and receives the conversation
- `manager` — the `GroupChatManager` orchestrating agent turns

**Usage:**
```python
agent, proxy, manager = create_society_of_mind_system(
    task="Propose a neural architecture combining spiking networks with transformers"
)
result = proxy.initiate_chat(agent, message="Propose a neural architecture combining spiking networks with transformers")
```

### `create_scientist_agents(llm_config=None)`

Creates the three domain scientist agents.

**Returns:** `dict` with keys `"computer_vision"`, `"ai_language_models"`, `"ai_hardware"` mapping to `AssistantAgent` instances.

### `create_grant_writers(llm_config=None)`

Creates the eight grant writing agents.

**Returns:** `dict` with keys `"scientist"`, `"hypothesis"`, `"objective"`, `"methodology"`, `"ethics"`, `"comparison"`, `"novelty"`, `"budget"`.

### `create_orchestrators(llm_config=None)`

Creates orchestrator agents.

**Returns:** `dict` with key `"planner"`.

### `create_critic(llm_config=None)`

Creates the critic agent.

**Returns:** `AssistantAgent` instance.

### `get_llm_config()`

Returns the LLM configuration dict from Settings.

**Returns:** `dict` in the format `{"config_list": [jamba_config]}`.

## Model Client

### `AI21JambaModelClient(config, **kwargs)`

Custom model client bridging AutoGen with AI21's Jamba API. You typically don't construct this directly — it is registered on agents by the factory functions.

**Config dict keys:**

| Key | Type | Description |
|-----|------|-------------|
| `api_key` | `str` | AI21 API key |
| `model` | `str` | Model name (e.g., `"jamba-1.5-large"`) |
| `temperature` | `float` | Sampling temperature |
| `top_p` | `float` | Nucleus sampling parameter |
| `max_tokens` | `int` | Maximum completion tokens |

**Methods:**

- `create(params) -> SimpleNamespace` — sends messages to AI21 and returns an AutoGen-compatible response. Automatically records usage to `CostTracker`.
- `message_retrieval(response) -> List[str]` — extracts message text from response.
- `cost(response) -> float` — returns the cost of the response.
- `get_usage(response) -> dict` — returns `{"prompt_tokens", "completion_tokens", "total_tokens", "cost"}`.

## Configuration

### `Settings`

Class that reads configuration from environment variables. Loads `.env` files automatically via `python-dotenv`.

**Class attributes (all configurable via environment):**

| Attribute | Env Variable | Default | Description |
|-----------|-------------|---------|-------------|
| `AI21_API_KEY` | `AI21_API_KEY` | required | AI21 API key |
| `JAMBA_MODEL` | `JAMBA_MODEL` | `"jamba-1.5-large"` | Model identifier |
| `JAMBA_TEMPERATURE` | `JAMBA_TEMPERATURE` | `0.7` | Sampling temperature |
| `JAMBA_TOP_P` | `JAMBA_TOP_P` | `1.0` | Top-p sampling |
| `JAMBA_MAX_TOKENS` | `JAMBA_MAX_TOKENS` | `2048` | Max completion tokens |
| `EXA_API_KEY` | `EXA_API_KEY` | `None` | Exa search API key (optional) |
| `AGENT_WORK_DIR` | `AGENT_WORK_DIR` | `"coding"` | Agent working directory |
| `AGENT_USE_DOCKER` | `AGENT_USE_DOCKER` | `False` | Docker for code execution |
| `DATA_DIR` | — | `<package>/data` | Path to cached data files |

**Class methods:**

- `get_jamba_config() -> dict` — returns config dict for the Jamba model client. Raises `ValueError` if `AI21_API_KEY` is not set.
- `get_exa_api_key() -> Optional[str]` — returns the Exa key or `None`.
- `validate() -> bool` — validates required settings. Raises `ValueError` with a list of missing keys.

## Research Tools

### `ExaSearch(api_key=None, use_cache=True)`

Wraps the Exa API for research paper search, with cache-first behavior.

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `api_key` | from Settings | Exa API key. If `None`, uses Settings. |
| `use_cache` | `True` | Whether to check cached data before API calls |

**Methods:**

- `search_papers(query, search_type="neural", num_results=20, use_cache_first=True, ...) -> Any` — searches for papers. Returns cached summaries if available and `use_cache_first=True`, otherwise calls the Exa API.
- `get_cached_summaries(topic=None) -> List[str]` — loads cached summaries. Filter by topic or get all.
- `parse_results(fields) -> List[dict]` — extracts specified fields from search results.
- `export_results_to_file(fields, filename, output_dir) -> str` — writes results to a text file.

### `exa_search_function(query, use_cache=True) -> str`

AutoGen-compatible search function. Registered as a tool on agents. Returns a formatted string with title, URL, and summary for the top 10 results.

### `load_research_summaries(topic=None) -> List[str]`

Loads paper summaries from `data/exported_*.txt` files. Topic options: `'computational_neuroscience'`, `'computer_vision'`, `'large_language_models'`, `'hardware_for_AI'`. Pass `None` for all topics.

### Context Functions

Convenience functions returning pre-formatted summary strings:

- `get_computer_vision_context() -> str`
- `get_ai_language_models_context() -> str`
- `get_ai_hardware_context() -> str`
- `get_computational_neuroscience_context() -> str`

## Cost Tracking

### `CostTracker(log_file=None)`

Tracks API usage and costs. Persists to JSON.

**Constructor:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `log_file` | `data/api_usage_log.json` | Path to the JSON log file |

**Methods:**

- `calculate_cost(model, prompt_tokens, completion_tokens) -> float` — computes cost using AI21 pricing.
- `record_usage(model, prompt_tokens, completion_tokens, total_tokens, operation) -> APIUsage` — records a usage event and saves to disk.
- `get_total_cost(model=None) -> float` — total cost, optionally filtered by model.
- `get_usage_stats() -> dict` — returns `{"total_calls", "total_cost", "total_tokens", "by_model": {...}}`.
- `print_summary()` — prints a formatted usage report to stdout.

### `get_tracker() -> CostTracker`

Returns the global singleton `CostTracker` instance.

### `ModelPricing`

Dataclass with AI21 pricing per 1K tokens:

| Model | Prompt | Completion |
|-------|--------|------------|
| `jamba-large` / `jamba-large-1.7-2025-07` | $0.002 | $0.008 |
| `jamba-mini-2-2026-01` | $0.0002 | $0.0004 |
| `jamba-mini-1.7-2025-07` | $0.0002 | $0.0004 |

## Compatibility Utilities

### `get_autogen_version() -> Tuple[int, ...]`

Returns the installed AutoGen/AG2 version as a tuple.

### `get_autogen_type() -> str`

Returns `'ag2'`, `'microsoft_old'`, `'microsoft_new'`, or `'unknown'`.

### `is_ag2() -> bool`

Returns `True` if the installed package is AG2 (the recommended fork).

### `is_autogen_v3_plus() -> bool`

Returns `True` if the installed version is 0.3.0 or later.

### `VERSION_INFO -> dict`

Dict with keys `"type"`, `"version"`, `"is_ag2"`, `"is_v3_plus"`.

## REST API Endpoints

The `society_of_scientists.api.server` module provides a FastAPI application:

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | API info and version |
| `GET` | `/api/stats` | Dashboard statistics |
| `POST` | `/api/proposal/start` | Start proposal generation. Body: `{"task": "..."}` |
| `POST` | `/api/proposal/stop` | Stop current generation |
| `GET` | `/api/proposal/status` | Current session status |
| `GET` | `/api/proposal/history` | List of all sessions |
| `GET` | `/api/cost/summary` | Cost tracking summary |
| `GET` | `/api/cost/details` | Detailed cost information |
| `WebSocket` | `/ws` | Real-time agent activity stream |

Run the server:
```bash
python -m society_of_scientists.api
```

The server listens on `0.0.0.0:8000` with CORS configured for `localhost:5173` (Vite dev server) and `localhost:3000`.
