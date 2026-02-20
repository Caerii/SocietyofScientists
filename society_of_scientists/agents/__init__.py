"""Agent definitions and configurations."""
from .agent_factory import (
    create_scientist_agents,
    create_grant_writers,
    create_orchestrators,
    create_critic,
    create_society_of_mind_system,
    get_llm_config
)

__all__ = [
    'create_scientist_agents',
    'create_grant_writers',
    'create_orchestrators',
    'create_critic',
    'create_society_of_mind_system',
    'get_llm_config'
]
