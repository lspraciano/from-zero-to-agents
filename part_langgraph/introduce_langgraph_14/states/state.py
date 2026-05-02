from typing import TypedDict, Annotated, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    router_destination: Literal[
        "knowledge_agent",
        "general_agent",
    ]
