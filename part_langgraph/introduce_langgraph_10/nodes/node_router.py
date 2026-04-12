from langchain_core.messages import BaseMessage

from part_langgraph.introduce_langgraph_10.states.state import State


def node_router(state: State) -> dict:
    current_user_message: BaseMessage = state["messages"][-1]
    current_user_message_length: int = len(current_user_message.content)

    print(f"[Router] User Message Length: {current_user_message_length}")

    return {
        "user_message_length": current_user_message_length,
    }
