from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field



class Meal(BaseModel):
    """Represents a meal from Notion"""
    id: str
    title: str
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    prep_time: Optional[int] = None  # in minutes
    cook_time: Optional[int] = None  # in minutes
    difficulty: Optional[str] = None
    ingredients: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    last_made: Optional[datetime] = None
    rating: Optional[int] = None
    page_content: Optional[str] = None
    raw_notion_data: Dict[str, Any] = Field(default_factory=dict)


class DayPlan(BaseModel):
    """Represents meals planned for a single day"""
    day: str
    breakfast: Optional[Meal] = None
    lunch: Optional[Meal] = None
    dinner: Optional[Meal] = None
    snacks: List[Meal] = Field(default_factory=list)


class WeeklyMealPlan(BaseModel):
    """Represents a complete weekly meal plan"""
    week_starting: datetime
    days: List[DayPlan]
    notes: Optional[str] = None
    grocery_list: List[str] = Field(default_factory=list)


class MealPlanningState(BaseModel):
    """State object for the LangGraph workflow"""
    existing_meals: List[Meal] = Field(default_factory=list)
    meal_preferences: Dict[str, Any] = Field(default_factory=dict)
    weekly_plan: Optional[WeeklyMealPlan] = None
    error_message: Optional[str] = None
    step: str = "start"