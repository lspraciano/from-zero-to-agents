from langchain_core.messages import BaseMessage, AIMessage

from part_langgraph.introduce_langgraph_10.states.state import State


def node_b(state: State) -> dict:
    current_user_message: BaseMessage = state["messages"][-1]
    current_user_message_length: int = len(current_user_message.content)

    print("[Node B] Processing...")

    node_b_response: str = (
        f"Eu, o node_b recebi: {current_user_message_length} carácteres"
    )

    ai_message: AIMessage = AIMessage(content=node_b_response)

    return {
        "messages": [ai_message],
    }
