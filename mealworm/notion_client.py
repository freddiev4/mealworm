import asyncio
import json

from typing import List, Dict, Any, Optional

from langchain_mcp_adapters.client import MultiServerMCPClient

from mealworm.models import Meal
from mealworm.config import Config


class NotionMCPClient:
    """Client for interacting with Notion via local MCP server"""

    def __init__(self):
        self.api_key = Config.NOTION_API_KEY
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the MCP client with local notion-mcp-server"""
        try:
            if not self.api_key:
                raise Exception("NOTION_API_KEY environment variable is required")

            # Create MCP client configuration for local notion-mcp-server
            config = {
                "Notion": {
                    "transport": "stdio",
                    "command": "npx",
                    "args": ["-y", "@notionhq/notion-mcp-server"],
                    "env": {
                        "OPENAPI_MCP_HEADERS": json.dumps(
                            {
                                "Authorization": f"Bearer {self.api_key}",
                                "Notion-Version": "2022-06-28",
                            }
                        )
                    },
                }
            }

            # Initialize the MCP client
            self.client = MultiServerMCPClient(config)
            print("✅ Notion MCP client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Notion MCP client: {e}")
            self.client = None

    async def _call_mcp_async(
        self, tool_name: str, arguments: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Make an async call to the Notion MCP server"""
        if not self.client:
            raise Exception("MCP client not initialized")

        try:
            # Get tools from the client
            tools = await self.client.get_tools()

            # Find the specific tool
            target_tool = None
            for tool in tools:
                if tool.name == tool_name:
                    target_tool = tool
                    break

            if not target_tool:
                raise Exception(
                    f"Tool {tool_name} not found. Available tools: {[t.name for t in tools]}"
                )

            # Call the tool
            result = await target_tool.ainvoke(arguments or {})

            # Parse JSON string if the result is a string
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    # If it's not valid JSON, return as is
                    pass

            return result
        except Exception as e:
            raise Exception(f"Failed to call MCP tool {tool_name}: {e}")

    def _call_mcp_sync(
        self, tool_name: str, arguments: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Make a synchronous call to the Notion MCP server"""
        try:
            # Run async function in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._call_mcp_async(tool_name, arguments))
            loop.close()
            return result
        except Exception as e:
            raise Exception(f"Failed to call MCP tool {tool_name}: {e}")

    def search_pages(
        self, query: str = "", filter_type: str = "page"
    ) -> List[Dict[str, Any]]:
        """Search for pages in Notion workspace using the 'API-post-search' tool"""
        try:
            # Notion API expects different filter format
            if filter_type == "page":
                filter_obj = {"property": "object", "value": "page"}
            elif filter_type == "database":
                filter_obj = {"property": "object", "value": "database"}
            else:
                filter_obj = None

            arguments = {"query": query}

            if filter_obj:
                arguments["filter"] = filter_obj

            result = self._call_mcp_sync("API-post-search", arguments)
            return result.get("results", [])
        except Exception as e:
            print(f"Error searching pages: {e}")
            return []

    def get_database_pages(self, database_id: str) -> List[Dict[str, Any]]:
        """Get all pages from a specific database using the 'API-post-database-query' tool"""
        try:
            arguments = {"database_id": database_id}

            result = self._call_mcp_sync("API-post-database-query", arguments)
            return result.get("results", [])
        except Exception as e:
            print(f"Error querying database: {e}")
            return []

    def get_page_content(self, page_id: str) -> Dict[str, Any]:
        """Get detailed content of a specific page using the 'API-retrieve-a-page' tool"""
        try:
            arguments = {"page_id": page_id}

            result = self._call_mcp_sync("API-retrieve-a-page", arguments)
            return result
        except Exception as e:
            print(f"Error getting page content: {e}")
            return {}

    def get_page_blocks(self, page_id: str) -> List[Dict[str, Any]]:
        """Get the blocks (content) of a specific page using the 'API-get-block-children' tool"""
        try:
            arguments = {"block_id": page_id}

            result = self._call_mcp_sync("API-get-block-children", arguments)

            # Parse the result to extract blocks
            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except json.JSONDecodeError:
                    return []

            # Extract blocks from the response
            blocks = result.get("results", [])
            return blocks
        except Exception as e:
            print(f"Error getting page blocks: {e}")
            return []

    def find_meal_databases(self) -> List[Dict[str, Any]]:
        """Find databases that likely contain meal/recipe information"""
        try:
            # Search for databases with meal-related keywords
            meal_keywords = [
                "meal",
                "recipe",
                "food",
                "cooking",
                "kitchen",
                "dinner",
                "lunch",
                "breakfast",
            ]
            databases = []

            for keyword in meal_keywords:
                results = self.search_pages(query=keyword, filter_type="database")
                databases.extend(results)

            # Remove duplicates based on ID
            unique_databases = []
            seen_ids = set()
            for db in databases:
                db_id = db.get("id", "")
                if db_id not in seen_ids:
                    unique_databases.append(db)
                    seen_ids.add(db_id)

            return unique_databases
        except Exception as e:
            print(f"Error finding meal databases: {e}")
            return []

    def extract_meals_from_pages(self, pages: List[Dict[str, Any]]) -> List[Meal]:
        """Extract meal information from Notion pages"""
        meals = []

        for page in pages:
            try:
                meal = self._parse_page_to_meal(page)
                if meal:
                    meals.append(meal)
                break
            except Exception as e:
                print(f"Error parsing page to meal: {e}")
                continue

        return meals

    def _parse_page_to_meal(self, page: Dict[str, Any]) -> Optional[Meal]:
        """Parse a Notion page into a Meal object"""
        try:
            properties = page.get("properties", {})

            # Extract title
            title_prop = (
                properties.get("Name")
                or properties.get("Title")
                or properties.get("title", {})
            )
            title = ""
            if title_prop.get("type") == "title" and title_prop.get("title"):
                title = "".join([t.get("plain_text", "") for t in title_prop["title"]])

            if not title:
                return None

            # Get page content (blocks)
            page_id = page.get("id", "")
            page_blocks = []
            if page_id:
                page_blocks = self.get_page_blocks(page_id)

            # Extract other properties
            meal_data = {
                "id": page.get("id", ""),
                "title": title,
                "raw_notion_data": page,
                "page_content": self._extract_text_from_blocks(page_blocks),
            }

            # Try to extract common meal properties
            for prop_name, prop_data in properties.items():
                prop_type = prop_data.get("type", "")

                if prop_type == "rich_text" and prop_name.lower() in [
                    "description",
                    "notes",
                ]:
                    text_content = "".join(
                        [
                            t.get("plain_text", "")
                            for t in prop_data.get("rich_text", [])
                        ]
                    )
                    meal_data["description"] = text_content

                elif prop_type == "select" and prop_name.lower() in [
                    "cuisine",
                    "cuisine_type",
                    "type",
                ]:
                    select_data = prop_data.get("select", {})
                    if select_data:
                        meal_data["cuisine_type"] = select_data.get("name", "")

                elif prop_type == "number":
                    if prop_name.lower() in ["prep_time", "prep"]:
                        meal_data["prep_time"] = prop_data.get("number")
                    elif prop_name.lower() in ["cook_time", "cook"]:
                        meal_data["cook_time"] = prop_data.get("number")
                    elif prop_name.lower() in ["rating", "score"]:
                        meal_data["rating"] = prop_data.get("number")

                elif prop_type == "multi_select" and prop_name.lower() in [
                    "tags",
                    "categories",
                ]:
                    tags = [
                        tag.get("name", "") for tag in prop_data.get("multi_select", [])
                    ]
                    meal_data["tags"] = tags

                elif prop_type == "date" and prop_name.lower() in [
                    "last_made",
                    "last_cooked",
                ]:
                    date_data = prop_data.get("date", {})
                    if date_data and date_data.get("start"):
                        meal_data["last_made"] = date_data["start"]

            return Meal(**meal_data)
        except Exception as e:
            print(f"Error parsing meal data: {e}")
            return None

    def _extract_text_from_blocks(self, blocks: List[Dict[str, Any]]) -> str:
        """Extract readable text from Notion blocks"""
        if not blocks:
            return ""

        text_parts = []

        for block in blocks:
            block_type = block.get("type", "")
            block_data = block.get(block_type, {})

            if block_type == "paragraph":
                # Extract text from paragraph
                rich_text = block_data.get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                if text.strip():
                    text_parts.append(text)

            elif block_type == "heading_1":
                # Extract text from heading 1
                rich_text = block_data.get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                if text.strip():
                    text_parts.append(f"# {text}")

            elif block_type == "heading_2":
                # Extract text from heading 2
                rich_text = block_data.get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                if text.strip():
                    text_parts.append(f"## {text}")

            elif block_type == "heading_3":
                # Extract text from heading 3
                rich_text = block_data.get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                if text.strip():
                    text_parts.append(f"### {text}")

            elif block_type == "bulleted_list_item":
                # Extract text from bulleted list item
                rich_text = block_data.get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                if text.strip():
                    text_parts.append(f"- {text}")

            elif block_type == "numbered_list_item":
                # Extract text from numbered list item
                rich_text = block_data.get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                if text.strip():
                    text_parts.append(f"1. {text}")

            elif block_type == "to_do":
                # Extract text from to-do item
                rich_text = block_data.get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                checked = block_data.get("checked", False)
                if text.strip():
                    checkbox = "[x]" if checked else "[ ]"
                    text_parts.append(f"{checkbox} {text}")

            elif block_type == "toggle":
                # Extract text from toggle
                rich_text = block_data.get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                if text.strip():
                    text_parts.append(f"<details>\n<summary>{text}</summary>")

            elif block_type == "quote":
                # Extract text from quote
                rich_text = block_data.get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                if text.strip():
                    text_parts.append(f"> {text}")

            elif block_type == "callout":
                # Extract text from callout
                rich_text = block_data.get("rich_text", [])
                text = "".join([t.get("plain_text", "") for t in rich_text])
                if text.strip():
                    icon = block_data.get("icon", {}).get("emoji", "💡")
                    text_parts.append(f"{icon} {text}")

        return "\n".join(text_parts)
