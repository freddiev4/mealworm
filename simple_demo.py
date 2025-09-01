#!/usr/bin/env python3
"""
Simple demonstration of the mealworm application structure
This works without external dependencies to show the core functionality
"""

import sys
import os
from datetime import datetime

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from mealworm.simple_models import Meal, DayPlan, WeeklyMealPlan
from mealworm.simple_formatter import MealPlanFormatter


def create_sample_data():
    """Create sample meal data"""
    meals = [
        Meal(
            id="1",
            title="Spaghetti Carbonara",
            description="Classic Italian pasta with eggs, cheese, and pancetta",
            cuisine_type="Italian",
            prep_time=30,
            tags=["pasta", "italian", "quick", "comfort-food"]
        ),
        Meal(
            id="2", 
            title="Chicken Teriyaki Bowl",
            description="Grilled chicken with teriyaki sauce over rice",
            cuisine_type="Japanese",
            prep_time=25,
            tags=["chicken", "rice", "asian", "healthy"]
        ),
        Meal(
            id="3",
            title="Beef Tacos",
            description="Seasoned ground beef in soft tortillas with fixings",
            cuisine_type="Mexican", 
            prep_time=20,
            tags=["beef", "mexican", "quick", "family-friendly"]
        ),
        Meal(
            id="4",
            title="Mediterranean Salmon",
            description="Baked salmon with Mediterranean herbs and vegetables",
            cuisine_type="Mediterranean",
            prep_time=35,
            tags=["salmon", "healthy", "mediterranean", "fish"]
        ),
        Meal(
            id="5",
            title="Thai Green Curry",
            description="Coconut curry with vegetables and your choice of protein",
            cuisine_type="Thai",
            prep_time=40,
            tags=["curry", "thai", "spicy", "coconut"]
        ),
        Meal(
            id="6",
            title="BBQ Pulled Pork Sandwiches",
            description="Slow-cooked pulled pork with BBQ sauce on brioche buns",
            cuisine_type="American",
            prep_time=15,  # excluding slow cook time
            tags=["pork", "bbq", "american", "comfort-food"]
        ),
        Meal(
            id="7",
            title="Greek Lemon Chicken",
            description="Roasted chicken with lemon, oregano, and potatoes",
            cuisine_type="Greek",
            prep_time=45,
            tags=["chicken", "greek", "lemon", "roasted"]
        ),
        Meal(
            id="8",
            title="Vegetarian Stir Fry",
            description="Mixed vegetables stir-fried with ginger and soy sauce",
            cuisine_type="Asian",
            prep_time=20,
            tags=["vegetarian", "stir-fry", "healthy", "quick"]
        )
    ]
    
    return meals


def create_weekly_plan(meals):
    """Create a sample weekly meal plan"""
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Select meals for each day (using different meals)
    selected_meals = meals[:8]  # Use first 8 meals
    
    days = []
    for i, day in enumerate(days_of_week):
        day_plan = DayPlan(
            day=day,
            dinner=selected_meals[i] if i < len(selected_meals) else None
        )
        days.append(day_plan)
    
    weekly_plan = WeeklyMealPlan(
        week_starting=datetime.now(),
        days=days,
        notes="Balanced weekly meal plan with variety of cuisines and cooking times. Consider prep work on Sunday for easier weekday meals."
    )
    
    return weekly_plan


def main():
    """Demonstrate the mealworm application"""
    print("🐛 Mealworm - AI-Powered Meal Planning")
    print("=" * 50)
    print()
    
    # Simulate the workflow
    print("🔍 Fetching existing meals from Notion...")
    meals = create_sample_data()
    print(f"✅ Found {len(meals)} unique meals")
    
    print("\n🧠 Analyzing existing meals...")
    cuisines = list(set([meal.cuisine_type for meal in meals if meal.cuisine_type]))
    meals_with_prep = [meal.prep_time for meal in meals if meal.prep_time]
    avg_prep_time = sum(meals_with_prep) / len(meals_with_prep) if meals_with_prep else 0
    print(f"✅ Analysis complete - {len(cuisines)} cuisine types, avg prep: {avg_prep_time:.1f} minutes")
    
    print("\n📅 Generating weekly meal plan...")
    weekly_plan = create_weekly_plan(meals)
    print("✅ Weekly meal plan generated")
    
    print("\n📋 Formatting meal plan...")
    
    # Show different output formats
    print("\n" + "=" * 60)
    print("FORMATTED OUTPUT - TEXT FORMAT")
    print("=" * 60)
    text_output = MealPlanFormatter.to_text(weekly_plan)
    print(text_output)
    
    print("\n" + "=" * 60)
    print("FORMATTED OUTPUT - SIMPLE FORMAT")
    print("=" * 60)
    simple_output = MealPlanFormatter.to_simple_template(weekly_plan)
    print(simple_output)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"📊 Total meals in database: {len(meals)}")
    print(f"📅 Days planned: {len(weekly_plan.days)}")
    print(f"🍽️ Cuisine variety: {', '.join(cuisines)}")
    print(f"⏱️ Average prep time: {avg_prep_time:.1f} minutes")
    print(f"🎯 Planning completed successfully!")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("1. Set up your OpenAI API key in .env file")
    print("2. Configure Notion MCP server access")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Run the full application: python main.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())