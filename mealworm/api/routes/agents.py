from enum import Enum
from logging import getLogger
from typing import AsyncGenerator, List, Optional

from agno.agent import Agent

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import StreamingResponse
from opentelemetry.trace import use_span
from pydantic import BaseModel

from mealworm.agents.meal_planner import load_meal_plans_to_vector_db
from mealworm.agents.selector import AgentType, get_agent, get_available_agents
from mealworm.api.auth.dependencies import get_current_user
from mealworm.db.models import User

logger = getLogger(__name__)

######################################################
## Routes for the Agent Interface
######################################################

agents_router = APIRouter(prefix="/agents", tags=["Agents"])


class Model(str, Enum):
    # Anthropic Claude Models
    claude_opus_4_5 = "claude-opus-4-5"
    claude_sonnet_4_5 = "claude-sonnet-4-5"
    claude_sonnet_4_0 = "claude-sonnet-4-0"
    claude_opus_4_1 = "claude-opus-4-1"
    claude_haiku_4_5 = "claude-haiku-4-5"

    # OpenAI Models
    gpt_5_mini = "gpt-5-mini"
    gpt_5_2 = "gpt-5.2-2025-12-11"
    gpt_4 = "gpt-4"


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

    stream_ctx = use_span(root_span, end_on_exit=False)

    try:
        with stream_ctx:
            # Use agno streaming (returns a synchronous generator)
            response_stream = agent.run(message, stream=True)

            for chunk in response_stream:
                # Filter to only stream actual response content, not tool usage narration
                if hasattr(chunk, "content") and chunk.content:
                    content = chunk.content

                    # Skip tool execution timing messages
                    if "completed in" not in content:
                        yield content
    except Exception as e:
        logger.error(f"Error in chat_response_streamer: {e}", exc_info=True)
        yield f"\n\nError: {str(e)}\n\nThis appears to be a connection issue with the AI provider. Please try again.\n"


class RunRequest(BaseModel):
    """Request model for an running an agent"""

    message: str
    stream: bool = True
    model: Model = Model.claude_sonnet_4_0
    user_id: Optional[str] = None
    session_id: Optional[str] = None


@agents_router.post("/{agent_id}/runs", status_code=status.HTTP_200_OK)
async def create_agent_run(
    agent_id: AgentType,
    body: RunRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Sends a message to a specific agent and returns the response.
    Requires authentication.

    Args:
        agent_id: The ID of the agent to interact with
        body: Request parameters including the message
        current_user: Current authenticated user

    Returns:
        Either a streaming response or the complete agent response
    """
    logger.info(
        f"Agent run for {agent_id} by user {current_user.id} with model {body.model.value}"
    )

    try:
        agent: Agent = await get_agent(
            model_id=body.model.value,
            agent_id=agent_id,
            user_id=current_user.id,  # Use authenticated user's ID
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
        # Use agno non-streaming run
        result = agent.run(body.message, stream=False)
        # Return the content from the agno RunResponse
        return {
            "content": result.content if hasattr(result, "content") else str(result)
        }


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
