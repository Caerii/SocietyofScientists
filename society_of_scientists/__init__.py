"""
Society of Scientists - Multi-Agent AI System for Research Grant Proposal Generation

A collaborative multi-agent system where specialized scientist agents work together
to generate comprehensive research grant proposals.
"""

__version__ = "0.1.0"
__author__ = "Society of Scientists Team"

# Core imports
from .agents import (
    create_scientist_agents,
    create_grant_writers,
    create_orchestrators,
    create_critic,
    create_society_of_mind_system,
    get_llm_config
)

from .clients import AI21JambaModelClient
from .config import Settings
from .tools import (
    ExaSearch,
    exa_search_function,
    load_research_summaries,
    get_computer_vision_context,
    get_ai_language_models_context,
    get_ai_hardware_context,
    get_computational_neuroscience_context
)
from .utils import (
    CostTracker, 
    get_tracker,
    get_autogen_version,
    get_autogen_type,
    is_ag2,
    is_autogen_v3_plus,
    VERSION_INFO
)

__all__ = [
    # Version
    "__version__",
    
    # Agents
    "create_scientist_agents",
    "create_grant_writers",
    "create_orchestrators",
    "create_critic",
    "create_society_of_mind_system",
    "get_llm_config",
    
    # Clients
    "AI21JambaModelClient",
    
    # Config
    "Settings",
    
    # Tools
    "ExaSearch",
    "exa_search_function",
    "load_research_summaries",
    "get_computer_vision_context",
    "get_ai_language_models_context",
    "get_ai_hardware_context",
    "get_computational_neuroscience_context",
    
    # Utils
    "CostTracker",
    "get_tracker",
    "get_autogen_version",
    "get_autogen_type",
    "is_ag2",
    "is_autogen_v3_plus",
    "VERSION_INFO",
]
