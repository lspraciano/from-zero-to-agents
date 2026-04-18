from typing import Literal

from part_langgraph.introduce_langgraph_11.states.state import State


def node_router_conditional_edge(
        state: State,
) -> Literal[
    "reverse_text_agent",
    "general_agent",
]:
    return state["router_destination"]
