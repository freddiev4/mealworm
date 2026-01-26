#!/usr/bin/env python3
"""
Mealworm - AI-powered meal planning with Agno Agent

Usage:
    python main_agno.py [options]

Options:
    --stream                    Stream the response (default: True)
    --help                     Show this help message
"""

import argparse
import sys

from pathlib import Path

from mealworm.agents.meal_planner import create_meal_planning_agent, START_OF_WEEK
from openinference.instrumentation.agno import AgnoInstrumentor
from quotientai import QuotientAI

quotient = QuotientAI()

quotient.tracer.init(
    app_name="mealworm",
    environment="development",
    instruments=[AgnoInstrumentor()],
)


@quotient.trace()
def main():
    parser = argparse.ArgumentParser(
        description="Mealworm - AI-powered meal planning with Agno Agent"
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        default=True,
        help="Stream the response (default: True)",
    )
    parser.add_argument(
        "--no-stream", action="store_true", help="Don't stream the response"
    )

    args = parser.parse_args()

    # Override stream setting if --no-stream is provided
    stream = args.stream and not args.no_stream

    try:
        print("🐛 Welcome to Mealworm - AI Meal Planning with Agno")
        print("=" * 55)
        print(f"📅 Planning meals for week starting: {START_OF_WEEK}")
        print("=" * 55)
        print()

        # Create the meal planning agent
        print("🤖 Initializing AI agent...")
        agent = create_meal_planning_agent()

        print("🍽️  Generating meal plan...")
        print("-" * 30)

        # Run the agent
        if stream:
            agent.print_response("Please make me a meal plan", stream=True)
        else:
            response = agent.run()
            print(response.content)

        print("\n" + "=" * 55)
        print("✅ MEAL PLAN GENERATED SUCCESSFULLY!")
        print("=" * 55)

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
