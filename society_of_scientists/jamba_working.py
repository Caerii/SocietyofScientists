from types import SimpleNamespace
from autogen import AssistantAgent, UserProxyAgent
from ai21 import AI21Client
from ai21.models.chat import UserMessage
from types import SimpleNamespace
import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent
from markdown import markdown
from fpdf import FPDF

# Import our agents definitions from here:
from agent_list import scientist_computer_vision_engineer_prompt, scientist_ai_language_models_prompt, scientist_ai_hardware_engineer_prompt, scientist_prompt, hypothesis_agent_prompt, objective_agent_prompt, methodology_agent_prompt, ethics_agent_prompt, comparison_agent_prompt, novelty_agent_prompt, budget_agent_prompt, critic_agent_prompt

# import panel as pn
# import asyncio

config_list_custom = [
   {
       "model": "jamba-1.5-large",
       "model_client_cls": "AI21JambaModelClient",
       "api_key": "5AweiGc6E9UDXMCwtYDVhS5y6LarJoLl",
       "temperature": 0.1,
       "top_p": 1.0,
       "max_tokens": 2048
   }
]

class AI21JambaModelClient:
   def __init__(self, config, **kwargs):
       self.api_key = "5AweiGc6E9UDXMCwtYDVhS5y6LarJoLl"
       self.client = AI21Client(api_key=self.api_key)
       self.model = "jamba-1.5-large"
       self.temperature = config.get('temperature', 0.7)
       self.top_p = config.get('top_p', 1.0)
       print(f"AI21JambaModelClient initialized with config: {config}")

   def create(self, params):
       messages = [
           UserMessage(
               content=params["messages"][0]['content']  # Assuming single user message
           )
       ]
      
       # Calling AI21's Jamba API
       response = self.client.chat.completions.create(
           model=self.model,
           messages=messages,
           temperature=self.temperature,
           top_p=self.top_p,
           max_tokens=params.get("max_tokens", 256),
       )
      
       # Convert the response to the necessary structure
       choices = response.choices
       # Wrap the response in SimpleNamespace to make it compatible with AutoGen
       response_namespace = SimpleNamespace()
       response_namespace.choices = [
           SimpleNamespace(message=SimpleNamespace(content=choice.message.content))
           for choice in choices
       ]
       # Add a cost attribute (even if 0, since AutoGen expects it)
       response_namespace.cost = 0
      
       return response_namespace

   def message_retrieval(self, response):
       """Retrieve the assistant's response from the AI21 API response."""
       # Using attribute access for SimpleNamespace
       choices = response.choices
       return [choice.message.content for choice in choices]

   def cost(self, response) -> float:
       return response.cost


   @staticmethod
   def get_usage(response):
       return {
           "prompt_tokens": 0,
           "completion_tokens": 0,
           "total_tokens": 0,
           "cost": response.cost
       }

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

# assistant = AssistantAgent(
#    name="assistant",
#    system_message = '''You are a helpful AI assistant.
  
# Your role is to call the appropriate tools and functions as suggested in the plan. You act as an intermediary between the planner's suggested plan and the execution of specific tasks using the available tools. You ensure that the correct parameters are passed to each tool and that the results are accurately reported back to the team.

# Return "TERMINATE" in the end when the task is over.
# ''',
#    llm_config=config_list_custom[0],
#    description='''An assistant who calls the tools and functions as needed and returns the results. Tools include "rate_novelty_feasibility" and "generate_path".''',
# )
# assistant.register_model_client(model_client_cls=AI21JambaModelClient)

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

text_markdown = Markdown(formatted_text)

markdown_to_pdf(formatted_text, 'output_research')

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