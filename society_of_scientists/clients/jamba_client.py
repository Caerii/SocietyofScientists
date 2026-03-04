"""AI21 Jamba Model Client for AutoGen with cost tracking."""
import logging
from types import SimpleNamespace
from typing import Dict, Any, List
from ai21 import AI21Client
from ai21.models.chat import UserMessage
from ..config import Settings
from ..utils.cost_tracker import get_tracker

logger = logging.getLogger(__name__)


class AI21JambaModelClient:
    """Client for AI21 Jamba models compatible with AutoGen."""

    def __init__(self, config: Dict[str, Any], **kwargs):
        settings = Settings()
        self.api_key = config.get('api_key') or settings.AI21_API_KEY
        if not self.api_key:
            raise ValueError("API key not provided in config and AI21_API_KEY not set in environment")

        self.client = AI21Client(api_key=self.api_key)
        self.model = config.get('model', settings.JAMBA_MODEL)
        self.temperature = config.get('temperature', settings.JAMBA_TEMPERATURE)
        self.top_p = config.get('top_p', settings.JAMBA_TOP_P)
        self.max_tokens = config.get('max_tokens', settings.JAMBA_MAX_TOKENS)

    def create(self, params: Dict[str, Any]) -> SimpleNamespace:
        """Create a chat completion. Returns AutoGen-compatible response."""
        if not params.get("messages"):
            raise ValueError("No messages provided in params")

        messages = [
            UserMessage(content=msg['content'])
            for msg in params["messages"]
            if msg.get('content')
        ]

        if not messages:
            raise ValueError("No valid messages with content found")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=params.get("max_tokens", self.max_tokens),
            )
        except Exception as e:
            logger.error("AI21 API call failed: %s", e)
            raise

        # Extract token usage
        prompt_tokens = 0
        completion_tokens = 0
        total_tokens = 0
        cost = 0.0

        if hasattr(response, 'usage') and response.usage is not None:
            usage = response.usage
            prompt_tokens = getattr(usage, 'prompt_tokens', 0)
            completion_tokens = getattr(usage, 'completion_tokens', 0)
            total_tokens = getattr(usage, 'total_tokens', 0)
        else:
            logger.warning("No usage data in API response — cost tracking will be inaccurate")

        # Track cost
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
        if not response.choices:
            logger.warning("AI21 API returned empty choices")
            response_namespace = SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content=""))],
                cost=cost,
                usage=SimpleNamespace(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            )
            return response_namespace

        response_namespace = SimpleNamespace()
        response_namespace.choices = [
            SimpleNamespace(message=SimpleNamespace(content=choice.message.content or ""))
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
        """Extract message text from response."""
        return [choice.message.content for choice in response.choices]

    def cost(self, response: SimpleNamespace) -> float:
        """Return the cost of the response."""
        return response.cost

    @staticmethod
    def get_usage(response: SimpleNamespace) -> Dict[str, Any]:
        """Return usage statistics from response."""
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
