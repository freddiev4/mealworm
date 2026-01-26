"""User preferences API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from mealworm.db.session import get_db
from mealworm.db.models import User, UserPreferences
from mealworm.api.auth.dependencies import get_current_user


preferences_router = APIRouter(prefix="/preferences", tags=["Preferences"])


class PreferencesResponse(BaseModel):
    """User preferences response model."""

    id: int
    user_id: int

    # Meal Plan Requirements
    chicken_dishes_per_week: int
    fish_dishes_per_week: int
    vegetables_required: bool
    eating_out_days: List[str]
    leftovers_for_lunch: bool

    # Meal Preferences
    likes: List[str]
    dislikes: List[str]
    preferred_cuisines: List[str]
    sauce_preference: str
    easy_meal_preference: str

    # Dietary Restrictions
    dietary_restrictions: List[str]
    allergens: List[str]

    # Avoid certain meal types
    avoid_meal_types: List[str]

    # Shopping List Template
    other_items: List[str]

    # Metadata
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UpdatePreferencesRequest(BaseModel):
    """Request model for updating user preferences."""

    # Meal Plan Requirements
    chicken_dishes_per_week: Optional[int] = None
    fish_dishes_per_week: Optional[int] = None
    vegetables_required: Optional[bool] = None
    eating_out_days: Optional[List[str]] = None
    leftovers_for_lunch: Optional[bool] = None

    # Meal Preferences
    likes: Optional[List[str]] = None
    dislikes: Optional[List[str]] = None
    preferred_cuisines: Optional[List[str]] = None
    sauce_preference: Optional[str] = None
    easy_meal_preference: Optional[str] = None

    # Dietary Restrictions
    dietary_restrictions: Optional[List[str]] = None
    allergens: Optional[List[str]] = None

    # Avoid certain meal types
    avoid_meal_types: Optional[List[str]] = None

    # Shopping List Template
    other_items: Optional[List[str]] = None


@preferences_router.get("", response_model=PreferencesResponse)
async def get_preferences(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get the current user's meal planning preferences.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        UserPreferences object

    Raises:
        HTTPException: If preferences not found
    """
    preferences = (
        db.query(UserPreferences)
        .filter(UserPreferences.user_id == current_user.id)
        .first()
    )

    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found"
        )

    return preferences


@preferences_router.put("", response_model=PreferencesResponse)
async def update_preferences(
    body: UpdatePreferencesRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update the current user's meal planning preferences.

    Args:
        body: Updated preference values
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated UserPreferences object

    Raises:
        HTTPException: If preferences not found
    """
    preferences = (
        db.query(UserPreferences)
        .filter(UserPreferences.user_id == current_user.id)
        .first()
    )

    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Preferences not found"
        )

    # Update only provided fields
    update_data = body.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(preferences, field, value)

    preferences.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(preferences)

    return preferences
