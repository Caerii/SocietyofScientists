# AutoGen Version Check

## Current Configuration

- **Required Version**: `autogen>=0.2.28` (in `requirements.txt` and `setup.py`)
- **Package Name**: `pyautogen` (installed via pip)

## Usage Patterns

### ✅ Current Patterns (Up to Date)

1. **Agent Creation**
   ```python
   from autogen import AssistantAgent, UserProxyAgent
   agent = AssistantAgent(name="...", system_message="...", llm_config={...})
   ```

2. **Model Client Registration**
   ```python
   agent.register_model_client(model_client_cls=AI21JambaModelClient)
   ```
   ✅ This is the current pattern for custom model clients

3. **Group Chat**
   ```python
   from autogen import GroupChat, GroupChatManager
   groupchat = GroupChat(agents=[...], max_round=50, ...)
   manager = GroupChatManager(groupchat=groupchat, ...)
   ```
   ✅ Current pattern

4. **Function Registration**
   ```python
   from autogen import register_function
   register_function(
       exa_search_function,
       caller=agent,
       executor=user_proxy,
       name="exa_search",
       description="..."
   )
   ```
   ✅ Current pattern for tool registration

5. **Society of Mind Agent**
   ```python
   from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent
   ```
   ✅ Using contrib module (experimental but supported)

## Recommendations

### Check Latest Version
```bash
pip index versions pyautogen
# or
pip install --upgrade pyautogen --dry-run
```

### Update if Needed
If a newer version is available:
```bash
pip install --upgrade pyautogen
# Then update requirements.txt:
# autogen>=0.2.28  # Update to latest version
```

## Potential Issues to Watch

1. **Breaking Changes**: AutoGen 0.2.x is relatively stable, but check release notes for 0.3.x if it exists
2. **Contrib Modules**: `SocietyOfMindAgent` is in contrib, so it may change more frequently
3. **Model Client API**: The `register_model_client` pattern is current, but verify it hasn't changed

## Status

✅ **Current patterns appear to be up-to-date** based on AutoGen 0.2.x API

To verify:
1. Check installed version: `pip show pyautogen`
2. Check latest version: `pip index versions pyautogen`
3. Review AutoGen changelog: https://github.com/microsoft/autogen/releases
