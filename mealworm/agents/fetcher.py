from typing import Dict, Any

from langchain_openai import ChatOpenAI

from mealworm.models import MealPlanningState
from mealworm.notion_client import NotionMCPClient
from mealworm.config import Config


class MealFetcherAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-5",
            temperature=0.7,
            api_key=Config.OPENAI_API_KEY
        )
        self.notion_client = NotionMCPClient()

    def fetch_meals(self, state: MealPlanningState) -> Dict[str, Any]:
        """Fetch existing meals from Notion"""
        try:
            print("🔍 Fetching existing meals from Notion...")
            
            # Find meal-related databases
            databases = self.notion_client.find_meal_databases()
            
            all_meals = []
            for db in databases:
                db_id = db.get("id", "")
                if db_id:
                    pages = self.notion_client.get_database_pages(db_id)
                    meals = self.notion_client.extract_meals_from_pages(pages)
                    all_meals.extend(meals)
            
            # Also search for individual meal pages
            meal_pages = self.notion_client.search_pages(query="meal recipe")
            additional_meals = self.notion_client.extract_meals_from_pages(meal_pages)
            all_meals.extend(additional_meals)
            
            # Remove duplicates based on title
            unique_meals = []
            seen_titles = set()
            for meal in all_meals:
                if meal.title.lower() not in seen_titles:
                    unique_meals.append(meal)
                    seen_titles.add(meal.title.lower())
            
            print(f"✅ Found {len(unique_meals)} unique meals")
            
            return {
                "existing_meals": unique_meals,
                "step": "meals_fetched"
            }
        
        except Exception as e:
            print(f"❌ Error fetching meals: {e}")
            return {
                "error_message": f"Failed to fetch meals: {str(e)}",
                "step": "error"
            }
