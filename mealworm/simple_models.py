"""
Simplified models without external dependencies for demonstration
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Meal:
    """Represents a meal from Notion"""
    id: str
    title: str
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    prep_time: Optional[int] = None  # in minutes
    cook_time: Optional[int] = None  # in minutes
    difficulty: Optional[str] = None
    ingredients: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    last_made: Optional[str] = None  # simplified as string
    rating: Optional[int] = None
    raw_notion_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DayPlan:
    """Represents meals planned for a single day"""
    day: str
    breakfast: Optional[Meal] = None
    lunch: Optional[Meal] = None
    dinner: Optional[Meal] = None
    snacks: List[Meal] = field(default_factory=list)


@dataclass
class WeeklyMealPlan:
    """Represents a complete weekly meal plan"""
    week_starting: datetime
    days: List[DayPlan]
    notes: Optional[str] = None
    grocery_list: List[str] = field(default_factory=list)


@dataclass
class MealPlanningState:
    """State object for the workflow"""
    existing_meals: List[Meal] = field(default_factory=list)
    meal_preferences: Dict[str, Any] = field(default_factory=dict)
    weekly_plan: Optional[WeeklyMealPlan] = None
    error_message: Optional[str] = None
    step: str = "start"