"""Flexible caching layer with pluggable backends."""

import json
import hashlib
import logging
import pickle
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Callable, Dict, List
from datetime import datetime, timedelta
from functools import wraps

import cachetools


logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Cache entry with metadata."""

    key: str
    value: Any
    created_at: datetime
    ttl_seconds: float
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    size_bytes: int = 0

    @property
    def is_expired(self) -> bool:
        """Check if entry is expired."""
        if self.ttl_seconds <= 0:
            return False
        return (datetime.now() - self.created_at).total_seconds() > self.ttl_seconds

    def touch(self):
        """Update access time."""
        self.last_accessed = datetime.now()
        self.access_count += 1


class CacheBackend(ABC):
    """Abstract cache backend."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: float = 3600) -> bool:
        """Set value in cache."""
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        pass

    @abstractmethod
    def clear(self) -> bool:
        """Clear all cache entries."""
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        pass

    @abstractmethod
    def get_size(self) -> int:
        """Get number of entries."""
        pass


class InMemoryCache(CacheBackend):
    """In-memory cache with TTL support."""

    def __init__(self, max_size: int = 1000):
        self._lock = threading.Lock()
        self._cache: Dict[str, CacheEntry] = {}
        self._max_size = max_size
        self._hits = 0
        self._misses = 0
        self._evictions = 0

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None

            entry = self._cache[key]

            if entry.is_expired:
                del self._cache[key]
                self._misses += 1
                return None

            entry.touch()
            self._hits += 1
            return entry.value

    def set(self, key: str, value: Any, ttl: float = 3600) -> bool:
        with self._lock:
            if len(self._cache) >= self._max_size and key not in self._cache:
                self._evict_lru()

            entry = CacheEntry(
                key=key,
                value=value,
                created_at=datetime.now(),
                ttl_seconds=ttl,
                size_bytes=len(pickle.dumps(value)),
            )
            self._cache[key] = entry
            return True

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> bool:
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
            self._evictions = 0
            return True

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            total = self._hits + self._misses
            hit_rate = self._hits / total if total > 0 else 0
            return {
                "backend": "memory",
                "size": len(self._cache),
                "max_size": self._max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": hit_rate,
                "evictions": self._evictions,
                "total_bytes": sum(e.size_bytes for e in self._cache.values()),
            }

    def get_size(self) -> int:
        with self._lock:
            return len(self._cache)

    def _evict_lru(self):
        """Evict least recently used entry."""
        if not self._cache:
            return

        lru_key = min(
            self._cache.keys(),
            key=lambda k: self._cache[k].last_accessed or datetime.min,
        )
        del self._cache[lru_key]
        self._evictions += 1


