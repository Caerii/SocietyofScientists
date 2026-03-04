"""Centralized configuration management using environment variables."""
import logging
import os
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    logging.getLogger(__name__).warning(
        "python-dotenv not installed — .env files will not be loaded. "
        "Install with: pip install python-dotenv"
    )
    def load_dotenv():
        pass

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


def _safe_float(env_var: str, default: float) -> float:
    """Parse a float from an environment variable, falling back to default."""
    raw = os.getenv(env_var)
    if raw is None:
        return default
    try:
        return float(raw)
    except (ValueError, TypeError):
        logger.warning("Invalid value for %s=%r, using default %s", env_var, raw, default)
        return default


def _safe_int(env_var: str, default: int) -> int:
    """Parse an int from an environment variable, falling back to default."""
    raw = os.getenv(env_var)
    if raw is None:
        return default
    try:
        return int(raw)
    except (ValueError, TypeError):
        logger.warning("Invalid value for %s=%r, using default %s", env_var, raw, default)
        return default


class Settings:
    """Application settings loaded from environment variables."""

    # AI21 Jamba API Configuration
    AI21_API_KEY: str = os.getenv("AI21_API_KEY", "")
    JAMBA_MODEL: str = os.getenv("JAMBA_MODEL", "jamba-1.5-large")
    JAMBA_TEMPERATURE: float = _safe_float("JAMBA_TEMPERATURE", 0.7)
    JAMBA_TOP_P: float = _safe_float("JAMBA_TOP_P", 1.0)
    JAMBA_MAX_TOKENS: int = _safe_int("JAMBA_MAX_TOKENS", 2048)

    # Exa API Configuration
    EXA_API_KEY: str = os.getenv("EXA_API_KEY", "")

    # Agent Configuration
    AGENT_WORK_DIR: str = os.getenv("AGENT_WORK_DIR", "coding")
    AGENT_USE_DOCKER: bool = os.getenv("AGENT_USE_DOCKER", "false").lower() == "true"

    # Data Configuration
    DATA_DIR: str = os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "data"))
    
    @classmethod
    def get_jamba_config(cls) -> dict:
        """Get Jamba model configuration dictionary."""
        if not cls.AI21_API_KEY:
            raise ValueError("AI21_API_KEY not set. Please set it in .env file or environment variables.")
        
        return {
            "model": cls.JAMBA_MODEL,
            "model_client_cls": "AI21JambaModelClient",
            "api_key": cls.AI21_API_KEY,
            "temperature": cls.JAMBA_TEMPERATURE,
            "top_p": cls.JAMBA_TOP_P,
            "max_tokens": cls.JAMBA_MAX_TOKENS
        }
    
    @classmethod
    def get_exa_api_key(cls) -> Optional[str]:
        """Get Exa API key. Returns None if not set (allows cache-only mode)."""
        return cls.EXA_API_KEY if cls.EXA_API_KEY else None
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required settings are present."""
        errors = []
        if not cls.AI21_API_KEY:
            errors.append("AI21_API_KEY is required")
        # EXA_API_KEY is optional - can use cache-only mode
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        return True


def get_settings() -> Settings:
    """Get settings instance."""
    return Settings()
