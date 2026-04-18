from typing import Literal

from part_langgraph.introduce_langgraph_11.states.state import State


def router_node_conditional_edge(
    state: State,
) -> Literal[
    "reverse_text_node",
    "general_node",
]:
    return state["router_destination"]
