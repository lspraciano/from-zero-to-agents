from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

from part_langchain.introduce_langchain_20.agents.router_agent.router_agent_response_format import \
    RouterAgentResponseFormat
from part_langgraph.introduce_langgraph_11.agents.general_agent.general_agent_response_format import \
    GeneralAgentResponseFormat
from part_langgraph.introduce_langgraph_11.llm_models.llm_models import get_llm_model

general_agent: CompiledStateGraph = create_agent(
    name="general_agent",
    model=get_llm_model(model_name="gpt-4.1-mini"),
    response_format=GeneralAgentResponseFormat,
    tools=[],
)
