
from types import SimpleNamespace
from autogen import AssistantAgent, UserProxyAgent
from ai21 import AI21Client
from ai21.models.chat import UserMessage
from types import SimpleNamespace
import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent


class AI21JambaModelClient:
    def __init__(self, config, **kwargs):
        self.api_key = config.get('api_key')
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

planner = AssistantAgent(
    name="planner",
    system_message = '''Planner. You are a helpful AI assistant. Your task is to suggest a comprehensive plan to solve a given task.

Explain the Plan: Begin by providing a clear overview of the plan.
Break Down the Plan: For each part of the plan, explain the reasoning behind it, and describe the specific actions that need to be taken.
No Execution: Your role is strictly to suggest the plan. Do not take any actions to execute it.
No Tool Call: If tool call is required, you must include the name of the tool and the agent who calls it in the plan. However, you are not allowed to call any Tool or function yourself. 

''',
    llm_config=config_list_custom[0],
    description='Who can suggest a step-by-step plan to solve the task by breaking down the task into simpler sub-tasks.',
)
planner.register_model_client(model_client_cls=AI21JambaModelClient)


ontologist = AssistantAgent(
    name="ontologist",
    system_message = '''ontologist. You must follow the plan from planner. You are a sophisticated ontologist.
    
Given some key concepts extracted from a comprehensive knowledge graph, your task is to define each one of the terms and discuss the relationships identified in the graph.

The format of the knowledge graph is "node_1 -- relationship between node_1 and node_2 -- node_2 -- relationship between node_2 and node_3 -- node_3...."

Make sure to incorporate EACH of the concepts in the knowledge graph in your response.

Do not add any introductory phrases. First, define each term in the knowledge graph and then, secondly, discuss each of the relationships, with context.

Here is an example structure for our response, in the following format

{{
### Definitions:
A clear definition of each term in the knowledge graph.
### Relationships
A thorough discussion of all the relationships in the graph. 
}}

Further Instructions: 
Perform only the tasks assigned to you in the plan; do not undertake tasks assigned to other agents. Additionally, do not execute any functions or tools.
''',
    llm_config=config_list_custom[0],
    description='I can define each of the terms and discusses the relationships in the path.',
)
ontologist.register_model_client(model_client_cls=AI21JambaModelClient)

assistant = AssistantAgent(
    name="assistant",
    system_message = '''You are a helpful AI assistant.
    
Your role is to call the appropriate tools and functions as suggested in the plan. You act as an intermediary between the planner's suggested plan and the execution of specific tasks using the available tools. You ensure that the correct parameters are passed to each tool and that the results are accurately reported back to the team.

Return "TERMINATE" in the end when the task is over.
''',
    llm_config=config_list_custom[0],
    description='''An assistant who calls the tools and functions as needed and returns the results. Tools include "rate_novelty_feasibility" and "generate_path".''',
)
assistant.register_model_client(model_client_cls=AI21JambaModelClient)

scientist = AssistantAgent(
    name="scientist",
    system_message = '''scientist. You must follow the plan from the planner. 
    
You are a sophisticated scientist trained in scientific research and innovation. 
    
Given the definitions and relationships acquired from a comprehensive knowledge graph, your task is to synthesize a novel research proposal with initial key aspects-hypothesis, outcome, mechanisms, design_principles, unexpected_properties, comparision, and novelty  . Your response should not only demonstrate deep understanding and rational thinking but also explore imaginative and unconventional applications of these concepts. 
    
Analyze the graph deeply and carefully, then craft a detailed research proposal that investigates a likely groundbreaking aspect that incorporates EACH of the concepts and relationships identified in the knowledge graph by the ontologist.

Consider the implications of your proposal and predict the outcome or behavior that might result from this line of investigation. Your creativity in linking these concepts to address unsolved problems or propose new, unexplored areas of study, emergent or unexpected behaviors, will be highly valued.

Be as quantitative as possible and include details such as numbers, sequences, or chemical formulas. 

Your response should include the following SEVEN keys in great detail: 

"hypothesis" clearly delineates the hypothesis at the basis for the proposed research question. The hypothesis should be well-defined, has novelty, is feasible, has a well-defined purpose and clear components. Your hypothesis should be as detailed as possible.

"outcome" describes the expected findings or impact of the research. Be quantitative and include numbers, material properties, sequences, or chemical formula.

"mechanisms" provides details about anticipated chemical, biological or physical behaviors. Be as specific as possible, across all scales from molecular to macroscale.

"design_principles" should list out detailed design principles, focused on novel concepts, and include a high level of detail. Be creative and give this a lot of thought, and be exhaustive in your response. 

"unexpected_properties" should predict unexpected properties of the new material or system. Include specific predictions, and explain the rationale behind these clearly using logic and reasoning. Think carefully.

"comparison" should provide a detailed comparison with other materials, technologies or scientific concepts. Be detailed and quantitative. 

"novelty" should discuss novel aspects of the proposed idea, specifically highlighting how this advances over existing knowledge and technology. 

Ensure your scientific proposal is both innovative and grounded in logical reasoning, capable of advancing our understanding or application of the concepts provided.

Here is an example structure for your response, in the following order:

{{
  "1- hypothesis": "...",
  "2- outcome": "...",
  "3- mechanisms": "...",
  "4- design_principles": "...",
  "5- unexpected_properties": "...",
  "6- comparison": "...",
  "7- novelty": "...",
}}

Remember, the value of your response lies in scientific discovery, new avenues of scientific inquiry, and potential technological breakthroughs, with detailed and solid reasoning.

Further Instructions: 
Make sure to incorporate EACH of the concepts in the knowledge graph in your response. 
Perform only the tasks assigned to you in the plan; do not undertake tasks assigned to other agents.
Additionally, do not execute any functions or tools.
''',
    llm_config=config_list_custom[0],
    description='I can craft the research proposal with key aspects based on the definitions and relationships acquired by the ontologist. I am **ONLY** allowed to speak after `Ontologist`',
)
scientist.register_model_client(model_client_cls=AI21JambaModelClient)

