"""
AutoGen/AG2 Version Compatibility Layer

Supports:
- AG2 (ag2ai/ag2) - RECOMMENDED - v0.10.4+ (active fork, matches your code)
- Microsoft AutoGen old (0.2.x) - DEPRECATED but supported
- Microsoft AutoGen new (0.7+) - DEPRECATED but supported

- Detects installed package (AG2 vs Microsoft AutoGen)
- Uses latest features when available
- Falls back to older patterns when needed
- Deprecation warnings for old usage (but never removes support)
"""
import warnings
from typing import Optional, Tuple, Any, Dict
import importlib

# Try to detect which AutoGen/AG2 package is installed
_autogen_version: Optional[Tuple[int, ...]] = None
_autogen_major: int = 0
_autogen_type: str = 'unknown'  # 'ag2', 'microsoft_old', 'microsoft_new'

# Try AG2 first (recommended - matches your code)
try:
    import autogen
    # Check if it's AG2 (has LLMConfig) or old Microsoft AutoGen
    try:
        from autogen import LLMConfig
        _autogen_type = 'ag2'
        if hasattr(autogen, '__version__'):
            version_str = autogen.__version__
            parts = version_str.split('.')
            _autogen_version = tuple(map(int, parts[:2]))
            _autogen_major = _autogen_version[0] if _autogen_version else 0
    except ImportError:
        # Old Microsoft AutoGen
        _autogen_type = 'microsoft_old'
        if hasattr(autogen, '__version__'):
            version_str = autogen.__version__
            parts = version_str.split('.')
            _autogen_version = tuple(map(int, parts[:2]))
            _autogen_major = _autogen_version[0] if _autogen_version else 0
        else:
            # Try package metadata
            try:
                import pkg_resources
                dist = pkg_resources.get_distribution('pyautogen')
                version_str = dist.version
                parts = version_str.split('.')
                _autogen_version = tuple(map(int, parts[:2]))
                _autogen_major = _autogen_version[0] if _autogen_version else 0
            except:
                _autogen_version = (0, 2)
                _autogen_major = 0
except ImportError:
    # Try Microsoft new API
    try:
        import autogen_agentchat
        _autogen_type = 'microsoft_new'
        if hasattr(autogen_agentchat, '__version__'):
            version_str = autogen_agentchat.__version__
            parts = version_str.split('.')
            _autogen_version = tuple(map(int, parts[:2]))
            _autogen_major = _autogen_version[0] if _autogen_version else 0
    except ImportError:
        _autogen_version = (0, 10)  # Default to AG2 latest
        _autogen_major = 0


def get_autogen_type() -> str:
    """Get which AutoGen/AG2 package is installed."""
    return _autogen_type or 'unknown'


def is_ag2() -> bool:
    """Check if AG2 is installed (recommended)."""
    return _autogen_type == 'ag2'


def is_microsoft_old() -> bool:
    """Check if old Microsoft AutoGen (0.2.x) is installed."""
    return _autogen_type == 'microsoft_old'


def is_microsoft_new() -> bool:
    """Check if new Microsoft AutoGen (0.7+) is installed."""
    return _autogen_type == 'microsoft_new'


def get_autogen_version() -> Tuple[int, ...]:
    """Get AutoGen/AG2 version tuple (major, minor)."""
    return _autogen_version or (0, 10)


def is_autogen_v3_plus() -> bool:
    """Check if AutoGen v3+ or AG2 is installed (0.3+, 0.4+, 0.10+, etc.)."""
    if is_ag2():
        return True  # AG2 is always "new"
    if _autogen_version:
        major, minor = _autogen_version[0], _autogen_version[1] if len(_autogen_version) > 1 else 0
        # 0.3+, 0.4+, 0.10+ are considered "new" versions
        # 0.2.x is v2
        return (major > 0 and minor >= 3) or (major >= 3)
    return False


def is_autogen_v2() -> bool:
    """Check if old Microsoft AutoGen v2 is installed (0.2.x)."""
    if is_ag2():
        return False  # AG2 is not v2
    if _autogen_version:
        major, minor = _autogen_version[0], _autogen_version[1] if len(_autogen_version) > 1 else 0
        return major == 0 and minor == 2
    return False


def deprecation_warning_v2(feature: str, alternative: str = None):
    """Show deprecation warning for old API usage (but still support it)."""
    if is_ag2():
        return  # No warning for AG2 - it's recommended!
    
    msg = f"Using old Microsoft AutoGen pattern for '{feature}'. "
    if alternative:
        msg += f"Consider using AG2: {alternative}. "
    msg += "Old API support will remain available but is deprecated."
    warnings.warn(msg, DeprecationWarning, stacklevel=3)


