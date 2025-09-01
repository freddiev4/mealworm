# 🐛 Mealworm - AI-Powered Meal Planning

Mealworm is an intelligent meal planning application that integrates with your Notion workspace to create personalized weekly meal plans. It uses LangGraph for workflow orchestration and OpenAI's GPT models for intelligent meal selection and planning.

## Features

- 🔗 **Notion Integration**: Automatically fetches existing meals and recipes from your Notion workspace using the Notion MCP server
- 🧠 **AI-Powered Planning**: Uses GPT-4 to analyze your meal preferences and generate balanced weekly plans
- 📅 **Custom Template**: Follows your specified Sunday-Saturday-Sunday format
- 🔄 **Workflow Orchestration**: Uses LangGraph for robust, step-by-step meal planning process
- 📊 **Multiple Output Formats**: Text, simple template, or markdown formats

## Setup

### Prerequisites

- Python 3.8+
- OpenAI API key
- Notion workspace with meal/recipe pages
- Access to Notion MCP server

### Installation

1. Clone and navigate to the project:
```bash
git clone <repository-url>
cd mealworm
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

4. Configure Notion MCP:
   - Follow the [Notion MCP setup guide](https://developers.notion.com/docs/get-started-with-mcp#connect-through-your-ai-tool)
   - Ensure the MCP server URL is correctly set in your `.env` file

## Usage

### Basic Usage

```bash
python main.py
```

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
Week starting: September 01, 2024

📅 SUNDAY
----------
🌙 Dinner: Spaghetti Carbonara
   Cuisine: Italian
   Prep time: 30 minutes

📅 MONDAY
----------
🌙 Dinner: Chicken Teriyaki
   Cuisine: Japanese
   Prep time: 25 minutes

...
```

## Architecture

### Components

- **NotionMCPClient**: Interfaces with Notion via MCP server to fetch meal data
- **MealPlanningWorkflow**: LangGraph workflow that orchestrates the planning process
- **Models**: Pydantic models for type-safe data handling
- **Formatter**: Multiple output format options

### Workflow Steps

1. **Fetch Meals**: Retrieves existing meals from Notion databases and pages
2. **Analyze Meals**: AI analysis of meal patterns and preferences
3. **Generate Plan**: Creates a balanced weekly meal schedule
4. **Format Output**: Presents the plan in your chosen format

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `NOTION_MCP_URL`: Notion MCP server URL (default: https://mcp.notion.com/mcp)

### Customization

The meal planning can be customized by modifying:
- `Config.DAYS_OF_WEEK`: Change the weekly template format
- Workflow prompts in `workflow.py` for different planning styles
- Output formats in `formatter.py`

## Troubleshooting

### Common Issues

1. **No meals found**: Ensure your Notion workspace has pages with meal/recipe content
2. **MCP connection errors**: Verify your Notion MCP server setup and permissions
3. **OpenAI API errors**: Check your API key and usage limits

### Debug Mode

For more detailed logging, modify the print statements in `workflow.py` or add logging configuration.

## Development

### Project Structure

```
mealworm/
├── mealworm/                 # Main application package
│   ├── config.py            # Configuration and environment settings
│   ├── models.py            # Pydantic data models
│   ├── notion_client.py     # Notion MCP server integration
│   ├── workflow.py          # LangGraph workflow orchestration
│   └── formatter.py         # Output formatting utilities
├── main.py                  # Command-line interface
├── simple_demo.py           # Standalone demonstration
├── requirements.txt         # Python dependencies
└── README.md               # Documentation
```

### Demo Mode

To see the application in action without external dependencies:

```bash
python simple_demo.py
```

This runs a demonstration with sample data showing the complete workflow and output formats.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Check the troubleshooting section above
- Review Notion MCP documentation
- Open an issue in the repository