from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from agents import Agent, Runner, function_tool

from mealworm.db.url import get_db_url

def get_start_of_coming_week():
    today = datetime.now()
    # Get days until next Sunday (6 = Sunday, 0 = Monday)
    days_until_sunday = (6 - today.weekday()) % 7
    if days_until_sunday == 0:  # If today is Sunday, get next Sunday
        days_until_sunday = 7

    start_of_week = today + timedelta(days=days_until_sunday)
    return start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

START_OF_WEEK = get_start_of_coming_week().strftime('%Y-%m-%d')

# Things that currently work well:
# - looking at previous meal plans
# - writing up new ones with the existing "other items"
# - following the format of Sunday, Monday, etc
#
# Things that don't work well right now:
# - doesn't always follow the rubric exactly: sometimes I'll get >1 chicken dish, or >2 fish dishes.
# - lunch for current day is leftovers of previous day
# - doesn't always do a proper web search for the meal it's trying to get a recipe for
# - I don't think it always looks through the previous 30 meals

# NOTE: modify this eventually to add
CUSTOM_INSTRUCTIONS = f"""
## Meal Plan Generation
Look through 30 meals I have made in the meal planning database, and make a new markdown file with meals planned for this week. Use the template I'll provide at the end of these instructions.

The first day of the week is a Sunday, {START_OF_WEEK}.

The meal plan should have the following requirements:

1. exactly 1 chicken dish
2. exactly 2 fish dishes
3. vegetables with every dish
4. exactly one meal that's eating out on a friday or saturday for dinner
5. every dinner should be able to be eaten as leftovers the next day for lunch.
6. every meal should have ingredients listed in the meal plan.

Don't include any meals that have been made in the last 10 meal plans.

## Meal Plan Ingredients
If there is a meal that doesn't have a link to the recipe, do a web search for the meal and include the link in the meal plan.
NOTE: the link must actually be a link to the recipe, not a website that lists the recipe. If it's a website that lists the recipe, you must find the actual recipe link.

For example, if the meal is "Korean BBQ Bowl with Marinated Vegetables", the link "https://bellyfull.net/chicken-and-vegetable-stir-fry/" is not a valid link to the recipe, because it's a totally different meal ("Chicken and Vegetable Stir Fry").

## Meal Preferences
Here are my meal preferences:

- Every meal should have some kind of sauce on top. I don't like dry meals.
- I do not like: olives, capers, or pesto.
- I prefer one super easy meal where I can buy the ingredients mostly pre-made & frozen. For example: chicken burgers w/ fries, salmon burgers w/ fries, BLT sandwich with chili crisp mayo, etc.
- I do not like stir fry meals.
- I love asian, latin, italian, and american food.

When you're finished, please write the meal plan to the file {START_OF_WEEK}.md

<TEMPLATE>

# <TITLE>

## Other Items:

- [ ]  Almond milk
- [ ]  Avocados
- [ ]  Eggs
- [ ]  Bread
- [ ]  Bars for snacking
- [ ]  Orange juice/drink for the week
- [ ]  Kashi peanut butter cereal x 3 boxes
- [ ]  Olive oil
- [ ]  Avocado oil
- [ ]  WW vinegar
- [ ]  Peanut Butter
- [ ]  Crisps
- [ ]  Dragonfruit fruit pouches
- [ ]  Fruit
- [ ]  Buns
- [ ]  Dish soap
- [ ]  Chia seeds
- [ ]  Frozen fruit
- [ ]  Pizza sauce
- [ ]  Pizza dough
- [ ]  Pizza cheese
- [ ]  Parchment paper
- [ ]  Dijon mustard


# Sunday

Lunch:

Dinner:

# Monday

## Lunch:

### Ingredients:

## Dinner:

### Ingredients:


# Tuesday

## Lunch:

### Ingredients:

## Dinner:

### Ingredients:

# Wednesday

## Lunch:

### Ingredients:

## Dinner:

### Ingredients:

# Thursday

## Lunch:

### Ingredients:

## Dinner:

### Ingredients:

# Friday

## Lunch:

### Ingredients:

## Dinner:

### Ingredients:

# Saturday

## Lunch:

### Ingredients:

## Dinner:

### Ingredients:

# Sunday

## Lunch:

### Ingredients:

## Dinner:

### Ingredients:
</TEMPLATE>
"""


