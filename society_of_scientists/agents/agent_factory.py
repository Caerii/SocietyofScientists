"""Factory for creating all agents in the Society of Scientists system."""
import autogen
from autogen import AssistantAgent, UserProxyAgent
from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent
from ..clients.jamba_client import AI21JambaModelClient
from ..config import Settings
from ..tools import exa_search_function

# Version-aware compatibility layer (supports v2 and v3+)
from ..utils.autogen_compat import (
    create_agent,
    register_model_client,
    register_function_compat,
    is_autogen_v3_plus,
    get_version_info,
    VERSION_INFO
)

# Import register_function for fallback
try:
    from autogen import register_function
except ImportError:
    register_function = None

# Import agent prompts
from ..agent_list import (
    scientist_computer_vision_engineer_prompt,
    scientist_ai_language_models_prompt,
    scientist_ai_hardware_engineer_prompt,
    scientist_prompt,
    hypothesis_agent_prompt,
    objective_agent_prompt,
    methodology_agent_prompt,
    ethics_agent_prompt,
    comparison_agent_prompt,
    novelty_agent_prompt,
    budget_agent_prompt,
    critic_agent_prompt
)


def get_llm_config():
    """Get LLM configuration from settings."""
    settings = Settings()
    return {
        "config_list": [settings.get_jamba_config()],
    }


def create_scientist_agents(llm_config=None) -> dict:
    """
    Create all scientist agents.
    
    Args:
        llm_config: Optional LLM config. If None, uses settings.
        
    Returns:
        Dictionary with scientist agents
    """
    if llm_config is None:
        llm_config = get_llm_config()
    
    config = llm_config["config_list"][0]
    
    # Use version-aware agent creation (supports v2 and v3+)
    scientist_computer_vision_engineer = create_agent(
        name="scientist_computer_vision_engineer",
        system_message=scientist_computer_vision_engineer_prompt,
        llm_config=llm_config,
    )
    register_model_client(scientist_computer_vision_engineer, AI21JambaModelClient)
    
    scientist_ai_language_models = create_agent(
        name="scientist_ai_language_models",
        system_message=scientist_ai_language_models_prompt,
        llm_config=llm_config,
    )
    register_model_client(scientist_ai_language_models, AI21JambaModelClient)
    
    scientist_ai_hardware_engineer = create_agent(
        name="scientist_ai_hardware_engineer",
        system_message=scientist_ai_hardware_engineer_prompt,
        llm_config=llm_config,
    )
    register_model_client(scientist_ai_hardware_engineer, AI21JambaModelClient)
    
    return {
        "computer_vision": scientist_computer_vision_engineer,
        "ai_language_models": scientist_ai_language_models,
        "ai_hardware": scientist_ai_hardware_engineer,
    }


def create_grant_writers(llm_config=None) -> dict:
    """
    Create all grant writing agents.
    
    Args:
        llm_config: Optional LLM config. If None, uses settings.
        
    Returns:
        Dictionary with grant writing agents
    """
    if llm_config is None:
        llm_config = get_llm_config()
    
    # Use version-aware agent creation
    scientist = create_agent(
        name="scientist",
        system_message=scientist_prompt,
        llm_config=llm_config,
        description='I can craft the grant research proposal with key aspects.',
    )
    register_model_client(scientist, AI21JambaModelClient)
    
    hypothesis_agent = create_agent(
        name="hypothesis_agent",
        system_message=hypothesis_agent_prompt,
        llm_config=llm_config,
        description='''I can expand the "hypothesis" aspect of the research proposal crafted by any of the scientists.''',
    )
    register_model_client(hypothesis_agent, AI21JambaModelClient)
    
    objective_agent = create_agent(
        name="objective_agent",
        system_message=objective_agent_prompt,
        llm_config=llm_config,
        description='''I can expand the "objective" aspect of the research proposal crafted by the "scientist".''',
    )
    register_model_client(objective_agent, AI21JambaModelClient)
    
    methodology_agent = create_agent(
        name="methodology_agent",
        system_message=methodology_agent_prompt,
        llm_config=llm_config,
        description='''I can expand the "methodology" aspect of the research proposal crafted by the "scientist"''',
    )
    register_model_client(methodology_agent, AI21JambaModelClient)
    
    ethics_agent = create_agent(
        name="ethics_agent",
        system_message=ethics_agent_prompt,
        llm_config=llm_config,
        description='''I can expand the "ethics" aspect of the research proposal crafted by the "scientist".''',
    )
    register_model_client(ethics_agent, AI21JambaModelClient)
    
    comparison_agent = create_agent(
        name="comparison_agent",
        system_message=comparison_agent_prompt,
        llm_config=llm_config,
        description='''I can expand the "comparison" aspect of the research proposal crafted by the "scientist".''',
    )
    register_model_client(comparison_agent, AI21JambaModelClient)
    
    novelty_agent = create_agent(
        name="novelty_agent",
        system_message=novelty_agent_prompt,
        llm_config=llm_config,
        description='''I can expand the "novelty" aspect of the research proposal crafted by the "scientist".''',
    )
    register_model_client(novelty_agent, AI21JambaModelClient)
    
    budget_agent = create_agent(
        name="budget_agent",
        system_message=budget_agent_prompt,
        llm_config=llm_config,
        description='''I can expand the "budget" aspect of the research proposal crafted by the "scientist".''',
    )
    register_model_client(budget_agent, AI21JambaModelClient)
    
    return {
        "scientist": scientist,
        "hypothesis": hypothesis_agent,
        "objective": objective_agent,
        "methodology": methodology_agent,
        "ethics": ethics_agent,
        "comparison": comparison_agent,
        "novelty": novelty_agent,
        "budget": budget_agent,
    }


