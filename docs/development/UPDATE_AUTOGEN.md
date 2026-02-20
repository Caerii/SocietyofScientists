# How to Update AutoGen

## Quick Update Guide

### 1. Check Current Version
```bash
pip show pyautogen
```

### 2. Check Latest Available Version
```bash
pip index versions pyautogen
# Or visit: https://pypi.org/project/pyautogen/
```

### 3. Review Release Notes
- GitHub Releases: https://github.com/microsoft/autogen/releases
- Look for breaking changes between your version and latest

### 4. Update in Development Environment
```bash
# Create test environment
python -m venv test_env
test_env\Scripts\activate  # Windows
# or: source test_env/bin/activate  # Linux/Mac

# Install latest
pip install --upgrade pyautogen

# Test your code
python -m pytest tests/
# Or run your examples
python examples/multi_agent_system.py
```

### 5. If Tests Pass, Update Requirements
```bash
# Update requirements.txt
autogen>=0.2.50  # or latest stable

# Update setup.py
install_requires=[
    'autogen>=0.2.50',
    ...
]
```

### 6. Update Documentation
- Note any API changes
- Update examples if needed
- Document new features used

## Version Compatibility

### Current Constraint
- **Minimum**: `>=0.2.28` (ensures required features)
- **Maximum**: `<0.3.0` (avoids breaking changes from major version)

### When to Update

**Safe Updates** (within 0.2.x):
- Bug fixes
- Performance improvements
- New features (backward compatible)

**Careful Updates** (0.3.x or later):
- Review breaking changes
- Test thoroughly
- May need code changes

## Testing After Update

1. **Agent Creation**: Verify all agents still work
2. **Model Client**: Test `AI21JambaModelClient` integration
3. **Group Chat**: Test multi-agent conversations
4. **Function Registration**: Test `exa_search` tool
5. **Cost Tracking**: Verify cost calculation still works

## Rollback Plan

If update causes issues:
```bash
pip install autogen==0.2.28  # or your previous version
```

## Monitoring

- Watch AutoGen GitHub for releases
- Check documentation for new features
- Review changelog for relevant updates
