import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_raw_token, oauth2_scheme
from app.core.exceptions import UnauthorizedError, ValidationError
from app.database import get_db
from app.models.user import User
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)

# Rate limiter for auth endpoints
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()


class LogoutRequest(BaseModel):
    """Request body for logout endpoint."""
    refresh_token: Optional[str] = None


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
@limiter.limit("3/minute")
def register(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Password requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    
    Rate limited to 3 requests per minute per IP address.
    """
    auth_service = AuthService(db)
    try:
        user = auth_service.register(user_data)
        return user
    except ValidationError as e:
        raise e  # ValidationError is already an HTTPException
    except Exception:
        # Log the actual error for debugging, but don't expose to user
        logger.exception("Unexpected error during registration")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration",
        )


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT tokens.
    
    Rate limited to 5 requests per minute per IP address.
    """
    auth_service = AuthService(db)
    try:
        result = auth_service.login(credentials)
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            token_type=result["token_type"],
            expires_in=result["expires_in"],
            user=result["user"],
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e.detail)
        )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Refresh access token using refresh token.
    
    Implements token rotation: the old refresh token is invalidated
    and a new one is issued with each refresh.
    """
    auth_service = AuthService(db)
    try:
        result = auth_service.refresh_token(token)
        return TokenResponse(
            access_token=result["access_token"],
            refresh_token=result["refresh_token"],
            token_type=result["token_type"],
            expires_in=result["expires_in"],
            user=result["user"],
        )
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e.detail)
        )


@router.post("/logout")
def logout(
    logout_data: Optional[LogoutRequest] = None,
    access_token: str = Depends(get_raw_token),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Logout user by invalidating their tokens.
    
    Both access token and refresh token (if provided) will be blacklisted.
    """
    auth_service = AuthService(db)
    refresh_token = logout_data.refresh_token if logout_data else None
    auth_service.logout(access_token, refresh_token)
    return {"message": "Logged out successfully"}


@router.post("/logout-all")
def logout_all_devices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Logout from all devices by invalidating all tokens for this user.
    
    This increments the user's token version, making all existing
    tokens invalid.
    """
    auth_service = AuthService(db)
    auth_service.invalidate_all_tokens(str(current_user.id))
    return {"message": "Logged out from all devices successfully"}
