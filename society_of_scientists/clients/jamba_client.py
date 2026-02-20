"""AI21 Jamba Model Client for AutoGen with cost tracking."""
from types import SimpleNamespace
from typing import Dict, Any, List, Optional
from ai21 import AI21Client
from ai21.models.chat import UserMessage
from ..config import Settings
from ..utils.cost_tracker import get_tracker


class AI21JambaModelClient:
    """Client for AI21 Jamba models compatible with AutoGen."""
    
    def __init__(self, config: Dict[str, Any], **kwargs):
        """
        Initialize the Jamba model client.
        
        Args:
            config: Configuration dictionary with model settings
            **kwargs: Additional keyword arguments
        """
        settings = Settings()
        self.api_key = config.get('api_key') or settings.AI21_API_KEY
        if not self.api_key:
            raise ValueError("API key not provided in config and AI21_API_KEY not set in environment")
        
        self.client = AI21Client(api_key=self.api_key)
        self.model = config.get('model', settings.JAMBA_MODEL)
        self.temperature = config.get('temperature', settings.JAMBA_TEMPERATURE)
        self.top_p = config.get('top_p', settings.JAMBA_TOP_P)
    
    def create(self, params: Dict[str, Any]) -> SimpleNamespace:
        """
        Create a chat completion.
        
        Args:
            params: Parameters dictionary with 'messages' and optional 'max_tokens'
            
        Returns:
            SimpleNamespace object compatible with AutoGen
        """
        messages = [
            UserMessage(content=params["messages"][0]['content'])
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=params.get("max_tokens", 256),
        )
        
        # Extract token usage and calculate cost
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        cost = 0.0
        
        # Try to get usage from response
        if hasattr(response, 'usage'):
            usage = response.usage
            prompt_tokens = getattr(usage, 'prompt_tokens', 0)
            completion_tokens = getattr(usage, 'completion_tokens', 0)
            total_tokens = getattr(usage, 'total_tokens', 0)
        
        # Calculate and track cost
        if total_tokens > 0:
            tracker = get_tracker()
            usage_record = tracker.record_usage(
                model=self.model,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=total_tokens,
                operation="chat_completion"
            )
            cost = usage_record.cost
        
        # Convert to AutoGen-compatible format
        response_namespace = SimpleNamespace()
        response_namespace.choices = [
            SimpleNamespace(message=SimpleNamespace(content=choice.message.content))
            for choice in response.choices
        ]
        response_namespace.cost = cost
        response_namespace.usage = SimpleNamespace(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens
        )
        
        return response_namespace
    
    def message_retrieval(self, response: SimpleNamespace) -> List[str]:
        """
        Retrieve messages from the response.
        
        Args:
            response: Response object from create()
            
        Returns:
            List of message contents
        """
        choices = response.choices
        return [choice.message.content for choice in choices]
    
    def cost(self, response: SimpleNamespace) -> float:
        """
        Get the cost of the response.
        
        Args:
            response: Response object
            
        Returns:
            Cost as float
        """
        return response.cost
    
    @staticmethod
    def get_usage(response: SimpleNamespace) -> Dict[str, Any]:
        """
        Get usage statistics from response.
        
        Args:
            response: Response object
            
        Returns:
            Dictionary with usage statistics
        """
        if hasattr(response, 'usage'):
            return {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
                "cost": response.cost
            }
        return {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "cost": response.cost
        }
