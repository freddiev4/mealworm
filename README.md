# 🐛 Mealworm - AI-Powered Meal Planning

Mealworm is an intelligent meal planning application that integrates with your Notion workspace to create personalized weekly meal plans. It uses LangGraph for workflow orchestration, OpenAI's GPT models for intelligent meal selection, and the Notion MCP server for seamless workspace integration.

## Features

- 🔗 **Notion MCP Integration**: Automatically fetches existing meals and recipes from your Notion workspace using the official Notion MCP server
- 🧠 **AI-Powered Planning**: Uses GPT-4 to analyze your meal preferences and generate balanced weekly plans
- 📅 **Custom Template**: Follows your specified Sunday-Saturday-Sunday format
- 🔄 **Workflow Orchestration**: Uses LangGraph for robust, step-by-step meal planning process
- 📊 **Multiple Output Formats**: Text, simple template, or markdown formats
- 🎯 **Smart Analysis**: Provides insights about your cooking patterns and meal preferences

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key
- Notion workspace with meal/recipe pages
- Notion integration token

### Installation

1. Clone and navigate to the project:
```bash
git clone https://github.com/freddiev4/mealworm.git
cd mealworm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Set up Notion Integration**:
   - Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
   - Click "New integration"
   - Give it a name (e.g., "Mealworm AI")
   - Select your workspace
   - Click "Submit"
   - Copy the "Internal Integration Token" (starts with `secret_`)
   - Set the environment variable: `export NOTION_API_KEY="your_token_here"`

5. **Share your Notion pages with the integration**:
   - Go to any Notion page or database you want to access
   - Click the "Share" button (top right)
   - Click "Invite"
   - Search for your integration name
   - Select it and click "Invite"

## Usage

### Basic Usage

```bash
python main.py
```

### Test MCP Connection

To verify your Notion MCP setup:

```bash
python test_mcp.py
```

This will test the connection and show available tools.

### Output Formats

```bash
# Simple day: meal format
python main.py --format simple

# Markdown format
python main.py --format markdown

# Detailed text format (default)
python main.py --format text
```

### Example Output

```
🍽️ WEEKLY MEAL PLAN
==============================
Week starting: September 01, 2025

📅 SUNDAY
--------
🌙 Dinner: Sheet-Pan Miso-Glazed Salmon with Broccoli and Sweet Potatoes

📅 MONDAY
--------
🌙 Dinner: Mediterranean Chickpea–Quinoa Bowls with Tzatziki

📅 TUESDAY
---------
🌙 Dinner: Chicken and Veggie Stir-Fry with Brown Rice

...

📈 Meal Analysis:
Here's a concise read on your meal history and how to use it for weekly planning:

1) Most common cuisine types
- Italian (very frequent: pasta, pizza), Mediterranean, Mexican, Asian
- "Curry" shows up regularly, often within Asian/Mediterranean rotations

2) Most common meal tags/categories
- Very frequent: Pasta, Bowls, Salads, Chicken, Vegetarian, Italian, Mexican, Mediterranean, Asian
- Frequent: Turkey, Stir-fry, Soup, Wraps, Pizza, Sandwiches

3) Patterns in meal complexity/types
- Strong bias toward quick weeknights: bowls, stir-fries, wraps, salads, pasta
- Proteins skew to poultry and vegetarian; seafood appears but less often
```

## Architecture

### Components

- **NotionMCPClient**: Interfaces with Notion via the official MCP server to fetch meal data
- **MealPlanningWorkflow**: LangGraph workflow that orchestrates the planning process
- **Agents**: Specialized agents for fetching, analyzing, generating, and formatting
- **Models**: Pydantic models for type-safe data handling
- **Formatter**: Multiple output format options

### Workflow Steps

1. **Fetch Meals**: Retrieves existing meals from Notion databases and pages using MCP tools
2. **Analyze Meals**: AI analysis of meal patterns, preferences, and cooking styles
3. **Generate Plan**: Creates a balanced weekly meal schedule based on analysis
4. **Format Output**: Presents the plan in your chosen format with detailed insights

### Available MCP Tools

The application uses these Notion MCP tools:
- `API-post-search`: Search for pages and databases
- `API-post-database-query`: Query database contents
- `API-retrieve-a-page`: Get detailed page information
- `API-get-users`: List workspace users
- `API-get-self`: Get your user information

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `NOTION_API_KEY`: Your Notion integration token (required)

### Customization

The meal planning can be customized by modifying:
- `Config.DAYS_OF_WEEK`: Change the weekly template format
- Workflow prompts in the agent files for different planning styles
- Output formats in the formatter agent

## Troubleshooting

### Common Issues

1. **"NOTION_API_KEY environment variable is required"**: 
   - Make sure you've set up your Notion integration and exported the token
   - Run: `export NOTION_API_KEY="your_token_here"`

2. **"No meals found"**: 
   - Ensure your Notion workspace has pages with meal/recipe content
   - Make sure you've shared the pages with your integration
   - Check that pages have titles that contain meal-related keywords

3. **"Failed to initialize Notion MCP client"**: 
   - Verify your Notion API key is correct
   - Check that you have internet connectivity
   - Ensure the `@notionhq/notion-mcp-server` package can be installed

4. **"OpenAI API errors"**: 
   - Check your API key and usage limits
   - Verify your OpenAI account has access to GPT-4

### Debug Mode

For more detailed logging, run the test script:

```bash
python test_mcp.py
```

This will show available tools and test the connection.

## Development

### Project Structure

```
mealworm/
├── mealworm/                 # Main application package
│   ├── agents/              # Specialized workflow agents
│   │   ├── analyzer.py      # Meal analysis agent
│   │   ├── fetcher.py       # Notion data fetching agent
│   │   ├── formatter.py     # Output formatting agent
│   │   └── generator.py     # Meal plan generation agent
│   ├── config.py            # Configuration and environment settings
│   ├── models.py            # Pydantic data models
│   ├── notion_client.py     # Notion MCP server integration
│   └── workflow.py          # LangGraph workflow orchestration
├── main.py                  # Command-line interface
├── test_mcp.py              # MCP connection testing
├── requirements.txt         # Python dependencies
└── README.md               # Documentation
```

### Testing

Test the MCP connection:
```bash
python test_mcp.py
```

Run the full application:
```bash
python main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Check the troubleshooting section above
- Review [Notion MCP documentation](https://developers.notion.com/docs/get-started-with-mcp)
- Open an issue in the repository

## Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for workflow orchestration
- Uses [Notion MCP Server](https://github.com/notionhq/notion-mcp-server) for workspace integration
- Powered by OpenAI's GPT models for intelligent meal planning