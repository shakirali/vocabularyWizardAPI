import logging
import uuid

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import UnauthorizedError, ValidationError
from app.core.security import (blacklist_token, create_access_token,
                               create_refresh_token, decode_token,
                               get_password_hash, verify_password)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register(self, user_data: UserCreate) -> User:
        """Register a new user."""
        # Check if username already exists
        if self.user_repo.get_by_username(user_data.username):
            raise ValidationError("Username already exists", field="username")

        # Check if email already exists
        if self.user_repo.get_by_email(user_data.email):
            raise ValidationError("Email already exists", field="email")

        # Create new user
        user = User(
            id=uuid.uuid4(),
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            full_name=user_data.full_name,
            is_admin=False,
            token_version=0,
        )

        return self.user_repo.create(user)

    def login(self, credentials: UserLogin) -> dict:
        """Authenticate user and return tokens."""
        user = self.user_repo.get_by_username_or_email(credentials.username)

        if not user or not verify_password(credentials.password, user.password_hash):
            raise UnauthorizedError("Incorrect username or password")

        if not user.is_active:
            raise UnauthorizedError("User account is inactive")

        # Create tokens with token version for invalidation support
        token_data = {"sub": str(user.id), "username": user.username}
        access_token = create_access_token(token_data, token_version=user.token_version)
        refresh_token = create_refresh_token(token_data, token_version=user.token_version)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": user,
        }

    def refresh_token(self, old_refresh_token: str) -> dict:
        """
        Refresh access token using refresh token.
        
        Implements token rotation: issues new refresh token and
        blacklists the old one for security.
        """
        payload = decode_token(old_refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid refresh token")

        user_id = payload.get("sub")
        user = self.user_repo.get(user_id)

        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")

        # Check token version - reject if user has invalidated tokens
        token_version = payload.get("tv", 0)
        if token_version != user.token_version:
            raise UnauthorizedError("Token has been revoked")

        # Blacklist the old refresh token (rotation)
        blacklist_token(old_refresh_token)

        # Create new tokens
        token_data = {"sub": str(user.id), "username": user.username}
        access_token = create_access_token(token_data, token_version=user.token_version)
        new_refresh_token = create_refresh_token(token_data, token_version=user.token_version)

        logger.info(f"Token refreshed for user {user.username}")

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": user,
        }

    def logout(self, access_token: str, refresh_token: str = None) -> None:
        """
        Logout user by blacklisting their tokens.
        
        Args:
            access_token: The access token to invalidate
            refresh_token: Optional refresh token to invalidate
        """
        # Blacklist the access token
        blacklist_token(access_token)
        
        # Blacklist refresh token if provided
        if refresh_token:
            blacklist_token(refresh_token)
        
        logger.info("User logged out, tokens blacklisted")

    def invalidate_all_tokens(self, user_id: str) -> None:
        """
        Invalidate all tokens for a user by incrementing their token version.
        
        This is useful for:
        - Password changes
        - Security breaches
        - Admin force logout
        """
        user = self.user_repo.get(user_id)
        if user:
            user.token_version += 1
            self.user_repo.update(user)
            logger.info(f"All tokens invalidated for user {user.username}")
