"""Authentication API endpoints."""

import logging
import sys
from datetime import timedelta, datetime
from os import getenv

from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from mealworm.api.auth.dependencies import get_current_user
from mealworm.api.auth.jwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    verify_password,
)
from mealworm.db.models import User, UserPreferences
from mealworm.db.session import get_db

logger = logging.getLogger(__name__)
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# Development mode - allows cross-origin cookies without HTTPS
IS_DEVELOPMENT = getenv("ENVIRONMENT", "development") == "development"

# Partitioned cookie (CHIPS) only supported in Python 3.14+; omit on 3.12 to avoid ValueError
SUPPORTS_PARTITIONED_COOKIE = sys.version_info >= (3, 14)


class RegisterRequest(BaseModel):
    """Registration request body."""

    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """Login request body."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response model."""

    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Authentication response with user and token."""

    user: UserResponse
    access_token: str
    token_type: str = "bearer"


@auth_router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    body: RegisterRequest, response: Response, db: Session = Depends(get_db)
):
    """
    Register a new user. Only allows ONE user to be created (single-user system).

    Args:
        body: Registration request with email and password
        response: FastAPI response object to set cookies
        db: Database session

    Returns:
        AuthResponse with user object and access token

    Raises:
        HTTPException: If user already exists
    """
    # Check if a user already exists (single-user system)
    existing_user_count = db.query(User).count()
    if existing_user_count > 0:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists. This is a single-user system.",
        )

    # Check if email is already registered
    existing_user = db.query(User).filter(User.email == body.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(body.password)
    new_user = User(email=body.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create default preferences for the user
    default_preferences = UserPreferences(user_id=new_user.id)
    db.add(default_preferences)
    db.commit()

    # Create JWT token
    access_token = create_access_token(
        data={"sub": str(new_user.id)},  # Convert to string for JWT
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # Set httpOnly cookie (for browsers that support it)
    # partitioned only on Python 3.14+ (Starlette raises on 3.12)
    cookie_kwargs = {
        "key": "access_token",
        "value": access_token,
        "httponly": True,
        "secure": not IS_DEVELOPMENT,
        "samesite": "none" if not IS_DEVELOPMENT else "lax",
        "max_age": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
    if SUPPORTS_PARTITIONED_COOKIE:
        cookie_kwargs["partitioned"] = True
    response.set_cookie(**cookie_kwargs)

    return AuthResponse(
        user=UserResponse.model_validate(new_user),
        access_token=access_token,
        token_type="bearer",
    )


@auth_router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest, response: Response, db: Session = Depends(get_db)):
    """
    Login with email and password, returns user info, access token, and sets JWT cookie.

    Args:
        body: Login request with email and password
        response: FastAPI response object to set cookies
        db: Database session

    Returns:
        AuthResponse with user object and access token

    Raises:
        HTTPException: If credentials are invalid or user is inactive
    """
    user = db.query(User).filter(User.email == body.email).first()

    if not user:
        logger.info("Login 401: no user for email=%s", body.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not verify_password(body.password, user.hashed_password):
        logger.info("Login 401: password mismatch for email=%s", body.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

    # Create JWT token
    access_token = create_access_token(
        data={"sub": str(user.id)},  # Convert to string for JWT
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # Set httpOnly cookie (for browsers that support it)
    # partitioned only on Python 3.14+ (Starlette raises on 3.12)
    cookie_kwargs = {
        "key": "access_token",
        "value": access_token,
        "httponly": True,
        "secure": not IS_DEVELOPMENT,
        "samesite": "none" if not IS_DEVELOPMENT else "lax",
        "max_age": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
    if SUPPORTS_PARTITIONED_COOKIE:
        cookie_kwargs["partitioned"] = True
    response.set_cookie(**cookie_kwargs)

    return AuthResponse(
        user=UserResponse.model_validate(user),
        access_token=access_token,
        token_type="bearer",
    )


@auth_router.post("/logout")
async def logout(response: Response):
    """
    Logout by clearing the JWT cookie.

    Args:
        response: FastAPI response object to clear cookies

    Returns:
        Success message
    """
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}


@auth_router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.

    Args:
        current_user: Current authenticated user from dependency

    Returns:
        User object
    """
    return current_user
