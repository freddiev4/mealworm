from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """Single user account for the meal planner owner"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    preferences = relationship(
        "UserPreferences",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    meal_plans = relationship(
        "GeneratedMealPlan", back_populates="user", cascade="all, delete-orphan"
    )


class UserPreferences(Base):
    """Personalized meal planning preferences"""

    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True
    )

    # Meal Plan Requirements
    chicken_dishes_per_week = Column(Integer, default=1)
    fish_dishes_per_week = Column(Integer, default=2)
    vegetables_required = Column(Boolean, default=True)
    eating_out_days = Column(
        JSON, default=lambda: ["Friday", "Saturday"]
    )  # List of days
    leftovers_for_lunch = Column(Boolean, default=True)

    # Meal Preferences
    likes = Column(JSON, default=list)  # List of liked foods/cuisines
    dislikes = Column(
        JSON, default=lambda: ["olives", "capers", "pesto"]
    )  # List of disliked foods
    preferred_cuisines = Column(
        JSON, default=lambda: ["Asian", "Latin", "Italian", "American"]
    )
    sauce_preference = Column(
        String(255),
        default="Every meal should have some kind of sauce on top. I don't like dry meals.",
    )
    easy_meal_preference = Column(
        Text,
        default="I prefer one super easy meal where I can buy the ingredients mostly pre-made & frozen. For example: chicken burgers w/ fries, salmon burgers w/ fries, BLT sandwich with chili crisp mayo, etc.",
    )

    # Dietary Restrictions
    dietary_restrictions = Column(
        JSON, default=list
    )  # e.g., ["vegetarian", "gluten-free"]
    allergens = Column(JSON, default=list)  # e.g., ["nuts", "shellfish"]

    # Avoid certain meal types
    avoid_meal_types = Column(JSON, default=lambda: ["stir fry"])  # Meal types to avoid

    # Shopping List Template
    other_items = Column(
        JSON,
        default=lambda: [
            "Almond milk",
            "Avocados",
            "Eggs",
            "Bread",
            "Bars for snacking",
            "Orange juice/drink for the week",
            "Kashi peanut butter cereal x 3 boxes",
            "Olive oil",
            "Avocado oil",
            "WW vinegar",
            "Peanut Butter",
            "Crisps",
            "Dragonfruit fruit pouches",
            "Fruit",
            "Buns",
            "Dish soap",
            "Chia seeds",
            "Frozen fruit",
            "Pizza sauce",
            "Pizza dough",
            "Pizza cheese",
            "Parchment paper",
            "Dijon mustard",
        ],
    )

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="preferences")


class GeneratedMealPlan(Base):
    """Track generated meal plans for history"""

    __tablename__ = "generated_meal_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    week_starting = Column(DateTime, nullable=False, index=True)
    markdown_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="meal_plans")
