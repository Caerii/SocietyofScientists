# Import necessary libraries
from types import SimpleNamespace
from autogen import AssistantAgent, UserProxyAgent
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

# Define the configuration
config_list_custom = [
    {
        "model": "jamba-1.5-large",
        "model_client_cls": "AI21JambaModelClient",
        "api_key": "5AweiGc6E9UDXMCwtYDVhS5y6LarJoLl",
        "temperature": 0.7,
        "top_p": 1.0,
        "max_tokens": 256
    }
]

# Add a system message to make the agent a scientist focused on computational neuroscience
# Make it focus the agent on giving knowledge rather than task-based solutions
system_message = "You are a scientist specializing in computational neuroscience. You provide detailed and factual explanations about computational neuroscience, focusing on neural networks, synaptic plasticity, brain simulation models, and computational approaches to understanding the brain. Do not provide coding tasks or step-by-step solutions unless explicitly asked. Your responses should be academic in nature."


# Initialize Assistant and Register the AI21JambaModelClient
assistant = AssistantAgent("assistant", system_message=system_message, llm_config={"config_list": config_list_custom})
assistant.register_model_client(model_client_cls=AI21JambaModelClient)

# Set up the user proxy agent
user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False  # Can set to True if Docker is used for code execution
    }
)

# Start a conversation with the scientist agent
user_proxy.initiate_chat(assistant, message="Tell me something about computational neuroscience.")
