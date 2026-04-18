from langchain_core.prompt_values import PromptValue

from part_langgraph.introduce_langgraph_11.agents.router_agent.router_agent import (
    router_agent,
)
from part_langgraph.introduce_langgraph_11.agents.router_agent.router_agent_response_format import (
    RouterAgentResponseFormat,
)
from part_langgraph.introduce_langgraph_11.agents.router_agent.router_agent_template import (
    router_agent_template,
)
from part_langgraph.introduce_langgraph_11.states.state import State


def router_node(state: State) -> dict:
    router_agent_input: PromptValue = router_agent_template.invoke(
        input={
            "history": state["messages"],
        },
    )

    router_agent_result: dict = router_agent.invoke(input=router_agent_input)

    router_agent_response: RouterAgentResponseFormat = router_agent_result[
        "structured_response"
    ]

    return {
        "router_destination": router_agent_response.router_destination,
    }
