from typing import Dict, Any
from datetime import datetime, timedelta
from langgraph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from .models import MealPlanningState, WeeklyMealPlan, DayPlan, Meal
from .notion_client import NotionMCPClient
from .config import Config


class MealPlanningWorkflow:
    """LangGraph workflow for meal planning"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # Will upgrade to gpt-5 when available
            temperature=0.7,
            api_key=Config.OPENAI_API_KEY
        )
        self.notion_client = NotionMCPClient()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(MealPlanningState)
        
        # Add nodes
        workflow.add_node("fetch_meals", self._fetch_existing_meals)
        workflow.add_node("analyze_meals", self._analyze_meals)
        workflow.add_node("generate_plan", self._generate_weekly_plan)
        workflow.add_node("format_output", self._format_meal_plan)
        
        # Add edges
        workflow.add_edge(START, "fetch_meals")
        workflow.add_edge("fetch_meals", "analyze_meals")
        workflow.add_edge("analyze_meals", "generate_plan")
        workflow.add_edge("generate_plan", "format_output")
        workflow.add_edge("format_output", END)
        
        return workflow.compile()
    
    def _fetch_existing_meals(self, state: MealPlanningState) -> Dict[str, Any]:
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
    
    def _analyze_meals(self, state: MealPlanningState) -> Dict[str, Any]:
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
    
    def _generate_weekly_plan(self, state: MealPlanningState) -> Dict[str, Any]:
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
            
            planning_prompt = f"""
            Create a weekly meal plan using the following {len(meals)} available meals:
            
            {chr(10).join(available_meals)}
            
            Requirements:
            - Plan for 8 days: {', '.join(Config.DAYS_OF_WEEK)}
            - Focus on dinner meals primarily
            - Ensure variety across the week
            - Consider meal complexity and prep time balance
            - Avoid repeating the same meal in the same week
            
            Analysis of existing meals: {preferences.get('analysis', 'No analysis available')}
            
            Please respond with a structured meal plan in this exact format:
            
            Sunday: [Meal Name]
            Monday: [Meal Name]
            Tuesday: [Meal Name]
            Wednesday: [Meal Name]
            Thursday: [Meal Name]
            Friday: [Meal Name]
            Saturday: [Meal Name]
            Sunday: [Meal Name]
            
            Notes: [Any additional planning notes or grocery considerations]
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
            
            return {
                "weekly_plan": weekly_plan,
                "step": "plan_generated"
            }
        
        except Exception as e:
            print(f"❌ Error generating meal plan: {e}")
            return {
                "error_message": f"Failed to generate meal plan: {str(e)}",
                "step": "error"
            }
    
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
    
    def _format_meal_plan(self, state: MealPlanningState) -> Dict[str, Any]:
        """Format the meal plan for output"""
        try:
            print("📋 Formatting meal plan...")
            
            plan = state.weekly_plan
            if not plan:
                return {
                    "error_message": "No meal plan generated",
                    "step": "error"
                }
            
            # The plan is already formatted in the desired structure
            print("✅ Meal plan formatted successfully")
            
            return {
                "step": "completed"
            }
        
        except Exception as e:
            print(f"❌ Error formatting meal plan: {e}")
            return {
                "error_message": f"Failed to format meal plan: {str(e)}",
                "step": "error"
            }
    
    def run(self, preferences: Dict[str, Any] = None) -> MealPlanningState:
        """Run the complete meal planning workflow"""
        print("🚀 Starting meal planning workflow...")
        
        initial_state = MealPlanningState(
            meal_preferences=preferences or {}
        )
        
        try:
            final_state = self.graph.invoke(initial_state)
            return MealPlanningState(**final_state)
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            return MealPlanningState(
                error_message=f"Workflow failed: {str(e)}",
                step="error"
            )