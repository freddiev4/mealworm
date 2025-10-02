from enum import Enum
from logging import getLogger
from typing import AsyncGenerator, List, Optional

from agents import Agent, Runner

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from opentelemetry.trace import use_span
from pydantic import BaseModel

from mealworm.api.monitoring import quotient
from mealworm.agents.meal_planner_openai import load_meal_plans_to_vector_db
from mealworm.agents.selector import AgentType, get_agent, get_available_agents

logger = getLogger(__name__)

######################################################
## Routes for the Agent Interface
######################################################

agents_router = APIRouter(prefix="/agents", tags=["Agents"])


class Model(str, Enum):
    claude_sonnet_4_0 = "claude-sonnet-4-0"
    gpt_5_mini = "gpt-5-mini"


@agents_router.get("", response_model=List[str])
async def list_agents():
    """
    Returns a list of all available agent IDs.

    Returns:
        List[str]: List of agent identifiers
    """
    return get_available_agents()


async def chat_response_streamer(agent: Agent, message: str) -> AsyncGenerator:
    """
    Stream agent responses chunk by chunk.

    Args:
        agent: The agent instance to interact with
        message: User message to process

    Yields:
        Text chunks from the agent response
    """
    root_span = quotient.tracer.start_span(f'{agent.name}-run')

    stream_ctx = use_span(root_span, end_on_exit=False)

    with stream_ctx:
        # Use OpenAI Agents SDK streaming
        result = Runner.run_streamed(agent, message)
        async for event in result.stream_events():
            # Stream raw response events (token by token)
            if hasattr(event, 'data') and hasattr(event.data, 'text'):
                yield event.data.text

    root_span.end()
    quotient.force_flush()


class RunRequest(BaseModel):
    """Request model for an running an agent"""

    message: str
    stream: bool = True
    model: Model = Model.gpt_5_mini
    user_id: Optional[str] = None
    session_id: Optional[str] = None


@agents_router.post("/{agent_id}/runs", status_code=status.HTTP_200_OK)
async def create_agent_run(agent_id: AgentType, body: RunRequest):
    """
    Sends a message to a specific agent and returns the response.

    Args:
        agent_id: The ID of the agent to interact with
        body: Request parameters including the message

    Returns:
        Either a streaming response or the complete agent response
    """
    logger.debug(f"RunRequest: {body}")

    try:
        agent: Agent = await get_agent(
            model_id=body.model.value,
            agent_id=agent_id,
            user_id=body.user_id,
            session_id=body.session_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


    if body.stream:
        response = StreamingResponse(
            chat_response_streamer(agent, body.message),
            media_type="text/event-stream",
        )
        return response
    else:
        # Use OpenAI Agents SDK non-streaming run
        result = await Runner.run(agent, body.message)
        # Return the final output from the agent
        return result.final_output

@agents_router.post("/{agent_id}/knowledge/load", status_code=status.HTTP_200_OK)
async def load_agent_knowledge(agent_id: AgentType):
    """
    Loads the knowledge base for a specific agent.

    Args:
        agent_id: The ID of the agent to load knowledge for.

    Returns:
        A success message if the knowledge base is loaded.
    """
    if agent_id == AgentType.MEAL_PLANNING_AGENT:
        try:
            await load_meal_plans_to_vector_db()
        except Exception as e:
            logger.error(f"Error loading knowledge base for {agent_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to load knowledge base for {agent_id}.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Agent {agent_id} does not have a knowledge base.",
        )

    return {"message": f"Knowledge base for {agent_id} loaded successfully."}
