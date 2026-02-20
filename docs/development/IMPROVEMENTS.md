# Codebase Improvements & Organization

## Issues Identified

### 1. **Exported .txt Files Not Being Used**
- **Location**: `society_of_scientists/data/exported_*.txt` and `society_of_scientists/old/exported_*.txt`
- **Status**: These files contain research paper summaries but are **NOT being imported or used** anywhere in the codebase
- **Current Usage**: They're only created as output files by `exa_files.py` when searching papers
- **Recommendation**: Either:
  - Create a utility to load and use these files as context for agents
  - Or document them as reference/archive data only

### 2. **"old" Folder Naming is Confusing**
- **Location**: `society_of_scientists/old/`
- **Problem**: Contains both old code versions AND duplicate data files
- **Current Contents**:
  - Old Python scripts (backups): `jamba_working.py`, `exa_agent.py`, etc.
  - Duplicate data files: `exported_*.txt` (same as in `data/` folder)
- **Recommendation**: 
  - Rename to `archive/` or `backup/` for clarity
  - Remove duplicate data files (keep only in `data/`)
  - Or split into `archive/code/` and `archive/data/`

### 3. **Hardcoded Summaries in agent_list.py**
- **Location**: `society_of_scientists/agent_list.py` (lines ~237-1048)
- **Status**: Contains hardcoded paper summaries embedded as strings
- **Issue**: These appear to be manually copied from exported files, not dynamically loaded
- **Recommendation**: Consider creating a data loader utility if you want to use the exported files

## Proposed Improvements

### ✅ Completed
1. Created proper package structure (`agents/`, `clients/`, `tools/`, `config/`)
2. Created centralized configuration management with `.env` support
3. Moved data files to `society_of_scientists/data/`
4. Created `.gitignore` for security
5. Created `requirements.txt`

### 🔄 In Progress / Recommended
1. **Remove duplicate data files from `old/` folder** (keep only in `data/`)
2. **Rename `old/` to `archive/` or remove if not needed**
3. **Create data loader utility** if exported files should be used:
   ```python
   # society_of_scientists/tools/data_loader.py
   def load_research_summaries(topic: str) -> List[str]:
       """Load research summaries from exported files."""
   ```
4. **Consolidate duplicate code** (exa.py, exa_files.py, exa_agent.py have similar functionality)
5. **Remove hardcoded API keys** (use .env instead)
6. **Add type hints** throughout codebase
7. **Create examples/** folder with usage examples
8. **Add tests/** structure

## File Usage Analysis

### Files That ARE Used:
- `agent_list.py` - Agent prompt definitions (actively imported)
- `jamba_working.py` - Main multi-agent system (main entry point)
- `exa_files.py` - Creates exported files (output only)
- `tools.py` - Exa search tool function

### Files That Are NOT Used:
- `exported_*.txt` files - Created but never imported/loaded
- Files in `old/` folder - Old versions, not imported

## Next Steps

1. Decide if exported .txt files should be used as input
2. Clean up `old/` folder (remove duplicates, rename or archive)
3. Create utility to load exported files if needed
4. Continue refactoring with new package structure
