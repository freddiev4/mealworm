from pydantic import BaseModel

class MealPlanJudge(BaseModel):
    reason: str
    valid: bool

LLM_JUDGE_LEFTOVERS_FROM_DINNER = """
You are a judge that is tasked with evaluating whether a meal plan is valid.
A meal plan is valid if for each lunch dish, there is a corresponding dinner dish from the previous day.

Return the reason why it is valid or invalid, along with your reasoning.
"""