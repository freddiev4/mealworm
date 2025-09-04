#!/usr/bin/env python3
"""
Mealworm - AI-powered meal planning with Notion integration

Usage:
    python main.py [options]

Options:
    --format {text,simple,markdown}  Output format (default: text)
    --help                          Show this help message
"""

import sys
import argparse
from mealworm.config import Config
from mealworm.workflow import MealPlanningWorkflow

from openinference.instrumentation.langchain import LangChainInstrumentor
from quotientai import QuotientAI

quotient = QuotientAI()

quotient.tracer.init(
    app_name='mealworm',
    environment='development',
    instruments=[LangChainInstrumentor()],
)

@quotient.trace()
def main():
    parser = argparse.ArgumentParser(
        description="Mealworm - AI-powered meal planning with Notion integration"
    )
    parser.add_argument(
        "--format",
        choices=["text", "simple", "markdown"],
        default="text",
        help="Output format for the meal plan"
    )
    
    args = parser.parse_args()
    
    try:
        # Validate configuration
        Config.validate()
        
        print("🐛 Welcome to Mealworm - AI Meal Planning")
        print("=========================================")
        print()
        
        # Create and run the workflow
        workflow = MealPlanningWorkflow()
        result = workflow.run()
        
        # Check for errors
        if result.error_message:
            print(f"❌ Error: {result.error_message}")
            sys.exit(1)
        
        if not result.formatted_plan:
            print("❌ No meal plan was generated")
            sys.exit(1)
        
        # Display the formatted result
        print("\n" + "=" * 50)
        print("MEAL PLAN GENERATED SUCCESSFULLY!")
        print("=" * 50)
        
        print(result.formatted_plan)
        
        # Show summary
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        print(f"📊 Total meals found in Notion: {len(result.existing_meals)}")
        print(f"🎯 Planning completed successfully!")
        
        if result.meal_preferences.get("analysis"):
            print(f"\n📈 Meal Analysis:")
            print(result.meal_preferences["analysis"])
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()