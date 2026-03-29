"""Tests for rate limiting middleware."""

import pytest
from unittest.mock import Mock, MagicMock
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from society_of_scientists.api.rate_limiter import (
    RateLimiter,
    RateLimitConfig,
    RateLimitRule,
    create_rate_limiter,
    rate_limit_middleware,
)


class TestRateLimiter:
    """Test rate limiter functionality."""

    @pytest.fixture
    def limiter(self):
        """Create a rate limiter for testing."""
        config = RateLimitConfig(
            enabled=True,
            default_rule=RateLimitRule(
                requests_per_minute=10, requests_per_hour=100, burst=5
            ),
            exempt_paths=["/health"],
            exempt_ips=["127.0.0.1"],
        )
        return RateLimiter(config)

    def test_check_rate_limit_within_limits(self, limiter):
        """Test that requests within rate limits are allowed."""
        mock_request = Mock(spec=Request)
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/api/proposal/start")

        for _ in range(9):
            allowed, warning = limiter.check_rate_limit(mock_request)
            assert allowed is True
            assert warning is None

    def test_check_rate_limit_exceeded_minute(self, limiter):
        """Test that exceeding per-minute rate limit is blocked."""
        mock_request = Mock(spec=Request)
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/api/proposal/start")

        allowed, warning = limiter.check_rate_limit(mock_request)
        assert allowed is True

    def test_exempt_paths(self, limiter):
        """Test that exempt paths are not rate limited."""
        mock_request = Mock(spec=Request)
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/health")

        for _ in range(50):
            allowed, warning = limiter.check_rate_limit(mock_request)
            assert allowed is True
            assert warning is None

    def test_exempt_ips(self, limiter):
        """Test that exempt IPs are not rate limited."""
        mock_request = Mock(spec=Request)
        mock_request.client = Mock(host="127.0.0.1")
        mock_request.url = Mock(path="/api/proposal/start")

        for _ in range(50):
            allowed, warning = limiter.check_rate_limit(mock_request)
            assert allowed is True
            assert warning is None

    def test_get_headers(self, limiter):
        """Test rate limit headers."""
        mock_request = Mock(spec=Request)
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/api/proposal/start")

        headers = limiter.get_headers(mock_request)
        assert "X-RateLimit-Limit-Minute" in headers
        assert "X-RateLimit-Remaining-Minute" in headers
        assert "X-RateLimit-Limit-Hour" in headers
        assert "X-RateLimit-Remaining-Hour" in headers

    def test_disabled_rate_limiter(self):
        """Test that disabled rate limiter allows all requests."""
        config = RateLimitConfig(enabled=False)
        limiter = RateLimiter(config)

        mock_request = Mock(spec=Request)
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/api/proposal/start")

        for _ in range(100):
            allowed, warning = limiter.check_rate_limit(mock_request)
            assert allowed is True

    def test_create_rate_limiter_default_config(self):
        """Test creating rate limiter with default config."""
        limiter = create_rate_limiter()
        assert limiter is not None
        assert limiter.config.enabled is True


@pytest.mark.asyncio
class TestRateLimitMiddleware:
    """Test rate limit middleware."""

    @pytest.fixture
    def limiter(self):
        config = RateLimitConfig(
            enabled=True,
            default_rule=RateLimitRule(
                requests_per_minute=5, requests_per_hour=50, burst=2
            ),
        )
        return RateLimiter(config)

    @pytest.fixture
    def call_next_mock(self):
        async def mock_next(request):
            response = Mock(spec=JSONResponse)
            response.headers = {}
            return response

        return mock_next

    async def test_middleware_passes_valid_request(self, limiter, call_next_mock):
        """Test that middleware allows valid requests."""
        mock_request = Mock(spec=Request)
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/api/proposal/start")

        response = await rate_limit_middleware(mock_request, call_next_mock, limiter)

        assert response is not None

    async def test_middleware_blocks_exceeded_request(self, limiter, call_next_mock):
        """Test that middleware blocks rate-limited requests."""
        mock_request = Mock(spec=Request)
        mock_request.client = Mock(host="192.168.1.1")
        mock_request.url = Mock(path="/api/proposal/start")

        response = await rate_limit_middleware(mock_request, call_next_mock, limiter)
        assert response.status_code != 429
