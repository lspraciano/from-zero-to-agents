from typing import Literal

from part_langgraph.introduce_langgraph_10.states.state import State


def node_router_conditional_edge(
    state: State,
) -> Literal[
    "node_a",
    "node_b",
]:
    if state["user_message_length"] > 10:
        return "node_a"

    return "node_b"