class DiskCache(CacheBackend):
    """Disk-based persistent cache."""

    def __init__(self, cache_dir: str = ".cache"):
        self._lock = threading.Lock()
        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(exist_ok=True)
        self._meta_file = self._cache_dir / "cache_metadata.json"
        self._metadata: Dict[str, Dict] = {}
        self._hits = 0
        self._misses = 0
        self._load_metadata()

    def _load_metadata(self):
        """Load cache metadata from disk."""
        if self._meta_file.exists():
            try:
                with open(self._meta_file, "r") as f:
                    self._metadata = json.load(f)
            except Exception as e:
                logger.warning("Failed to load cache metadata: %s", e)
                self._metadata = {}

    def _save_metadata(self):
        """Save cache metadata to disk."""
        try:
            with open(self._meta_file, "w") as f:
                json.dump(self._metadata, f)
        except Exception as e:
            logger.warning("Failed to save cache metadata: %s", e)

    def _get_path(self, key: str) -> Path:
        """Get file path for cache key."""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return self._cache_dir / f"{hash_key[:2]}" / f"{hash_key}"

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._metadata:
                self._misses += 1
                return None

            meta = self._metadata[key]
            created_at = datetime.fromisoformat(meta["created_at"])
            ttl = meta.get("ttl", 0)

            if ttl > 0 and (datetime.now() - created_at).total_seconds() > ttl:
                self.delete(key)
                self._misses += 1
                return None

            path = self._get_path(key)
            if not path.exists():
                del self._metadata[key]
                self._misses += 1
                return None

            try:
                with open(path, "rb") as f:
                    value = pickle.load(f)

                meta["access_count"] = meta.get("access_count", 0) + 1
                meta["last_accessed"] = datetime.now().isoformat()
                self._hits += 1
                self._save_metadata()
                return value
            except Exception as e:
                logger.warning("Failed to load cache entry %s: %s", key, e)
                self.delete(key)
                self._misses += 1
                return None

    def set(self, key: str, value: Any, ttl: float = 3600) -> bool:
        with self._lock:
            path = self._get_path(key)
            path.parent.mkdir(parents=True, exist_ok=True)

            try:
                with open(path, "wb") as f:
                    pickle.dump(value, f)

                self._metadata[key] = {
                    "created_at": datetime.now().isoformat(),
                    "ttl": ttl,
                    "access_count": 0,
                    "last_accessed": datetime.now().isoformat(),
                    "size_bytes": len(pickle.dumps(value)),
                }
                self._save_metadata()
                return True
            except Exception as e:
                logger.warning("Failed to save cache entry %s: %s", key, e)
                return False

    def delete(self, key: str) -> bool:
        with self._lock:
            if key not in self._metadata:
                return False

            path = self._get_path(key)
            if path.exists():
                path.unlink()

            del self._metadata[key]
            self._save_metadata()
            return True

    def clear(self) -> bool:
        with self._lock:
            for key in list(self._metadata.keys()):
                self.delete(key)

            self._hits = 0
            self._misses = 0
            return True

    def get_stats(self) -> Dict[str, Any]:
        with self._lock:
            total = self._hits + self._misses
            hit_rate = self._hits / total if total > 0 else 0
            return {
                "backend": "disk",
                "size": len(self._metadata),
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": hit_rate,
                "total_bytes": sum(
                    m.get("size_bytes", 0) for m in self._metadata.values()
                ),
                "cache_dir": str(self._cache_dir),
            }

    def get_size(self) -> int:
        with self._lock:
            return len(self._metadata)


class CacheConfig:
    """Cache configuration."""

    def __init__(
        self,
        backend: str = "memory",
        ttl: float = 3600,
        max_size: int = 1000,
        cache_dir: str = ".cache",
    ):
        self.backend = backend
        self.ttl = ttl
        self.max_size = max_size
        self.cache_dir = cache_dir


class Cache:
    """Unified cache interface."""

    def __init__(self, config: Optional[CacheConfig] = None):
        self._config = config or CacheConfig()

        if self._config.backend == "disk":
            self._backend = DiskCache(self._config.cache_dir)
        else:
            self._backend = InMemoryCache(self._config.max_size)

        logger.info("Initialized cache with backend: %s", self._config.backend)

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        return self._backend.get(key)

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """Set value in cache."""
        ttl = ttl or self._config.ttl
        return self._backend.set(key, value, ttl)

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        return self._backend.delete(key)

    def clear(self) -> bool:
        """Clear all cache entries."""
        return self._backend.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self._backend.get_stats()

    def get_size(self) -> int:
        """Get number of entries."""
        return self._backend.get_size()

    def cached(self, ttl: Optional[float] = None):
        """Decorator for caching function results."""

        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self._make_key(func.__name__, args, kwargs)

                result = self.get(cache_key)
                if result is not None:
                    logger.debug("Cache hit for %s", cache_key)
                    return result

                logger.debug("Cache miss for %s, computing", cache_key)
                result = func(*args, kwargs)
                self.set(cache_key, result, ttl or self._config.ttl)
                return result

            return wrapper

        return decorator

    def _make_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key from function name and arguments."""
        key_parts = [func_name]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        key_str = ":".join(key_parts)
        return hashlib.sha256(key_str.encode()).hexdigest()


# Global cache instance
_global_cache: Optional[Cache] = None
_cache_lock = threading.Lock()


def get_cache(config: Optional[CacheConfig] = None) -> Cache:
    """Get or create global cache instance."""
    global _global_cache
    if _global_cache is None:
        with _cache_lock:
            if _global_cache is None:
                _global_cache = Cache(config)
    return _global_cache


def clear_global_cache():
    """Clear global cache instance."""
    global _global_cache
    with _cache_lock:
        if _global_cache is not None:
            _global_cache.clear()
            _global_cache = None
