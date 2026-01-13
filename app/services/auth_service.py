import uuid

from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedError, ValidationError
from app.core.security import (create_access_token, create_refresh_token,
                               get_password_hash, verify_password)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin


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
        )

        return self.user_repo.create(user)

    def login(self, credentials: UserLogin) -> dict:
        """Authenticate user and return tokens."""
        user = self.user_repo.get_by_username_or_email(credentials.username)

        if not user or not verify_password(credentials.password, user.password_hash):
            raise UnauthorizedError("Incorrect username or password")

        if not user.is_active:
            raise UnauthorizedError("User account is inactive")

        # Create tokens
        token_data = {"sub": str(user.id), "username": user.username}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "user": user,
        }

    def refresh_token(self, refresh_token: str) -> dict:
        """Refresh access token using refresh token."""
        from app.core.security import decode_token

        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid refresh token")

        user_id = payload.get("sub")
        user = self.user_repo.get(user_id)

        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")

        token_data = {"sub": str(user.id), "username": user.username}
        access_token = create_access_token(token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "user": user,
        }
