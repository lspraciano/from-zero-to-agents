from langchain_core.messages import BaseMessage, AIMessage

from part_langgraph.introduce_langgraph_10.states.state import State


def node_a(state: State) -> dict:
    current_user_message: BaseMessage = state["messages"][-1]
    current_user_message_length: int = len(current_user_message.content)

    print("[Node A] Processing...")

    node_a_response: str = (
        f"Eu, o node_a recebi: {current_user_message_length} carácteres"
    )

    ai_message: AIMessage = AIMessage(content=node_a_response)

    return {
        "messages": [ai_message],
    }
