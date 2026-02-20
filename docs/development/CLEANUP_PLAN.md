# Comprehensive Cleanup & Reorganization Plan

## Critical Issues Found

### 1. **Duplicate Code - ExaSearch Classes** 🔴 HIGH PRIORITY
**Problem**: Three duplicate implementations of ExaSearch
- `exa.py` - Old implementation
- `exa_files.py` - Old implementation  
- `exa_agent.py` - Old implementation with agent integration
- `tools/exa_search.py` - ✅ NEW (should be the only one)

**Action**: 
- Delete `exa.py`, `exa_files.py`, `exa_agent.py`
- Update any imports to use `tools.exa_search.ExaSearch`
- Keep `tools/exa_search.py` as the canonical implementation

### 2. **Duplicate AI21JambaModelClient** 🔴 HIGH PRIORITY
**Problem**: Client class defined in multiple places
- `jamba.py` - Has AI21JambaModelClient
- `jamba_working.py` - Has AI21JambaModelClient (hardcoded API key!)
- `exa_agent.py` - Has AI21JambaModelClient
- `clients/jamba_client.py` - ✅ NEW (should be the only one)

**Action**:
- Delete duplicate client classes
- Update all files to import from `clients.jamba_client`
- Remove hardcoded API keys

### 3. **Missing agent_factory.py** 🔴 HIGH PRIORITY
**Problem**: `agents/__init__.py` imports from `agent_factory` but file doesn't exist
- `agents/__init__.py` line 2: `from .agent_factory import ...`
- File `agent_factory.py` doesn't exist

**Action**:
- Create `agents/agent_factory.py` with agent creation functions
- Extract agent creation logic from `jamba_working.py`

### 4. **Hardcoded API Keys** 🔴 SECURITY ISSUE
**Problem**: API keys hardcoded in multiple files
- `jamba_working.py` line 22, 31: `"5AweiGc6E9UDXMCwtYDVhS5y6LarJoLl"`
- `exa_files.py` line 75: `"03af6e3c-7b7f-4d46-b541-6771b8a240e0"`
- `exa_agent.py` line 73, 102: Hardcoded keys
- `exa.py` line 76: Hardcoded key
- `tools.py` line 8: Hardcoded key

**Action**:
- Remove all hardcoded keys
- Use `config.settings` everywhere
- Add to `.gitignore` (already done)

### 5. **Legacy/Duplicate Files** 🟡 MEDIUM PRIORITY
**Files to remove or move**:
- `exa.py` - Duplicate, delete
- `exa_files.py` - Duplicate, delete
- `exa_agent.py` - Duplicate, delete
- `tools.py` - Duplicate functionality, delete
- `testing.py` - Just a curl command, not a test file (move to docs or delete)
- `test_panel.py` - Demo/example, move to `examples/`

### 6. **Main Entry Point Issues** 🟡 MEDIUM PRIORITY
**Problem**: 
- `jamba_working.py` is the main file but:
  - Has hardcoded API keys
  - Creates agents inline (should use factory)
  - Has duplicate client class
  - Not in proper location (should be in root or examples/)

**Action**:
- Create `society_of_scientists/__main__.py` as entry point
- Refactor `jamba_working.py` to use:
  - `clients.jamba_client.AI21JambaModelClient`
  - `agents.agent_factory` for agent creation
  - `config.settings` for configuration
- Move current `jamba_working.py` to `examples/` as reference

### 7. **Agent Creation Scattered** 🟡 MEDIUM PRIORITY
**Problem**: Agent creation logic is in `jamba_working.py` instead of centralized

**Action**:
- Create `agents/agent_factory.py` with:
  - `create_scientist_agents()` - Creates all scientist agents
  - `create_grant_writers()` - Creates grant writing agents
  - `create_orchestrators()` - Creates planner/assistant
  - `create_critic()` - Creates critic agent
  - `create_society_of_mind_system()` - Creates full system

### 8. **Inconsistent Imports** 🟡 MEDIUM PRIORITY
**Problem**: Mix of relative and absolute imports
- `jamba_working.py` uses: `from agent_list import ...` (should be relative)
- Some files use relative imports, some absolute

**Action**:
- Standardize on relative imports within package
- Use absolute imports for external packages

### 9. **Missing Documentation** 🟢 LOW PRIORITY
**Needs**:
- API documentation
- Architecture overview
- Setup guide
- Usage examples

### 10. **No Tests** 🟢 LOW PRIORITY
**Problem**: No test structure
- `testing.py` is just a curl command
- No actual unit tests

**Action**:
- Create proper `tests/` structure
- Add unit tests for key functions

## Recommended File Structure

```
society_of_scientists/
├── __init__.py                 # Package init
├── __main__.py                 # Entry point (NEW)
├── agents/
│   ├── __init__.py
│   ├── agent_factory.py        # NEW - Centralized agent creation
│   └── prompts.py              # NEW - Extract prompts from agent_list.py
├── clients/
│   ├── __init__.py
│   └── jamba_client.py         # ✅ Already exists
├── config/
│   ├── __init__.py
│   └── settings.py             # ✅ Already exists
├── tools/
│   ├── __init__.py
│   ├── exa_search.py           # ✅ Already exists (use this!)
│   ├── data_loader.py          # ✅ Already exists
│   └── agent_context.py        # ✅ Already exists
├── data/                       # ✅ Already exists
│   └── exported_*.txt
├── agent_list.py               # Keep for now (prompts)
└── examples/                   # NEW
    ├── simple_chat.py          # Based on jamba.py
    ├── multi_agent_system.py   # Based on jamba_working.py (refactored)
    └── panel_ui.py             # Based on test_panel.py
```

## Files to DELETE

1. `exa.py` - Duplicate
2. `exa_files.py` - Duplicate
3. `exa_agent.py` - Duplicate
4. `tools.py` - Duplicate
5. `testing.py` - Not a test file

## Files to MOVE

1. `jamba.py` → `examples/simple_chat.py`
2. `test_panel.py` → `examples/panel_ui.py`
3. `jamba_working.py` → `examples/multi_agent_system.py` (after refactoring)

## Files to CREATE

1. `society_of_scientists/__main__.py` - Main entry point
2. `society_of_scientists/agents/agent_factory.py` - Agent creation
3. `society_of_scientists/agents/prompts.py` - Extract prompts (optional)

## Implementation Order

1. ✅ Create agent_factory.py
2. ✅ Remove hardcoded API keys
3. ✅ Delete duplicate ExaSearch files
4. ✅ Delete duplicate client classes
5. ✅ Create __main__.py
6. ✅ Refactor jamba_working.py
7. ✅ Move files to examples/
8. ✅ Update all imports
9. ✅ Add documentation
