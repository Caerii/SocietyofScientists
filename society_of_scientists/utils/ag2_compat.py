"""
AG2 Compatibility Layer

AG2 (ag2ai/ag2) is the recommended AutoGen fork because:
- Latest version: v0.10.4 (very recent)
- API matches your current code
- Active community development
- Single package installation

This module provides compatibility for AG2 and Microsoft AutoGen.
"""

import warnings
from typing import Optional, Tuple, Any, Dict
import importlib

# Detect which AutoGen/AG2 package is installed
_autogen_type: Optional[str] = None  # 'ag2', 'microsoft_old', 'microsoft_new', None
_autogen_version: Optional[Tuple[int, ...]] = None

# Try AG2 first (recommended)
try:
    import autogen
    # Check if it's AG2 by trying to import AG2-specific features
    try:
        from autogen import LLMConfig
        _autogen_type = 'ag2'
        if hasattr(autogen, '__version__'):
            version_str = autogen.__version__
            parts = version_str.split('.')
            _autogen_version = tuple(map(int, parts[:2]))
    except ImportError:
        # Might be old Microsoft AutoGen
        _autogen_type = 'microsoft_old'
        if hasattr(autogen, '__version__'):
            version_str = autogen.__version__
            parts = version_str.split('.')
            _autogen_version = tuple(map(int, parts[:2]))
except ImportError:
    pass

# Try Microsoft new API
if _autogen_type is None:
    try:
        import autogen_agentchat
        _autogen_type = 'microsoft_new'
        if hasattr(autogen_agentchat, '__version__'):
            version_str = autogen_agentchat.__version__
            parts = version_str.split('.')
            _autogen_version = tuple(map(int, parts[:2]))
    except ImportError:
        pass

# Default
if _autogen_version is None:
    _autogen_version = (0, 10)


def get_autogen_type() -> str:
    """Get which AutoGen/AG2 package is installed."""
    return _autogen_type or 'unknown'


def is_ag2() -> bool:
    """Check if AG2 is installed (recommended)."""
    return _autogen_type == 'ag2'


def is_microsoft_old() -> bool:
    """Check if old Microsoft AutoGen is installed."""
    return _autogen_type == 'microsoft_old'


def is_microsoft_new() -> bool:
    """Check if new Microsoft AutoGen (autogen-agentchat) is installed."""
    return _autogen_type == 'microsoft_new'


def get_autogen_version() -> Tuple[int, ...]:
    """Get version tuple."""
    return _autogen_version or (0, 10)


def get_version_info() -> Dict[str, Any]:
    """Get comprehensive version information."""
    return {
        'type': get_autogen_type(),
        'version': get_autogen_version(),
        'version_string': '.'.join(map(str, get_autogen_version())),
        'is_ag2': is_ag2(),
        'is_microsoft_old': is_microsoft_old(),
        'is_microsoft_new': is_microsoft_new(),
        'recommended': 'ag2' if is_ag2() else 'Install AG2 for best compatibility',
    }


VERSION_INFO = get_version_info()
