"""
DEPRECATED: This file is kept for backward compatibility.

For new code, use:
    from society_of_scientists import create_society_of_mind_system
    
    agent, user_proxy, manager = create_society_of_mind_system(task="...")
    result = user_proxy.initiate_chat(agent, message="...")

See examples/multi_agent_system.py for the recommended approach.
"""
# from types import SimpleNamespace  # Not currently used
from autogen import AssistantAgent, UserProxyAgent
import autogen
from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent
# from markdown import markdown  # Uncomment if needed
# from fpdf import FPDF  # Uncomment if needed

# Use centralized client
from .clients.jamba_client import AI21JambaModelClient

# Import our agents definitions from here:
from .agent_list import scientist_computer_vision_engineer_prompt, scientist_ai_language_models_prompt, scientist_ai_hardware_engineer_prompt, scientist_prompt, hypothesis_agent_prompt, objective_agent_prompt, methodology_agent_prompt, ethics_agent_prompt, comparison_agent_prompt, novelty_agent_prompt, budget_agent_prompt, critic_agent_prompt

# Use centralized config and client
from .config import Settings
from .agents import get_llm_config

settings = Settings()
config_list_custom = [settings.get_jamba_config()]
config_list_custom[0]["model"] = "jamba-large"  # Use working model name
# API key is loaded from environment variables via Settings (already in config_list_custom)
config_list_custom[0]["temperature"] = 0.1
config_list_custom[0]["max_tokens"] = 2048

# Initialize Assistant and Register the AI21JambaModelClient
assistant = AssistantAgent("assistant", llm_config={"config_list": config_list_custom})
assistant.register_model_client(model_client_cls=AI21JambaModelClient)


# Set up the user proxy agent
user_proxy = UserProxyAgent(
   "user_proxy",
   code_execution_config={
       "work_dir": "coding",
       "use_docker": False
   }
)

"""
SCIENTISTS
"""
scientist_computer_vision_engineer = autogen.AssistantAgent(
    name="scientist_computer_vision_engineer",
    system_message = scientist_computer_vision_engineer_prompt,
    llm_config=config_list_custom[0],
)
scientist_computer_vision_engineer.register_model_client(model_client_cls=AI21JambaModelClient)

scientist_ai_language_models = autogen.AssistantAgent(
    name="scientist_ai_language_models",
    system_message = scientist_ai_language_models_prompt,
    llm_config=config_list_custom[0],
)
scientist_ai_language_models.register_model_client(model_client_cls=AI21JambaModelClient)

scientist_ai_hardware_engineer = autogen.AssistantAgent(
    name="scientist_ai_hardware_engineer",
    system_message = scientist_ai_hardware_engineer_prompt,
    llm_config=config_list_custom[0],
)
scientist_ai_hardware_engineer.register_model_client(model_client_cls=AI21JambaModelClient)

"""
GRANT WRITERS
"""
planner = AssistantAgent(
   name="planner",
   system_message = '''Planner. You are a helpful AI assistant. Your task is to suggest a comprehensive plan to write a scientific grant application.

Explain the Plan: Begin by providing a clear overview of the plan.
Break Down the Plan: For each part of the plan, explain the reasoning behind it, and describe the specific actions that need to be taken.
No Execution: Your role is strictly to suggest the plan. Do not take any actions to execute it.
No Tool Call: You are not allowed to call any Tool or function yourself. 

''',
   llm_config=config_list_custom[0],
   description='Who can suggest a step-by-step plan to solve the task by breaking down the task into simpler sub-tasks.',
)
planner.register_model_client(model_client_cls=AI21JambaModelClient)

scientist = AssistantAgent(
   name="scientist",
   system_message = scientist_prompt,
   llm_config=config_list_custom[0],
   description='I can craft the grant research proposal with key aspects.',
)
scientist.register_model_client(model_client_cls=AI21JambaModelClient)

hypothesis_agent = AssistantAgent(
   name="hypothesis_agent",
   system_message = hypothesis_agent_prompt,
   llm_config=config_list_custom[0],
   description='''I can expand the "hypothesis" aspect of the research proposal crafted by any of the scientists.''',
)
hypothesis_agent.register_model_client(model_client_cls=AI21JambaModelClient)

objective_agent = AssistantAgent(
   name="objective_agent",
   system_message = objective_agent_prompt,
   llm_config=config_list_custom[0],
   description='''I can expand the "objective" aspect of the research proposal crafted by the "scientist".''',
)
objective_agent.register_model_client(model_client_cls=AI21JambaModelClient)

methodology_agent = AssistantAgent(
   name="methodology_agent",
   system_message = methodology_agent_prompt,
   llm_config=config_list_custom[0],
   description='''I can expand the "methodology" aspect of the research proposal crafted by the "scientist"''',
)
methodology_agent.register_model_client(model_client_cls=AI21JambaModelClient)

ethics_agent = AssistantAgent(
   name="ethics_agent",
   system_message = ethics_agent_prompt,
   llm_config=config_list_custom[0],
   description='''I can expand the "ethics" aspect of the research proposal crafted by the "scientist".''',
)
ethics_agent.register_model_client(model_client_cls=AI21JambaModelClient)

