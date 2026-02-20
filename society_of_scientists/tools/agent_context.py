"""Utilities to provide research context to agents from cached data."""
from typing import Dict, List
from .data_loader import load_research_summaries_by_topic


def get_agent_research_context() -> Dict[str, str]:
    """
    Get research summaries organized by topic for agent context.
    
    Returns:
        Dictionary mapping topic names to formatted summary strings
    """
    summaries_by_topic = load_research_summaries_by_topic()
    
    context = {}
    for topic, summaries in summaries_by_topic.items():
        if summaries:
            # Format summaries for agent prompts
            formatted = "\n\n".join([f"summary: {s}" for s in summaries])
            context[topic] = formatted
    
    return context


def get_computer_vision_context() -> str:
    """Get computer vision research summaries for agent context."""
    summaries = load_research_summaries('computer_vision')
    if summaries:
        return "\n\n".join([f"summary: {s}" for s in summaries])
    return ""


def get_ai_language_models_context() -> str:
    """Get AI/language models research summaries for agent context."""
    summaries = load_research_summaries('large_language_models')
    if summaries:
        return "\n\n".join([f"summary: {s}" for s in summaries])
    return ""


def get_ai_hardware_context() -> str:
    """Get AI hardware research summaries for agent context."""
    summaries = load_research_summaries('hardware_for_AI')
    if summaries:
        return "\n\n".join([f"summary: {s}" for s in summaries])
    return ""


def get_computational_neuroscience_context() -> str:
    """Get computational neuroscience research summaries for agent context."""
    summaries = load_research_summaries('computational_neuroscience')
    if summaries:
        return "\n\n".join([f"summary: {s}" for s in summaries])
    return ""
