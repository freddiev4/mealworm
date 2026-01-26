from enum import Enum
from typing import List, Optional

from mealworm.agents.meal_planner import create_meal_planning_agent


class AgentType(Enum):
    MEAL_PLANNING_AGENT = "meal_planning_agent"


def get_available_agents() -> List[str]:
    """Returns a list of all available agent IDs."""
    return [agent.value for agent in AgentType]


async def get_agent(
    model_id: str = "claude-sonnet-4-0",
    agent_id: Optional[AgentType] = None,
    user_id: Optional[int] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
):
    if agent_id == AgentType.MEAL_PLANNING_AGENT:
        agent = await create_meal_planning_agent(
            model_id=model_id,
            user_id=user_id,
            session_id=session_id,
            debug_mode=debug_mode,
        )
    else:
        raise ValueError(f"Agent: {agent_id} not found")

    return agent
