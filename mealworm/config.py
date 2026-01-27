import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    NOTION_API_KEY: str = os.getenv("NOTION_API_KEY", "")

    # MCP Configuration
    NOTION_MCP_URL: str = os.getenv("NOTION_MCP_URL", "https://mcp.notion.com/mcp")
    NOTION_MCP_SSE_URL: str = os.getenv(
        "NOTION_MCP_SSE_URL", "https://mcp.notion.com/sse"
    )

    # Meal planning configuration
    DAYS_OF_WEEK = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    @classmethod
    def validate(cls) -> None:
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        if not cls.NOTION_API_KEY:
            raise ValueError("NOTION_API_KEY environment variable is required")
