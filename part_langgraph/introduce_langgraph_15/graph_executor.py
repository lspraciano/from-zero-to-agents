import uuid
from pathlib import Path

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langfuse.langchain import CallbackHandler

from part_langgraph.introduce_langgraph_15.checkpointers.memory_saver_checkpointer import (
    memory_saver_checkpointer,
)
from part_langgraph.introduce_langgraph_15.graphs.graph_1 import graph_compiled
from part_langgraph.introduce_langgraph_15.observability.langfuse_handler import (
    get_langfuse_handler,
)
from part_langgraph.introduce_langgraph_15.pipelines.ingestion_pipeline import (
    run_ingestion_pipeline,
)
from part_langgraph.introduce_langgraph_15.states.state import State

current_file_path: Path = Path(__file__)
current_directory: Path = current_file_path.parent
documents_directory: Path = current_directory / "documents"
knowledge_base_file: Path = documents_directory / "knowledge_base.txt"
knowledge_base_file_str: str = str(knowledge_base_file)

run_ingestion_pipeline(file_path=knowledge_base_file_str)

graph_compiled.checkpointer = memory_saver_checkpointer

langfuse_handler: CallbackHandler = get_langfuse_handler()

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
            callbacks=[langfuse_handler],
        ),
    )

    print(f"[Graph Result]: {graph_result}")
    print("-" * 100)
