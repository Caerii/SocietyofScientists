"""Rate limiting middleware for API protection."""

import time
import logging
from typing import Callable, Dict, Optional
from functools import wraps
from dataclasses import dataclass, field
from collections import defaultdict
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


@dataclass
class RateLimitRule:
    """Configuration for rate limiting rules."""

    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    burst: int = 10


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""

    enabled: bool = True
    default_rule: RateLimitRule = field(default_factory=RateLimitRule)
    endpoint_rules: Dict[str, RateLimitRule] = field(default_factory=dict)
    exempt_paths: list[str] = field(default_factory=lambda: ["/health", "/metrics"])
    exempt_ips: list[str] = field(default_factory=list)
    block_on_exceeded: bool = True
    warning_threshold: float = 0.8


class SlidingWindowCounter:
    """Sliding window counter for accurate rate limiting."""

    def __init__(self, window_size: float):
        self.window_size = window_size
        self.requests: list[float] = []

    def add_request(self, timestamp: float) -> None:
        """Add a request timestamp and clean old entries."""
        self.requests.append(timestamp)
        self._cleanup_old(timestamp)

    def _cleanup_old(self, current: float) -> None:
        """Remove requests outside the window."""
        cutoff = current - self.window_size
        self.requests = [t for t in self.requests if t > cutoff]

    def count(self, current: float) -> int:
        """Count requests in the current window."""
        self._cleanup_old(current)
        return len(self.requests)


class RateLimiter:
    """Thread-safe rate limiter using sliding window."""

    def __init__(self, config: RateLimitConfig):
        self.config = config
        self.minute_windows: Dict[str, SlidingWindowCounter] = defaultdict(
            lambda: SlidingWindowCounter(60)
        )
        self.hour_windows: Dict[str, SlidingWindowCounter] = defaultdict(
            lambda: SlidingWindowCounter(3600)
        )

    def _get_key(self, request: Request) -> str:
        """Get rate limit key from request."""
        client_ip = request.client.host if request.client else "unknown"
        # Could also use user ID from auth header
        return f"{client_ip}"

    def _get_rule(self, path: str) -> RateLimitRule:
        """Get rate limit rule for path."""
        path = path.split("?")[0]
        return self.config.endpoint_rules.get(path, self.config.default_rule)

    def check_rate_limit(self, request: Request) -> tuple[bool, Optional[str]]:
        """
        Check if request is within rate limits.

        Returns:
            Tuple of (allowed, warning_message)
        """
        if not self.config.enabled:
            return True, None

        path = request.url.path
        key = self._get_key(request)
        rule = self._get_rule(path)
        now = time.time()

        if key in self.config.exempt_ips:
            return True, None

        if any(path.startswith(p) for p in self.config.exempt_paths):
            return True, None

        minute_window = self.minute_windows[key]
        hour_window = self.hour_windows[key]

        minute_count = minute_window.count(now)
        hour_count = hour_window.count(now)

        if minute_count >= rule.requests_per_minute:
            return (
                False,
                f"Rate limit exceeded: {rule.requests_per_minute} requests per minute",
            )
        if hour_count >= rule.requests_per_hour:
            return (
                False,
                f"Rate limit exceeded: {rule.requests_per_hour} requests per hour",
            )

        minute_window.add_request(now)
        hour_window.add_request(now)

        minute_ratio = minute_count / rule.requests_per_minute
        hour_ratio = hour_count / rule.requests_per_hour

        warning = None
        if minute_ratio >= self.config.warning_threshold:
            warning = f"Approaching rate limit: {minute_count}/{rule.requests_per_minute} per minute"
        elif hour_ratio >= self.config.warning_threshold:
            warning = f"Approaching rate limit: {hour_count}/{rule.requests_per_hour} per hour"

        return True, warning

    def get_headers(self, request: Request) -> Dict[str, str]:
        """Get rate limit headers."""
        key = self._get_key(request)
        rule = self._get_rule(request.url.path)
        now = time.time()

        minute_count = self.minute_windows[key].count(now)
        hour_count = self.hour_windows[key].count(now)

        return {
            "X-RateLimit-Limit-Minute": str(rule.requests_per_minute),
            "X-RateLimit-Remaining-Minute": str(
                max(0, rule.requests_per_minute - minute_count)
            ),
            "X-RateLimit-Limit-Hour": str(rule.requests_per_hour),
            "X-RateLimit-Remaining-Hour": str(
                max(0, rule.requests_per_hour - hour_count)
            ),
            "X-RateLimit-Used-Minute": str(minute_count),
            "X-RateLimit-Used-Hour": str(hour_count),
        }


def create_rate_limiter(config: Optional[RateLimitConfig] = None) -> RateLimiter:
    """Create a rate limiter instance."""
    if config is None:
        config = RateLimitConfig()
    return RateLimiter(config)


async def rate_limit_middleware(
    request: Request, call_next: Callable, limiter: RateLimiter
) -> JSONResponse:
    """FastAPI middleware for rate limiting."""
    allowed, warning = limiter.check_rate_limit(request)

    if not allowed:
        logger.warning(
            "Rate limit exceeded for %s: %s", request.client.host, request.url.path
        )
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"error": warning or "Rate limit exceeded"},
            headers=limiter.get_headers(request),
        )

    response = await call_next(request)

    if warning:
        logger.info("Rate limit warning for %s: %s", request.client.host, warning)

    response.headers.update(limiter.get_headers(request))
    return response
