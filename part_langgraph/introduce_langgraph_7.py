from typing import TypedDict, Literal

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph


class State(TypedDict):
    user_message_length: int
    messages: list[BaseMessage]
    graph_response: str


def node_router(state: State) -> dict:
    current_user_message: BaseMessage = state["messages"][-1]
    current_user_message_length: int = len(current_user_message.content)

    print(f"[Router] User Message Length: {current_user_message_length}")

    return {
        "user_message_length": current_user_message_length,
    }


def node_a(state: State) -> dict:
    current_user_message: BaseMessage = state["messages"][-1]
    current_user_message_length: int = len(current_user_message.content)

    print("[Node A] Processing...")

    node_a_response: str = f"Eu, o node_a recebi: {current_user_message_length} carácteres"

    return {
        "graph_response": node_a_response,
    }


def node_b(state: State) -> dict:
    current_user_message: BaseMessage = state["messages"][-1]
    current_user_message_length: int = len(current_user_message.content)

    print("[Node B] Processing...")

    node_b_response: str = f"Eu, o node_b recebi: {current_user_message_length} carácteres"

    return {
        "graph_response": node_b_response,
    }


def node_router_conditional_edge(state: State) -> Literal[
    "node_a",
    "node_b",
]:
    if state["user_message_length"] > 10:
        return "node_a"

    return "node_b"


graph: StateGraph = StateGraph(State)  # type: ignore

graph.add_node(node="node_router", action=node_router)  # type: ignore
graph.add_node(node="node_a", action=node_a)  # type: ignore
graph.add_node(node="node_b", action=node_b)  # type: ignore

graph.add_edge(start_key=START, end_key="node_router")

graph.add_conditional_edges(source="node_router", path=node_router_conditional_edge)

graph.add_edge(start_key="node_a", end_key=END)
graph.add_edge(start_key="node_b", end_key=END)

graph_compiled: CompiledStateGraph = graph.compile()

messages: list[BaseMessage] = []

while True:
    user_message: str = input("You: ")

    human_message: HumanMessage = HumanMessage(content=user_message)

    messages.append(human_message)

    initial_state: State = {
        "user_message_length": 0,
        "messages": messages,
        "graph_response": "",
    }

    graph_result: State = graph_compiled.invoke(input=initial_state)  # type: ignore

    graph_response: str = graph_result["graph_response"]

    ai_message: AIMessage = AIMessage(content=graph_response)

    messages.append(ai_message)

    print(f"[Graph Result]: {graph_result}")
    print("-" * 100)
