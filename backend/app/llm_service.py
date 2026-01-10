"""
LLM Service Layer for scalable API key management, rate limiting, and caching.

This service abstracts LLM calls and provides:
- API key rotation (support multiple keys)
- Rate limiting per key
- Response caching to reduce API costs
- Async processing support
- Cost tracking
"""

import os
import json
import re
import hashlib
from typing import Optional, Dict, List, Tuple, Any
from datetime import datetime, timedelta
from collections import deque
from enum import Enum
import asyncio
from contextlib import asynccontextmanager

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    GEMINI = "gemini"
    # Add more providers as needed: OPENAI = "openai", ANTHROPIC = "anthropic"


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded"""
    pass


class LLMKey:
    """Represents an API key with rate limiting"""
    def __init__(self, key: str, requests_per_minute: int = 60, requests_per_day: int = 1000):
        self.key = key
        self.requests_per_minute = requests_per_minute
        self.requests_per_day = requests_per_day
        self.minute_requests = deque()  # timestamps of requests in last minute
        self.day_requests = deque()  # timestamps of requests in last 24h
        self.total_requests = 0
        self.total_errors = 0
        self.last_used = None
        self.is_active = True
    
    def can_make_request(self) -> bool:
        """Check if we can make a request without exceeding rate limits"""
        if not self.is_active:
            return False
        
        now = datetime.now()
        
        # Clean old requests outside time windows
        cutoff_minute = now - timedelta(minutes=1)
        cutoff_day = now - timedelta(days=1)
        
        while self.minute_requests and self.minute_requests[0] < cutoff_minute:
            self.minute_requests.popleft()
        while self.day_requests and self.day_requests[0] < cutoff_day:
            self.day_requests.popleft()
        
        # Check limits
        if len(self.minute_requests) >= self.requests_per_minute:
            return False
        if len(self.day_requests) >= self.requests_per_day:
            return False
        
        return True
    
    def record_request(self):
        """Record a successful request"""
        now = datetime.now()
        self.minute_requests.append(now)
        self.day_requests.append(now)
        self.total_requests += 1
        self.last_used = now
    
    def record_error(self):
        """Record a failed request"""
        self.total_errors += 1
        # If too many errors, deactivate this key temporarily
        if self.total_errors > 10 and self.total_errors / max(self.total_requests, 1) > 0.5:
            self.is_active = False


class LLMService:
    """Service for managing LLM API calls with key rotation and caching"""
    
    def __init__(
        self,
        provider: LLMProvider = LLMProvider.GEMINI,
        model: str = "gemini-2.5-flash",
        temperature: float = 0,
        enable_cache: bool = True,
        cache_ttl_hours: int = 24
    ):
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.enable_cache = enable_cache
        self.cache_ttl_hours = cache_ttl_hours
        
        # Load API keys from environment
        self.keys: List[LLMKey] = self._load_api_keys()
        if not self.keys:
            raise RuntimeError(
                "No API keys found. Set GOOGLE_API_KEY or GOOGLE_API_KEYS (comma-separated) "
                "environment variable(s)."
            )
        
        # In-memory cache (can be moved to Redis/DB for production)
        self._cache: Dict[str, Tuple[Any, datetime]] = {}
        
        # Round-robin key selection
        self._current_key_index = 0
    
    def _load_api_keys(self) -> List[LLMKey]:
        """Load API keys from environment variables"""
        keys = []
        
        # Try GOOGLE_API_KEYS first (comma-separated list)
        keys_str = os.environ.get("GOOGLE_API_KEYS", "")
        if keys_str:
            for key in keys_str.split(","):
                key = key.strip()
                if key:
                    keys.append(LLMKey(key))
        
        # Fall back to single GOOGLE_API_KEY
        if not keys:
            single_key = os.environ.get("GOOGLE_API_KEY")
            if single_key:
                keys.append(LLMKey(single_key))
        
        return keys
    
    def _get_available_key(self) -> Optional[LLMKey]:
        """Get an available API key using round-robin with availability check"""
        # Try current key first
        for _ in range(len(self.keys)):
            key = self.keys[self._current_key_index]
            if key.can_make_request():
                return key
            
            # Move to next key
            self._current_key_index = (self._current_key_index + 1) % len(self.keys)
        
        # No keys available
        return None
    
    def _create_model(self, api_key: str) -> BaseChatModel:
        """Create a model instance for the given API key"""
        if self.provider == LLMProvider.GEMINI:
            return ChatGoogleGenerativeAI(
                model=self.model,
                retries=2,
                api_key=api_key,
                temperature=self.temperature
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _cache_key(self, messages: List[Tuple[str, str]]) -> str:
        """Generate cache key from messages"""
        # Create a deterministic key from the message content
        content = json.dumps(messages, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get response from cache if available and not expired"""
        if not self.enable_cache:
            return None
        
        if cache_key not in self._cache:
            return None
        
        response, cached_at = self._cache[cache_key]
        age = datetime.now() - cached_at
        
        if age > timedelta(hours=self.cache_ttl_hours):
            # Expired, remove from cache
            del self._cache[cache_key]
            return None
        
        return response
    
    def _save_to_cache(self, cache_key: str, response: Any):
        """Save response to cache"""
        if not self.enable_cache:
            return
        self._cache[cache_key] = (response, datetime.now())
        
        # Clean old cache entries periodically (simple LRU-style cleanup)
        if len(self._cache) > 1000:  # Limit cache size
            # Remove oldest 20% of entries
            sorted_items = sorted(self._cache.items(), key=lambda x: x[1][1])
            for key, _ in sorted_items[:len(sorted_items) // 5]:
                del self._cache[key]
    
    async def invoke(
        self,
        messages: List[Tuple[str, str]],
        use_cache: bool = True
    ) -> str:
        """
        Invoke the LLM with the given messages.
        
        Args:
            messages: List of (role, content) tuples, e.g. [("system", "prompt"), ("user", "input")]
            use_cache: Whether to use cache for this request
        
        Returns:
            Response text from the LLM
        
        Raises:
            RateLimitExceeded: If all API keys are rate limited
            RuntimeError: If the API call fails
        """
        # Check cache first
        cache_key = self._cache_key(messages)
        if use_cache and self.enable_cache:
            cached = self._get_from_cache(cache_key)
            if cached is not None:
                return cached
        
        # Get an available key
        llm_key = self._get_available_key()
        if not llm_key:
            raise RateLimitExceeded(
                "All API keys are rate limited. Please try again later."
            )
        
        # Create model and convert messages
        model = self._create_model(llm_key.key)
        langchain_messages = []
        for role, content in messages:
            if role == "system":
                langchain_messages.append(SystemMessage(content=content))
            elif role in ("user", "human"):
                langchain_messages.append(HumanMessage(content=content))
            else:
                langchain_messages.append(HumanMessage(content=content))
        
        try:
            # Make the API call
            # Note: LangChain's invoke is sync, but we wrap it in asyncio
            response = await asyncio.to_thread(model.invoke, langchain_messages)
            raw_text = getattr(response, "content", getattr(response, "text", str(response)))
            
            # Record success
            llm_key.record_request()
            
            # Cache the response
            if use_cache:
                self._save_to_cache(cache_key, raw_text)
            
            return raw_text
            
        except Exception as e:
            llm_key.record_error()
            raise RuntimeError(f"LLM API call failed: {str(e)}") from e
    
    def parse_json_response(self, raw_text: str) -> Optional[Dict]:
        """
        Parse JSON from LLM response, handling markdown code blocks and extra text.
        
        Returns:
            Parsed JSON dict or None if parsing fails
        """
        # Try direct JSON parse first
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from markdown code blocks
        json_patterns = [
            r"```json\s*(\{.*?\}|\[.*?\])\s*```",  # ```json {...} ```
            r"```\s*(\{.*?\}|\[.*?\])\s*```",      # ``` {...} ```
            r"`([^`]*(?:\{.*?\}|\[.*?\])[^`]*)`",  # `{...}`
        ]
        
        for pattern in json_patterns:
            match = re.search(pattern, raw_text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    continue
        
        # Try to find any JSON-like structure in the text
        match = re.search(r"(\{.*\}|\[.*\])", raw_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about API key usage"""
        return {
            "total_keys": len(self.keys),
            "active_keys": sum(1 for k in self.keys if k.is_active),
            "keys": [
                {
                    "key_prefix": k.key[:10] + "..." if len(k.key) > 10 else k.key,
                    "total_requests": k.total_requests,
                    "total_errors": k.total_errors,
                    "requests_last_minute": len(k.minute_requests),
                    "requests_last_day": len(k.day_requests),
                    "is_active": k.is_active,
                    "last_used": k.last_used.isoformat() if k.last_used else None,
                }
                for k in self.keys
            ],
            "cache_size": len(self._cache),
        }


# Global service instance (can be initialized per request or as singleton)
_global_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create the global LLM service instance"""
    global _global_llm_service
    if _global_llm_service is None:
        _global_llm_service = LLMService()
    return _global_llm_service


def reset_llm_service():
    """Reset the global LLM service (useful for testing)"""
    global _global_llm_service
    _global_llm_service = None
