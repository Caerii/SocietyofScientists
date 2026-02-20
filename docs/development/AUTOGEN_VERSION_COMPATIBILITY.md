# AutoGen Version Compatibility Strategy

## Overview

This codebase supports **all AutoGen versions** (v2 and v3+) through a compatibility layer that:
- ✅ **Detects** installed AutoGen version automatically
- ✅ **Uses latest features** when available (v3+)
- ✅ **Falls back** to v2 patterns when needed
- ✅ **Deprecates** v2 usage with warnings (but **never removes** support)
- ✅ **Future-proof** for new AutoGen versions

## Architecture

### Compatibility Layer

Located in `society_of_scientists/utils/autogen_compat.py`:

```python
from society_of_scientists.utils.autogen_compat import (
    create_agent,              # Version-aware agent creation
    register_model_client,     # Version-aware model registration
    register_function_compat,  # Version-aware function registration
    get_version_info,          # Get AutoGen version info
    is_autogen_v3_plus,        # Check if v3+ installed
    is_autogen_v2,             # Check if v2 installed
)
```

### How It Works

1. **Version Detection**: Automatically detects installed AutoGen version
2. **Feature Selection**: Uses latest features when available, falls back to v2
3. **Deprecation Warnings**: Shows warnings for v2 usage but continues to work
4. **No Breaking Changes**: All versions supported forever

## Usage

### Automatic (Recommended)

The compatibility layer is used automatically in `agent_factory.py`:

```python
# This works with both v2 and v3+
agent = create_agent(
    name="scientist",
    system_message=prompt,
    llm_config=config,
)

register_model_client(agent, AI21JambaModelClient)
```

### Manual Version Checking

```python
from society_of_scientists.utils.autogen_compat import (
    is_autogen_v3_plus,
    get_version_info,
    VERSION_INFO
)

# Check version
if is_autogen_v3_plus():
    # Use v3+ features
    pass
else:
    # Use v2 features
    pass

# Get detailed version info
info = get_version_info()
print(f"AutoGen version: {info['version']}")
print(f"Is v3+: {info['is_v3_plus']}")
```

## Version Support

### AutoGen v2 (0.2.x)
- ✅ **Fully Supported** (deprecated but never removed)
- ⚠️ **Deprecation warnings** shown
- 🔄 **Automatic fallback** when v3+ not available

### AutoGen v3+ (0.3.x, 0.4.x, etc.)
- ✅ **Fully Supported** with latest features
- 🚀 **Uses new affordances** automatically
- 📈 **Future-proof** for new versions

## Deprecation Policy

### v2 Support
- **Status**: Deprecated but **NEVER removed**
- **Warnings**: Shown when v2 patterns are used
- **Support**: Maintained indefinitely
- **Migration**: Optional (v2 code continues to work)

### Example Warning

```
DeprecationWarning: Using AutoGen v2 pattern for 'create_agent'. 
Consider using: Using latest AutoGen version for new features. 
v2 support will remain available but is deprecated.
```

This warning **does not break** anything - it just informs users.

## Requirements

```txt
autogen>=0.2.28  # Supports all versions
```

No upper bound - supports latest and future versions!

## Benefits

1. **Future-Proof**: Automatically uses new features when available
2. **Backward Compatible**: Old code never breaks
3. **No Migration Required**: Existing code works with all versions
4. **Best of Both Worlds**: Latest features + stability

## Testing

Test with different AutoGen versions:

```bash
# Test with v2
pip install autogen==0.2.28
python -m pytest tests/

# Test with latest
pip install --upgrade autogen
python -m pytest tests/
```

Both should work! 🎉

## Implementation Details

### Version Detection

```python
# Automatically detects version
_autogen_version = tuple(map(int, autogen.__version__.split('.')[:2]))
_autogen_major = _autogen_version[0]
```

### Feature Selection

```python
def create_agent(...):
    if is_autogen_v3_plus():
        # Use v3+ features
        return create_agent_v3_plus(...)
    else:
        # Use v2 features (with deprecation warning)
        return create_agent_v2(...)
```

### Deprecation (Never Removal)

```python
def deprecation_warning_v2(feature: str, alternative: str = None):
    """Show deprecation warning but continue to work."""
    warnings.warn(msg, DeprecationWarning, stacklevel=3)
    # Code continues - never breaks!
```

## Migration Guide

### For Users

**No migration needed!** Your code works with all versions automatically.

### For Developers

If you want to use latest features explicitly:

```python
from society_of_scientists.utils.autogen_compat import is_autogen_v3_plus

if is_autogen_v3_plus():
    # Use new v3+ features
    pass
```

## Summary

✅ **Supports all AutoGen versions** (v2, v3, v4, etc.)  
✅ **Uses latest features** when available  
✅ **Deprecates but never removes** v2 support  
✅ **Future-proof** for new versions  
✅ **No breaking changes** ever  

The compatibility layer ensures your code works with **any** AutoGen version, now and forever! 🚀
