from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from mealworm.models import MealPlanningState
from mealworm.config import Config


class MealPlanGeneratorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-5",
            temperature=0.7,
            api_key=Config.OPENAI_API_KEY
        )

    def generate_weekly_plan(self, state: MealPlanningState) -> Dict[str, Any]:
        """
        Generate a weekly meal plan using AI
        """
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
            
            Please respond with a structured meal plan in this exact format, excluding the <start-of-format> and <end-of-format> tags:

            <start-of-format>
            # 🍽️ Weekly Meal Plan
            **Week starting:** [Current Date]
            
            ## Sunday
            - **Lunch:** [Meal Name or "Eat out" or "Leftovers"]
            - **Dinner:** [Meal Name]
            
            ## Monday
            - **Lunch:** [Meal Name or "Eat out" or "Leftovers"]
            - **Dinner:** [Meal Name]
            
            ## Tuesday
            - **Lunch:** [Meal Name or "Eat out" or "Leftovers"]
            - **Dinner:** [Meal Name]
            
            ## Wednesday
            - **Lunch:** [Meal Name or "Eat out" or "Leftovers"]
            - **Dinner:** [Meal Name]
            
            ## Thursday
            - **Lunch:** [Meal Name or "Eat out" or "Leftovers"]
            - **Dinner:** [Meal Name]
            
            ## Friday
            - **Lunch:** [Meal Name or "Eat out" or "Leftovers"]
            - **Dinner:** [Meal Name]
            
            ## Saturday
            - **Lunch:** [Meal Name or "Eat out" or "Leftovers"]
            - **Dinner:** [Meal Name]
            
            ## Sunday
            - **Lunch:** [Meal Name or "Eat out" or "Leftovers"]
            - **Dinner:** [Meal Name]
            
            ## Notes:
            [Any additional planning notes or grocery considerations]
            <end-of-format>
            """
            
            messages = [
                SystemMessage(content="You are an expert meal planner. Create balanced, varied weekly meal plans."),
                HumanMessage(content=planning_prompt)
            ]
            
            response = self.llm.invoke(messages)
            plan_text = response.content
            
            print("✅ Weekly meal plan generated")
            
            response = {
                "formatted_plan": plan_text,
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
