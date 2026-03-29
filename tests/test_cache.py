"""Tests for caching layer."""

import pytest
import time
from society_of_scientists.utils.cache import (
    InMemoryCache,
    DiskCache,
    Cache,
    CacheConfig,
    get_cache,
    clear_global_cache,
    CacheEntry,
)


class TestInMemoryCache:
    """Test in-memory cache backend."""

    @pytest.fixture
    def cache(self):
        """Create an in-memory cache for testing."""
        return InMemoryCache(max_size=5)

    def test_set_and_get(self, cache):
        """Test basic set and get operations."""
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_get_nonexistent(self, cache):
        """Test getting nonexistent key returns None."""
        assert cache.get("nonexistent") is None

    def test_delete(self, cache):
        """Test delete operation."""
        cache.set("key1", "value1")
        assert cache.delete("key1") is True
        assert cache.get("key1") is None
        assert cache.delete("key1") is False

    def test_clear(self, cache):
        """Test clear operation."""
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert cache.get_size() == 0
        assert cache.get("key1") is None

    def test_ttl_expiry(self, cache):
        """Test that entries expire after TTL."""
        cache.set("key1", "value1", ttl=0.1)
        assert cache.get("key1") == "value1"
        time.sleep(0.15)
        assert cache.get("key1") is None

    def test_lru_eviction(self, cache):
        """Test LRU eviction when cache is full."""
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        cache.set("key4", "value4")
        cache.set("key5", "value5")

        # Access key1 to make it most recently used
        cache.get("key1")

        # Add one more entry, should evict key2 (LRU)
        cache.set("key6", "value6")

        assert cache.get("key1") is not None
        assert cache.get("key2") is None

    def test_get_stats(self, cache):
        """Test getting cache statistics."""
        cache.set("key1", "value1")
        cache.get("key1")
        cache.get("nonexistent")

        stats = cache.get_stats()
        assert stats["backend"] == "memory"
        assert stats["size"] == 1
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["hit_rate"] == 0.5


class TestCache:
    """Test unified cache interface."""

    @pytest.fixture
    def cache(self):
        """Create a cache instance for testing."""
        config = CacheConfig(backend="memory", ttl=3600, max_size=100)
        return Cache(config)

    def test_basic_operations(self, cache):
        """Test basic cache operations."""
        assert cache.set("key1", "value1") is True
        assert cache.get("key1") == "value1"
        assert cache.delete("key1") is True
        assert cache.get("key1") is None

    def test_cached_decorator(self, cache):
        """Test cached decorator."""
        call_count = 0

        @cache.cached(ttl=1)
        def expensive_function(x, y):
            nonlocal call_count
            call_count += 1
            return x + y

        # First call should execute function
        result1 = expensive_function(2, 3)
        assert result1 == 5
        assert call_count == 1

        # Second call should use cache
        result2 = expensive_function(2, 3)
        assert result2 == 5
        assert call_count == 1

        # Different arguments should execute function
        result3 = expensive_function(3, 4)
        assert result3 == 7
        assert call_count == 2

    def test_global_cache(self):
        """Test global cache singleton."""
        cache1 = get_cache()
        cache2 = get_cache()
        assert cache1 is cache2

        clear_global_cache()
        cache3 = get_cache()
        # Creating new cache after clearing
        assert cache3 is not None


class TestCacheEntry:
    """Test CacheEntry dataclass."""

    def test_expiry_check(self):
        """Test is_expired property."""
        from datetime import datetime, timedelta

        expired_entry = CacheEntry(
            key="key1",
            value="value1",
            created_at=datetime.now() - timedelta(seconds=10),
            ttl_seconds=5,
        )
        assert expired_entry.is_expired is True

        valid_entry = CacheEntry(
            key="key2",
            value="value2",
            created_at=datetime.now(),
            ttl_seconds=3600,
        )
        assert valid_entry.is_expired is False

    def test_touch_updates_access(self):
        """Test that touch updates access information."""
        entry = CacheEntry(
            key="key1", value="value1", created_at=datetime.now(), ttl_seconds=3600
        )
        assert entry.access_count == 0
        assert entry.last_accessed is None

        entry.touch()
        assert entry.access_count == 1
        assert entry.last_accessed is not None
