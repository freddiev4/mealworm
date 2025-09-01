from typing import List, Dict, Any, Optional
import json
import requests
from .models import Meal
from .config import Config


class NotionMCPClient:
    """Client for interacting with Notion via MCP server"""
    
    def __init__(self):
        self.mcp_url = Config.NOTION_MCP_URL
    
    def _call_mcp(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a call to the Notion MCP server"""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
            "id": 1
        }
        
        try:
            response = requests.post(
                self.mcp_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                raise Exception(f"MCP Error: {result['error']}")
            
            return result.get("result", {})
        except requests.RequestException as e:
            raise Exception(f"Failed to connect to Notion MCP: {e}")
    
    def search_pages(self, query: str = "", filter_type: str = "page") -> List[Dict[str, Any]]:
        """Search for pages in Notion workspace"""
        try:
            result = self._call_mcp("search", {
                "query": query,
                "filter": {"object": filter_type}
            })
            return result.get("results", [])
        except Exception as e:
            print(f"Error searching pages: {e}")
            return []
    
    def get_database_pages(self, database_id: str) -> List[Dict[str, Any]]:
        """Get all pages from a specific database"""
        try:
            result = self._call_mcp("query_database", {
                "database_id": database_id
            })
            return result.get("results", [])
        except Exception as e:
            print(f"Error querying database: {e}")
            return []
    
    def get_page_content(self, page_id: str) -> Dict[str, Any]:
        """Get detailed content of a specific page"""
        try:
            result = self._call_mcp("get_page", {
                "page_id": page_id
            })
            return result
        except Exception as e:
            print(f"Error getting page content: {e}")
            return {}
    
    def find_meal_databases(self) -> List[Dict[str, Any]]:
        """Find databases that likely contain meal/recipe information"""
        try:
            # Search for databases with meal-related keywords
            meal_keywords = ["meal", "recipe", "food", "cooking", "kitchen", "dinner", "lunch", "breakfast"]
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
            except Exception as e:
                print(f"Error parsing page to meal: {e}")
                continue
        
        return meals
    
    def _parse_page_to_meal(self, page: Dict[str, Any]) -> Optional[Meal]:
        """Parse a Notion page into a Meal object"""
        try:
            properties = page.get("properties", {})
            
            # Extract title
            title_prop = properties.get("Name") or properties.get("Title") or properties.get("title", {})
            title = ""
            if title_prop.get("type") == "title" and title_prop.get("title"):
                title = "".join([t.get("plain_text", "") for t in title_prop["title"]])
            
            if not title:
                return None
            
            # Extract other properties
            meal_data = {
                "id": page.get("id", ""),
                "title": title,
                "raw_notion_data": page
            }
            
            # Try to extract common meal properties
            for prop_name, prop_data in properties.items():
                prop_type = prop_data.get("type", "")
                
                if prop_type == "rich_text" and prop_name.lower() in ["description", "notes"]:
                    text_content = "".join([t.get("plain_text", "") for t in prop_data.get("rich_text", [])])
                    meal_data["description"] = text_content
                
                elif prop_type == "select" and prop_name.lower() in ["cuisine", "cuisine_type", "type"]:
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
                
                elif prop_type == "multi_select" and prop_name.lower() in ["tags", "categories"]:
                    tags = [tag.get("name", "") for tag in prop_data.get("multi_select", [])]
                    meal_data["tags"] = tags
                
                elif prop_type == "date" and prop_name.lower() in ["last_made", "last_cooked"]:
                    date_data = prop_data.get("date", {})
                    if date_data and date_data.get("start"):
                        meal_data["last_made"] = date_data["start"]
            
            return Meal(**meal_data)
        
        except Exception as e:
            print(f"Error parsing meal data: {e}")
            return None