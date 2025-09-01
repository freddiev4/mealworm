from typing import Dict, Any

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, START, END

from mealworm.agents import MealFetcherAgent, MealAnalyzerAgent, MealPlanGeneratorAgent
from mealworm.models import MealPlanningState

class MealPlanningWorkflow:
    """LangGraph workflow for meal planning"""
    
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(MealPlanningState)

        # Initialize agents
        meal_fetcher_agent = MealFetcherAgent()
        # TODO: replace this with a summarizer agent that can group the unique meals we have
        meal_analyzer_agent = MealAnalyzerAgent()
        meal_plan_generator_agent = MealPlanGeneratorAgent()
        
        # Add nodes
        workflow.add_node("fetch_meals", meal_fetcher_agent.fetch_meals)
        workflow.add_node("analyze_meals", meal_analyzer_agent.analyze_meals)
        workflow.add_node("generate_plan", meal_plan_generator_agent.generate_weekly_plan)
        
        # Add edges
        workflow.add_edge(START, "fetch_meals")
        workflow.add_edge("fetch_meals", "analyze_meals")
        workflow.add_edge("analyze_meals", "generate_plan")
        workflow.add_edge("generate_plan", END)
        
        return workflow.compile()
    
    def run(self, preferences: Dict[str, Any] = None) -> MealPlanningState:
        """Run the complete meal planning workflow"""
        print("🚀 Starting meal planning workflow...")
        
        initial_state = MealPlanningState(
            meal_preferences=preferences or {}
        )
        
        try:
            final_state = self.graph.invoke(initial_state)
            state = MealPlanningState(**final_state)
        except Exception as e:
            print(f"❌ Workflow failed: {e}")
            state = MealPlanningState(
                error_message=f"Workflow failed: {str(e)}",
                step="error"
            )
        
        return state
