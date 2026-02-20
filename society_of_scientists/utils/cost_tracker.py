"""Cost tracking and measurement for AI21 API usage."""
import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import os
from pathlib import Path


@dataclass
class APIUsage:
    """Track a single API call usage."""
    timestamp: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost: float = 0.0
    operation: str = ""


@dataclass
class ModelPricing:
    """Pricing information for AI21 models."""
    # Based on API response and documentation
    # Prices are per 1K tokens (so divide by 1000)
    jamba_large_1_7: Dict[str, float] = field(default_factory=lambda: {
        "prompt": 0.002,  # $0.002 per 1K tokens
        "completion": 0.008  # $0.008 per 1K tokens
    })
    
    jamba_mini_2: Dict[str, float] = field(default_factory=lambda: {
        "prompt": 0.0002,  # $0.0002 per 1K tokens
        "completion": 0.0004  # $0.0004 per 1K tokens
    })
    
    jamba_mini_1_7: Dict[str, float] = field(default_factory=lambda: {
        "prompt": 0.0002,  # $0.0002 per 1K tokens
        "completion": 0.0004  # $0.0004 per 1K tokens
    })
    
    # Alias for jamba-large (uses large pricing)
    jamba_large: Dict[str, float] = field(default_factory=lambda: {
        "prompt": 0.002,  # $0.002 per 1K tokens
        "completion": 0.008  # $0.008 per 1K tokens
    })


class CostTracker:
    """Track and measure API costs."""
    
    def __init__(self, log_file: Optional[str] = None):
        """
        Initialize cost tracker.
        
        Args:
            log_file: Optional path to JSON log file for persistence
        """
        self.usage_history: List[APIUsage] = []
        self.pricing = ModelPricing()
        
        if log_file is None:
            # Default to data directory
            data_dir = Path(__file__).parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            log_file = str(data_dir / "api_usage_log.json")
        
        self.log_file = log_file
        self._load_history()
    
    def _get_pricing(self, model: str) -> Dict[str, float]:
        """Get pricing for a model."""
        model_lower = model.lower()
        
        if "large" in model_lower and "1.7" in model_lower:
            return self.pricing.jamba_large_1_7
        elif "large" in model_lower:
            return self.pricing.jamba_large
        elif "mini" in model_lower and "2" in model_lower:
            return self.pricing.jamba_mini_2
        elif "mini" in model_lower:
            return self.pricing.jamba_mini_1_7
        else:
            # Default to mini pricing (cheapest)
            return self.pricing.jamba_mini_2
    
    def calculate_cost(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int
    ) -> float:
        """
        Calculate cost for API usage.
        
        Args:
            model: Model name
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
            
        Returns:
            Total cost in USD
        """
        pricing = self._get_pricing(model)
        
        prompt_cost = (prompt_tokens / 1000) * pricing["prompt"]
        completion_cost = (completion_tokens / 1000) * pricing["completion"]
        
        return prompt_cost + completion_cost
    
    def record_usage(
        self,
        model: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        total_tokens: Optional[int] = None,
        operation: str = ""
    ) -> APIUsage:
        """
        Record API usage and calculate cost.
        
        Args:
            model: Model name used
            prompt_tokens: Prompt tokens used
            completion_tokens: Completion tokens used
            total_tokens: Total tokens (if not provided, calculated)
            operation: Description of the operation
            
        Returns:
            APIUsage object with cost calculated
        """
        if total_tokens is None:
            total_tokens = prompt_tokens + completion_tokens
        
        cost = self.calculate_cost(model, prompt_tokens, completion_tokens)
        
        usage = APIUsage(
            timestamp=datetime.now().isoformat(),
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost=cost,
            operation=operation
        )
        
        self.usage_history.append(usage)
        self._save_history()
        
        return usage
    
    def get_total_cost(self, model: Optional[str] = None) -> float:
        """
        Get total cost across all usage or for a specific model.
        
        Args:
            model: Optional model name to filter by
            
        Returns:
            Total cost in USD
        """
        if model:
            return sum(u.cost for u in self.usage_history if u.model == model)
        return sum(u.cost for u in self.usage_history)
    
    def get_usage_stats(self) -> Dict:
        """
        Get usage statistics.
        
        Returns:
            Dictionary with usage statistics
        """
        if not self.usage_history:
            return {
                "total_calls": 0,
                "total_cost": 0.0,
                "total_tokens": 0,
                "by_model": {}
            }
        
        total_calls = len(self.usage_history)
        total_cost = self.get_total_cost()
        total_tokens = sum(u.total_tokens for u in self.usage_history)
        
        by_model = {}
        for usage in self.usage_history:
            if usage.model not in by_model:
                by_model[usage.model] = {
                    "calls": 0,
                    "cost": 0.0,
                    "tokens": 0
                }
            by_model[usage.model]["calls"] += 1
            by_model[usage.model]["cost"] += usage.cost
            by_model[usage.model]["tokens"] += usage.total_tokens
        
        return {
            "total_calls": total_calls,
            "total_cost": round(total_cost, 6),
            "total_tokens": total_tokens,
            "by_model": {
                model: {
                    "calls": stats["calls"],
                    "cost": round(stats["cost"], 6),
                    "tokens": stats["tokens"]
                }
                for model, stats in by_model.items()
            }
        }
    
    def _save_history(self):
        """Save usage history to file."""
        try:
            data = [
                {
                    "timestamp": u.timestamp,
                    "model": u.model,
                    "prompt_tokens": u.prompt_tokens,
                    "completion_tokens": u.completion_tokens,
                    "total_tokens": u.total_tokens,
                    "cost": u.cost,
                    "operation": u.operation
                }
                for u in self.usage_history
            ]
            
            with open(self.log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save usage history: {e}")
    
    def _load_history(self):
        """Load usage history from file."""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                
                self.usage_history = [
                    APIUsage(**item) for item in data
                ]
            except Exception as e:
                print(f"Warning: Could not load usage history: {e}")
    
    def print_summary(self):
        """Print a summary of usage and costs."""
        stats = self.get_usage_stats()
        
        print("=" * 60)
        print("API Usage & Cost Summary")
        print("=" * 60)
        print(f"Total API Calls: {stats['total_calls']}")
        print(f"Total Tokens: {stats['total_tokens']:,}")
        
        # Show cost with appropriate precision
        total_cost = stats['total_cost']
        if total_cost < 0.000001:
            print(f"Total Cost: ${total_cost:.10f} (${total_cost * 1000:.6f} per 1K tokens)")
        elif total_cost < 0.01:
            print(f"Total Cost: ${total_cost:.8f}")
        else:
            print(f"Total Cost: ${total_cost:.6f}")
        print()
        
        if stats['by_model']:
            print("By Model:")
            for model, model_stats in stats['by_model'].items():
                print(f"  {model}:")
                print(f"    Calls: {model_stats['calls']}")
                print(f"    Tokens: {model_stats['tokens']:,}")
                cost = model_stats['cost']
                if cost < 0.000001:
                    print(f"    Cost: ${cost:.10f} (${cost * 1000:.6f} per 1K tokens)")
                elif cost < 0.01:
                    print(f"    Cost: ${cost:.8f}")
                else:
                    print(f"    Cost: ${cost:.6f}")
                print()


# Global tracker instance
_tracker: Optional[CostTracker] = None


def get_tracker() -> CostTracker:
    """Get or create global cost tracker instance."""
    global _tracker
    if _tracker is None:
        _tracker = CostTracker()
    return _tracker
