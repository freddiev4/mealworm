"""Authentication dependencies for FastAPI."""
from fastapi import Depends, HTTPException, status, Cookie, Header
from sqlalchemy.orm import Session
from typing import Optional

from mealworm.db.session import get_db
from mealworm.db.models import User
from mealworm.api.auth.jwt import decode_access_token


async def get_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization"),
    access_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    Checks Authorization header first, then falls back to httpOnly cookie.

    Args:
        authorization: Authorization header with Bearer token
        access_token: JWT token from httpOnly cookie
        db: Database session

    Returns:
        User object

    Raises:
        HTTPException: If token is missing, invalid, or user not found
    """
    token = None

    # Try to get token from Authorization header first
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    # Fall back to cookie
    elif access_token:
        token = access_token

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = decode_access_token(token)
    if token_data is None or token_data.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == token_data.user_id, User.is_active == True).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user