# Tool definitions to replace agno's tools
@function_tool
async def search_web(query: str) -> str:
    """Search the web using Tavily API for information about recipes and meal ideas."""
    from tavily import TavilyClient
    import os

    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = client.search(query, max_results=5)

    # Format results
    results = []
    for result in response.get('results', []):
        results.append(f"Title: {result.get('title')}\nURL: {result.get('url')}\nContent: {result.get('content')}\n")

    return "\n".join(results) if results else "No results found"


@function_tool
async def extract_url(url: str) -> str:
    """Extract content from a webpage using Tavily API to get recipe details."""
    from tavily import TavilyClient
    import os

    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = client.extract(urls=[url])

    # Extract returns results array
    results = response.get('results', [])
    if results:
        result = results[0]
        return result.get('raw_content', 'No content found')

    # Check for failed results
    failed = response.get('failed_results', [])
    if failed:
        return f"Failed to extract content: {failed[0]}"

    return "No content found"


@function_tool
async def write_file(file_path: str, content: str) -> str:
    """Write content to a file in the current directory."""
    try:
        path = Path(file_path)
        path.write_text(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to {file_path}: {str(e)}"


@function_tool
async def read_file(file_path: str) -> str:
    """Read content from a file in the current directory."""
    try:
        path = Path(file_path)
        return path.read_text()
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"


@function_tool
async def list_files(directory: str = ".") -> str:
    """List files in a directory."""
    try:
        path = Path(directory)
        files = [f.name for f in path.iterdir() if f.is_file()]
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files in {directory}: {str(e)}"


async def load_meal_plans_to_vector_db():
    """Load historical meal plans from markdown files into PGVector database."""
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import PGVector
    from langchain_community.document_loaders import DirectoryLoader, TextLoader

    db_url = get_db_url()
    embeddings = OpenAIEmbeddings()

    # Load markdown files from historical-meal-plans directory
    historical_plans_dir = Path("historical-meal-plans")
    if not historical_plans_dir.exists():
        print(f"Directory {historical_plans_dir} does not exist")
        return

    loader = DirectoryLoader(
        str(historical_plans_dir),
        glob="*.md",
        loader_cls=TextLoader,
    )
    print(f"Loading meal plans from {historical_plans_dir}")
    documents = loader.load()
    print(f"Loaded {len(documents)} meal plans from {historical_plans_dir} to vector database")

    if not documents:
        print("No meal plans found to load")
        return

    # Create or connect to vector store and add documents
    vector_store = PGVector.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="meal_plans",
        connection_string=db_url,
    )

    print(f"Loaded {len(documents)} meal plans into vector database")
    return vector_store


@function_tool
async def search_historical_meals(query: str, limit: int = 30) -> str:
    """Search through historical meal plans stored in the vector database."""
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import PGVector

    db_url = get_db_url()
    embeddings = OpenAIEmbeddings()

    vector_store = PGVector(
        collection_name="meal_plans",
        connection_string=db_url,
        embedding_function=embeddings,
    )

    # Search for relevant meal plans
    results = vector_store.similarity_search(query, k=limit)

    # Format results
    formatted_results = []
    for i, doc in enumerate(results, 1):
        formatted_results.append(f"Meal Plan {i}:\n{doc.page_content}\n")

    return "\n---\n".join(formatted_results)


async def create_meal_planning_agent():
    """Create and return a configured meal planning agent using OpenAI Agents SDK"""
    agent = Agent(
        name="mealworm-meal-planner",
        instructions=CUSTOM_INSTRUCTIONS,
        model="gpt-5-mini",
        tools=[
            search_web,
            extract_url,
            write_file,
            read_file,
            list_files,
            search_historical_meals,
        ],
    )
    return agent


async def run_meal_planner():
    """Run the meal planning agent"""
    await load_meal_plans_to_vector_db()

    agent = await create_meal_planning_agent()
    result = await Runner.run(agent, "Generate a meal plan for the week.")
    print(result.final_output)
    return result


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_meal_planner())
