from pathlib import Path

from typing import Optional, Union

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.tavily import TavilyTools
from agno.vectordb.pgvector import PgVector
from sqlalchemy.orm import Session

from mealworm.db.url import get_db_url
from mealworm.db.session import SessionLocal
from mealworm.db.models import UserPreferences
from mealworm.agents.instructions_builder import build_custom_instructions

# Note: Custom instructions are now dynamically generated from user preferences
# See mealworm/agents/instructions_builder.py for the template builder


async def load_meal_plans_to_vector_db():
    """Load historical meal plans from markdown files into PGVector database."""
    db_url = get_db_url()

    knowledge = Knowledge(
        vector_db=PgVector(
            table_name="meal_plans",
            db_url=db_url,
        ),
    )

    # Add Markdown content from historical meal plans to knowledge base
    historical_plans_dir = Path("historical-meal-plans")
    if historical_plans_dir.exists():
        print(
            f"Adding historical meal plans to knowledge base from {historical_plans_dir}"
        )
        paths = list(historical_plans_dir.glob("*.md"))
        if paths:
            await knowledge.add_contents_async(
                paths=paths,
                reader=MarkdownReader(),
                skip_if_exists=True,
            )
            print(f"Added {len(paths)} meal plans to knowledge base")
    else:
        print(f"Directory {historical_plans_dir} does not exist")

    return knowledge


async def get_meal_planning_knowledge():
    """Get or create meal planning knowledge base."""
    return await load_meal_plans_to_vector_db()


def get_model_instance(model_id: str) -> Union[Claude, OpenAIChat]:
    """
    Returns the appropriate model instance based on the model_id.

    Args:
        model_id: Model identifier (e.g., "claude-sonnet-4-5", "gpt-5-mini")

    Returns:
        Either a Claude or OpenAIChat model instance
    """
    if model_id.startswith("claude-"):
        return Claude(
            id=model_id,
            client_params={
                "max_retries": 5,  # Retry up to 5 times
                "timeout": 60.0,  # 60 second timeout
            },
        )
    else:
        # Assume OpenAI for all other models
        # Add retry configuration to handle transient network errors
        return OpenAIChat(
            id=model_id,
            client_params={
                "max_retries": 5,  # Retry up to 5 times
                "timeout": 60.0,  # 60 second timeout
            },
        )


async def create_meal_planning_agent(
    model_id: str = "claude-sonnet-4-0",
    user_id: Optional[int] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
):
    """
    Create and return a configured meal planning agent with user-specific preferences.

    Args:
        model_id: Model identifier (supports Anthropic Claude and OpenAI models)
        user_id: User identifier (REQUIRED for authenticated requests)
        session_id: Optional session identifier
        debug_mode: Enable debug mode

    Returns:
        Configured Agent instance

    Raises:
        ValueError: If user_id is not provided or preferences not found
    """
    if user_id is None:
        raise ValueError("user_id is required to create a meal planning agent")

    # Fetch user preferences from database
    db: Session = SessionLocal()
    try:
        preferences = (
            db.query(UserPreferences).filter(UserPreferences.user_id == user_id).first()
        )

        if not preferences:
            raise ValueError(f"No preferences found for user_id: {user_id}")

        # Build custom instructions from preferences
        custom_instructions = build_custom_instructions(preferences)
    finally:
        db.close()

    model = get_model_instance(model_id)

    agent = Agent(
        name="mealworm-meal-planner",
        model=model,
        instructions=custom_instructions,
        tools=[
            TavilyTools(),
            FirecrawlTools(enable_scrape=True, enable_crawl=True),
        ],
        knowledge=await get_meal_planning_knowledge(),
        search_knowledge=True,
        markdown=True,
    )
    return agent


if __name__ == "__main__":
    import asyncio

    agent = asyncio.run(create_meal_planning_agent())
    agent.run("Generate a meal plan for the week.")