def create_orchestrators(llm_config=None) -> dict:
    """
    Create orchestrator agents (planner, assistant).
    
    Args:
        llm_config: Optional LLM config. If None, uses settings.
        
    Returns:
        Dictionary with orchestrator agents
    """
    if llm_config is None:
        llm_config = get_llm_config()
    
    planner = create_agent(
        name="planner",
        system_message='''Planner. You are a helpful AI assistant. Your task is to suggest a comprehensive plan to write a scientific grant application.

Explain the Plan: Begin by providing a clear overview of the plan.
Break Down the Plan: For each part of the plan, explain the reasoning behind it, and describe the specific actions that need to be taken.
No Execution: Your role is strictly to suggest the plan. Do not take any actions to execute it.
No Tool Call: You are not allowed to call any Tool or function yourself. 

''',
        llm_config=llm_config,
        description='Who can suggest a step-by-step plan to solve the task by breaking down the task into simpler sub-tasks.',
    )
    register_model_client(planner, AI21JambaModelClient)
    
    return {
        "planner": planner,
    }


def create_critic(llm_config=None) -> AssistantAgent:
    """
    Create the critic agent.
    
    Args:
        llm_config: Optional LLM config. If None, uses settings.
        
    Returns:
        Critic agent
    """
    if llm_config is None:
        llm_config = get_llm_config()
    
    critic_agent = create_agent(
        name="critic_agent",
        system_message=critic_agent_prompt,
        llm_config=llm_config,
        description='''I can summarizes, critique, and suggest improvements after all seven aspects of the proposal have been expanded by the agents.''',
    )
    register_model_client(critic_agent, AI21JambaModelClient)
    
    return critic_agent


def create_society_of_mind_system(
    task: str,
    max_rounds: int = 50,
    speaker_selection_method: str = 'round_robin',
    register_exa_tool: bool = True
) -> tuple:
    """
    Create the complete Society of Mind multi-agent system.
    
    Args:
        task: The research task/proposal topic
        max_rounds: Maximum number of conversation rounds
        speaker_selection_method: Method for selecting speakers ('round_robin' or 'auto')
        register_exa_tool: Whether to register Exa search tool
        
    Returns:
        Tuple of (society_of_mind_agent, user_proxy, manager)
    """
    llm_config = get_llm_config()
    
    # Create all agents
    scientists = create_scientist_agents(llm_config)
    grant_writers = create_grant_writers(llm_config)
    orchestrators = create_orchestrators(llm_config)
    critic = create_critic(llm_config)
    
    # Collect all agents
    all_agents = [
        orchestrators["planner"],
        scientists["computer_vision"],
        scientists["ai_language_models"],
        scientists["ai_hardware"],
        grant_writers["scientist"],
        grant_writers["hypothesis"],
        grant_writers["objective"],
        grant_writers["methodology"],
        grant_writers["novelty"],
        grant_writers["ethics"],
        grant_writers["budget"],
        critic,
    ]
    
    # Create group chat
    groupchat = autogen.GroupChat(
        agents=all_agents,
        messages=[],
        max_round=max_rounds,
        admin_name='user',
        send_introductions=True,
        allow_repeat_speaker=True,
        speaker_selection_method=speaker_selection_method,
    )
    
    manager = autogen.GroupChatManager(
        groupchat=groupchat,
        llm_config=llm_config,
        system_message='moderator. You are a helpful AI assistant. Your task is to moderate an academic discussion between scientists who are experts in distinct different fields and select the next speaker from the group of scientists that would be good to speak based on the discussion.'
    )
    
    # Create Society of Mind agent
    society_of_mind_agent = SocietyOfMindAgent(
        "society_of_mind",
        chat_manager=manager,
        llm_config=llm_config,
    )
    register_model_client(society_of_mind_agent, AI21JambaModelClient)
    
    # Create user proxy
    user_proxy = autogen.UserProxyAgent(
        "user_proxy",
        human_input_mode="NEVER",
        code_execution_config=False,
        default_auto_reply="",
        is_termination_msg=lambda x: True,
    )
    
    # Register Exa search tool if requested (version-aware)
    if register_exa_tool:
        register_function_compat(
            exa_search_function,
            caller=society_of_mind_agent,
            executor=user_proxy,
            name="exa_search",
            description="A tool to search for research papers. Uses cached data by default."
        )
    
    return society_of_mind_agent, user_proxy, manager
