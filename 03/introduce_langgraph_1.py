import random
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph


class State(TypedDict):
    message: str
    destination: str


def router(state: State) -> dict:
    chosen_destination: str = random.choice(seq=["A", "B", "C"])

    print(f"[Router] Directing to node: {chosen_destination}")

    return {"destination": chosen_destination}


def node_a(state: State) -> dict:
    print("[Node A] Processing...")

    return {"message": "Handled by node A"}


def node_b(state: State) -> dict:
    print("[Node B] Processing...")

    return {"message": "Handled by node B"}


def node_c(state: State) -> dict:
    print("[Node C] Processing...")

    return {"message": "Handled by node C"}


def decide_destination(state: State) -> str:
    return state["destination"]


graph: StateGraph = StateGraph(State)  # type: ignore

graph.add_node(node="router", action=router)  # type: ignore
graph.add_node(node="A", action=node_a)  # type: ignore
graph.add_node(node="B", action=node_b)  # type: ignore
graph.add_node(node="C", action=node_c)  # type: ignore

graph.add_edge(start_key=START, end_key="router")

graph.add_conditional_edges(
    source="router",
    path=decide_destination,
    path_map={"A": "A", "B": "B", "C": "C"},
)

graph.add_edge(start_key="A", end_key=END)
graph.add_edge(start_key="B", end_key=END)
graph.add_edge(start_key="C", end_key=END)

app: CompiledStateGraph = graph.compile()

initial_state: State = {"message": "Hello!", "destination": ""}

result: dict = app.invoke(input=initial_state)  # type: ignore

print(f"\nFinal result: {result['message']}")
