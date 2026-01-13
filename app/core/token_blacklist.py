"""
Token blacklist for logout functionality.

This provides an in-memory token blacklist for development.
For production with multiple instances, use Redis instead.
"""
import logging
from datetime import UTC, datetime
from threading import Lock
from typing import Optional, Set

logger = logging.getLogger(__name__)


class TokenBlacklist:
    """
    In-memory token blacklist with automatic cleanup of expired entries.
    
    For production deployments with multiple server instances,
    replace this with a Redis-based implementation.
    """

    def __init__(self):
        self._blacklisted_tokens: Set[str] = set()
        self._token_expiry: dict[str, datetime] = {}
        self._lock = Lock()

    def add(self, token: str, expires_at: Optional[datetime] = None) -> None:
        """
        Add a token to the blacklist.
        
        Args:
            token: The JWT token to blacklist
            expires_at: When the token expires (for cleanup purposes)
        """
        with self._lock:
            self._blacklisted_tokens.add(token)
            if expires_at:
                self._token_expiry[token] = expires_at
            logger.info("Token added to blacklist")

    def is_blacklisted(self, token: str) -> bool:
        """Check if a token is blacklisted."""
        with self._lock:
            return token in self._blacklisted_tokens

    def cleanup_expired(self) -> int:
        """
        Remove expired tokens from the blacklist.
        
        Returns:
            Number of tokens removed
        """
        now = datetime.now(UTC)
        removed = 0
        
        with self._lock:
            expired_tokens = [
                token for token, expiry in self._token_expiry.items()
                if expiry < now
            ]
            
            for token in expired_tokens:
                self._blacklisted_tokens.discard(token)
                del self._token_expiry[token]
                removed += 1
        
        if removed > 0:
            logger.info(f"Cleaned up {removed} expired tokens from blacklist")
        
        return removed

    def clear(self) -> None:
        """Clear all blacklisted tokens (for testing)."""
        with self._lock:
            self._blacklisted_tokens.clear()
            self._token_expiry.clear()


# Global singleton instance
token_blacklist = TokenBlacklist()
