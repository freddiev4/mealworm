"""Dynamic instruction template builder for meal planning agent."""

from datetime import datetime, timedelta

from mealworm.db.models import UserPreferences


def get_start_of_coming_week() -> datetime:
    """
    Calculate the start of the coming week (Sunday).

    Returns:
        datetime object for the coming Sunday
    """
    today = datetime.now()
    days_until_sunday = (6 - today.weekday()) % 7
    if days_until_sunday == 0:
        days_until_sunday = 7
    start_of_week = today + timedelta(days=days_until_sunday)
    return start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)


def build_custom_instructions(preferences: UserPreferences) -> str:
    """
    Build custom instructions for the meal planning agent based on user preferences.

    This function dynamically generates the agent's instruction prompt by incorporating
    the user's meal requirements, preferences, dietary restrictions, and shopping list.

    Args:
        preferences: UserPreferences object from database

    Returns:
        Formatted instruction string for the agent
    """
    start_of_week = get_start_of_coming_week().strftime("%Y-%m-%d")

    # Build meal requirements section
    requirements = []
    requirements.append(
        f"exactly {preferences.chicken_dishes_per_week} chicken dish"
        f"{'es' if preferences.chicken_dishes_per_week != 1 else ''}"
    )
    requirements.append(
        f"exactly {preferences.fish_dishes_per_week} fish dish"
        f"{'es' if preferences.fish_dishes_per_week != 1 else ''}"
    )

    if preferences.vegetables_required:
        requirements.append("vegetables with every dish")

    if preferences.eating_out_days:
        eating_out_days_str = " or ".join(
            [day.lower() for day in preferences.eating_out_days]
        )
        requirements.append(
            f"exactly one meal that's eating out on a {eating_out_days_str} for dinner"
        )

    if preferences.leftovers_for_lunch:
        requirements.append(
            "every dinner should be able to be eaten as leftovers the next day for lunch"
        )

    requirements.append("every meal should have ingredients listed in the meal plan")

    requirements_text = "\n".join(
        [f"{i + 1}. {req}" for i, req in enumerate(requirements)]
    )

    # Build meal preferences section
    preferences_list = []

    if preferences.sauce_preference:
        preferences_list.append(f"- {preferences.sauce_preference}")

    if preferences.dislikes:
        dislikes_str = ", ".join(preferences.dislikes)
        preferences_list.append(f"- I do not like: {dislikes_str}.")

    if preferences.easy_meal_preference:
        preferences_list.append(f"- {preferences.easy_meal_preference}")

    if preferences.likes:
        likes_str = ", ".join(preferences.likes)
        preferences_list.append(f"- I specifically like: {likes_str}.")

    if preferences.avoid_meal_types:
        avoid_str = ", ".join(preferences.avoid_meal_types)
        preferences_list.append(f"- I do not like {avoid_str} meals.")

    if preferences.preferred_cuisines:
        cuisines_str = ", ".join([c.lower() for c in preferences.preferred_cuisines])
        preferences_list.append(f"- I love {cuisines_str} food.")

    preferences_text = (
        "\n".join(preferences_list)
        if preferences_list
        else "- No specific preferences."
    )

    # Build dietary restrictions section
    dietary_section = ""
    if preferences.dietary_restrictions or preferences.allergens:
        restrictions = []
        if preferences.dietary_restrictions:
            restrictions.extend(preferences.dietary_restrictions)
        if preferences.allergens:
            restrictions.extend(
                [f"allergic to {allergen}" for allergen in preferences.allergens]
            )

        dietary_section = f"""
## Dietary Restrictions
Please ensure all meals comply with the following:
{chr(10).join([f"- {r}" for r in restrictions])}
"""

    # Build shopping list template
    other_items_text = "\n".join([f"- [ ]  {item}" for item in preferences.other_items])

    # Construct the full instruction template
    instructions = f"""
## Meal Plan Generation
You have access to my historical meal plans in your knowledge base. Search your knowledge base to find my past meal plans and use them to avoid repeating recent meals.

Create a new markdown file with meals planned for this week. Use the template I'll provide at the end of these instructions.

The first day of the week is a Sunday, {start_of_week}.

The meal plan should have the following requirements:

{requirements_text}

**IMPORTANT:** Don't include any meals that have been made in the last 10 meal plans. Search your knowledge base to check for recent meals. If you can't find specific past meal plans, proceed anyway with your best judgment to create a diverse and interesting week of meals.

## Meal Plan Ingredients
If there is a meal that doesn't have a link to the recipe, do a web search for the meal and include the link in the meal plan.
NOTE: the link must actually be a link to the recipe, not a website that lists the recipe. If it's a website that lists the recipe, you must find the actual recipe link.

For example, if the meal is "Korean BBQ Bowl with Marinated Vegetables", the link "https://bellyfull.net/chicken-and-vegetable-stir-fry/" is not a valid link to the recipe, because it's a totally different meal ("Chicken and Vegetable Stir Fry").

## Meal Preferences
Here are my meal preferences:

{preferences_text}
{dietary_section}

## How to Proceed
1. Search your knowledge base for recent meal plans to avoid repetition
2. Choose reasonable defaults for any unspecified preferences (e.g., pick Friday or Saturday for eating out, choose a mid-week day for the easy meal)
3. Generate a complete, diverse meal plan following all requirements
4. Write the meal plan to the file {start_of_week}.md

**IMPORTANT INSTRUCTIONS:**
- Do NOT narrate your actions or explain what you're doing
- Do NOT say things like "Let me search...", "Now I'll...", "Based on...", etc.
- Work silently and only output the final meal plan content
- After you've finished creating the meal plan, simply present it in markdown format
- Do not ask clarifying questions - use your best judgment to create an excellent meal plan based on the requirements and preferences above

<TEMPLATE>

# <TITLE>

## Other Items:

{other_items_text}


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

    return instructions
