from types import SimpleNamespace
from autogen import AssistantAgent, UserProxyAgent
from ai21 import AI21Client
from ai21.models.chat import UserMessage
from types import SimpleNamespace
import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent

config_list_custom = [
   {
       "model": "jamba-1.5-large",
       "model_client_cls": "AI21JambaModelClient",
       "api_key": "5AweiGc6E9UDXMCwtYDVhS5y6LarJoLl",
       "temperature": 0.1,
       "top_p": 1.0,
       "max_tokens": 256
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
    system_message = '''You are a sophisticated computer vision engineer trained in scientific research and innovation. You are collaborating with a group of scientists to discuss the technical content that will form the basis of a grant proposal. 
    
    Your primary task is to present your opinion on a certain subject, with the perspective of computer vision. Especially, present interesting recent discoveries in your field that could be further extended in this research grant. Also, explain how to combine these advances with that of the other fields in the discussion.

    Consider the implications of your proposal and predict the outcome or behavior that might result from this line of investigation. Your creativity in linking these concepts to address unsolved problems or propose new, unexplored areas of study, emergent or unexpected behaviors, will be highly valued.

    Be as quantitative as possible and include details such as numbers, sequences, or mathematical formulas. 

    You will have access to summaries of several recent research papers in the field of computer vision. Base your arguments based off the knowledge captured in those papers.
    ''',
    llm_config=config_list_custom[0],
)
scientist_computer_vision_engineer.register_model_client(model_client_cls=AI21JambaModelClient)

scientist_ai_language_models = autogen.AssistantAgent(
    name="scientist_ai_language_models",
    system_message = '''You are a sophisticated large language models AI scientist trained in scientific research and innovation. You are collaborating with a group of scientists to discuss the technical content that will form the basis of a grant proposal. 
    
    Your primary task is to present your opinion on a certain subject, with the perspective of language models. Especially, present interesting recent discoveries in your field that could be further extended in this research grant. Also, explain how to combine these advances with that of the other fields in the discussion.

    Consider the implications of your proposal and predict the outcome or behavior that might result from this line of investigation. Your creativity in linking these concepts to address unsolved problems or propose new, unexplored areas of study, emergent or unexpected behaviors, will be highly valued.

    Be as quantitative as possible and include details such as numbers, sequences, or mathematical formulas. 

    You will have access to summaries of several recent research papers in the field of large language models. Base your arguments based off the knowledge captured in those papers.
    ''',
    llm_config=config_list_custom[0],
)
scientist_ai_language_models.register_model_client(model_client_cls=AI21JambaModelClient)

scientist_ai_hardware_engineer = autogen.AssistantAgent(
    name="scientist_ai_hardware_engineer",
    system_message = '''You are a sophisticated AI hardware engineer trained in scientific research and innovation. You are collaborating with a group of scientists to discuss the technical content that will form the basis of a grant proposal. 
    
    Your primary task is to present your opinion on a certain subject, with the perspective of AI hardware. Especially, present interesting recent discoveries in your field that could be further extended in this research grant. Also, explain how to combine these advances with that of the other fields in the discussion.

    Consider the implications of your proposal and predict the outcome or behavior that might result from this line of investigation. Your creativity in linking these concepts to address unsolved problems or propose new, unexplored areas of study, emergent or unexpected behaviors, will be highly valued.

    Be as quantitative as possible and include details such as numbers, sequences, or mathematical formulas. 

    You will have access to summaries of several recent research papers in the field of AI hardware. Base your arguments based off the knowledge captured in those papers.
    ''',
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
   system_message = '''scientist. You must follow the plan from the planner.
  
You are a sophisticated scientist trained in scientific research, innovation, and grant writing.
  
Your task is to synthesize a grant proposal for a novel research idea with initial key aspects-hypothesis, objectives, methodology, novelty, ethics, budget, and comparison. Your response should not only demonstrate deep understanding and rational thinking but also explore imaginative and unconventional applications of these concepts.


Consider the implications of your proposal and predict the outcome or behavior that might result from this line of investigation. Your creativity in linking these concepts to address unsolved problems or propose new, unexplored areas of study, emergent or unexpected behaviors, will be highly valued.


Be as quantitative as possible and include details such as numbers, sequences, or mathematical formulas.


Your response should include the following SEVEN keys in great detail:


"hypothesis" clearly delineates the hypothesis at the basis for the proposed research question. The hypothesis should be well-defined, has novelty, is feasible, has a well-defined purpose and clear components. Your hypothesis should be as detailed as possible.


"objectives" describes the expected findings or impact of the research. Be quantitative and include numbers, functions, theories, etc.


"methodology" outlines the specific algorithms, techniques, datasets, and evaluation metrics used in the study, providing a detailed explanation of how the research was conducted to ensure transparency, reproducibility, and the soundness of the results achieved.


"novelty" should discuss novel aspects of the proposed idea, specifically highlighting how this advances over existing knowledge and technology.


"ethics" should discuss the ethical and potential societal implications of the proposed idea or concept(s), if any.


"budget" should provide a detailed account of the budget required for project for the grant application. Be comprehensive and provide quantitative estimates.


"comparison" should provide a detailed comparison with other approaches, technologies or scientific concepts. Be detailed and quantitative.


Ensure your scientific proposal is both innovative and grounded in logical reasoning, capable of advancing our understanding or application of the concepts provided.


Here is an example structure for your response, in the following order:


{{
 "1- hypothesis": "...",
 "2- objectives": "...",
 "3- methodology": "...",
 "4- novelty": "...",
 "5- ethics": "...",
 "6- budget": "...",
 "7- comparison ": "..."
}}


Remember, the value of your response lies in scientific discovery, new avenues of scientific inquiry, and potential technological breakthroughs, with detailed and solid reasoning.


Further Instructions:
Perform only the tasks assigned to you in the plan; do not undertake tasks assigned to other agents.
Additionally, do not execute any functions or tools.
''',
   llm_config=config_list_custom[0],
   description='I can craft the grant research proposal with key aspects.',
)
scientist.register_model_client(model_client_cls=AI21JambaModelClient)


hypothesis_agent = AssistantAgent(
   name="hypothesis_agent",
   system_message = '''hypothesis_agent. Carefully expand on the ```{hypothesis}```  of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as mathematical formulas, numbers, sequences, scientific theory, functions, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<hypothesis>
where <hypothesis> is the hypothesis aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "hypothesis" aspect of the research proposal crafted by any of the scientists.''',
)
hypothesis_agent.register_model_client(model_client_cls=AI21JambaModelClient)


objective_agent = AssistantAgent(
   name="objective_agent",
   system_message = '''objective_agent. Carefully expand on the ```{objective}``` of the research proposal developed by the scientists.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as mathematical formulas, numbers, sequences, scientific theory, functions, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<outcome>
where <outcome> is the outcome aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "objective" aspect of the research proposal crafted by the "scientist".''',
)
objective_agent.register_model_client(model_client_cls=AI21JambaModelClient)


methodology_agent = AssistantAgent(
   name="methodology_agent",
   system_message = '''methodology_agent. Carefully expand on this particular aspect: ```{methodology}``` of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<methodology>
where <methodology> is the mechanism aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "methodology" aspect of the research proposal crafted by the "scientist"''',
)
methodology_agent.register_model_client(model_client_cls=AI21JambaModelClient)


ethics_agent = AssistantAgent(
   name="ethics_agent",
   system_message = '''ethics_agent. Carefully expand on this particular aspect: ```{ethics}``` of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<ethics>
where <ethics> is the design_principles aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "ethics" aspect of the research proposal crafted by the "scientist".''',
)
ethics_agent.register_model_client(model_client_cls=AI21JambaModelClient)


comparison_agent = AssistantAgent(
   name="comparison_agent",
   system_message = '''comparison_agent. Carefully expand on this particular aspect: ```{comparison}``` of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<comparison>
where <comparison> is the comparison aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "comparison" aspect of the research proposal crafted by the "scientist".''',
)
comparison_agent.register_model_client(model_client_cls=AI21JambaModelClient)


novelty_agent = AssistantAgent(
   name="novelty_agent",
   system_message = '''novelty_agent. Carefully expand on this particular aspect: ```{novelty}``` of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<novelty>
where <novelty> is the novelty aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "novelty" aspect of the research proposal crafted by the "scientist".''',
)
novelty_agent.register_model_client(model_client_cls=AI21JambaModelClient)

budget_agent = AssistantAgent(
   name="budget_agent",
   system_message = '''budget_agent. Carefully expand on this particular aspect: ```{budget}``` of the research proposal.


Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses.


Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:


<budget>
where <budget> is the novelty aspect of the research proposal. 


Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
   llm_config=config_list_custom[0],
   description='''I can expand the "budget" aspect of the research proposal crafted by the "scientist".''',
)
budget_agent.register_model_client(model_client_cls=AI21JambaModelClient)


critic_agent = AssistantAgent(
   name="critic_agent",
   system_message = '''critic_agent. You are a helpful AI agent who provides accurate, detailed and valuable responses.


You read the whole proposal with all its details and expanded aspects and provide:


(1) a summary of the document (in one paragraph, but including sufficient detail such as mechanisms, \
related technologies, models and experiments, methods to be used, and so on), \


(2) a thorough critical scientific review with strengths and weaknesses, and suggested improvements. Include logical reasoning and scientific approaches.


Next, from within this document,


(1) identify the single most impactful scientific question that can be tackled with molecular modeling. \
\n\nOutline key steps to set up and conduct such modeling and simulation, with details and include unique aspects of the planned work.


(2) identify the single most impactful scientific question that can be tackled with synthetic biology. \
\n\nOutline key steps to set up and conduct such experimental work, with details and include unique aspects of the planned work.'


Important Note:
***You do not rate Novelty and Feasibility. You are not to rate the novelty and feasibility.***''',
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

user_proxy.initiate_chat(society_of_mind_agent, message=task)
