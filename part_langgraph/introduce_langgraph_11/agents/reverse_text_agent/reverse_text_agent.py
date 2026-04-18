from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph

from part_langgraph.introduce_langgraph_11.agents.reverse_text_agent.reverse_text_agent_response_format import (
    ReverseTextAgentResponseFormat,
)
from part_langgraph.introduce_langgraph_11.llm_models.llm_models import get_llm_model
from part_langgraph.introduce_langgraph_11.tools.invert_text_tool import (
    reverse_text_tool,
)

reverse_text_agent: CompiledStateGraph = create_agent(
    name="reverse_text_agent",
    model=get_llm_model(model_name="gpt-4.1-mini"),
    response_format=ReverseTextAgentResponseFormat,
    tools=[reverse_text_tool],
)
