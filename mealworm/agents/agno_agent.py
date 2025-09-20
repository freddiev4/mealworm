
from datetime import datetime, timedelta
from pathlib import Path

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.models.anthropic import Claude
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.local_file_system import LocalFileSystemTools
from agno.tools.tavily import TavilyTools
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://freddie:ai@localhost:5432/freddie"

knowledge = Knowledge(
    vector_db=PgVector(
        table_name="meal_plans",
        db_url=db_url,
    ),
)

# Add Markdown content from historical meal plans to knowledge base
historical_plans_dir = Path("historical-meal-plans")
if historical_plans_dir.exists():
    print(f"Adding historical meal plans to knowledge base from {historical_plans_dir}")
    paths = historical_plans_dir.glob("*.md")
    knowledge.add_contents(
        paths=paths,
        reader=MarkdownReader(),
        skip_if_exists=True,
    )
        
print(f"Added {len(list(paths))} meal plans to knowledge base")


def get_start_of_coming_week():
    today = datetime.now()
    # Get days until next Sunday (6 = Sunday, 0 = Monday)
    days_until_sunday = (6 - today.weekday()) % 7
    if days_until_sunday == 0:  # If today is Sunday, get next Sunday
        days_until_sunday = 7
    
    start_of_week = today + timedelta(days=days_until_sunday)
    return start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

START_OF_WEEK = get_start_of_coming_week().strftime('%Y-%m-%d')

# NOTE: modify this eventually to add
CUSTOM_INSTRUCTIONS = f"""
## Meal Plan Generation
Look through 30 meals I have made in the meal planning database, and make a new markdown file with meals planned for this week. Use the template I'll provide at the end of these instructions.

The first day of the week is a Sunday, {START_OF_WEEK}.

The meal plan should have the following requirements:

1. exactly 1 chicken dish
2. exactly 2 fish dishes
3. vegetables with every dish
4. exactly one meal that’s eating out on a friday or saturday for dinner
5. every dinner should be able to be eaten as leftovers the next day for lunch.
6. every meal should have ingredients listed in the meal plan.

Don't include any meals that have been made in the last 10 meal plans.

## Meal Plan Ingredients
If there is a meal that doesn't have a link to the recipe, do a web search for the meal and include the link in the meal plan.
NOTE: the link must actually be a link to the recipe, not a website that lists the recipe. If it's a website that lists the recipe, you must find the actual recipe link.

For example, if the meal is "Korean BBQ Bowl with Marinated Vegetables", the link "https://bellyfull.net/chicken-and-vegetable-stir-fry/" is not a valid link to the recipe, because it's a totally different meal ("Chicken and Vegetable Stir Fry").

## Meal Preferences
Here are my meal preferences:

- Every meal should have some kind of sauce on top. I don’t like dry meals.
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

def create_meal_planning_agent():
    """Create and return a configured meal planning agent"""
    agent = Agent(
        model=Claude(id="claude-sonnet-4-0"),
        instructions=CUSTOM_INSTRUCTIONS,
        tools=[
            TavilyTools(), 
            FirecrawlTools(enable_scrape=True, enable_crawl=True),
            LocalFileSystemTools(target_directory=".")
        ],
        knowledge=knowledge,
        search_knowledge=True,
        markdown=True,
    )
    return agent
