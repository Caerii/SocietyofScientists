import os
from autogen import AssistantAgent, UserProxyAgent, register_function
from exa_py import Exa
from types import SimpleNamespace
from ai21 import AI21Client
from ai21.models.chat import UserMessage

# Define AI21 Jamba Model Client Class
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

# Define the Exa search tool
def exa_search(query: str) -> str:
    """
    A tool to search research papers via the Exa API.

    :param query: The search query for research papers.
    :return: The search result.
    """
    # Initialize the Exa client
    exa = Exa(api_key="03af6e3c-7b7f-4d46-b541-6771b8a240e0")  # Add your Exa API key

    # Perform the search using the Exa API
    result = exa.search_and_contents(
        query,
        type="neural",
        use_autoprompt=True,
        num_results=20,
        summary={
            "query": "What does this paper cover?"
        },
        category="research paper",
        exclude_domains=["en.wikipedia.org"],
        start_published_date="2023-01-01",
        text={
            "include_html_tags": True
        },
        livecrawl="always",
        highlights=True
    )
    
    # Return the formatted result
    return result

# Define the configuration
config_list_custom = [
    {
        "model": "jamba-1.5-large",
        "model_client_cls": "AI21JambaModelClient",
        "api_key": "5AweiGc6E9UDXMCwtYDVhS5y6LarJoLl",  # Replace with your Jamba API key
        "temperature": 0.7,
        "top_p": 1.0,
        "max_tokens": 256
    }
]

register_model_client(model_client_cls=AI21JambaModelClient)


# Add a system message to set the agent's personality
system_message = "You are a scientist specializing in computational neuroscience. " + "\n" + "You provide detailed and factual explanations about computational neuroscience, " + "\n" + "focusing on neural networks, synaptic plasticity, brain simulation models, " + "\n" + "and computational approaches to understanding the brain. You also have access to a tool " + "\n" + "for searching research papers. Use this tool when a user asks for references or studies." + "\n"

# Initialize the Jamba Assistant agent and register the Exa tool
assistant = AssistantAgent("scientist_agent", system_message=system_message, llm_config={"config_list":config_list_custom} )
assistant.register_model_client(model_client_cls=AI21JambaModelClient)

# Set up the user proxy agent
user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False  # Can set to True if Docker is used for code execution
    }
)
# Register the tool to both agents
register_function(
    exa_search,
    caller=assistant,  # The assistant agent can suggest calls to the tool.
    executor=user_proxy,  # The user proxy agent can execute the tool calls.
    name="exa_search",  # Tool name
    description="A tool to search for research papers."  # A description of the tool.
)

# Start a conversation where the Jamba agent can also invoke the Exa search tool
if __name__ == "__main__":
    # Example user query
    user_query = "Find research papers on computational neuroscience."
    
    # Get the assistant's response by invoking the Exa search tool if necessary
    response = user_proxy.initiate_chat(assistant, message=user_query)
    
    # Print the result
    print(response)
