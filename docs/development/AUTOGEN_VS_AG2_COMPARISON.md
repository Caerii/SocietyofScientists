# AutoGen vs AG2 Comparison

## Overview

There are now **TWO** AutoGen projects:

1. **Microsoft AutoGen** (microsoft/autogen) - Original, now evolved
2. **AG2** (ag2ai/ag2) - Community fork/evolution, more active

## Microsoft AutoGen (microsoft/autogen)

### Status
- **Latest Version**: v0.7.5 (Sep 30, 2025)
- **Package**: `autogen-agentchat`, `autogen-ext`, `autogen-core`
- **Installation**: `pip install -U "autogen-agentchat" "autogen-ext[openai]"`
- **API**: **Completely new** (async-based, different structure)
- **Status**: "If you are new to AutoGen, please checkout Microsoft Agent Framework"

### New API Structure
```python
# NEW API (completely different)
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio

async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4.1")
    agent = AssistantAgent("assistant", model_client=model_client)
    print(await agent.run(task="Hello World!"))
    await model_client.close()

asyncio.run(main())
```

### Characteristics
- ✅ Official Microsoft project
- ❌ **Breaking changes** - completely new API
- ❌ **Async-only** - requires async/await
- ❌ **Different package structure** - multiple packages
- ⚠️ Less active (last release 3 months ago)
- ⚠️ Recommends "Microsoft Agent Framework" for new users

## AG2 (ag2ai/ag2)

### Status
- **Latest Version**: v0.10.4 (2 weeks ago - VERY RECENT!)
- **Package**: `ag2` (or alias `autogen`)
- **Installation**: `pip install ag2[openai]`
- **API**: **Similar to old AutoGen** (backward compatible patterns)
- **Status**: Active community fork, open governance

### API Structure
```python
# AG2 API (similar to old AutoGen)
from autogen import AssistantAgent, UserProxyAgent, LLMConfig

llm_config = LLMConfig.from_json(path="OAI_CONFIG_LIST")
assistant = AssistantAgent("assistant", llm_config=llm_config)
user_proxy = UserProxyAgent("user_proxy", code_execution_config={...})

user_proxy.run(assistant, message="...").process()
```

### Characteristics
- ✅ **Active development** (latest release 2 weeks ago)
- ✅ **Backward compatible** - similar to old AutoGen API
- ✅ **Single package** - easier installation
- ✅ **Open governance** - community-driven
- ✅ **Apache 2.0 license** - more permissive
- ✅ **Matches your current code** - same API patterns!

## Comparison for Your Codebase

### Your Current Code Uses:
```python
from autogen import AssistantAgent, UserProxyAgent
from autogen import GroupChat, GroupChatManager
from autogen import register_function
```

### Which Matches Better?

**AG2** ✅ - Your code matches AG2's API perfectly!

**Microsoft AutoGen** ❌ - Would require complete rewrite (async, new packages, new API)

## Recommendation: **AG2**

### Why AG2 is Better for You:

1. **API Compatibility**: Your code works with AG2 with minimal changes
2. **Active Development**: Latest release 2 weeks ago vs 3 months
3. **Community-Driven**: Open governance, more responsive
4. **Easier Migration**: Similar patterns to what you already have
5. **Better License**: Apache 2.0 vs MIT/CC-BY mix

### Migration Path

**To AG2** (Easy):
```python
# Your current code mostly works!
from autogen import AssistantAgent, UserProxyAgent  # Same!
# Just need to update LLM config format
```

**To Microsoft AutoGen** (Hard):
```python
# Complete rewrite required
from autogen_agentchat.agents import AssistantAgent  # Different!
import asyncio  # Must use async
# Everything changes
```

## Decision Matrix

| Feature | Microsoft AutoGen | AG2 |
|---------|------------------|-----|
| **API Compatibility** | ❌ Completely new | ✅ Similar to old |
| **Your Code Works?** | ❌ No (needs rewrite) | ✅ Yes (minimal changes) |
| **Latest Release** | 3 months ago | 2 weeks ago |
| **Activity** | Lower | Higher |
| **Package Structure** | Multiple packages | Single package |
| **Async Required** | ✅ Yes | ❌ No |
| **Community** | Microsoft | Open community |
| **License** | MIT/CC-BY | Apache 2.0 |

## Recommendation

**Use AG2** because:
1. ✅ Your code already matches its API
2. ✅ More active development
3. ✅ Easier migration path
4. ✅ Better community support
5. ✅ Single package installation

## Next Steps

1. Update requirements to use AG2
2. Update compatibility layer to support AG2
3. Test with AG2
4. Keep Microsoft AutoGen support as fallback (deprecated)
