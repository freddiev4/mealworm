from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from mealworm.models import MealPlanningState
from mealworm.config import Config


class MealAnalyzerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-5",
            temperature=0.7,
            api_key=Config.OPENAI_API_KEY
        )

    def analyze_meals(self, state: MealPlanningState) -> Dict[str, Any]:
        """Analyze existing meals to understand patterns and preferences"""
        try:
            print("🧠 Analyzing existing meals...")
            
            meals = state.existing_meals
            if not meals:
                return {
                    "meal_preferences": {"note": "No existing meals found"},
                    "step": "meals_analyzed"
                }
            
            # Create analysis prompt
            meals_summary = []
            for meal in meals[:50]:  # Limit to avoid token limits
                meal_info = f"- {meal.title}"
                if meal.cuisine_type:
                    meal_info += f" ({meal.cuisine_type})"
                if meal.tags:
                    meal_info += f" [Tags: {', '.join(meal.tags)}]"
                meals_summary.append(meal_info)
            
            analysis_prompt = f"""
            Analyze the following {len(meals)} meals from the user's Notion workspace:
            
            {chr(10).join(meals_summary)}
            
            Please provide a brief analysis including:
            1. Most common cuisine types
            2. Common meal categories/tags
            3. Any patterns in meal complexity or types
            4. Suggested variety for weekly planning
            
            Keep your response concise and focused on insights for meal planning.
            """
            
            messages = [
                SystemMessage(content="You are a meal planning assistant analyzing existing recipes."),
                HumanMessage(content=analysis_prompt)
            ]
            
            response = self.llm.invoke(messages)
            analysis = response.content
            
            preferences = {
                "total_meals": len(meals),
                "analysis": analysis,
                "cuisine_types": list(set([m.cuisine_type for m in meals if m.cuisine_type])),
                "common_tags": list(set([tag for m in meals for tag in m.tags]))
            }
            
            print("✅ Meal analysis complete")
            
            return {
                "meal_preferences": preferences,
                "step": "meals_analyzed"
            }
        
        except Exception as e:
            print(f"❌ Error analyzing meals: {e}")
            return {
                "error_message": f"Failed to analyze meals: {str(e)}",
                "step": "error"
            }
