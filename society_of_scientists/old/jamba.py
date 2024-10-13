# Import necessary libraries
from types import SimpleNamespace
from autogen import AssistantAgent, UserProxyAgent
from ai21 import AI21Client
from ai21.models.chat import UserMessage
import panel as pn
import asyncio

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

# Define frontend using Panel
pn.extension(design="material")

# Global variable to manage input
input_future = None
initiate_chat_task_created = False

# Define callback function for chat input
async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    global initiate_chat_task_created
    global input_future

    if not initiate_chat_task_created:
        asyncio.create_task(delayed_initiate_chat(user_proxy, assistant, contents))
    else:
        if input_future and not input_future.done():
            input_future.set_result(contents)
        else:
            print("There is currently no input being awaited.")

# Chat interface initialization
chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send("Send a message to the Neuroscience Assistant!", user="System", respond=False)

# Function to print messages
def print_messages(recipient, messages, sender, config):
    content = messages[-1]['content']
    chat_interface.send(content, user=recipient.name, avatar="🧠", respond=False)
    return False, None  # Ensure the agent communication flow continues

# Register the message handler for the assistant
user_proxy.register_reply([AssistantAgent, None], reply_func=print_messages, config={"callback": None})

# Async task to delay the initiation of the chat
async def delayed_initiate_chat(agent, recipient, message):
    global initiate_chat_task_created
    initiate_chat_task_created = True
    await asyncio.sleep(2)
    await agent.a_initiate_chat(recipient, message=message)

# Serve the chat interface as the Panel app
chat_interface.servable()


if __name__ == '__main__':
    pn.serve(chat_interface, start=True, show=True)

    # Start a conversation with the scientist agent (Initial prompt)
    user_proxy.initiate_chat(assistant, message="Tell me something about computational neuroscience.")

