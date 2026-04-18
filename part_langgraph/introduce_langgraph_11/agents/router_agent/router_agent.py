from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

from part_langgraph.introduce_langgraph_11.agents.router_agent.router_agent_response_format import (
    RouterAgentResponseFormat,
)
from part_langgraph.introduce_langgraph_11.llm_models.llm_models import get_llm_model

router_agent: CompiledStateGraph = create_agent(
    name="router_agent",
    model=get_llm_model(model_name="gpt-4.1-mini"),
    response_format=RouterAgentResponseFormat,
    tools=[],
)
