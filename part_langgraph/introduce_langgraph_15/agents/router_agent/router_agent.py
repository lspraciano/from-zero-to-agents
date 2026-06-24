from langchain.agents import create_agent
from langchain_core.prompt_values import PromptValue
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command

from part_langgraph.introduce_langgraph_15.agents.router_agent.router_agent_response_format import (
    RouterAgentResponseFormat,
)
from part_langgraph.introduce_langgraph_15.agents.router_agent.router_agent_template import (
    router_agent_template,
)
from part_langgraph.introduce_langgraph_15.llm_models.llm_models import get_llm_model
from part_langgraph.introduce_langgraph_15.states.state import State

_router_agent: CompiledStateGraph = create_agent(
    name="router_agent",
    model=get_llm_model(model_name="gpt-4.1-mini"),
    response_format=RouterAgentResponseFormat,
    tools=[],
)


def router_agent(state: State) -> Command:
    router_agent_input: PromptValue = router_agent_template.invoke(
        input={
            "history": state["messages"],
        },
    )

    router_agent_result: dict = _router_agent.invoke(input=router_agent_input)

    router_agent_response: RouterAgentResponseFormat = router_agent_result[
        "structured_response"
    ]

    return Command(
        goto=router_agent_response.router_destination,
        update=router_agent_response.model_dump(),
    )
