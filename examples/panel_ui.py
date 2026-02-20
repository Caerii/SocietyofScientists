# Import necessary libraries
from types import SimpleNamespace
from autogen import AssistantAgent, UserProxyAgent
import panel as pn
import asyncio

# Define a simple Project Manager Agent Client Class
class ProjectManagerAgentClient:
    def __init__(self, config, **kwargs):
        self.temperature = config.get('temperature', 0.7)
        print(f"ProjectManagerAgentClient initialized with config: {config}")

    def create(self, params):
        # Simulate a conversation with the project manager about IT issues
        messages = params["messages"]
        user_message = messages[0]['content']

        # Simulated responses based on user input
        if "server down" in user_message.lower():
            response_text = "It seems the server is down. Have you tried rebooting it? I'll escalate this to the infrastructure team."
        elif "priority" in user_message.lower():
            response_text = "Let's prioritize based on urgency. Focus on the client-side bugs first."
        elif "timeline" in user_message.lower():
            response_text = "The timeline is tight. We need to resolve these issues by the end of the week. Can your team handle it?"
        else:
            response_text = "Can you provide more details on the issue?"

        # Return the response in a compatible format
        response_namespace = SimpleNamespace()
        response_namespace.choices = [SimpleNamespace(message=SimpleNamespace(content=response_text))]
        response_namespace.cost = 0  # Adding a dummy cost attribute
        
        return response_namespace

    def message_retrieval(self, response):
        """Retrieve the assistant's response."""
        return [choice.message.content for choice in response.choices]

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
        "model": "project-manager",
        "model_client_cls": "ProjectManagerAgentClient",
        "temperature": 0.7,
    }
]

# Initialize the Project Manager Agent
pm_system_message = "You are a project manager overseeing IT issues. Provide actionable and managerial responses."
project_manager = AssistantAgent("project_manager", system_message=pm_system_message, llm_config={"config_list": config_list_custom})
project_manager.register_model_client(model_client_cls=ProjectManagerAgentClient)

# Set up the user proxy agent
user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={"work_dir": "coding", "use_docker": False}
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
        asyncio.create_task(delayed_initiate_chat(user_proxy, project_manager, contents))
    else:
        if input_future and not input_future.done():
            input_future.set_result(contents)
        else:
            print("There is currently no input being awaited.")

# Chat interface initialization
chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send("Welcome! Discuss your IT issues with the Project Manager.", user="System", respond=False)

# Function to print messages
def print_messages(recipient, messages, sender, config):
    content = messages[-1]['content']
    chat_interface.send(content, user=recipient.name, avatar="💼", respond=False)
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

    # Start a conversation with the project manager (Initial prompt)
    user_proxy.initiate_chat(project_manager, message="We are facing issues with the server being down.")
