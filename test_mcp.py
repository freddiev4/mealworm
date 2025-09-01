#!/usr/bin/env python3
"""
Test script to check Notion MCP connection and available tools
"""

import asyncio
import json
import os
from langchain_mcp_adapters.client import MultiServerMCPClient

async def test_notion_mcp():
    """Test connection to Notion MCP server"""
    
    # Check for API key
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key:
        print("❌ NOTION_API_KEY environment variable is required")
        print("Please set it with: export NOTION_API_KEY=your_notion_api_key")
        return
    
    # MCP configuration for local notion-mcp-server
    config = {
        "Notion": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@notionhq/notion-mcp-server"],
            "env": {
                "OPENAPI_MCP_HEADERS": json.dumps({
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28"
                })
            }
        }
    }
    
    try:
        print("🔌 Connecting to Notion MCP server...")
        client = MultiServerMCPClient(config)
        
        # List available tools
        print("📋 Available tools:")
        tools = await client.get_tools()
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Test search functionality
        print("\n🔍 Testing search functionality...")
        search_tool = None
        for tool in tools:
            if tool.name == "API-post-search":
                search_tool = tool
                break
        
        if search_tool:
            result = await search_tool.ainvoke({
                "query": "meal",
                "filter": {"property": "object", "value": "page"}
            })
            print(f"Search result: {json.dumps(result, indent=2)}")
        else:
            print("❌ API-post-search tool not found")
        
        # Test database query functionality
        print("\n📊 Testing database query functionality...")
        db_query_tool = None
        for tool in tools:
            if tool.name == "API-post-database-query":
                db_query_tool = tool
                break
        
        if db_query_tool:
            print("✅ API-post-database-query tool found (would need a real database ID to test)")
        else:
            print("❌ API-post-database-query tool not found")
        
        # Test page retrieval functionality
        print("\n📄 Testing page retrieval functionality...")
        page_tool = None
        for tool in tools:
            if tool.name == "API-retrieve-a-page":
                page_tool = tool
                break
        
        if page_tool:
            print("✅ API-retrieve-a-page tool found (would need a real page ID to test)")
        else:
            print("❌ API-retrieve-a-page tool not found")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_notion_mcp())
