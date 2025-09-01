from typing import Dict, Any

from langchain_openai import ChatOpenAI
from tavily import TavilyClient


from mealworm.models import MealPlanningState
from mealworm.notion_client import NotionMCPClient
from mealworm.config import Config


tavily_client = TavilyClient(api_key=Config.TAVILY_API_KEY)


class MealIngredientSearcherAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-5",
            temperature=0.7,
            api_key=Config.OPENAI_API_KEY
        )
        self.notion_client = NotionMCPClient()

    def search_ingredients(self, state: MealPlanningState) -> Dict[str, Any]:
        """Fetch existing meals from Notion"""
        try:
            print("🔍 Searching for ingredients...")
            
            # get the urls of the meals
            # find their ingredients from the urls using Tavily to extract the page contents
            # using tavily.extract(url)
            # return the ingredients for each meal
            # fill in the ingredients for the meal in the plan

            
        
        except Exception as e:
            print(f"❌ Error fetching meals: {e}")
            return {
                "error_message": f"Failed to fetch meals: {str(e)}",
                "step": "error"
            }
