from typing import Dict, Any
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from mealworm.models import MealPlanningState, WeeklyMealPlan, DayPlan, Meal
from mealworm.config import Config


class MealPlanGeneratorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-5",
            temperature=0.7,
            api_key=Config.OPENAI_API_KEY
        )

    def generate_weekly_plan(self, state: MealPlanningState) -> Dict[str, Any]:
        """Generate a weekly meal plan using AI"""
        try:
            print("📅 Generating weekly meal plan...")
            
            meals = state.existing_meals
            preferences = state.meal_preferences
            
            # Create meal selection prompt
            available_meals = []
            for meal in meals:
                meal_desc = f"- {meal.title}"
                if meal.cuisine_type:
                    meal_desc += f" ({meal.cuisine_type})"
                if meal.description:
                    meal_desc += f": {meal.description[:100]}..."
                available_meals.append(meal_desc)


            analysis = preferences.get('analysis', 'No analysis available')
            
            planning_prompt = f"""
            Create a weekly meal plan using the following {len(meals)} available meals:
            
            {chr(10).join(available_meals)}
            
            Requirements:
            - Plan for 8 days: {', '.join(Config.DAYS_OF_WEEK)}
            - Focus on dinner meals primarily
            - Ensure variety across the week
            - Consider meal complexity and prep time balance
            - Avoid repeating the same meal in the same week
            
            Analysis of existing meals: {analysis}
            
            Please respond with a structured meal plan in this exact format:

            <start-of-format>
            # Sunday:
            **Lunch:**
            **Dinner:**

            # Monday:
            **Lunch:**
            **Dinner:**

            # Tuesday:
            **Lunch:**
            **Dinner:**
            
            # Wednesday:
            **Lunch:**
            **Dinner:**

            # Thursday:
            **Lunch:**
            **Dinner:**

            # Friday:
            **Lunch:**
            **Dinner:**

            **Lunch:**
            **Dinner:**

            # Saturday:
            **Lunch:**
            **Dinner:**

            # Sunday:
            **Lunch:**
            **Dinner:**
            
            ## Notes:
            <any additional planning notes or grocery considerations>
            <end-of-format>
            """
            
            messages = [
                SystemMessage(content="You are an expert meal planner. Create balanced, varied weekly meal plans."),
                HumanMessage(content=planning_prompt)
            ]
            
            response = self.llm.invoke(messages)
            plan_text = response.content
            
            # Parse the response into structured data
            weekly_plan = self._parse_meal_plan_response(plan_text, meals)
            
            print("✅ Weekly meal plan generated")
            
            response = {
                "weekly_plan": weekly_plan,
                "step": "plan_generated"
            }

            return response

        except Exception as e:
            print(f"❌ Error generating meal plan: {e}")
            response = {
                "error_message": f"Failed to generate meal plan: {str(e)}",
                "step": "error"
            }
            return response

    def _parse_meal_plan_response(self, plan_text: str, available_meals: list) -> WeeklyMealPlan:
        """Parse the AI response into a structured meal plan"""
        lines = plan_text.strip().split('\n')
        days = []
        notes = ""
        
        # Create a lookup for meals by title
        meal_lookup = {meal.title.lower(): meal for meal in available_meals}
        
        for line in lines:
            line = line.strip()
            if ':' in line and any(day in line for day in Config.DAYS_OF_WEEK):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    day_name, meal_name = parts
                    day_name = day_name.strip()
                    meal_name = meal_name.strip()
                
                    # Find the matching meal
                    selected_meal = None
                    for title, meal in meal_lookup.items():
                        if title in meal_name.lower() or meal_name.lower() in title:
                            selected_meal = meal
                            break
                    
                    # If no exact match, create a placeholder meal
                    if not selected_meal and meal_name:
                        selected_meal = Meal(
                            id="placeholder",
                            title=meal_name,
                            description="Selected from meal plan"
                        )
                    
                    days.append(DayPlan(
                        day=day_name,
                        dinner=selected_meal
                    ))
            
            elif line.lower().startswith('notes:'):
                notes = line.split(':', 1)[1].strip()
        
        return WeeklyMealPlan(
            week_starting=datetime.now(),
            days=days,
            notes=notes
        )
