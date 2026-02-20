"""
AutoGen v0.7+ Compatibility Layer

AutoGen has been restructured into new packages:
- autogen-agentchat (new main package)
- autogen-ext (extensions)
- autogen-core (core functionality)
- pyautogen (old package, still available)

This module provides compatibility for BOTH old and new AutoGen APIs.
"""

import warnings
from typing import Optional, Tuple, Any, Dict, List
import importlib

# Detect which AutoGen version/packages are installed
_autogen_package_type: Optional[str] = None  # 'old' or 'new'
_autogen_version: Optional[Tuple[int, ...]] = None
_autogen_agentchat_available: bool = False
_autogen_old_available: bool = False

# Try to detect new AutoGen (autogen-agentchat)
try:
    import autogen_agentchat
    _autogen_agentchat_available = True
    _autogen_package_type = 'new'
    if hasattr(autogen_agentchat, '__version__'):
        version_str = autogen_agentchat.__version__
        parts = version_str.split('.')
        _autogen_version = tuple(map(int, parts[:2]))
except ImportError:
    pass

# Try to detect old AutoGen (pyautogen/autogen)
if not _autogen_agentchat_available:
    try:
        import autogen
        _autogen_old_available = True
        _autogen_package_type = 'old'
        if hasattr(autogen, '__version__'):
            version_str = autogen.__version__
            parts = version_str.split('.')
            _autogen_version = tuple(map(int, parts[:2]))
    except ImportError:
        pass

# Default fallback
if _autogen_version is None:
    _autogen_version = (0, 2)


def get_autogen_package_type() -> str:
    """Get which AutoGen package is installed ('old' or 'new')."""
    return _autogen_package_type or 'old'


def is_autogen_new_api() -> bool:
    """Check if new AutoGen API (autogen-agentchat) is installed."""
    return _autogen_agentchat_available


def is_autogen_old_api() -> bool:
    """Check if old AutoGen API (pyautogen) is installed."""
    return _autogen_old_available


def get_autogen_version() -> Tuple[int, ...]:
    """Get AutoGen version tuple (major, minor)."""
    return _autogen_version or (0, 2)


def deprecation_warning_old_api(feature: str, alternative: str = None):
    """Show deprecation warning for old API usage (but still support it)."""
    msg = f"Using old AutoGen API (pyautogen) for '{feature}'. "
    if alternative:
        msg += f"Consider using new API: {alternative}. "
    msg += "Old API support will remain available but is deprecated."
    warnings.warn(msg, DeprecationWarning, stacklevel=3)


# New API imports (autogen-agentchat)
def import_new_autogen():
    """Import new AutoGen API components."""
    try:
        from autogen_agentchat.agents import AssistantAgent
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        # Try to import other new components
        try:
            from autogen_agentchat.tools import AgentTool
        except ImportError:
            AgentTool = None
        
        try:
            from autogen_agentchat.ui import Console
        except ImportError:
            Console = None
        
        return {
            'AssistantAgent': AssistantAgent,
            'OpenAIChatCompletionClient': OpenAIChatCompletionClient,
            'AgentTool': AgentTool,
            'Console': Console,
        }
    except ImportError as e:
        raise ImportError(f"New AutoGen API (autogen-agentchat) not installed: {e}")


# Old API imports (pyautogen)
def import_old_autogen():
    """Import old AutoGen API components."""
    try:
        import autogen
        from autogen import AssistantAgent, UserProxyAgent
        
        GroupChat = None
        GroupChatManager = None
        try:
            from autogen import GroupChat, GroupChatManager
        except ImportError:
            pass
        
        register_function = None
        try:
            from autogen import register_function
        except ImportError:
            pass
        
        SocietyOfMindAgent = None
        try:
            from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent
        except ImportError:
            pass
        
        return {
            'autogen': autogen,
            'AssistantAgent': AssistantAgent,
            'UserProxyAgent': UserProxyAgent,
            'GroupChat': GroupChat,
            'GroupChatManager': GroupChatManager,
            'register_function': register_function,
            'SocietyOfMindAgent': SocietyOfMindAgent,
        }
    except ImportError as e:
        raise ImportError(f"Old AutoGen API (pyautogen) not installed: {e}")


# Unified agent creation (works with both APIs)
def create_agent_unified(
    name: str,
    system_message: str,
    llm_config: Dict = None,
    model_client=None,
    **kwargs
) -> Any:
    """
    Create agent using appropriate API (new or old).
    
    Args:
        name: Agent name
        system_message: System message/prompt
        llm_config: LLM config (old API) or None
        model_client: Model client (new API) or None
        **kwargs: Additional arguments
    """
    if is_autogen_new_api():
        # Use new API (autogen-agentchat)
        components = import_new_autogen()
        AssistantAgent = components['AssistantAgent']
        
        if model_client is None:
            raise ValueError("New API requires model_client parameter")
        
        return AssistantAgent(
            name=name,
            system_message=system_message,
            model_client=model_client,
            **kwargs
        )
    else:
        # Use old API (pyautogen)
        deprecation_warning_old_api(
            'create_agent',
            'autogen_agentchat.agents.AssistantAgent'
        )
        components = import_old_autogen()
        AssistantAgent = components['AssistantAgent']
        
        if llm_config is None:
            raise ValueError("Old API requires llm_config parameter")
        
        return AssistantAgent(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            **kwargs
        )


def get_version_info() -> Dict[str, Any]:
    """Get comprehensive AutoGen version information."""
    return {
        'version': get_autogen_version(),
        'version_string': '.'.join(map(str, get_autogen_version())),
        'package_type': get_autogen_package_type(),
        'is_new_api': is_autogen_new_api(),
        'is_old_api': is_autogen_old_api(),
        'new_api_available': _autogen_agentchat_available,
        'old_api_available': _autogen_old_available,
    }


# Export version info
VERSION_INFO = get_version_info()