comparison_agent = AssistantAgent(
   name="comparison_agent",
   system_message = comparison_agent_prompt,
   llm_config=config_list_custom[0],
   description='''I can expand the "comparison" aspect of the research proposal crafted by the "scientist".''',
)
comparison_agent.register_model_client(model_client_cls=AI21JambaModelClient)

novelty_agent = AssistantAgent(
   name="novelty_agent",
   system_message = novelty_agent_prompt,
   llm_config=config_list_custom[0],
   description='''I can expand the "novelty" aspect of the research proposal crafted by the "scientist".''',
)
novelty_agent.register_model_client(model_client_cls=AI21JambaModelClient)

budget_agent = AssistantAgent(
   name="budget_agent",
   system_message = budget_agent_prompt,
   llm_config=config_list_custom[0],
   description='''I can expand the "budget" aspect of the research proposal crafted by the "scientist".''',
)
budget_agent.register_model_client(model_client_cls=AI21JambaModelClient)

critic_agent = AssistantAgent(
   name="critic_agent",
   system_message = critic_agent_prompt,
   llm_config=config_list_custom[0],
   description='''I can summarizes, critique, and suggest improvements after all seven aspects of the proposal have been expanded by the agents.''',
)
critic_agent.register_model_client(model_client_cls=AI21JambaModelClient)

"""
INITIATE GROUP CHAT
"""

groupchat = autogen.GroupChat(
   agents=[planner, scientist_computer_vision_engineer, scientist_ai_language_models, scientist_ai_hardware_engineer, scientist, hypothesis_agent, objective_agent, methodology_agent, novelty_agent, ethics_agent, budget_agent, critic_agent],
     messages=[],
     max_round=50,
     admin_name='user',
     send_introductions=True,
     allow_repeat_speaker=True,
   speaker_selection_method='round_robin', #change to auto later
)
manager = autogen.GroupChatManager(groupchat=groupchat,
                                  llm_config=config_list_custom[0],
                                  system_message='moderator. You are a helpful AI assistant. Your task is to moderate an academic discussion between scientists who are experts in distinct different fields and select the next speaker from the group of scientists that would be good to speak based on the discussion.')

task = "Propose a novel neural network architecture that draws inspiration from multiple disciplines."

society_of_mind_agent = SocietyOfMindAgent(
   "society_of_mind",
   chat_manager=manager,
   llm_config=config_list_custom[0],
)

society_of_mind_agent.register_model_client(model_client_cls=AI21JambaModelClient)

user_proxy = autogen.UserProxyAgent(
   "user_proxy",
   human_input_mode="NEVER",
   code_execution_config=False,
   default_auto_reply="",
   is_termination_msg=lambda x: True,
)

res = user_proxy.initiate_chat(society_of_mind_agent, message=task)

# Save data
formatted_text = ""
formatted_text_summary = ""
for i in range(len(res.chat_history)):
    try:
        formatted_text += f'''{res.chat_history[i]['tool_calls'][0]['function']['name']}-{res.chat_history[1]['tool_calls'][0]['function']['arguments']}\n\n'''
    except:
        if i==0:
            formatted_text += '### ' + f'''{res.chat_history[i]['content']}\n\n'''
        else:
            formatted_text += f'''{res.chat_history[i]['content']}\n\n'''
            if res.search("Summary of the Initial Research Hypothesis", f'''{res.chat_history[i]['content']}'''):
                formatted_text_summary += f'''{res.chat_history[i]['content']}'''

# Note: Markdown and PDF export functionality commented out
# Uncomment and implement if needed:
# text_markdown = markdown(formatted_text)
# from fpdf import FPDF
# def markdown_to_pdf(text, filename):
#     # Implement PDF export if needed
#     pass
# markdown_to_pdf(formatted_text, 'output_research')

# """
# USER INTERFACE"""

# # Define frontend using Panel
# pn.extension(design="material")

# # Global variable to manage input
# input_future = None
# initiate_chat_task_created = False

# # Define callback function for chat input
# async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
#     global initiate_chat_task_created
#     global input_future

#     if not initiate_chat_task_created:
#         asyncio.create_task(delayed_initiate_chat(user_proxy, assistant, contents))
#     else:
#         if input_future and not input_future.done():
#             input_future.set_result(contents)
#         else:
#             print("There is currently no input being awaited.")

# # Chat interface initialization
# chat_interface = pn.chat.ChatInterface(callback=callback)
# chat_interface.send("Send a message to the Neuroscience Assistant!", user="System", respond=False)

# # Function to print messages
# def print_messages(recipient, messages, sender, config):
#     content = messages[-1]['content']
#     chat_interface.send(content, user=recipient.name, avatar="🧠", respond=False)
#     return False, None  # Ensure the agent communication flow continues

# # Register the message handler for the assistant
# user_proxy.register_reply([AssistantAgent, None], reply_func=print_messages, config={"callback": None})

# # Async task to delay the initiation of the chat
# async def delayed_initiate_chat(agent, recipient, message):
#     global initiate_chat_task_created
#     initiate_chat_task_created = True
#     await asyncio.sleep(2)
#     await agent.a_initiate_chat(recipient, message=message)

# # Serve the chat interface as the Panel app
# chat_interface.servable()

# # Start a conversation with the scientist agent (Initial prompt)