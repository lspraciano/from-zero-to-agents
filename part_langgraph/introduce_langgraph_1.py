import random
import time
from typing import TypedDict, Literal

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph


class State(TypedDict):
    destination: str


def node_router(state: State) -> dict:
    chosen_destination: str = random.choice(
        seq=[
            "node_a",
            "node_b",
        ]
    )

    print(f"[Router] Directing to node: {chosen_destination}")

    return {"destination": chosen_destination}


def node_a(state: State) -> None:
    print("[Node A] Processing...")


def node_b(state: State) -> None:
    print("[Node B] Processing...")


def node_router_conditional_edge(state: State) -> Literal[
    "node_a",
    "node_b",
]:
    current_destination: str = state["destination"]

    return current_destination  # type: ignore


graph: StateGraph = StateGraph(State)  # type: ignore

graph.add_node(node="node_router", action=node_router)  # type: ignore
graph.add_node(node="node_a", action=node_a)  # type: ignore
graph.add_node(node="node_b", action=node_b)  # type: ignore

graph.add_edge(start_key=START, end_key="node_router")

graph.add_conditional_edges(source="node_router", path=node_router_conditional_edge)

graph.add_edge(start_key="node_a", end_key=END)
graph.add_edge(start_key="node_b", end_key=END)

graph_compiled: CompiledStateGraph = graph.compile()

while True:
    initial_state: State = {
        "destination": "",
    }

    graph_result: State = graph_compiled.invoke(input=initial_state)  # type: ignore

    print(f"[Graph Result]: {graph_result}")
    print("-" * 100)

    time.sleep(3)
