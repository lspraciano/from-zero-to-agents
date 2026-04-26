import uuid

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from part_langgraph.introduce_langgraph_13.checkpointers.memory_saver_checkpointer import (
    memory_saver_checkpointer,
)
from part_langgraph.introduce_langgraph_13.graphs.graph_1 import graph_compiled
from part_langgraph.introduce_langgraph_13.states.state import State

graph_compiled.checkpointer = memory_saver_checkpointer

thread_id: str = str(uuid.uuid4())

print(graph_compiled.get_graph().draw_mermaid())
print("-" * 100)

while True:
    user_message: str = input("You: ")

    human_message: HumanMessage = HumanMessage(content=user_message)

    graph_result: State = graph_compiled.invoke(  # type: ignore
        input={
            "messages": [human_message],
        },
        config=RunnableConfig(
            configurable={
                "thread_id": thread_id,
            },
        ),
    )

    print(f"[Graph Result]: {graph_result}")
    print("-" * 100)
