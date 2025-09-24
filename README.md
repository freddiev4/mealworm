# 🐛 Mealworm - AI-Powered Meal Planning

Mealworm is an intelligent meal planning application that creates personalized weekly meal plans using AI agents. It features a modern FastAPI backend with PostgreSQL database, Docker containerization, and intelligent meal planning capabilities.

## Features

- 🧠 **AI-Powered Planning**: Uses advanced AI agents to generate balanced weekly meal plans
- 📅 **Custom Template**: Follows your specified Sunday-Saturday-Sunday format
- 🔄 **Agent-Based Architecture**: Uses specialized AI agents for meal planning and analysis
- 🐳 **Docker Ready**: Fully containerized with Docker Compose for easy deployment
- 🗄️ **PostgreSQL Database**: Robust data storage with pgvector support
- 🌐 **REST API**: Modern FastAPI backend with automatic documentation
- 📊 **Historical Tracking**: Archives and tracks your meal planning history

## Setup

### Prerequisites

- Docker and Docker Compose
- OpenAI API key (or other AI provider API keys)

### Installation

1. Clone and navigate to the project:
```bash
git clone https://github.com/freddiev4/mealworm.git
cd mealworm
```

2. Set up environment variables:
```bash
cp example.env .env
# Edit .env with your API keys
```

3. Start the application:
```bash
docker-compose up -d
```


## Usage

### Docker Setup (Recommended)

Start the complete application stack:

```bash
# Start all services (API + Database)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The application will be available at:
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Database**: localhost:5432 (PostgreSQL with pgvector)

### Development Mode

For development with hot reload:

```bash
# Start in development mode
docker-compose up -d

# The API will automatically reload when you make changes
# Database persists between restarts
```

### Environment Variables

Required environment variables (add to your `.env` file):

```bash
# Required - At least one AI provider
OPENAI_API_KEY=your_openai_api_key_here

# Optional - Additional AI providers
ANTHROPIC_API_KEY=your_anthropic_key
TAVILY_API_KEY=your_tavily_key
FIRECRAWL_API_KEY=your_firecrawl_key
QUOTIENT_API_KEY=your_quotient_key

# Database Configuration (defaults provided)
DB_USER=ai
DB_PASSWORD=ai
DB_NAME=ai
DB_HOST=pgvector
DB_PORT=5432
DB_DRIVER=postgresql+psycopg
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

- **FastAPI Backend**: Modern REST API with automatic documentation
- **PostgreSQL Database**: Robust data storage with pgvector for embeddings
- **AI Agents**: Specialized agents for meal planning, analysis, and generation
- **Docker Containerization**: Fully containerized deployment
- **Historical Tracking**: Archives meal plans and tracks patterns over time

### System Architecture

1. **API Layer**: FastAPI application with health checks and monitoring
2. **Agent Layer**: AI agents handle meal planning logic and analysis
3. **Database Layer**: PostgreSQL with pgvector for data persistence
4. **Container Layer**: Docker Compose orchestrates all services

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `ANTHROPIC_API_KEY`: Your Anthropic API key (optional)
- `TAVILY_API_KEY`: Your Tavily API key (optional)
- `FIRECRAWL_API_KEY`: Your Firecrawl API key (optional)
- `QUOTIENT_API_KEY`: Your Quotient API key (optional)

### Customization

The meal planning can be customized by modifying:
- Agent prompts in the `mealworm/agents/` directory
- API routes in the `mealworm/api/routes/` directory
- Database models in `mealworm/models.py`

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY environment variable is required"**: 
   - Make sure you've set up your OpenAI API key in the `.env` file
   - Verify your API key is valid and has sufficient credits

2. **"Database connection failed"**: 
   - Ensure Docker Compose is running: `docker-compose up -d`
   - Check that the PostgreSQL container is healthy: `docker-compose ps`
   - Verify database credentials in your `.env` file

3. **"API not responding"**: 
   - Check if the API container is running: `docker-compose logs api`
   - Ensure port 8000 is not in use by another application
   - Restart the services: `docker-compose restart`

4. **"Container build failed"**: 
   - Check Docker is running and has sufficient resources
   - Try rebuilding: `docker-compose build --no-cache`
   - Verify all dependencies are available

### Debug Mode

For more detailed logging:

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f pgvector

# Check service status
docker-compose ps
```

## Development

### Project Structure

```
mealworm/
├── mealworm/                    # Main application package
│   ├── agents/                 # AI agents for meal planning
│   │   ├── judge.py           # Meal plan evaluation agent
│   │   ├── meal_planner.py    # Main meal planning agent (Agno)
│   │   └── selector.py        # Meal selection agent
│   ├── api/                   # FastAPI web interface
│   │   ├── main.py           # FastAPI app creation
│   │   ├── monitoring.py     # Health checks and monitoring
│   │   ├── routes/           # API route handlers
│   │   └── settings.py       # API configuration
│   ├── db/                   # Database configuration
│   │   ├── session.py        # Database session management
│   │   └── url.py           # Database URL construction
│   ├── workflows/            # LangGraph workflow components
│   │   ├── analyzer.py      # Meal analysis workflow
│   │   ├── fetcher.py       # Notion data fetching workflow
│   │   ├── generator.py     # Meal plan generation workflow
│   │   ├── searcher.py      # Meal search workflow
│   │   └── workflow.py      # Main workflow orchestration
│   ├── scripts/             # Development and deployment scripts
│   │   ├── dev_setup.sh     # Development environment setup
│   │   ├── build_image.sh   # Docker image building
│   │   └── entrypoint.sh    # Container entrypoint
│   ├── config.py            # Configuration and environment settings
│   ├── models.py            # Pydantic data models
│   └── notion_client.py     # Legacy Notion integration (deprecated)
├── historical-meal-plans/   # Archive of generated meal plans
├── evals/                   # Evaluation and testing scripts
├── compose.yaml            # Docker Compose configuration
├── Dockerfile              # Container image definition
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

### Development Setup

1. **Docker Development**:
```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f api
```

2. **Development Scripts**:
```bash
# Format code
./mealworm/scripts/format.sh

# Validate setup
./mealworm/scripts/validate.sh

# Build Docker image
./mealworm/scripts/build_image.sh
```

### Testing

```bash
# Test individual agents
python evals/test_agents.py

# Test workflow components
python evals/test_workflow.py

# Test API endpoints
curl http://localhost:8000/health
```

### API Development

```bash
# Start with Docker Compose (recommended)
docker-compose up -d

# API automatically reloads on code changes
# Access at http://localhost:8000/docs
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
- Review the API documentation at http://localhost:8000/docs
- Open an issue in the repository

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) for the REST API
- Uses [PostgreSQL](https://www.postgresql.org/) with [pgvector](https://github.com/pgvector/pgvector) for data storage
- Powered by AI agents for intelligent meal planning
- Containerized with [Docker](https://www.docker.com/) for easy deployment