# Import AutoGen components with version-aware handling
def import_autogen_components():
    """Import AutoGen components, handling version differences."""
    try:
        import autogen
        from autogen import AssistantAgent, UserProxyAgent
        
        # Try to import GroupChat and GroupChatManager
        GroupChat = None
        GroupChatManager = None
        try:
            from autogen import GroupChat, GroupChatManager
        except ImportError:
            pass  # Not available in some versions
        
        # Try to import register_function
        register_function = None
        try:
            from autogen import register_function
        except ImportError:
            pass  # Not available in some versions
        
        # Try to import SocietyOfMindAgent
        SocietyOfMindAgent = None
        try:
            from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent
        except ImportError:
            pass  # Not available in some versions
        
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
        raise ImportError(f"AutoGen not installed: {e}")


# Version-aware agent creation
def create_agent_v3_plus(name: str, system_message: str, llm_config: Dict, **kwargs) -> Any:
    """Create agent using v3+ patterns (latest features)."""
    components = import_autogen_components()
    AssistantAgent = components['AssistantAgent']
    
    # Use latest API if available
    # In v3+, there might be new parameters or patterns
    # Try to use any new features that might be available
    try:
        return AssistantAgent(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            **kwargs
        )
    except TypeError:
        # If new parameters don't work, fall back to basic
        basic_kwargs = {k: v for k, v in kwargs.items() 
                       if k in ['description', 'human_input_mode', 'code_execution_config']}
        return AssistantAgent(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            **basic_kwargs
        )


def create_agent_v2(name: str, system_message: str, llm_config: Dict, **kwargs) -> Any:
    """Create agent using v2 patterns (deprecated but supported)."""
    deprecation_warning_v2(
        'create_agent',
        'Using latest AutoGen version for new features'
    )
    components = import_autogen_components()
    AssistantAgent = components['AssistantAgent']
    
    return AssistantAgent(
        name=name,
        system_message=system_message,
        llm_config=llm_config,
        **kwargs
    )


def create_agent(name: str, system_message: str, llm_config: Dict, **kwargs) -> Any:
    """Create agent with version-aware implementation."""
    if is_autogen_v3_plus():
        return create_agent_v3_plus(name, system_message, llm_config, **kwargs)
    else:
        return create_agent_v2(name, system_message, llm_config, **kwargs)


# Version-aware model client registration
def register_model_client_v3_plus(agent: Any, model_client_cls: type):
    """Register model client using v3+ patterns."""
    # In v3+, the API might be the same or enhanced
    if hasattr(agent, 'register_model_client'):
        agent.register_model_client(model_client_cls=model_client_cls)
    else:
        # Fallback for different API
        raise AttributeError("register_model_client not available in this AutoGen version")


def register_model_client_v2(agent: Any, model_client_cls: type):
    """Register model client using v2 patterns (deprecated but supported)."""
    deprecation_warning_v2(
        'register_model_client',
        'Using latest AutoGen version for enhanced model client support'
    )
    if hasattr(agent, 'register_model_client'):
        agent.register_model_client(model_client_cls=model_client_cls)
    else:
        raise AttributeError("register_model_client not available")


def register_model_client(agent: Any, model_client_cls: type):
    """Register model client with version-aware implementation."""
    if is_autogen_v3_plus():
        register_model_client_v3_plus(agent, model_client_cls)
    else:
        register_model_client_v2(agent, model_client_cls)


# Version-aware function registration
def register_function_v3_plus(func, caller, executor, name: str, description: str):
    """Register function using v3+ patterns."""
    components = import_autogen_components()
    register_function = components['register_function']
    
    if register_function:
        # In v3+, there might be enhanced function registration
        register_function(
            func,
            caller=caller,
            executor=executor,
            name=name,
            description=description
        )
    else:
        raise ImportError("register_function not available in this AutoGen version")


def register_function_v2(func, caller, executor, name: str, description: str):
    """Register function using v2 patterns (deprecated but supported)."""
    deprecation_warning_v2(
        'register_function',
        'Using latest AutoGen version for enhanced tool support'
    )
    components = import_autogen_components()
    register_function = components['register_function']
    
    if register_function:
        register_function(
            func,
            caller=caller,
            executor=executor,
            name=name,
            description=description
        )
    else:
        raise ImportError("register_function not available in this AutoGen version")


def register_function_compat(func, caller, executor, name: str, description: str):
    """Register function with version-aware implementation."""
    if is_autogen_v3_plus():
        register_function_v3_plus(func, caller, executor, name, description)
    else:
        register_function_v2(func, caller, executor, name, description)


# Version info
def get_version_info() -> Dict[str, Any]:
    """Get AutoGen/AG2 version information."""
    version = get_autogen_version()
    return {
        'type': get_autogen_type(),
        'version': version,
        'version_string': '.'.join(map(str, version)),
        'major': version[0] if version else 0,
        'minor': version[1] if len(version) > 1 else 0,
        'is_ag2': is_ag2(),
        'is_microsoft_old': is_microsoft_old(),
        'is_microsoft_new': is_microsoft_new(),
        'is_v3_plus': is_autogen_v3_plus(),
        'is_v2': is_autogen_v2(),
        'recommended': 'AG2' if is_ag2() else 'Install AG2 for best compatibility',
    }


# Export version info at module level
VERSION_INFO = get_version_info()
