import hashlib
import uuid
from datetime import UTC, datetime, timedelta
from typing import Optional

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings
from app.core.token_blacklist import token_blacklist


def _preprocess_password(password: str) -> bytes:
    """
    Preprocess password to handle bcrypt's 72-byte limit.

    Recommended approach: Pre-hash passwords longer than 72 bytes with SHA-256
    before passing to bcrypt. This ensures:
    - Consistent behavior (no truncation)
    - Better security (full password entropy preserved)
    - Standard industry practice
    """
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        # Pre-hash with SHA-256 to get a fixed 64-byte hex string
        password_bytes = hashlib.sha256(password_bytes).hexdigest().encode("utf-8")
    return password_bytes


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    password_bytes = _preprocess_password(plain_password)
    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt with SHA-256 pre-hashing for long passwords.

    This implements the recommended approach: passwords longer than 72 bytes
    are pre-hashed with SHA-256 before bcrypt hashing. This is a widely used
    pattern recommended by security experts.
    """
    password_bytes = _preprocess_password(password)
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
    token_version: int = 0,
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Token payload data (must include 'sub' for user ID)
        expires_delta: Optional custom expiration time
        token_version: User's current token version for invalidation
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({
        "exp": expire,
        "type": "access",
        "jti": str(uuid.uuid4()),  # Unique token ID for blacklisting
        "tv": token_version,  # Token version for invalidation
    })
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict, token_version: int = 0) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        data: Token payload data (must include 'sub' for user ID)
        token_version: User's current token version for invalidation
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "jti": str(uuid.uuid4()),  # Unique token ID for blacklisting
        "tv": token_version,  # Token version for invalidation
    })
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str, check_blacklist: bool = True) -> Optional[dict]:
    """
    Decode and verify a JWT token.
    
    Args:
        token: The JWT token to decode
        check_blacklist: Whether to check if token is blacklisted
        
    Returns:
        Token payload if valid, None otherwise
    """
    try:
        # Check blacklist first (before expensive decode)
        if check_blacklist and token_blacklist.is_blacklisted(token):
            return None
            
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def blacklist_token(token: str) -> None:
    """
    Add a token to the blacklist.
    
    Args:
        token: The JWT token to blacklist
    """
    # Try to get expiry from token for cleanup purposes
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": False},  # Allow expired tokens to be blacklisted
        )
        exp = payload.get("exp")
        expires_at = datetime.fromtimestamp(exp, tz=UTC) if exp else None
    except JWTError:
        expires_at = None
    
    token_blacklist.add(token, expires_at)