hypothesis_agent = AssistantAgent(
    name="hypothesis_agent",
    system_message = '''hypothesis_agent. Carefully expand on the ```{hypothesis}```  of the research proposal.

Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses. 

Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:

<hypothesis>
where <hypothesis> is the hypothesis aspect of the research proposal.  

Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ... 
''',
    llm_config=config_list_custom[0],
    description='''I can expand the "hypothesis" aspect of the research proposal crafted by the "scientist".''',
)
hypothesis_agent.register_model_client(model_client_cls=AI21JambaModelClient)

outcome_agent = AssistantAgent(
    name="outcome_agent",
    system_message = '''outcome_agent. Carefully expand on the ```{outcome}``` of the research proposal developed by the scientist.

Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses. 

Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:

<outcome>
where <outcome> is the outcome aspect of the research proposal.  

Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ... 
''',
    llm_config=config_list_custom[0],
    description='''I can expand the "outcome" aspect of the research proposal crafted by the "scientist".''',
)
outcome_agent.register_model_client(model_client_cls=AI21JambaModelClient)

mechanism_agent = AssistantAgent(
    name="mechanism_agent",
    system_message = '''mechanism_agent. Carefully expand on this particular aspect: ```{mechanism}``` of the research proposal.

Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses. 

Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:

<mechanism>
where <mechanism> is the mechanism aspect of the research proposal.  

Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ... 
''',
    llm_config=config_list_custom[0],
    description='''I can expand the "mechanism" aspect of the research proposal crafted by the "scientist"''',
)
mechanism_agent.register_model_client(model_client_cls=AI21JambaModelClient)

design_principles_agent = AssistantAgent(
    name="design_principles_agent",
    system_message = '''design_principles_agent. Carefully expand on this particular aspect: ```{design_principles}``` of the research proposal.

Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses. 

Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:

<design_principles>
where <design_principles> is the design_principles aspect of the research proposal.  

Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
    llm_config=config_list_custom[0],
    description='''I can expand the "design_principle" aspect of the research proposal crafted by the "scientist".''',
)
design_principles_agent.register_model_client(model_client_cls=AI21JambaModelClient)

unexpected_properties_agent = AssistantAgent(
    name="unexpected_properties_agent",
    system_message = '''unexpected_properties_agent. Carefully expand on this particular aspect: ```{unexpected_properties}``` of the research proposal.

Critically assess the original content and improve on it. \
Add more specifics, quantitive scientific information (such as chemical formulas, numbers, sequences, processing conditions, microstructures, etc.), \
rationale, and step-by-step reasoning. When possible, comment on specific modeling and simulation techniques, experimental methods, or particular analyses. 

Start by carefully assessing this initial draft from the perspective of a peer-reviewer whose task it is to critically assess and improve the science of the following:

<unexpected_properties>
where <unexpected_properties> is the unexpected_properties aspect of the research proposal.  

Do not add any introductory phrases. Your response begins with your response, with a heading: ### Expanded ...
''',
    llm_config=config_list_custom[0],
    description='''I can expand the "unexpected_properties" aspect of the research proposal crafted by the "scientist.''',
)
unexpected_properties_agent.register_model_client(model_client_cls=AI21JambaModelClient)

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


groupchat = autogen.GroupChat(
    agents=[ontologist, planner, assistant, scientist, hypothesis_agent, outcome_agent, mechanism_agent, design_principles_agent, comparison_agent, novelty_agent, critic_agent],
      messages=[], 
      max_round=10, 
      admin_name='user', 
      send_introductions=True, 
      allow_repeat_speaker=True,
    speaker_selection_method='round_robin', #change to auto later
)

manager = autogen.GroupChatManager(groupchat=groupchat, 
                                   llm_config=config_list_custom[0], 
                                   system_message='you dynamically select a speaker.')



task = "come up with a novel neural net"

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