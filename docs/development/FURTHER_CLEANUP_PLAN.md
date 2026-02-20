# Further Cleanup Plan - Rational Structure

## 🔴 CRITICAL - Duplicate Code Removal

### 1. Duplicate ExaSearch Implementations
**Files to DELETE:**
- `society_of_scientists/exa.py` - Duplicate of `tools/exa_search.py`
- `society_of_scientists/exa_files.py` - Duplicate of `tools/exa_search.py`
- `society_of_scientists/exa_agent.py` - Duplicate with agent integration (functionality in `tools/exa_search.py`)

**Reason:** All three are old implementations. The canonical version is `tools/exa_search.py` which has:
- Cache support
- Proper configuration management
- Better structure

### 2. Duplicate tools.py
**File to DELETE:**
- `society_of_scientists/tools.py` - Old standalone file with `exa_search_tool` function

**Reason:** Functionality is in `tools/exa_search.py` and `tools/__init__.py` exports it properly.

### 3. Non-functional testing.py
**File to DELETE:**
- `society_of_scientists/testing.py` - Just contains a curl command, not actual test code

**Reason:** Not a real test file. If needed, move curl command to docs.

## 🟡 MEDIUM - Structure Improvements

### 4. jamba_working.py Refactoring
**Current Issues:**
- Still creates agents inline instead of using agent_factory
- Has hardcoded API key (user wants to keep for now)
- Mix of old and new patterns

**Options:**
- **Option A:** Keep as-is for backward compatibility, add deprecation notice
- **Option B:** Fully refactor to use agent_factory, move to examples/
- **Option C:** Create wrapper that uses agent_factory internally

**Recommendation:** Option A - Add deprecation notice, keep for now.

### 5. old/ Archive Folder
**Current State:**
- Contains old versions of files
- Has duplicate data files

**Options:**
- **Option A:** Delete entire folder (cleanest)
- **Option B:** Keep as archive but remove duplicate data files
- **Option C:** Move to `docs/archive/` for reference

**Recommendation:** Option A - Delete if not needed, or Option B if user wants to keep history.

## 🟢 LOW - Code Quality

### 6. Unused Imports
- Check all files for unused imports
- Remove dead code

### 7. Type Hints
- Add type hints where missing
- Improve code documentation

### 8. Consistent Naming
- Ensure all modules follow naming conventions
- Check for inconsistent patterns

## Execution Order

1. ✅ Check for imports of files to be deleted
2. ✅ Delete duplicate ExaSearch files
3. ✅ Delete duplicate tools.py
4. ✅ Delete testing.py
5. ✅ Update jamba_working.py with deprecation notice
6. ✅ Remove old/ folder (or clean it)
7. ✅ Verify no broken imports
8. ✅ Run final checks
