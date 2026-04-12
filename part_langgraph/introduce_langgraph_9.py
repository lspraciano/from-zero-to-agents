from typing import TypedDict, Literal, Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, add_messages
from langgraph.graph.state import CompiledStateGraph


class State(TypedDict):
    user_message_length: int
    messages: Annotated[list[BaseMessage], add_messages]


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

    ai_message: AIMessage = AIMessage(content=node_a_response)

    return {
        "messages": [ai_message],
    }


def node_b(state: State) -> dict:
    current_user_message: BaseMessage = state["messages"][-1]
    current_user_message_length: int = len(current_user_message.content)

    print("[Node B] Processing...")

    node_b_response: str = f"Eu, o node_b recebi: {current_user_message_length} carácteres"

    ai_message: AIMessage = AIMessage(content=node_b_response)

    return {
        "messages": [ai_message],
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

checkpointer: MemorySaver = MemorySaver()

graph_compiled: CompiledStateGraph = graph.compile(checkpointer=checkpointer)

while True:
    user_message: str = input("You: ")

    human_message: HumanMessage = HumanMessage(content=user_message)

    graph_result: State = graph_compiled.invoke(
        input={  # type: ignore
            "user_message_length": 0,
            "messages": [human_message],
        },
        config=RunnableConfig(
            configurable={
                "thread_id": 123,
            },
        ),
    )

    print(f"[Graph Result]: {graph_result}")
    print("-" * 100)
