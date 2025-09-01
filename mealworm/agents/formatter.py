from typing import Dict, Any

from langchain_openai import ChatOpenAI
from mealworm.models import MealPlanningState
from mealworm.config import Config


class MealPlanFormatterAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-5",
            temperature=0.7,
            api_key=Config.OPENAI_API_KEY
        )

    def format_meal_plan(self, state: MealPlanningState) -> Dict[str, Any]:
        """Format the meal plan for output"""
        try:
            print("📋 Formatting meal plan...")
            
            plan = state.weekly_plan
            if not plan:
                response = {
                    "error_message": "No meal plan generated",
                    "step": "error"
                }
                return response
            
            # The plan is already formatted in the desired structure
            print("✅ Meal plan formatted successfully")
            
            response = {
                "step": "completed"
            }
            return response
        
        except Exception as e:
            print(f"❌ Error formatting meal plan: {e}")
            response = {
                "error_message": f"Failed to format meal plan: {str(e)}",
                "step": "error"
            }
            return response